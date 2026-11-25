---
type: state
date: 2026-11-24
as-of-work: 2026-09-26 (play 1, v122)
---

# Current state

Play 1 renders as a full 11-on-11 3D recreation from snap to whistle (v122,
2026-09-26). It is the only play worked through end to end. The output is a
video plus a joints file for the viewer, not yet the play data the goal asks
for. Nothing has run on this PC yet: the footage, weights and play folders are
on the previous developer's machine.

## Against the goal

The goal: two broadcast clips in; a clean 3D recreation and every object's
location on every frame out.

| Object | Located today? | Where the work is |
| --- | --- | --- |
| [Player body (root)](concepts/player-body.md) | Yes. Two-camera triangulation where both cameras see the player; one camera's box bottom otherwise. | [Placement](findings/placement.md), [tracking and pairing](findings/tracking-and-pairing.md) |
| [Player head](concepts/head.md) | Yes, as a SMPL-X joint; drives the viewer's first-person view | [Render and viewer](findings/render-and-viewer.md) |
| [Player hands](concepts/hands.md) | Wrists only; hand poses are zero | [Pose](findings/pose.md) |
| [Player feet](concepts/feet.md) | Ankles only, plus a foot-lock rule | [Pose](findings/pose.md), [placement](findings/placement.md) |
| [Ball](concepts/ball.md) | Placed from the bodies, with release and catch frames typed in by hand | [Ball and play events](findings/ball-and-play-events.md) |
| [Referees](concepts/referees.md) | Not tracked as separate bodies; one generic avatar | [Decision 0008](decisions/0008-officials-not-by-shirt-stripes.md) |
| [Player identity](concepts/identity.md) | Team from kit colour, jersey and roster name; ID folds made by hand on the film | [Identity and teams](findings/identity-and-teams.md) |

| Layer | State |
| --- | --- |
| 1, extraction ([play data](concepts/play-data.md)) | Works for play 1 through `scripts/pipeline_play.sh` (about 30 stages, two Python environments, paths to the old machine). No single play-data output. |
| 4, viewing ([render and viewer](concepts/render-and-viewer.md)) | 1080p render (`scripts/05k_render_hifi.py`) and the browser viewer (`viewer/play_room.html`, hardcoded to play 1). |
| 2 and 3 | Not started, by decision ([0002](decisions/0002-layers-1-and-4-first.md)). |

## Play 1 at v122 (2026-09-26)

Measured on the live tables (from the [last entry](findings/pipeline-and-versions.md)):

- **[Census](concepts/census.md)** (bodies per team against 11): 0.00 from snap to whistle, every
  frame 11 on 11. Clip frames at 11 on 11: 390 of 401.
- **Steps** 20 / 0, **hops** 0, **surges** 4.3 %.

Known defects, in the order a viewer would notice them:

1. After the whistle (frames 602 to 615) the pile's depths are off, and track
   69 draws a twelfth Raven at 610 to 615.
2. The right guard flickers out at 342 to 344, before the snap.
3. Two frames with 12 KC players, at 215 to 216.
4. Poses in piles.

## What was delivered, and where it is

- Three private claude.ai artifacts owned by the previous developer: a
  showcase, the Film Room viewer and a write-up (links in the last
  [pipeline-and-versions](findings/pipeline-and-versions.md) entry). They are
  likely not visible from this account.
- Videos in `C:/Users/sumedh/diag/` on the previous machine. None are on this PC.

## Next

The [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz):
foundations, then the play data contract, measurement, every object, breadth.

## Open items as listed on 2026-09-10 (word for word)

Kept from HANDOFF.md for its measurements. Several items are done or have
moved on since; the v122 list above is newer.


0. Twin tracks: DONE 2026-09-10 (scripts/08o, tracking.twins) -- see the
   entry below. Play 1 folded the left tackle (18 & 19) and the
   quarterback (16 & 22); 148 ids -> 146. Do NOT lower the 20-frame
   minimum to catch more: at 6 frames the rule folds ids 21 & 28 (0.02 m
   at the feet over 8 frames) and 14 & 32 (0.05 m over 6), and the footage
   shows 21 & 28 to be two Baltimore players one behind the other -- with
   few ankle frames the filled tracks agree by construction. The margin
   that makes the rule safe is many frames, not a tighter distance.
0b. Left/right label flips: the detector swaps a limb group's labels for
   one to four frames (play 1's motion man at 267, arms and legs at once).
   pose.keypoint_filter.fix_lr_flips catches those frames but swaps 3 % of
   all (player, group, frame) decisions and 13-24 % for the players who run
   at the camera, because the shoulders are only 16 px apart at the median
   -- the test runs at the noise level. MEASURED 2026-09-10 (05p --fix-lr,
   ids 9 and 12): the runner's arm speed p90 in the body frame fell 8.91 ->
   7.66 m/s and his reprojection p90 rose 16.5 -> 21.6 px (the fit stops
   following the flipped frames, so that ruler is biased against it); the
   lineman did not move at all; on the footage strips the arms are no
   better. Still off. Gate it on the pair's separation, or decide the flip
   in 3-D where the body's orientation is known.

1. Two-view coverage: 9-10 of 22 players a frame are paired; the rest
   stand on one camera's box point (0.5 m from a triangulated pelvis at
   the median) with a one-view pose (heading within 21 deg of the two-view
   fit at the p50, 3 % facing the wrong way). Measured 2026-09-08 (v22's
   tracks): of 30 sideline tracks of 30+ frames without a partner, 17 have
   no endzone track within 4 m and sit OUTSIDE the endzone image on 100 %
   of their frames (staff on the near sideline, excluded from the render
   anyway), 5 face another kit at their nearest endzone track, 4 are
   eligible but their partner is taken by a longer overlapping fragment, 2
   overlap no endzone track for 6 frames. The pairing is at its ceiling
   for what both cameras see; the ceiling is the endzone camera's 4-6 deg
   lens (frames 125-634 only, and it never holds the wide receivers) and
   the fragments. The regressed pose is a weak cue (18 % top-1); pair
   truth exists only on the helmet set.
2. Fragments: 73 sideline tracks for ~29 people; every stitching cue
   measured is a dead end (position, colour, betas, kit+number vetoes);
   the visible cost is small (one avatar swap at a track end within 30
   frames and 80 px on play 1) but each fragment is a separate identity.
3. Officials inside the field are not tracked as separate bodies (the
   detector/linker folds them in); boundary staff and the sideline
   official are excluded by position and stripes.
4. Compute hygiene: DONE 2026-09-11 with the user's go-ahead -- the 30
   superseded render_hifi_* directories and render_abs were deleted (play_001
   16 GB -> 765 MB); only render_hifi (v31) is kept, and every delivered
   version's 720p clip stays in C:\Users\sumedh\diag\play_001_vNN_hifi_720.mp4.
   appearance_v1/v2 (26 MB) were left. A render script that moves render_hifi
   aside before rendering should delete the old one once the new clip is sent.
   The 05d render is opt-in (RENDER_ABS=1).
5. Plumbing: 08c's --kicking-play is manual (the pipeline does not pass
   it); a kickoff/punt/field-goal play needs it or its specialists render
   unnamed.
6. Generalise across the ~160 downloaded play pairs (paint-solve dead zone
   35-55 deg handled by --vertical-deg 45; expect new failure classes) --
   NOT before play 1 is signed off (the standing directive).
