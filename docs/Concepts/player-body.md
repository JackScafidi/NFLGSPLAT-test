---
type: concept
kind: object
status: located
updated: 2026-11-24
---

# Player body

Where each player's body is on every frame: the root (pelvis) on the field, and the full SMPL-X joint set the render draws.

**Goal object** · status: **located**

## Today

- Two-camera triangulation where both cameras see the player; the box bottom of one camera otherwise ([0007](../Decisions/0007-box-bottom-is-the-one-view-ground-point.md)).
- About 9 to 10 of 22 players are seen by both cameras on a given frame (open items, 2026-09-10).
- Not yet exported as play data; it lives in stage files and the render's timeline.

## Where in the code

- `nfl_gsplat/render/play_timeline.py`, `nfl_gsplat/render/timeline.py`: ground position per frame
- `nfl_gsplat/pose/triangulate.py`, `nfl_gsplat/pose/refit_fused.py`: two-view joints and SMPL-X refit
- `nfl_gsplat/pose/forward_kinematics.py`: SMPL-X joints from pose parameters

## Notes

- **Findings:** [Placement](../Findings/placement.md), [Pose](../Findings/pose.md), [Rulers](../Findings/rulers.md), [Render and viewer](../Findings/render-and-viewer.md)
- **Decisions:** [0007: Keep the box bottom as the one-view ground point](../Decisions/0007-box-bottom-is-the-one-view-ground-point.md)
- **Related:** [Placement](placement.md), [Pose](pose.md), [Tracking](tracking.md), [Play data](play-data.md)

## Next

Export root position, speed and heading per frame in the play data. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
