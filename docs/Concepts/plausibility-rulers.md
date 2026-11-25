---
type: concept
kind: measure
status: in use
updated: 2026-11-24
---

# Plausibility rulers

Checks that the motion is physically possible: steps, hops, surges, joint jitter and the census.

**Measure** · status: **in use**

## Today

- Run on every version (`scripts/07l`, about 3 minutes on CPU).
- Play 1 at v122: steps 20 / 0, hops 0, surges 4.3 %.

## Where in the code

- `scripts/07l_measure_plausibility.py`
- `nfl_gsplat/pose/plausibility.py`
- `nfl_gsplat/render/motion_rulers.py`
- Described in [PLAUSIBILITY.md](../PLAUSIBILITY.md)

## Notes

- **Findings:** [Rulers](../Findings/rulers.md), [Pipeline runs and versions](../Findings/pipeline-and-versions.md), [Ball and play events](../Findings/ball-and-play-events.md)
- **Related:** [Census](census.md), [Reprojection error](reprojection-error.md), [Footage review](footage-review.md)

## Next

Store each run's results by date so progress is visible. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
