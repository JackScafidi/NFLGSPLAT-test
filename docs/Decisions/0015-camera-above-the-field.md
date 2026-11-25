---
type: decision
status: accepted
date: 2026-11-24
---

# 0015: The joint solve keeps the camera above the field

## Context

The joint solve tries both labelings of the hashes, as given and mirrored
left to right, and assumed no rigid camera fits the mirrored one. One does:
the true camera turned 180 degrees about the X axis. That maps every field
point (x, y, 0) to (x, -y, 0), exactly the mirrored field, and puts the camera
at (x, -y, -z), under the turf. Nothing bounded the camera's height.

Measured 2026-11-24 on `test_cross_cam_calib`'s synthetic (true endzone camera
at (-110, -8, 45) m, 40 frames): once the anchor candidate got a 200-evaluation
budget, a mirrored grid candidate walked to (-110.7, 8.0, -45.1) and won with a
subsample cost of 1487. The right-side candidate reaches 1518 (measured with
the bound in place, where it wins), so the twin's fit is no worse. The endzone camera came out 91 m off,
with 17 of 40 frames solved. At the old 50-evaluation budget the right camera
had won, but by luck.

## Decision

`_solve_once` bounds the camera centre's height at `_MIN_CAMERA_Z` = 1 m
(`nfl_gsplat/calibration/joint_solve.py`, merged in PR #3, commit 1a60622).

## Consequences

- With the bound, the synthetic recovers the camera 0.08 m off with all 40
  frames, at both budgets.
- Real footage is covered too: a play whose hash labeling is flipped can no
  longer get an underground camera.
- `test_mirrored_labels_cannot_fit_a_camera_under_the_field` starts the solve
  at the exact twin. Without the bound it stays at z = -95 m.

## Related

- **Concepts:** [Cameras](../Concepts/cameras.md)
- **Journal:** [2026-11-24: CI and the joint solve](../Journal/2026-11-24-ci-and-joint-solve.md)
