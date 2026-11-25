---
type: reference
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Working method (from the previous developer)

> Moved word for word from HANDOFF.md, dated 2026-09. The review loop still applies. Some hard rules name the old machine (RTX 4080, `C:\Users\sumedh\diag\`, the GPU embargo, a co-author line); the current rules are in [CLAUDE.md](../../CLAUDE.md).

# NFLGSPLAT — Project Handoff / Agent Context

**Last updated:** 2026-09-04 (branch `pipeline/avatar-twin`; `main` at `93e4cf5`).
Purpose: give any agent full working context WITHOUT the chat history. Read
this, then the memory index the harness loads, then `docs/agent-context/`.

## What this project is

NFL **All-22** broadcast footage (synced sideline + endzone clips per play,
from pro.nfl.com Film Room) → camera calibration from paint and players →
detection, ground-plane linking, SMPL-X pose in both views, jersey identity →
an **avatar twin** render: real bodies (roster height/weight) at the real
positions with colours read off the footage, drawn as Gaussians from any
viewpoint. Everything runs on the local machine.

## The loop (standing process from 2026-09-16)

hypotheses -> tests for them -> code -> run -> a new footage version -> REVIEW THE FOOTAGE -> affirm or
deny -> loop. The rendered clip is the output; the rulers are instruments, not the verdict. Reviewing
the footage means frame SEQUENCES, not one still: `05q_overlay_footage.py --player N --start F --count 8
--step 2` (the drawn body over the real player, both cameras) for every id a ruler flags, plus tiled
consecutive rendered frames (ffmpeg select+tile) of the phases that matter. A ruler that says "fixed"
while the strips show flailing is a ruler to be replaced (v44: joint jitter p90 0.058 and the user
still sees flailing -- the jitter ruler cannot see a smooth, wrong sweep).

## Hard rules (do not violate)

- **Never commit real NFL video/frames.** `data/` and `kp_eval/` are
  gitignored. Diagnostics go to `C:\Users\sumedh\diag\` or the scratchpad.
- **Local only, never PACE** (user, 2026-09-02): the RTX 4080 runs everything,
  so results can be looked at here. **GPU embargo until 2026-09-03 12:00**
  (user's other project); CPU work is fine meanwhile.
- **The machine gets switched off at will.** Long work must be resumable:
  `scripts/pipeline_play.sh` leaves `.done_<stage>` markers per play-dir;
  re-run the same command to resume. Keep stages under ~10 min.
- **Fail loud** (`SetupError`/`CalibrationError` + pointer). No silent fallback.
- **Corrections must beat what they correct, measured**, and a calibration
  correction needs a SECOND ruler before it is applied (five cases where a
  sensible prior made things worse are in memory).
- Commit and push freely, small and often, `git commit -F <file>`; messages
  say what was tried and rejected. End with
  `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` and the
  `Claude-Session:` line the harness gives.
- Substantial work gets an independent review before a `--no-ff` merge.
- Secrets: Roboflow key at `C:/Users/sumedh/.roboflow_key` (never echo, never
  quote a Roboflow error URL); NFL bearer is borrowed from the logged-in
  browser and never written down; Kaggle needs `~/.kaggle/access_token`.
