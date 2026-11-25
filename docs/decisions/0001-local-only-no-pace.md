---
type: decision
status: accepted
date: 2026-11-24
---

# 0001: Run everything locally; no PACE, no SLURM

## Context

The README and `scripts/run_season.py` describe a SLURM path for Georgia Tech's
PACE cluster, and an older memory note asks for GPU jobs on PACE's embers
partition. The working pipeline (`scripts/pipeline_play.sh`) has run locally
since 2026-09-02.

## Decision

Everything runs on the local PC (RTX 2060, 12 GB). PACE is not used.

## Consequences

- The SLURM files (`run_season.py`, `*.sbatch`, `scripts/slurm/`) are removed
  or archived. Archived on 2026-11-25, see
  [0017](0017-archive-the-slurm-path.md).
- The PACE memory note and `PACE_FIELD_TRAIN.md` moved to
  [archive/](../archive/Archive.md) on 2026-11-24.
- Stages must fit 12 GB of VRAM and stay under about 10 minutes, so a power-off
  costs little.
