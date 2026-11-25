---
type: journal
date: 2026-11-25
---

# Settings layer

## What was done

- Added `nfl_gsplat/settings.py`, `local.example.yaml` and
  `tests/test_settings.py` (17 tests). `local.yaml` is gitignored. Design:
  [decision 0014](../Decisions/0014-machine-settings-layer.md).
- Replaced every path that named the previous developer's machine:
  - `scripts/pipeline_play.sh`: the repo root comes from the script's own
    location, and the interpreters and diagnostics folder from the settings.
  - `07l`, `08`, `08b`, `09e`, `diag_joints2d`: real paths in code.
  - Nine usage docstrings now say `<smplx312 python>` or `<nflgsplat python>`.
  - `smplx_joints`'s missing-smplx message.
  - The Chrome profile in `06` and `06c`'s instructions is now
    `$env:USERPROFILE\chrome-nfl-profile`, outside the repo.
- Pointed 27 scripts' relative `data/...` argparse defaults, and four package
  defaults (`smplx_joints`, `pose_prior`, `detect_ball`, `lhm_wrapper`), at
  the settings.
- Declared `pyyaml` in `pyproject.toml`. It was arriving only through
  omegaconf.

## What was measured

- CPU suite on Windows: 1391 passed, 20 skipped. That's 1373 before, plus
  the 17 new tests, plus one `test_no_shadowed_definitions` case, which runs
  once per module. Ruff passes.
- `--help` runs on 26 of the 27 changed scripts in the test venv. `05q` fails
  on `import smplx`, which isn't installed there; it imports it at the top
  regardless of this change.
- `pipeline_play.sh`, run with no settings, stops with: "python_nflgsplat is
  not set or does not exist ('')". With both interpreters set, it reaches the
  first stage (`export`) and fails there for lack of footage, as expected.
- No search hit for `sumedh` or `C:/venvs` remains in `nfl_gsplat/`,
  `scripts/` or `tests/`.

## What it means

- A clone on this PC can now point the pipeline at its own environments with
  one `local.yaml`. Running play 1 still needs the two environments built,
  and the footage and body models copied here.
- Next in Phase 1: build and define the two environments, then the Python
  runner.

## Related

- **Concepts:** none directly (machine setup).
- **Decisions:** [0014: One settings layer for this machine's paths and interpreters](../Decisions/0014-machine-settings-layer.md)
