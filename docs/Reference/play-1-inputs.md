---
type: reference
date: 2026-11-25
---

# Play 1's inputs: re-download checklist

Play 1 can't run on this PC until these are here. The owner chose to download
them again (2026-11-25) rather than copy them from the previous machine.
Paths are relative to the repo root, which is also the default `data_root`
(see `local.example.yaml`).

Downloads that need your login or a licence are marked **you**. Never commit
any of these files: `data/` and `third_party/` are gitignored.

## 1. The two clips (you, NFL+ Premium)

- [ ] `data/all22/bal_at_kc_2024_wk1/001_Sideline_KC_2-20_BLT_24.mp4`
- [ ] `data/all22/bal_at_kc_2024_wk1/002_Endzone_KC_2-20_BLT_24.mp4`

BAL at KC, 2024 week 1. The play is KC 2nd and 20 at the BLT 24. Clips pair
by play description, not by number.

The download scripts, `scripts/06_download_all22.py` and
`scripts/06c_download_game_auto.py`, drive a Chrome window you've logged into.
Start Chrome with its own profile outside the repo, as their docstrings say:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:USERPROFILE\chrome-nfl-profile"
```

Log in to pro.nfl.com in that window and open the game's film room. Then run
the script. The NFL+ licence is for personal viewing.

## 2. SMPL-X body model (you, licence)

- [ ] Register and accept the licence at https://smpl-x.is.tue.mpg.de/ and
  download the SMPL-X model zip (the `.npz` release). Non-commercial research
  use only.
- [ ] Install it: `python scripts/00b_install_body_models.py`. It scans
  `~/Downloads`, or takes the zip paths. It writes
  `data/body_models/smplx/SMPLX_NEUTRAL.npz` (and the other genders) and
  checks each file loads.

## 3. VPoser checkpoint (you, licence)

- [ ] From the same MPI site family (https://smpl-x.is.tue.mpg.de/), download
  VPoser v2.0 (`V02_05`).
- [ ] Unpack to `data/body_models/vposer/V02_05/`, with the `snapshots/`
  folder (epoch checkpoints) and the `.yaml` beside it. `tests/test_pose_prior.py`
  runs once it's there.

## 4. SMPLest-X (code and weights)

- [ ] The repo: `scripts/01_download_models.sh` clones
  `https://github.com/wqyin/SMPLest-X` to `third_party/SMPLest-X`.
- [ ] Its pretrained model: `smplest_x_h.pth.tar` and `config_base.py`, into
  `third_party/SMPLest-X/pretrained_models/smplest_x_h/`. The SMPLest-X README
  links the release. Stage `pose_s` / `pose_e` (05c) runs it.

## 5. Detector weights (automatic, mostly)

- `yolov8m.pt` (08, 08b), `yolov8x.pt` (tracking) and `yolov8x-pose.pt`
  (05m): ultralytics downloads these by name on first use, into the
  working folder (the repo root).
- easyocr downloads its models on first use.
- `data/body_models/ball_yolov8.pt`: optional. The ball is placed from the
  bodies today, so play 1 doesn't need it.
- The fine-tuned pose detector behind `keypoints_2d_ft2.parquet` (`pose_ft2`):
  it was trained on play 1 on the previous machine and isn't in any download.
  `scripts/09h_finetune_pose.py` retrains it from play 1's own pseudo-labels
  (about 40 minutes there). Whether it becomes a stage is still open (runner
  spec, question 1).

## 6. Rosters (automatic)

- [ ] `python scripts/fetch_nflverse_rosters.py --season 2024` writes
  `data/rosters/2024/rosters.parquet` and `roster_weekly.parquet` from
  nflverse. Identity (08c) needs them.

## 7. Settings and environment

- [ ] Build the environment ([decision 0016](../Decisions/0016-one-numpy-2-environment.md):
  one NumPy 2 environment; the trial at `C:\Users\jacks\venvs\np2trial` is a
  start).
- [ ] Copy `local.example.yaml` to `local.yaml` and set `python_nflgsplat` and
  `python_smplx` to that environment's `python.exe` (both the same while
  trying one environment).

## Then

```powershell
bash scripts/pipeline_play.sh data/all22/bal_at_kc_2024_wk1/play_001 001_Sideline_KC_2-20_BLT_24.mp4 002_Endzone_KC_2-20_BLT_24.mp4 24 --from-paint
```

`--from-paint` is needed on a fresh play-dir. Without it the export stage
looks for a reconstruction in the diagnostics folder. The play's other
choices default to play 1's (`RED=KC`, `WHITE=BAL`). Compare the result
with v122 in [STATE.md](../STATE.md).

## Related

- **Concepts:** [Play data](../Concepts/play-data.md), [Pose](../Concepts/pose.md)
- **Play:** [BAL at KC 2024 wk1, play 001](../Plays/bal-at-kc-2024-wk1-play-001.md)
