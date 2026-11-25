---
type: journal
date: 2026-11-25
---

# Pipeline runner: the core

## What was done

- Drafted the runner's design from a stage-by-stage read of
  `scripts/pipeline_play.sh`: [the spec](../Superpowers/specs/2026-11-25-pipeline-runner-design.md)
  (draft, with four open questions for the owner).
- Built step 1, the core: `nfl_gsplat/pipeline/runner.py`, tested in
  `tests/test_pipeline_runner.py` with fake stages. No real stage is declared
  yet, and `pipeline_play.sh` is unchanged and still the way to run a play.

## What was measured

- 17 runner tests pass. To check they test the logic, each of the three chain
  rules was broken in turn:
  - stop re-running later writers of an overwritten file: 2 tests fail;
  - drop the hand-edit check: 1 fails;
  - compare inputs on disk instead of along the chain: 2 fail.
- Full CPU suite: 1410 passed, 20 skipped. Ruff passes.

## What it means

- The runner decides re-runs from content, not markers. In-place rewrites
  (`cameras.npz` through refine and shift; `tracks.parquet` about ten times)
  don't re-run every invocation, and a re-run that writes the same bytes
  stops there.
- A stage's code is its script plus every `nfl_gsplat` module it imports, so
  editing one module re-runs only the stages that use it.
- Step 2, declaring the 30 real stages, waits on the spec's open questions.
  Step 3, running play 1, waits on its inputs being on this PC.

## Related

- **Concepts:** [Play data](../Concepts/play-data.md) (the runner's manifest
  records what produced each file)
- **Spec:** [Pipeline runner](../Superpowers/specs/2026-11-25-pipeline-runner-design.md)
