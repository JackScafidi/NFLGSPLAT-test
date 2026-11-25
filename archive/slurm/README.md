# Archived: the SLURM / PACE path

Not used, not tested, not linted. Kept for reference only.

The project runs locally on one PC; Georgia Tech's PACE cluster and SLURM are
not used ([decision 0001](../../docs/decisions/0001-local-only-no-pace.md)).
These files were moved here on 2026-11-25
([decision 0017](../../docs/decisions/0017-archive-the-slurm-path.md)), keeping
their original paths under this folder:

| File | Was |
| --- | --- |
| `scripts/run_season.py` | builds and submits the season's SLURM job plan |
| `scripts/slurm/*.sbatch`, `scripts/render_play.sbatch`, `scripts/train_landmarks.sbatch` | the PACE job files |
| `nfl_gsplat/season/dag.py` | the job-plan builder `run_season.py` used |
| `tests/test_season_dag.py` | its tests |
| `configs/season.yaml` | the season and SLURM settings (account, partition, QOS, time limits) |

The rest of `nfl_gsplat/season/` (play discovery, play scaffolding, the
cross-play UID and body-shape steps) is not SLURM and stays in the package.
A season-wide run on this PC will need its own design, as part of Layer 2.

The archived code imports `nfl_gsplat.season.dag`, which is no longer in the
package, so it won't run as it stands.
