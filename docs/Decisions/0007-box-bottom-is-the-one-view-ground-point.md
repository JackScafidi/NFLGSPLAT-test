---
type: decision
status: accepted
date: 2026-09-08
source: docs/HANDOFF.md, "What has been measured and rejected" (recorded 2026-11-24)
---

# 0007: Keep the box bottom as the one-view ground point

## Decision

A body seen by one camera stands on its box bottom, not on its ankle keypoints. The ankles gave no gain.

## Evidence

Word for word from HANDOFF.md. Re-propose only with new evidence.

- **Ankle keypoints as the one-view ground point (2026-09-08, play 1, 2773
  two-view frames, judged against the fused refit's pelvis):** box bottom
  p50 0.55 m (p90 1.35), mean of the two ankle keypoints dropped 8 cm to
  the turf p50 0.53 (p90 1.45), the lower ankle 0.62. No gain. (The
  "opposite biases" first reported here, box -0.32 / ankles +0.28 along
  y, were the rest-pelvis offset: that comparison used transl, not the
  pelvis; against the true pelvis the box point is unbiased, x -0.01 y
  +0.04, p50 0.52 m.) The 0.5 m is the placement ambiguity of one view
  against the hips' triangulation, not the choice of pixel.

## Related

- **Concepts:** [Placement](../Concepts/placement.md), [Feet](../Concepts/feet.md), [Player body](../Concepts/player-body.md)
- **Findings:** [Placement on the field](../Findings/placement.md)
