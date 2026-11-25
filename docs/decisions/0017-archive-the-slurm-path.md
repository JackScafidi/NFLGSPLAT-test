---
type: decision
status: accepted
date: 2026-11-25
---

# 0017: Archive the SLURM path, don't delete it

## Context

[Decision 0001](0001-local-only-no-pace.md) took PACE out of the project and
said the SLURM files are "removed or archived". The SLURM path was more than
job files:

- `scripts/run_season.py` built the season's job plan with
  `nfl_gsplat/season/dag.py`, which had its own tests;
- `configs/season.yaml` held the SLURM settings, and only `run_season.py`
  read it.

The rest of `nfl_gsplat/season/` (play discovery, scaffolding, the cross-play
UID and body-shape steps) does not use SLURM. `scripts/new_play.py` and four
test files use it.

## Decision

Archive, chosen by the owner on 2026-11-25. Move the SLURM files to
`archive/slurm/`, keeping their original paths under it. That folder is
outside the package, the test suite and the lint.

Moved:

- `scripts/run_season.py`;
- the ten `.sbatch` files;
- `nfl_gsplat/season/dag.py` and `tests/test_season_dag.py`;
- `configs/season.yaml`.

## Consequences

- Nothing in the package, scripts or tests refers to SLURM any more. Two
  messages that named `.sbatch` files now name the local command
  (`run_autocalib.py`) or the archive (`05h`'s docstring).
- The non-SLURM parts of `nfl_gsplat/season/` stay where they are.
- A season-wide run on this PC needs its own design, as part of Layer 2.
- The archived files won't run as they stand. They're a record, not a fallback.

## Related

- **Concepts:** none directly (compute setup).
- **Decisions:** [0001: Run everything locally; no PACE, no SLURM](0001-local-only-no-pace.md)
