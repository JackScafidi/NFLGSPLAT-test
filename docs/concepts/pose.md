---
type: concept
kind: stage
status: working
updated: 2026-11-25
---

# Pose

Each body's joints: 2D keypoints in both views, triangulated where both see the body, then a SMPL-X body fitted to them.

**Pipeline stage** · status: **working**

## Today

- YOLOv8-pose keypoints (17 COCO points) per tracked person in both views.
- Two-view bodies are refit to both cameras' keypoints; one-view bodies to one camera's.
- A pose detector fine-tuned on this footage is in use; VPoser priors were measured and not shipped.
- The pose stack runs in its own NumPy 1.26 environment (`smplx312`). On 2026-11-25 its CPU tests all passed under NumPy 2, so one environment may do ([0016](../decisions/0016-one-numpy-2-environment.md), proposed).

## Where in the code

- `nfl_gsplat/pose/`: `triangulate.py`, `refit_fused.py`, `fit_mono2d.py`, `pose_prior.py`, `keypoint_filter.py`, `infill.py`
- `scripts/05c`, `05m`, `05n`, `05f`, `05p`, `05r`, `09h_finetune_pose.py`

## Notes

- **Findings:** [Pose](../findings/pose.md), [Rulers](../findings/rulers.md), [Render and viewer](../findings/render-and-viewer.md)
- **Decisions:** [0006: Don't pair cameras by the regressor's body pose](../decisions/0006-regressor-pose-is-not-a-pairing-cue.md), [0016: One NumPy 2 environment](../decisions/0016-one-numpy-2-environment.md) (proposed)
- **Journal:** [2026-11-25: One NumPy 2 environment, trial](../journal/2026-11-25-one-environment-trial.md)
- **Related:** [Player body](player-body.md), [Hands](hands.md), [Feet](feet.md), [Head](head.md), [Reprojection error](reprojection-error.md)

## Next

Add hand and foot points; export joints with their source and confidence. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
