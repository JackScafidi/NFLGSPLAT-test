---
type: spec
status: accepted except the stage list; step 1 (runner core) built
date: 2026-11-25
---

# Pipeline runner: design

Draft written unattended on 2026-11-25 from a read of `scripts/pipeline_play.sh`. Step 1 of the order of work, the runner core, is built (`nfl_gsplat/pipeline/runner.py`, 17 tests with fake stages). Nothing else is, and the owner answered three of the four questions at the end on 2026-11-25; the stage list waits for play 1.

## Goal

Foundations plan, Phase 1: one command runs a play end to end, resumes after the PC is switched off, and records exactly what produced each output. It replaces `scripts/pipeline_play.sh`.

Phase 1 gate: a fresh clone runs play 1 on this PC with one command.

## What the shell script does today

About 30 stages, each run when its `.done_<stage>` marker is missing. Stages reach the two Python environments through `PYN` (nflgsplat) and `PYS` (smplx312), now read from the settings ([0014](../../Decisions/0014-machine-settings-layer.md)).

Today, two things are done by hand that the runner must do itself:

- **Pass or fail:** a stage passes when `grep` finds an expected word in its output.
- **Re-runs:** when a stage re-runs, it deletes the markers of the stages that depend on it.

### Stage inventory

In run order. "Clears" lists the markers a stage deletes when it runs. "Verdict" is how it passes today.

| Stage | Env | Scripts | Runs when | Clears | Verdict today |
| --- | --- | --- | --- | --- | --- |
| paint | N | 08 (`--out recon.npz`) | `--from-paint` | export, refine, shift, endzone | grep |
| export | N | 08b; copies the clips into the play-dir | always | | grep |
| refine | N | 08e | always | | grep; "median grid nan" and "did not lower" pass with a log line |
| shift | N | 08d `--no-rows --apply` | always | | grep |
| endzone | N | 08 `--sideline-from`, then 08b | always | pose_s, pose_e, identity, keypoints, tri, fuse, refit, refit_ez, hifi, render; deletes both pose files | grep |
| check | N | 08d `--los-yards` | always | | exit code; "MISMATCH" fails; "DISAGREE" passes only if numerals are within 0.95 to 1.05 and the line of scrimmage matched |
| endzone_paint | N | 08l `--apply` | always | | grep |
| endzone_track | N | 08h | `ENDZONE_TRACK=1` | | "wrote" or a measured refusal passes |
| link | N | 08b `--cameras --pairing track` | always | pose_s, pose_e, identity, keypoints, tri, refit, refit_ez | grep |
| split | N | 08k | always | | grep |
| field | N | 05l | always | | grep |
| identity | N | 08c, 08i, 08c `--from-cache` | always | | grep |
| pose_s | S | 05c sideline | always | | `tail -1` (never fails) |
| pose_e | S | 05c endzone `--match-frames` | always | | `tail -1` (never fails) |
| keypoints | N | 05m | always | | grep |
| offset | N | 05o | always | | grep |
| repair | N, S | 08i `--lag`, 08m (S), 08c `--from-cache` | always | | `tail` (never fails) |
| twins | S, N | 08o (S), 08c `--from-cache` | always | | `grep -v` (never fails) |
| pair | N | 08r; then, if the proposal has no rejection, 08s and 08c | always | | grep |
| switches | N, S | 08u; 08t looped up to 8 times until "0 cuts"; 08v (S) | always | | grep, plus the fixpoint loop |
| roles | N | 08n `--offence` | always | | `tail` (never fails) |
| tri | S | 05n | always | | grep |
| fuse | S | 05e | `FUSE=1` | | grep |
| refit | S | 05f | always | | grep |
| refit_mono | S | 05p | always | | grep |
| fit | S | 05i | `FIT=1` | | grep |
| teams | N | 08f | always | | always passes (`|| true`); 08f's refusal is by design |
| play_end | S | 08x | always | | grep |
| refit_ez | S | 05r | unless `REFIT_EZ=0` | | grep |
| measure | S | 07l | every run, never marked | | a failure only logs |
| hifi | S | 05k, then an ffmpeg 720p encode into the diagnostics folder | always | | grep |
| render | S | 05d | `RENDER_ABS=1` | | grep |

`N` is nflgsplat, `S` is smplx312. The fits (tri, refit_mono, refit_ez) read `keypoints_2d_ft2.parquet` when it exists, else `keypoints_2d.parquet`.

Per-play inputs that are environment variables today: `RED`, `WHITE`, `OFFENCE`, `KICKING`, `SEED_FROM`, `GRID_PX`, `ENDZONE_WEIGHT`, `ONE_VIEW`, `PAIR_ADDITIONS_ONLY`, `CUT_TO_FRAME`, `LIVE_LO`, `END_LIVE`, `GAIT`, plus the four opt-in flags above.

