"""The docs/ vault keeps its own rules (CLAUDE.md, "Notes go in the docs/ vault").

Indexes and links are kept by hand, so drift is easy and silent: a note left
out of its index, a link to a renamed file, a decision whose status differs
between its note and the index. These checks make that drift fail the build.

Legacy notes (the June to August specs and plans, the archive, the old
agent-context notes, the root-level HANDOFF-era files) predate the rules: they
are only link-checked.
"""
import json
import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"

# folder -> its index note (every other note in the folder must be linked from it)
INDEXES = {
    "decisions": "Decisions.md",
    "journal": "Journal.md",
    "findings": "Findings.md",
    "plays": "Plays.md",
    "concepts": "Concepts.md",
    "archive": "Archive.md",
    "agent-context": "MEMORY.md",
    "superpowers/specs": "../Specs-and-plans.md",
    "superpowers/plans": "../Specs-and-plans.md",
}

# folder -> (front matter type, keys every note there must carry)
FRONT_MATTER = {
    "decisions": ("decision", ("date", "status")),
    "journal": ("journal", ("date",)),
    "plays": ("play", ("date", "status")),
    "concepts": ("concept", ("updated", "status")),
    "findings": ("findings", ()),
    "reference": ("reference", ()),
}

# folders under the current rules, where [[wikilinks]] are not allowed
NO_WIKILINKS = ("decisions", "journal", "plays", "concepts", "findings", "reference")

_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_FENCE = re.compile(r"^```.*?^```", re.S | re.M)
_CODE = re.compile(r"`[^`\n]*`")


def _prose(text: str) -> str:
    """The text with fenced blocks and inline code removed (examples, not links)."""
    return _CODE.sub("", _FENCE.sub("", text))


def _notes(folder: str = "") -> list[Path]:
    root = DOCS / folder
    return sorted(p for p in root.glob("*.md") if p.name != "README.md")


def _all_notes() -> list[Path]:
    return sorted(p for p in DOCS.rglob("*.md") if ".obsidian" not in p.parts)


def _front_matter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return yaml.safe_load(text[4:end]) or {}


def _local_links(path: Path) -> list[str]:
    out = []
    for target in _LINK.findall(_prose(path.read_text(encoding="utf-8"))):
        target = target.split("#")[0]
        if target and not re.match(r"[a-z][a-z0-9+.-]*:", target):     # skip https:, mailto: ...
            out.append(target)
    return out


_LINKED_FILES = [*_all_notes(), REPO / "CLAUDE.md", REPO / "README.md",
                 *sorted((REPO / "archive").rglob("README.md"))]


@pytest.mark.parametrize("path", _LINKED_FILES, ids=lambda p: p.relative_to(REPO).as_posix())
def test_every_relative_link_resolves(path):
    broken = [t for t in _local_links(path) if not (path.parent / t).exists()]
    assert not broken, f"{path.relative_to(REPO)} links to missing files: {broken}"


@pytest.mark.parametrize("folder", sorted(INDEXES))
def test_every_note_is_listed_in_its_folders_index(folder):
    index = (DOCS / folder / INDEXES[folder]).resolve()
    listed = {(index.parent / t).resolve() for t in _local_links(index)}
    missing = [p.name for p in _notes(folder) if p.resolve() != index and p.resolve() not in listed]
    assert not missing, f"{index.relative_to(REPO)} does not list: {missing}"


@pytest.mark.parametrize("folder", sorted(FRONT_MATTER))
def test_notes_carry_their_front_matter(folder):
    kind, keys = FRONT_MATTER[folder]
    index = INDEXES.get(folder)
    problems = []
    for p in _notes(folder):
        if p.name == index:
            continue
        fm = _front_matter(p)
        if fm is None:
            problems.append(f"{p.name}: no front matter")
            continue
        if fm.get("type") != kind:
            problems.append(f"{p.name}: type is {fm.get('type')!r}, not {kind!r}")
        problems += [f"{p.name}: no {k!r}" for k in keys if not fm.get(k)]
    assert not problems, "\n".join(problems)


@pytest.mark.parametrize("folder", NO_WIKILINKS)
def test_current_notes_use_markdown_links_not_wikilinks(folder):
    offenders = [p.name for p in _notes(folder) if "[[" in _prose(p.read_text(encoding="utf-8"))]
    assert not offenders, f"wikilinks (use [text](path.md), so links work on GitHub): {offenders}"


def test_decisions_are_numbered_and_the_index_agrees_with_each_note():
    rows = {}
    for line in (DOCS / "decisions" / "Decisions.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| \[(\d{4})\]\(([^)]+)\) \| ([^|]+) \| ([^|]+) \|", line)
        if m:
            rows[m.group(1)] = (m.group(2), m.group(4).strip())
    notes = [p for p in _notes("decisions") if p.name != "Decisions.md"]
    numbers = [p.name[:4] for p in notes]
    assert numbers == [f"{i:04d}" for i in range(1, len(notes) + 1)], "decision numbers have a gap or a repeat"
    for p in notes:
        num = p.name[:4]
        assert num in rows, f"Decisions.md has no row for {p.name}"
        link, status = rows[num]
        assert link == p.name, f"Decisions.md row {num} links to {link}, not {p.name}"
        fm_status = str(_front_matter(p)["status"])
        assert status.startswith(fm_status), (
            f"{p.name} says status {fm_status!r} but Decisions.md says {status!r}")
        title = p.read_text(encoding="utf-8").split("\n# ", 1)[1].splitlines()[0]
        assert title.startswith(f"{num}:"), f"{p.name}'s title should start '{num}:'"


def test_journal_names_carry_their_date():
    for p in _notes("journal"):
        if p.name == "Journal.md":
            continue
        assert re.match(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$", p.name), f"{p.name}: name it YYYY-MM-DD-short-title.md"
        assert str(_front_matter(p)["date"]) == p.name[:10], f"{p.name}: its date differs from its name"


def test_every_readme_pointer_is_hidden_from_obsidian():
    ignored = set(json.loads((DOCS / ".obsidian" / "app.json").read_text(encoding="utf-8"))["userIgnoreFilters"])
    readmes = {p.relative_to(DOCS).as_posix() for p in DOCS.rglob("README.md") if ".obsidian" not in p.parts}
    assert readmes <= ignored, f"add to userIgnoreFilters in docs/.obsidian/app.json: {sorted(readmes - ignored)}"
    for folder in ("decisions", "journal", "findings", "plays", "concepts", "archive"):
        assert (DOCS / folder / "README.md").is_file(), f"docs/{folder}/ needs its one-line README.md pointer"
