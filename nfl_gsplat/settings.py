"""Machine settings: where this PC keeps data, models, diagnostics and the
two pipeline Python environments.

Nothing in the code names a particular person's machine. Each setting is read
from, in order:

1. an environment variable (``NFLG_DATA_ROOT`` and so on, see ``ENV``);
2. ``local.yaml`` at the repo root, which git ignores (copy
   ``local.example.yaml`` to start one);
3. a default inside the repo.

A command-line flag on a script still beats all three. Relative paths are
taken from the repo root, never from the working directory, so a script runs
the same from any folder.

Secrets are not settings. The Roboflow key stays in ``ROBOFLOW_API_KEY`` and
the Kaggle token where the Kaggle client looks for it (``~/.kaggle``); neither
is ever written to ``local.yaml``.

``python -m nfl_gsplat.settings --shell`` prints the settings as ``export``
lines, which is how ``scripts/pipeline_play.sh`` reads them.
"""
from __future__ import annotations

import argparse
import functools
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from nfl_gsplat.errors import SetupError

REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_YAML = REPO_ROOT / "local.yaml"

# setting -> environment variable
ENV = {
    "data_root": "NFLG_DATA_ROOT",
    "body_models": "NFLG_BODY_MODELS",
    "diag_dir": "NFLG_DIAG_DIR",
    "python_nflgsplat": "NFLG_PY_NFLGSPLAT",
    "python_smplx": "NFLG_PY_SMPLX",
}
KEYS = tuple(ENV)

# environment name -> setting. nflgsplat (NumPy 2) runs calibration, tracking
# and identity; smplx312 (NumPy 1.26) runs pose, refit and render.
_PYTHONS = {"nflgsplat": "python_nflgsplat", "smplx": "python_smplx"}

_FIX = "set it in local.yaml at the repo root (copy local.example.yaml) or in"


@dataclass(frozen=True)
class Settings:
    data_root: Path
    body_models: Path
    diag_dir: Path
    python_nflgsplat: Path | None
    python_smplx: Path | None

    def python(self, env: str) -> Path:
        """The interpreter of one pipeline environment: "nflgsplat" or "smplx"."""
        key = _PYTHONS.get(env)
        if key is None:
            raise SetupError(f"no Python environment called {env!r}; "
                             f"the pipeline has {sorted(_PYTHONS)}.")
        exe = getattr(self, key)
        if exe is None:
            raise SetupError(f"{key} is not set: {_FIX} the {ENV[key]} environment variable. "
                             f"It is the python.exe of the {env} environment.")
        if not exe.is_file():
            raise SetupError(f"{key} = {exe} does not exist. Fix the path in local.yaml "
                             f"or {ENV[key]}.")
        return exe


def _read_local_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    import yaml
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise SetupError(f"{path} must be a mapping of setting: value (see local.example.yaml).")
    unknown = sorted(set(data) - set(KEYS))
    if unknown:
        raise SetupError(f"{path} has unknown settings {unknown}; the known ones are {list(KEYS)} "
                         "(see local.example.yaml).")
    return data


def _as_path(value) -> Path:
    p = Path(str(value)).expanduser()
    return p if p.is_absolute() else (REPO_ROOT / p).resolve()


def load(*, environ: Mapping[str, str] | None = None, local_yaml: Path | None = None) -> Settings:
    """Resolve every setting. ``environ`` and ``local_yaml`` default to the
    real environment and the repo's local.yaml (tests pass their own)."""
    environ = os.environ if environ is None else environ
    from_file = _read_local_yaml(LOCAL_YAML if local_yaml is None else Path(local_yaml))

    def raw(key):
        value = environ.get(ENV[key])
        if value:
            return value
        value = from_file.get(key)
        return None if value in (None, "") else value

    data_root = _as_path(raw("data_root") or "data")
    body_models = _as_path(raw("body_models")) if raw("body_models") else data_root / "body_models"
    return Settings(
        data_root=data_root,
        body_models=body_models,
        diag_dir=_as_path(raw("diag_dir") or "outputs/diag"),
        python_nflgsplat=_as_path(raw("python_nflgsplat")) if raw("python_nflgsplat") else None,
        python_smplx=_as_path(raw("python_smplx")) if raw("python_smplx") else None,
    )


@functools.cache
def get() -> Settings:
    """This machine's settings, read once per process."""
    return load()


def _quote(path: Path) -> str:
    return "'" + path.as_posix().replace("'", "'\\''") + "'"


def shell_exports(s: Settings) -> list[str]:
    """``export`` lines for bash. An environment Python that is not set is
    left out, so the script can say which one is missing."""
    lines = [f"export NFLG_REPO_ROOT={_quote(REPO_ROOT)}"]
    for key in KEYS:
        value = getattr(s, key)
        if value is not None:
            lines.append(f"export {ENV[key]}={_quote(value)}")
    return lines


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--shell", action="store_true", help="print the settings as bash export lines")
    args = ap.parse_args(argv)
    s = get()
    if args.shell:
        print("\n".join(shell_exports(s)))
        return
    print(f"repo_root        {REPO_ROOT}")
    for key in KEYS:
        print(f"{key:<17}{getattr(s, key) or '(not set)'}")


if __name__ == "__main__":
    main()
