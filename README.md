# NFLGSPLAT

Turn two synced broadcast clips of an NFL play (sideline + endzone) into a
clean 3D recreation of the play, plus data that locates every player's body,
head, hands and feet, the ball and the referees on every frame.

**Status:** play 1 of BAL at KC (2024, week 1) renders as an 11-on-11 3D
recreation from snap to whistle. It is the only play worked through end to
end, and the pipeline still carries paths from the previous developer's
machine. See [docs/STATE.md](docs/STATE.md) and the
[Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).

## How it works

1. **Cameras:** both cameras are solved on every frame from the painted field.
2. **Tracking and identity:** players are detected and tracked in each view,
   paired across the two views, and named from kit colour, jersey number and
   the roster.
3. **Placement and pose:** each player is placed on the field and fitted with a
   SMPL-X body from 2D keypoints in both views.
4. **Ball and events:** the ball is placed from the bodies and the play's events.
5. **Render and viewer:** a 1080p render and a browser viewer show the play
   from any angle.

The stage-by-stage description is in
[docs/reference/pipeline.md](docs/reference/pipeline.md). The pipeline runs as
`scripts/pipeline_play.sh`, across two Python environments.

## Set up (Windows, CPU tests)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[test]" "pyarrow<21"
pip install torch --index-url https://download.pytorch.org/whl/cu128
```

Use the `cpu` wheel index instead if there is no NVIDIA GPU. ffmpeg must be on
PATH (`winget install -e --id Gyan.FFmpeg`).

```powershell
pytest -m "not gpu and not slow and not real_video" -n 4
ruff check nfl_gsplat tests scripts
```

Running the full pipeline also needs the SMPL-X body models, the footage and
the fine-tuned weights, none of which are in the repo. `SETUP.md` is out of
date, but the code's error messages still point at its sections.

## Layout

```
nfl_gsplat/    the Python package: calibration, tracking, identity, pose, ball, render, ...
scripts/       numbered pipeline stages and tools; pipeline_play.sh runs a play
tests/         CPU unit tests
viewer/        the browser viewer (play_room.html)
configs/       OmegaConf settings
docs/          project notes, an Obsidian vault: start at docs/Home.md
data/          footage, models and per-play outputs (gitignored)
```

## Notes and rules

- Project notes live in [docs/](docs/Home.md). Claude's working rules are in
  [CLAUDE.md](CLAUDE.md).
- Never commit NFL footage, frames, diagnostic images or secrets.
- SMPL-X body models are licensed for non-commercial research. The footage
  comes from NFL+ Premium.
