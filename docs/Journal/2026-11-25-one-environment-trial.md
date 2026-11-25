---
type: journal
date: 2026-11-25
---

# One NumPy 2 environment: trial

## What was done

The foundations plan asks first whether the pose stack now runs on NumPy 2,
which would let one environment replace the two (`nflgsplat` on NumPy 2,
`smplx312` on NumPy 1.26).

- Built a trial venv outside the repo, `C:\Users\jacks\venvs\np2trial`
  (Python 3.11), with every third-party package the pipeline's scripts import.
  The list came from walking each `pipeline_play.sh` stage's imports through
  `nfl_gsplat`.
- torch and torchvision came from the cu128 index. `human_body_prior` (VPoser)
  was installed from GitHub with `--no-deps`, because a plain install swaps
  torch for a CPU build (see the trap in [render and viewer](../Findings/render-and-viewer.md)).
- Ran the CPU suite in it, with the repo on `PYTHONPATH` (no editable install).

Versions: numpy 2.4.6, torch 2.11.0+cu128 (CUDA available), torchvision
0.26.0, opencv 5.1.0, scipy 1.17.1, pandas 3.1.1, pyarrow 26.0.1, omegaconf
2.4.0, smplx (latest), human_body_prior (GitHub head), ultralytics 8.4.218,
easyocr 1.7.2.

## What was measured

- CPU suite: **1396 passed, 17 skipped**. The test venv (NumPy 1.26) runs
  1391; five more run here because torchvision and smplx are installed.
- All 17 skips need model files that aren't on this PC: the SMPL-X model
  (`test_foot_lock`, `test_gait`, `test_roster_shape_weight`) or the VPoser
  checkpoint (`test_pose_prior`, `test_fit_mono2d`).
- One NumPy 2 deprecation: `np.cross` on 2-D vectors, in
  `tests/test_play_timeline_rules.py:70` (the test, not the package). Every
  `np.cross` in `nfl_gsplat/` uses 3-D vectors.
- Pickles: NumPy 2.4.6 / pandas 3.1.1 reads a NumPy 1.26 pickle of arrays,
  scalars, a DataFrame and a random generator, and an `.npz`. NumPy 1.26 also
  reads a NumPy 2 pickle of a plain array.
- Nothing imports `mmcv` any more, and `paddleocr` is only a lazy import in
  `nfl_gsplat/tracking/jersey_ocr.py`. Those were the reasons the comment on
  `pyproject.toml`'s `numpy<2` pin gives.

## What it means

- Nothing found so far needs NumPy 1. One environment looks possible, which
  would remove the two-interpreter setup and the pickle rule between them.
- Not tested, because the inputs aren't on this PC:
  - every stage that needs the SMPL-X model, the VPoser checkpoint or
    SMPLest-X (`05c` runs it from a `third_party/SMPLest-X` checkout with
    its own weights);
  - the GPU stages;
  - YOLO and OCR on real frames;
  - loading play 1's real pickles (`identity_resolved.pkl` and the pose
    caches).
- Next: once play 1's inputs and the models are here, run play 1 end to end
  in this environment. If its measures match v122, adopt it
  ([decision 0016](../Decisions/0016-one-numpy-2-environment.md)) and lift the
  `numpy<2` pin.

## Related

- **Concepts:** [Pose](../Concepts/pose.md), [Render and viewer](../Concepts/render-and-viewer.md)
- **Decisions:** [0016: One NumPy 2 environment for the whole pipeline](../Decisions/0016-one-numpy-2-environment.md)
