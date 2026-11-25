---
type: concept
kind: stage
status: working
updated: 2026-11-24
---

# Cameras

Both cameras' position, orientation and lens on every frame, and the time offset between the two clips. Every 3D position goes through them.

**Pipeline stage** · status: **working**

## Today

- The sideline camera is solved from the painted yard lines, then refined frame by frame.
- The endzone camera is solved on its own paint (`scripts/08l`).
- The endzone clip is offset from the sideline clip (play 1: -15 frames), measured from moving players (`scripts/05o`).

## Where in the code

- `nfl_gsplat/calibration/`: `from_paint.py`, `endzone_paint.py`, `joint_solve.py`, `cameras_io.py`
- `scripts/08_reconstruct_all22.py`, `08e_refine_cameras.py`, `08d_field_offset.py`, `08l_endzone_paint.py`
- `nfl_gsplat/pose/clip_offset.py`: the clip offset

## Notes

- **Findings:** [Cameras and clip sync](../findings/cameras-and-sync.md), [Rulers](../findings/rulers.md)
- **Decisions:** [0009: Don't refine per-frame cameras to the yard lines alone](../decisions/0009-no-per-frame-camera-refine-to-yard-lines-alone.md), [0010: Don't refine the endzone camera to its own paint](../decisions/0010-endzone-camera-not-refined-to-its-paint.md), [0011: Don't set the endzone pitch from the ankle ruler alone](../decisions/0011-endzone-pitch-not-from-ankle-ruler.md), [0012: Don't seed the joint solve with another play's mount](../decisions/0012-no-seeding-joint-solve-from-another-play.md), [0013: Bound the paint reader's implied lens](../decisions/0013-bound-implied-lens-in-paint-labelling.md)
- **Related:** [Tracking](tracking.md), [Placement](placement.md), [Reprojection error](reprojection-error.md)

## Next

Make every stage read cameras through one settings layer, not hardcoded paths. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
