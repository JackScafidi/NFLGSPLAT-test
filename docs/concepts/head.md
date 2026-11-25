---
type: concept
kind: object
status: located
updated: 2026-11-24
---

# Head

Where each player's head is and which way it faces.

**Goal object** · status: **located**

## Today

- The SMPL-X head joint, plus the keypoint detector's nose, eyes and ears.
- Drives the viewer's first-person view and the render's helmets.

## Where in the code

- `nfl_gsplat/pose/head_yaw.py`: head facing
- `nfl_gsplat/render/gaze.py`: first-person look direction
- `nfl_gsplat/render/helmet.py`: helmet drawing

## Notes

- **Findings:** [Render and viewer](../findings/render-and-viewer.md), [Pipeline runs and versions](../findings/pipeline-and-versions.md), [Pose](../findings/pose.md)
- **Related:** [Pose](pose.md), [Render and viewer](render-and-viewer.md), [Player body](player-body.md)

## Next

Export head position and facing per frame. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
