"""Run a play's stages in order, re-running a stage only when something it
depends on changed.

A stage declares its commands, the play-dir files it reads and writes, the
per-play settings it uses and its code files. It passes when every command
exits 0 and every declared output exists. What each stage saw and wrote goes
into ``<play-dir>/run_manifest.json``; each stage's full output goes to
``<play-dir>/logs/<stage>.log``.

When does a stage re-run? Its fingerprint (rendered commands, environment,
settings, code hashes and the version of each input it reads) is compared
with the one recorded at its last successful run. Many stages rewrite a file
they read (``cameras.npz`` and ``tracks.parquet`` are rewritten several
times), so "the version of an input" is not the file on disk now. It is
what the last EARLIER stage that writes that file left there, as recorded in
the manifest. Two more rules follow from files being rewritten in place:

- A stage that re-runs overwrites its outputs, so every LATER stage that
  also writes one of those files re-runs too. Its edits were lost.
- If a file on disk no longer matches what its last writer recorded (deleted
  or edited by hand), the chain is redone from the file's FIRST writer.

A re-run that writes the same bytes as before stops the cascade there.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from nfl_gsplat.errors import PipelineError
from nfl_gsplat.settings import REPO_ROOT
from nfl_gsplat.utils.io import read_json, sha256_file, write_json

MANIFEST = "run_manifest.json"
LOGS = "logs"
ABSENT = "absent"
_PENDING = "pending (written by a stage that would re-run)"
_PLACEHOLDER = re.compile(r"\{(\w+)\}")


class StageFailed(PipelineError):
    """A stage's command exited non-zero, or it did not write a declared output."""


@dataclass(frozen=True)
class Stage:
    name: str
    commands: tuple[tuple[str, ...], ...]
    inputs: tuple[str, ...] = ()            # play-dir relative; must exist or be written earlier
    outputs: tuple[str, ...] = ()           # play-dir relative; must exist after the stage
    optional_inputs: tuple[str, ...] = ()   # read if present (the stage decides what to do without)
    settings: tuple[str, ...] = ()          # per-play settings the stage's commands use
    code: tuple[Path, ...] = ()             # files whose contents the stage's behaviour depends on
    env: str = "nflgsplat"                  # which interpreter runs its commands (settings.python)
    when: Callable[[Mapping], bool] | None = None   # None: always; else run only if true


@dataclass
class Report:
    ran: list[str] = field(default_factory=list)
    up_to_date: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    would_run: list[tuple[str, str]] = field(default_factory=list)


# --- code dependencies -----------------------------------------------------

def _module_file(name: str) -> Path | None:
    p = REPO_ROOT / Path(*name.split("."))
    for c in (p.with_suffix(".py"), p / "__init__.py"):
        if c.is_file():
            return c
    return None


def code_files(script: Path | str) -> tuple[Path, ...]:
    """The script plus every ``nfl_gsplat`` module it imports, at any depth
    and including imports inside functions (repo-relative paths). The
    runner's own package is left out: changing the runner re-runs nothing."""
    start = Path(script)
    start = start if start.is_absolute() else REPO_ROOT / start
    seen: set[Path] = set()
    todo = [start]
    while todo:
        f = todo.pop()
        if f in seen:
            continue
        seen.add(f)
        for node in ast.walk(ast.parse(f.read_text(encoding="utf-8"))):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = [node.module] + [f"{node.module}.{a.name}" for a in node.names]
            for name in names:
                if name.split(".")[0] == "nfl_gsplat" and not name.startswith("nfl_gsplat.pipeline"):
                    m = _module_file(name)
                    if m is not None:
                        todo.append(m)
    return tuple(sorted(p.relative_to(REPO_ROOT) for p in seen))


# --- hashing with a size/mtime cache ---------------------------------------

class _Hasher:
    """sha256 of play files, cached on (size, mtime) so the clips are read once."""

    def __init__(self, play: Path, cache: dict):
        self.play, self.cache = play, cache

    def __call__(self, rel: str) -> str:
        p = self.play / rel
        if not p.exists():
            return ABSENT
        st = p.stat()
        hit = self.cache.get(rel)
        if hit and hit["size"] == st.st_size and hit["mtime_ns"] == st.st_mtime_ns:
            return hit["sha256"]
        digest = sha256_file(p)
        self.cache[rel] = {"size": st.st_size, "mtime_ns": st.st_mtime_ns, "sha256": digest}
        return digest


def _code_hash(path: Path) -> str:
    p = path if path.is_absolute() else REPO_ROOT / path
    if not p.is_file():
        raise PipelineError(f"code file {p} does not exist (check the stage's declaration).")
    return sha256_file(p)


# --- the run ---------------------------------------------------------------

def _render(cmd: Sequence[str], play: Path, values: Mapping) -> list[str]:
    def sub(m):
        key = m.group(1)
        if key == "play":
            return str(play)
        if key not in values:
            raise PipelineError(f"command {list(cmd)} uses {{{key}}}, which is not a per-play setting "
                                f"(known: {sorted(values)}).")
        return str(values[key])
    return [_PLACEHOLDER.sub(sub, a) for a in cmd]


