# NFLGSPLAT

Two synced broadcast clips of an NFL play (sideline + endzone) in. Out: a clean
3D recreation of the play, plus play data locating every player's body, head,
hands and feet, the ball and the referees on every frame.

- **Layer 1, extraction:** video to play data. Built first.
- **Layer 4, viewing:** the 3D render and viewer, reading only the play data.
  Built first.
- **Layers 2 and 3:** a store across plays and an analysis library. Added later.

Plan: [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
Start page for notes: [docs/Home.md](docs/Home.md).

## Layout

- `nfl_gsplat/`: the Python package. `nfl_gsplat/pipeline/` is the new runner's
  core (no stages declared yet; see its spec in `docs/Superpowers/specs/`).
- `scripts/`: numbered pipeline stages and tools. `scripts/pipeline_play.sh` is
  the working pipeline; the README's conda/SLURM path is out of date.
- `tests/`: CPU unit tests.
- `viewer/`: the browser viewer.
- `docs/`: an Obsidian vault (see below).
- `data/`: footage, models and per-play outputs. Gitignored.

## Commands (PowerShell, repo root)

```powershell
.\.venv\Scripts\Activate.ps1
pytest -m "not gpu and not slow and not real_video" -n 4
ruff check nfl_gsplat tests scripts
```

ffmpeg must be on PATH, or the `tests/test_field.py` extraction tests fail.

## Machine settings

Paths and interpreters for this machine come from `nfl_gsplat/settings.py`:
an environment variable (`NFLG_DATA_ROOT`, `NFLG_BODY_MODELS`,
`NFLG_DIAG_DIR`, `NFLG_PY_NFLGSPLAT`, `NFLG_PY_SMPLX`), then the gitignored
`local.yaml` at the repo root (copy `local.example.yaml`), then defaults inside
the repo. `python -m nfl_gsplat.settings` prints what's in effect.

- Never write a machine path into code. Use `settings.get()`, or add a setting.
- Relative paths are taken from the repo root, never the working folder.
- Secrets never go in `local.yaml`. Keys stay in environment variables or the
  tool's own location (`~/.kaggle`).

## Plugins

`.claude/settings.json` enables the project's Claude Code plugins, so any
machine that opens the repo is offered the same set:

- From `claude-plugins-official`: context7, github, claude-md-management,
  commit-commands, feature-dev, hookify, pyright-lsp, superpowers.
- From `knowledge-work-plugins`: data, design, engineering.

pyright-lsp needs the `pyright` language server on PATH
(`pip install pyright` in the venv). Personal overrides go in
`.claude/settings.local.json`, which git ignores.

## Notes go in the docs/ vault

| What | Where | Name |
| --- | --- | --- |
| A decision (what was chosen, why, what it rules out) | `docs/Decisions/` | `NNNN-short-title.md`, next free number |
| A session's work or a finding | `docs/Journal/` | `YYYY-MM-DD-short-title.md` |
| Facts about one play | `docs/Plays/` | `<away>-at-<home>-<season>-wk<N>-play-NNN.md` |
| A design spec, and its implementation plan | `docs/Superpowers/specs/`, `docs/Superpowers/plans/` | `YYYY-MM-DD-topic(-design).md` |
| One durable fact for future sessions | `docs/Agent-context/` | add a line to `MEMORY.md` |

- Start each note from `docs/Templates/`, with front matter (`type`, `date`, and
  `status` where it applies).
- Link every new finding, decision, play and journal note to the concepts it
  touches (`docs/Concepts/`: goal objects, pipeline stages, measures) in a
  "Related" section. When a concept's state changes, update its "Today"
  section. A new concept needs a note from `Templates/concept.md` and a row in
  `Concepts.md`.
- Add every new note to its folder's index, which is named after its section
  so the Obsidian graph reads clearly: `Decisions.md`, `Findings.md`,
  `Journal.md`, `Plays.md`, `Specs-and-plans.md`, `Archive.md`, `Concepts.md`,
  and `MEMORY.md` for agent-context. Each folder also has a one-line
  `README.md` that points GitHub readers at its index; Obsidian ignores those
  (`userIgnoreFilters` in `docs/.obsidian/app.json`). A new folder needs both,
  plus its README in that list.
- Use markdown links (`[text](relative/path.md)`), not `[[wikilinks]]`, so links
  work on GitHub.
- A decision is never rewritten to say something else. A new decision
  supersedes it, and both notes say so in `status`.
- Measured results include numbers, units and the play they came from.
- `tests/test_docs_vault.py` enforces these rules in CI. It checks that every
  link resolves, every note is in its folder's index, front matter is present,
  decisions are numbered with the index's status matching the note's, and
  README pointers are hidden. Run it after editing notes:
  `pytest tests/test_docs_vault.py -q`.

## Hard rules

- Never commit NFL footage, frames or diagnostic images. Pasted images go to
  `docs/_attachments/`, which is gitignored.
- Never print or commit secrets: the Roboflow key, the NFL login and the Kaggle
  token.
- Everything runs locally on this PC (RTX 2060, 12 GB). No PACE, no SLURM.
- Commit or push only when the owner asks.
- Don't run `pip install -e .` in the two pipeline environments (`nflgsplat`,
  NumPy 2; `smplx312`, NumPy 1.26). The project pins NumPy below 2.
- Fail loudly with a pointer to the fix; no silent fallbacks.
- A correction must beat what it corrects, measured, before it is applied.
