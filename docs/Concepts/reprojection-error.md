---
type: concept
kind: measure
status: in use
updated: 2026-11-24
---

# Reprojection error

How far a 3D point, projected back into a camera, lands from what that camera saw, in pixels. Judges cameras and fitted bodies.

**Measure** · status: **in use**

## Today

- Used for camera solves (grid distance to the paint) and body fits (joints against keypoints in each view).
- A ruler only sees errors across its camera's line of sight; depth needs the other camera.

## Where in the code

- `scripts/07m_measure_fit_reprojection.py`
- `scripts/05t_cross_view_error.py`: error in the other camera

## Notes

- **Findings:** [Rulers](../Findings/rulers.md), [Cameras and clip sync](../Findings/cameras-and-sync.md), [Pose](../Findings/pose.md), [Render and viewer](../Findings/render-and-viewer.md)
- **Decisions:** [0010: Don't refine the endzone camera to its own paint](../Decisions/0010-endzone-camera-not-refined-to-its-paint.md)
- **Related:** [Cameras](cameras.md), [Pose](pose.md), [Plausibility rulers](plausibility-rulers.md)

## Next

Keep it as the joint-level number where there is no ground truth. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