def _fingerprint(stage: Stage, rendered, settings_used, input_versions, code_hashes) -> str:
    blob = json.dumps({"env": stage.env, "commands": rendered, "settings": settings_used,
                       "inputs": input_versions, "code": code_hashes}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _validate(active: list[Stage], play: Path) -> None:
    writers = {}
    for i, s in enumerate(active):
        for o in s.outputs:
            writers.setdefault(o, []).append(i)
    for i, s in enumerate(active):
        for f in s.inputs + s.optional_inputs:
            ws = writers.get(f, [])
            if any(w < i for w in ws):
                continue
            if ws and f not in s.outputs:
                later = active[ws[0]].name
                raise PipelineError(f"stage {s.name!r} reads {f}, which only a later stage ({later!r}) "
                                    "writes. Fix the stage order or the declaration.")
            if f in s.inputs and not (play / f).exists():
                raise PipelineError(f"stage {s.name!r} needs {play / f}, which no earlier stage writes "
                                    "and which is not in the play-dir.")


def _git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True,
                             text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True,
                               text=True, check=True).stdout.strip()
        return out + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown (git not available)"


def _execute(stage: Stage, rendered: list[list[str]], play: Path, python_for) -> None:
    log_path = play / LOGS / f"{stage.name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONPATH=str(REPO_ROOT))
    with open(log_path, "w", encoding="utf-8") as log:
        log.write(f"# stage {stage.name}, {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        for argv in rendered:
            if argv[0] == "@copy":
                src, dst = play / argv[1], play / argv[2]
                log.write(f"$ copy {src} -> {dst}\n")
                shutil.copy2(src, dst)
                continue
            full = [str(python_for(stage.env)), *argv]
            log.write("$ " + " ".join(full) + "\n")
            log.flush()
            rc = subprocess.run(full, cwd=REPO_ROOT, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
            if rc != 0:
                raise StageFailed(f"stage {stage.name!r} failed: exit {rc} from {argv[:2]}. "
                                  f"Full output: {log_path}")
    missing = [o for o in stage.outputs if not (play / o).exists()]
    if missing:
        raise StageFailed(f"stage {stage.name!r} exited 0 but did not write {missing}. "
                          f"Full output: {log_path}")


def run(stages: Sequence[Stage], play_dir: Path | str, *, play_settings: Mapping | None = None,
        python_for: Callable[[str], Path | str] | None = None, force: Sequence[str] = (),
        dry_run: bool = False, echo: Callable[[str], None] = print) -> Report:
    """Run ``stages`` on one play. ``python_for(env)`` gives each environment's
    interpreter (default: the machine settings). ``force`` re-runs the named
    stages whatever their fingerprint. ``dry_run`` only reports."""
    play = Path(play_dir).resolve()
    values = dict(play_settings or {})
    if python_for is None:
        from nfl_gsplat import settings
        python_for = settings.get().python
    unknown = set(force) - {s.name for s in stages}
    if unknown:
        raise PipelineError(f"--force names unknown stages {sorted(unknown)}.")

    report = Report()
    active = []
    for s in stages:
        if s.when is None or s.when(values):
            active.append(s)
        else:
            report.skipped.append(s.name)
    _validate(active, play)

    mpath = play / MANIFEST
    manifest = read_json(mpath) if mpath.exists() else {}
    records = manifest.setdefault("stages", {})
    hasher = _Hasher(play, manifest.setdefault("files", {}))

    first_writer, last_writer = {}, {}
    for i, s in enumerate(active):
        for o in s.outputs:
            first_writer.setdefault(o, i)
            last_writer[o] = i
    forced = {i for i, s in enumerate(active) if s.name in force}
    for f, w in last_writer.items():            # a final file changed behind the runner's back
        rec = records.get(active[w].name)
        if rec and rec.get("status") == "ok" and hasher(f) != rec["outputs"].get(f):
            forced.add(first_writer[f])

    version: dict[str, str] = {}                # what each file holds at this point in the chain
    commit = _git_commit()
    for i, stage in enumerate(active):
        rendered = [_render(c, play, values) for c in stage.commands]
        used = {k: values.get(k) for k in stage.settings}
        inputs = {f: version.get(f, hasher(f)) for f in stage.inputs + stage.optional_inputs}
        code = {str(p): _code_hash(Path(p)) for p in stage.code}
        fp = _fingerprint(stage, rendered, used, inputs, code)
        rec = records.get(stage.name)
        if i in forced:
            why = "forced"
        elif not rec or rec.get("status") != "ok":
            why = "not run before" if not rec else f"last run {rec.get('status')}"
        elif rec.get("fingerprint") != fp:
            why = "an input, setting or code file changed"
        else:
            why = None
        if why is None:
            version.update(rec["outputs"])
            report.up_to_date.append(stage.name)
            echo(f"[{stage.name}] up to date")
            continue
        if dry_run:
            report.would_run.append((stage.name, why))
            echo(f"[{stage.name}] would run: {why}")
            version.update({o: _PENDING for o in stage.outputs})
            forced.update(j for j in range(i + 1, len(active)) if set(active[j].outputs) & set(stage.outputs))
            continue

        echo(f"[{stage.name}] running: {why}")
        t0 = time.time()
        records[stage.name] = {"status": "running", "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
                               "fingerprint": fp, "commit": commit}
        write_json(mpath, manifest)
        try:
            _execute(stage, rendered, play, python_for)
        except PipelineError:
            records[stage.name]["status"] = "failed"
            write_json(mpath, manifest)
            raise
        outputs = {o: hasher(o) for o in stage.outputs}
        records[stage.name].update(status="ok", seconds=round(time.time() - t0, 1), inputs=inputs,
                                   outputs=outputs, settings=used, code=code)
        write_json(mpath, manifest)
        version.update(outputs)
        # later stages that also write these files lost their edits: redo them
        forced.update(j for j in range(i + 1, len(active)) if set(active[j].outputs) & set(stage.outputs))
        report.ran.append(stage.name)
        echo(f"[{stage.name}] ok in {time.time() - t0:.1f} s")
    return report


if __name__ == "__main__":       # pragma: no cover
    sys.exit("nfl_gsplat.pipeline.runner is a library; the stage list and CLI come next.")
