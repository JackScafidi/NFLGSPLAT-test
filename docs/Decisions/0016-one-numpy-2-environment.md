---
type: decision
status: proposed
date: 2026-11-25
---

# 0016: One NumPy 2 environment for the whole pipeline

## Context

The pipeline runs in two environments: `nflgsplat` (NumPy 2) for
calibration, tracking and identity, and `smplx312` (NumPy 1.26) for pose,
refit and render. Data crosses between them as pickles, and HANDOFF.md's rule
was that pickles written under NumPy 2 must never reach NumPy 1.
`pyproject.toml` pins `numpy<2`, citing paddle and the old torch/mmcv stack.

The [trial on 2026-11-25](../Journal/2026-11-25-one-environment-trial.md) put
every package the pipeline imports into one NumPy 2.4.6 environment with CUDA
torch. The CPU suite passed (1396 passed; the 17 skips need model files), and
NumPy 2 read NumPy 1.26 pickles.

## Decision

Proposed: run the whole pipeline in one NumPy 2 environment, defined in the
repo with a lockfile, and lift the `numpy<2` pin.

Not adopted yet. The gate is play 1 run end to end in that environment on
this PC, with its measures (census, steps, hops, surges, joint jitter) no
worse than v122.

The owner chose this direction on 2026-11-25: build the one environment, and
fall back to two only if play 1 fails in it.

## Consequences

- If adopted: one interpreter setting instead of two, no pickle rule between
  environments, and one lockfile to maintain.
- `pipeline_play.sh`'s `PYN` / `PYS` split and the two `local.yaml`
  interpreter settings would collapse into one.
- If play 1 fails in it: keep two environments, both defined in the repo
  with lockfiles, as the foundations plan's fallback says.

## Related

- **Concepts:** [Pose](../Concepts/pose.md), [Render and viewer](../Concepts/render-and-viewer.md)
- **Journal:** [2026-11-25: One NumPy 2 environment, trial](../Journal/2026-11-25-one-environment-trial.md)
- **Decisions:** [0014: One settings layer](0014-machine-settings-layer.md)