## Proposed design

### 1. Stages declared once, in Python

`nfl_gsplat/pipeline/stages.py` holds one record per stage:

- name;
- environment;
- the commands to run;
- the files it reads and writes (paths relative to the play-dir);
- the per-play settings it uses;
- an optional condition.

The order is the order of the list. Dependencies come from the files: a stage depends on whichever earlier stage writes a file it reads.

### 2. Re-run on change, not on markers

A stage re-runs when any of these differ from its last successful run, as recorded in the play's run manifest:

- the hash of an input file;
- one of its settings;
- the hash of its script and of every `nfl_gsplat` module the script imports, at any depth (`runner.code_files`), so a change to one module re-runs only the stages that use it.

That replaces the `.done_<stage>` markers, the hand-written "clears" lists and `--fresh`'s file list. `--force <stage>` re-runs that stage. Later stages re-run if what they read changed.

Many stages rewrite a file they read (`cameras.npz`, `tracks.parquet`). So the version of an input a stage is compared on is what the last earlier stage that writes it left there, as recorded in the manifest, not the file on disk now. Two rules follow:

- A stage that re-runs overwrites its outputs, so every later stage that also writes one of those files re-runs.
- A file that no longer matches what its last writer recorded (deleted or edited by hand) is redone from its first writer.

A re-run that writes the same bytes stops the cascade.

Hashing the two clips on every run is slow, so inputs are keyed on size and modification time, with a full hash taken once and cached.

### 3. Pass on exit code and checked outputs

A stage passes when every command exits 0, every declared output exists, and its check (if any) passes. The grep verdicts move into the scripts:

- A script exits non-zero when it fails. Many already print "Error" and carry on; each is fixed as the runner takes it over.
- A measured refusal is not a failure. 08e "did not lower", 08h's refusal, 08f's refusal and 08r's "no proposal survived" each exit 0 and write a small JSON verdict the runner logs.
- `check`'s two-of-three rule moves into 08d itself.
- 08t's fixpoint loop moves into 08t (`--until-fixpoint`).

This is the bulk of the work: about 30 scripts' exit codes. It can go stage by stage, with `pipeline_play.sh` still working beside the runner until the last stage moves.

### 4. Per-play choices from the play's own file

`<play-dir>/meta.yaml` holds the per-play inputs (kits, offence, kicking, line of scrimmage, seed play, the opt-in flags). The runner reads it; nothing per-play comes from environment variables. Later, the same file (or `corrections.yaml`) carries the Phase 5 corrections.

### 5. Logs and the run manifest

- Each stage's full output goes to `<play-dir>/logs/<stage>.log`. The terminal shows one summary line per stage.
- `<play-dir>/run_manifest.json` records, per stage: git commit, settings, input and output hashes, start and end time, exit status and verdict.

### 6. Command line

```
python -m nfl_gsplat.pipeline run <play-dir> [--from-paint] [--force STAGE] [--only STAGE] [--dry-run]
python -m nfl_gsplat.pipeline status <play-dir>
```

`--dry-run` prints which stages would run and why. `status` reads the manifest.

### 7. Tests

The runner is tested with fake stages (small Python commands that write files), covering:

- the order;
- re-run on a changed input, setting or code;
- resume after a killed stage;
- failing on a missing output;
- the manifest's contents.

The real stages are checked by running play 1 once its inputs are on this PC.

## Order of work

1. Runner core and its tests, with fake stages.
2. Stage declarations for all 30 stages, running the existing scripts unchanged, with today's grep verdicts kept as temporary checks.
3. Play 1 end to end on this PC. Compare with v122 (census, steps, hops, surges, joint jitter).
4. Move each grep verdict into its script as an exit code or JSON verdict, one stage at a time, re-running play 1 from that stage.
5. Retire `pipeline_play.sh`.

Step 3 needs play 1's clips, the SMPL-X and VPoser files, the model weights and the SMPLest-X checkout on this PC.

## Questions, answered by the owner on 2026-11-25

1. **Is the stage list the whole pipeline?** Not settled. The hand-run steps behind v122 (09h's fine-tuned keypoints, the 08z / 08za folds and row drops) stay out of the first stage list and are decided after play 1 runs on this PC.
2. **One environment or two?** Aim for one NumPy 2 environment ([0016](../../Decisions/0016-one-numpy-2-environment.md)), and fall back to two only if play 1 fails in it. Until then the `Env` column stays, so the stages can run in either setup.
3. **Hash-based re-runs or markers?** Content hashes, as built in step 1.
4. **Should `measure` (07l) stay an every-run, never-failing step?** Yes. It reports before the render and never stops the run; its numbers go into the run manifest.
