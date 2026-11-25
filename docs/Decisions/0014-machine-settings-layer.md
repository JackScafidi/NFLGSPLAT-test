---
type: decision
status: accepted
date: 2026-11-25
---

# 0014: One settings layer for this machine's paths and interpreters

## Context

Sixteen code files named the previous developer's machine
(`C:/Users/sumedh/...`, `C:/venvs/...`). `scripts/pipeline_play.sh` could not
run anywhere else: it set `PYTHONPATH`, the two interpreters, the working
folder and the diagnostics folder to that machine's paths. About 37 more
argparse defaults were relative `data/...` paths, which only work when the
working folder is the repo root. Foundations plan, Phase 1, "configuration and
hardcoded paths".

## Decision

`nfl_gsplat/settings.py` resolves five settings: `data_root`, `body_models`,
`diag_dir`, `python_nflgsplat` and `python_smplx`. Each comes from an
environment variable (`NFLG_DATA_ROOT`, `NFLG_BODY_MODELS`, `NFLG_DIAG_DIR`,
`NFLG_PY_NFLGSPLAT`, `NFLG_PY_SMPLX`), then a gitignored `local.yaml` at the
repo root (template: `local.example.yaml`), then a default. A script's own
command-line flag still beats all three.

- Repo root: from the code's own location, never the working folder.
- Defaults: `data/`, `<data_root>/body_models`, `outputs/diag/`, all inside the
  repo. Relative values are taken from the repo root.
- The two interpreters have no default. The pipeline stops and names the
  missing one, rather than running a stage in the wrong environment.
- An unknown key in `local.yaml` is an error, so a typo can't silently fall
  back to a default.
- `python -m nfl_gsplat.settings --shell` prints `export` lines;
  `pipeline_play.sh` reads its settings that way.
- Secrets are not settings. The Roboflow key stays in `ROBOFLOW_API_KEY` and
  the Kaggle token where the Kaggle client looks (`~/.kaggle`). Neither goes
  in `local.yaml`.

## Consequences

- The pipeline and every changed script run from any clone on any machine,
  given a `local.yaml` naming the two interpreters.
- 27 scripts' `data/...` defaults now follow `data_root`. Ten scripts that
  never imported the package at the top (the download scripts, `00b`, `05v`,
  `07m`, `08x`, `08y`, `09j`, `fetch_nflverse_rosters`) keep relative defaults,
  so they still expect to run from the repo root. Adding an import to them
  would be a new requirement on environments that may not have the package.
- Diagnostics now default inside the repo (`outputs/diag/`, gitignored), not
  in a folder beside it.
- `DIAG`, the one environment variable `07l` read, is gone; it's
  `NFLG_DIAG_DIR` now.
- Out of scope here, and still in Phase 1: per-play choices that are
  environment variables today (`RED`, `WHITE`, `OFFENCE`, `KICKING`,
  `SEED_FROM`, `ENDZONE_WEIGHT`) move to each play's `meta.yaml`, and one
  play-folder layout is picked. `paths.py`'s season tree and
  `configs/pipeline.yaml`'s `paths:` block are unchanged.

Made while the owner was away (2026-11-25); accepted by the owner the same day.

## Related

- **Concepts:** none directly. This is machine setup, not a goal object, stage
  or measure.
- **Journal:** [2026-11-25: Settings layer](../Journal/2026-11-25-settings-layer.md)
- **Plan:** [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz), Phase 1
