---
type: journal
date: 2026-11-24
---

# CI and the joint solve

## What was done

- Enabled GitHub Actions on the fork, added a manual trigger, and fixed the
  CPU test job: `pyarrow<21` and `torch` declared in `pyproject.toml`, CPU
  torch installed first, ffmpeg and the OpenCV system libraries on the runner
  (PR #3).
- Installed WSL Ubuntu and Docker Engine on this PC to reproduce Linux-only
  failures in a `python:3.11` container running the CI recipe.
- Joint solve: the anchor candidate's budget raised from 50 to 200
  evaluations (`_ANCHOR_NFEV`), then the camera bounded above the field
  ([decision 0015](../decisions/0015-camera-above-the-field.md)).

## What was measured

- `test_joint_solve`'s shifted-frame scenario (40 frames, one frame shifted a
  yard line) failed only on GitHub's Linux runner: centre 0.53 m off, against
  0.10 m on Windows and 0.15 m in the Linux container on this PC's
  i7-11700F. With the old code, the full CI recipe in the container passed
  (1371 tests), so the failure also needed GitHub's processor.
- Cause: the anchor solve stopped at its 50-evaluation cap (scipy status 0)
  before converging. Its early-accept then turned on floating-point details.
  Windows accepted (cost 7587); Linux didn't (15004) and fell back to the
  grid. It needs 75 to 80 evaluations; at 200 it converges, giving 0.047 m on
  Windows and 0.037 m on Linux.
- The bigger budget broke `test_cross_cam_calib` on every platform: a
  mirrored grid candidate reached the camera's exact twin under the field
  (z = -45 m), and the endzone came out 91 m off. With a 1 m height bound:
  0.08 m, 40 of 40 frames.
- After both fixes: 1373 passed on Windows, in the container, and on GitHub.

## What it means

- A solve cut off before it converges lands wherever the machine's
  floating-point maths takes it, so a test of it is platform-dependent. The
  anchor now converges.
- The reflection test relied on "no rigid camera fits the mirrored labeling".
  That is only true for a camera above the field, and the code now enforces
  it.
- Not checked: real footage takes the grid route with 12-evaluation probes,
  which are also cut off before converging. Whether that route is
  platform-sensitive needs footage.

## Related

- **Concepts:** [Cameras](../concepts/cameras.md)
- **Decisions:** [0015: The joint solve keeps the camera above the field](../decisions/0015-camera-above-the-field.md)
