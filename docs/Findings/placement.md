---
type: findings
topic: placement
period: 2026-09-07 to 2026-09-26
entries: 9
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Placement on the field

Where each body stands on every frame: ground points, depth along a camera's line of sight, who is drawn, and how gaps are bridged.

9 entries from 2026-09-07 to 2026-09-26, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Placement](../Concepts/placement.md), [Player body](../Concepts/player-body.md), [Feet](../Concepts/feet.md), [Census](../Concepts/census.md)

**Decisions:** [0007: Keep the box bottom as the one-view ground point](../Decisions/0007-box-bottom-is-the-one-view-ground-point.md)

## Who is drawn: four exclusion rules, and v10's order (2026-09-07)

`play_timeline` now leaves out, in this order, each a set of ids: edge-clipped
one-view ids (`edge_rule`), endzone-only ids (`endzone_only_rule`, one avatar
per sideline track), sideline dwellers (`offfield_rule.sideline_dwellers`:
share of frames at |y| >= 23.5 m of at least 0.8 -- play 1: 26 ids, staff
in dark jackets and the sideline official, no roster-named player) and
striped officials (`offfield_rule.striped_ids`: torso gradient ratio 2.5
with a dark share 0.25; play 1: none beyond the dwellers). Measured
against the roster-named ids: none touched.

Appearance pairing (`tracking/pair_by_appearance`, `08i`): per-camera
tracks pair on the jersey number read in both cameras (3.5 m), else on
kit agreement (2.0 m), never across a kit or number conflict, never on
position alone. Dry run on play 1 (kit only): 44 pairs, 0 cross-kit, 10
paired per frame (the per-frame link: 84 two-camera ids, 23 cross-kit).
v10 is the first play through the new order: `08b --cameras --pairing
track --pair-gap 0` (camera tracks keep their ids) -> `08c` (OCR per
camera track) -> `08i` -> `08c --from-cache` -> pose -> keypoints -> tri
-> refit -> hifi. The pipeline patch for these stages
(`scratchpad/patch_pipeline_stages.py`) adds `endzone_track` and `link`
stages after the check and moves identity ahead of the pose stages
(pairing changes ids; pose caches are keyed by id); apply it when no
`pipeline_play.sh` instance runs.

## v16: the duplicate rule was eating six players a frame (2026-09-08)

Every render since v8 drew 16 bodies a frame and it passed as normal. An
audit of the path from boxes to states on v15's caches: the sideline has
21 boxes a frame, 20 ids after the exclusion rules, 32 ids with a ground
point; the timeline drew 16 and `dedupe_frames` had dropped 7511 states
(11.6 a frame); 47 sideline ids over 4056 id-frames were present and
undrawn. The rule treated any one-view state within its camera's
depth/across radii (4.0 m along the depth axis, 1.5 m across) of a kept
state as the other camera's copy -- built for play 2's endzone ghosts
strung along x -- and for a sideline-only id the depth axis is y, so the
linemen a metre apart along the line of scrimmage were "copies" of each
other. Now (timeline.dedupe_frames): a state whose id the SIDELINE
detected in that frame is never a duplicate (its boxes in one frame are
different people); an id the endzone alone sees that frame dedupes within
the endzone's depth/across radii of a kept state; an interpolated frame
within 0.9 m. Measured: 23 states a frame (p10 20, p90 25), 3396 dropped,
7 sideline id-frames undrawn, nearest-neighbour distance p5 0.47 m.
Render v16 = v15 + this rule (06:19, `diag/play_001_v16_hifi_720.mp4`,
strip `diag/p1_v15_v16_strip.jpg`): median 23 bodies a frame; the whole
offensive line is back at the snap (v15 drew four red bodies at 1.5 s, v16
the pack of eleven) and the 7 s frame shows a full formation. No visible
duplicates in the stills. v16 is the deliverable.

The states the new dedupe keeps that the sideline does not see in that
frame, per frame on v16: 1.1 interpolated (gap fills), 0.9 endzone-seen
PAIRED ids, 0.2 endzone-only ids the frustum test lets through. The paired
ones are one id: 68 = an endzone track of 510 frames (125-634) paired by
08i to a sideline fragment of 18 frames (606-642), drawn 474 frames from
the endzone alone -- a second copy of a player the sideline tracks under
other ids, metres away along x, past the dedupe radii. Id 40 the same
shape (endzone 125-634, sideline 398-526). `endzone_only_rule.
beyond_sideline_span` (in the timeline before the exclusion rules): an
id's frames beyond its sideline span by more than MAX_GAP_FRAMES (30) are
dropped where the sideline could see the spot, kept where it could not
(outside its image). Play 1: 1588 ground frames dropped, 22 bodies a
frame, dedupe drops 3396 -> 1841. v17 = v16 + this + the tilt prior (07:17,
`diag/play_001_v17_hifi_720.mp4`): 22 bodies a frame, tilt-clamped states
1158 -> 73, stills against v16 (`diag/p1_v16_v17_strip.jpg`) the same
formation without the endzone tails; no regression.

## v20: the timeline anchored the model's origin, 0.35 m from the pelvis (2026-09-08)

Found while chasing the last 0.35 m of the boundary jump (it survived the
placement weight and the sideline-only ground points): the SMPL-X rest
pelvis sits at (0.003, -0.351, 0.012) in model axes, and neither
pose.forward_kinematics nor the smplx model rotates that root offset --
the pelvis is always rest pelvis + transl, in WORLD axes. `placed_vertices`
put the model's origin at a state's xy, so a body with no refit record
(one-view sideline records, default poses) stood 0.35 m from its box
point along -y, toward the sideline camera; a record-placed body (xy =
transl) stood at its fitted pelvis. The two disagreed by 0.35 m, so a body
popped by that at every record boundary, and every earlier comparison of
"transl" against a ground point carried the constant: the "pelvis 0.46 m
off" in the 05p validation, the box point's "-0.32 m y bias" in the
ankle measurement (against the true pelvis: bias x -0.01, y +0.04, p50
0.52 m). Now `placed_vertices` anchors the pelvis joint at xy,
`place_from_refit` places records at transl + rest pelvis (per betas,
`rest_pelvis_xy`), and 05p interpolates the fused PELVIS across and beyond
a span. Play 1 re-run: the pelvis jump at the 71 boundaries 0.35 -> 0.05 m
(p90 0.14), the merged cache's jitter p99 408 -> 311 mm; the orientation
still turned 17 deg (p90 32) and body_pose 0.9 rad at a long-gap edge --
one view's keypoints against the two-view pose along the depth -- so a
one-view block now cross-fades into the fused block it borders
(`fit_mono2d.blend_params`, per-joint slerp, w = 1 at the edge to 0 a
max-gap away): boundaries pelvis 0.01 m, orientation 2 deg (p90 4),
body_pose 0.10 rad; the merged cache's jitter p99 260 mm and hands/feet
p90 103 against the fused-only cache's 255 / 102 -- the one-view records
no longer add roughness. v20 = v19 + pelvis anchoring + cross-fade (10:13,
`diag/play_001_v20_hifi_720.mp4`; stills against v19 in
`diag/p1_v19_v20_strip.jpg`: the same 22 bodies, the recordless ones
shifted onto their feet points; no regression). v19 (09:28) = v18 + the
short-gap rule, stills identical to v18.

## ground_positions keyed by the TRACKER's id, not the player's (2026-09-12)

`ankle_ground` keys `(cam, frame, global_player_id)`. `ground_positions` looked those ankles up by
`r.track_id` and emitted its own output under `r.track_id` too, while **every caller asks by player id**
-- 05p tests `pid not in ground.get(f, {})` with `pid` from the keypoints, the depth snap matches endzone
candidates the same way, the census counts players, and the docstring says `{pid: xy}`. It never showed
because this pipeline had never assigned a global id different from a track id.

08s is the first thing that does, and all four relabelled ids reported **zero endzone ground frames**
with their rows and keypoints perfectly intact (id 11: 423 endzone rows, 405 keypoint boxes, 0 ground
frames, against control id 12 at 381/377/381). Their points were landing under the OLD track ids and the
ankle lookup missed every time, falling back silently to the box bottom.

What it did and did not break, measured rather than assumed. The **fits are unaffected**: 05p uses the
sideline ground dict and the relabel only touched endzone rows, so the ids still coincide there, which is
why 05u showed v36 as a clean win. What was blind is the depth snap's endzone candidates for those ids
and **08r's turf ruler** -- the missing turf statistic is why the "beat the incumbent on both rulers"
check silently skipped and proposed `11 <- 97` (0.19 m over 30 frames) against an incumbent measuring
0.14 m over 150. After the fix that candidate disappears from the assignment entirely (23 pairs, 18
unchanged, against 20 and 14 before).

Fixed to key by `global_player_id`, and a table without that column is now refused with a `SetupError`
naming it rather than falling back to `track_id` -- silence is how this hid. Confirmed on the play: the
four ids now report 75, 423, 464 and 491 endzone ground frames, the stale keys 19/21/22/102 are empty,
and the controls are untouched. Two existing tests failed on the change and **both were fixture
artifacts, not a contradicting contract** -- `test_ankle_ground` and `test_timeline` built rows carrying
only `track_id`, so they hit an AttributeError; neither asserted the old key, and both assertions stand
once the fixture carries the column the real table always has. Suite 1112 passed.

## 2026-09-19 (evening): players vanishing in the pocket -- a man who vanishes stands still

**The user's question.** "players are vanishing in some frames, especially on the line of scrimmage when they are locked up in
the middle of the play - how can we address this?" Answered on v81's tables against the film.

**Why they vanish.** The sideline detector loses an engaged lineman to the man on him: his box merges into his opponent's
or his neighbour's. The centre 204's last sideline box is 499; from 500 the Raven 84's box covers 0.9-1.0 of it with
Thuney's at IoU 0.15-0.18, and the film shows the centre still locked with that Raven at 531 (`diag/pocket/centre_sl_zoom.png`).
The endzone camera keeps seeing him, but under other ids the pairing never joined to 204 (jersey 52 Humphrey is 174 until
~505, 166 from ~507 to ~546, 164 from 547 on -- `diag/pocket/ez_early_zoom.png`, `ez_switch_zoom.png`, `ez_164_zoom.png`),
and those endzone-only beyond-span rows are dropped or placed with the endzone camera's depth wander. On v81, 22 tracks end
inside the play window (395-607) and 19 holes open. New ruler `timeline.vanishings`: body-frames after an id's last drawn
frame, or inside a hole, with no same-team body within 0.6 m of his spot -- v81: 736 end frames, 160 hole frames (9 holes).
The twin rule's drops are not vanishings (the other id draws the man).

**The rule (timeline.stand_still; the loader runs it after every dedupe rule on the play window, knobs passed at call time).**
- Bridge: a hole of at most 50 frames (STAND_BRIDGE_MAX_FRAMES) whose ends lie within 1.5 m takes the straight line, copying
  the nearer end's state, on frames with no same-team body within 0.6 m. 33 body-frames on 55, 84, 198; census 0.92 -> 0.84
  (the bridged men were missing, not doubled); steps 5, hops 0; vanish holes 9 -> 5, hole frames 160 -> 127.
- Hold: a track that ends inside the window while the man moved <= 1.0 m over his last 10 frames is held at his last spot
  for at most 25 frames (STAND_HOLD_MAX); the BOXES stop it: a same-team box on his last box at IoU >= 0.45
  (STAND_SUCCESSOR_IOU; >= 0.35 for an id born within 3 frames of the end, STAND_NEWBORN_IOU/REACH) is the man under a new
  id; other boxes covering less than 0.5 of the last box (STAND_OCCLUDED_COVER) is open turf, he left; a same-team body
  within 0.6 m is a twin. The box numbers that set the gates (probe_end_boxes.py, every play-window end): re-identified men
  4/194 0.67, 12/76 0.86, 15/168 0.67, 19/37 0.85, 30/180 0.94, 38/12 0.90, 60/55 0.80, 84/168 0.75, 157/37 0.93, 40/198
  0.48, 6/78 0.49, 198/206 0.41 (born +2); two men: 204/139 0.18, 204/211 0.08 (born +1), 166/80 0.29-0.42 (Mahomes behind
  the centre in the endzone image), 9/77 0.29.
- Film check of every hold (`diag/pocket/holds_v83_film.png`): the centre 500-525 locked with the Raven -- right; BAL 1
  421-434 under Noah Gray's box, dropped on open turf at 435 -- right (he walks off); BAL 6 489-493 then 78 on his box --
  right; 74 (the receiver, tackled) 603-607 -- right; 166 (the centre's endzone id) 544-568 -- right to ~560, a Raven on
  the endzone spot by 563 (hence the 25 cap, not 40); 198 -> 206 newborn at IoU 0.41 -- the newborn gate.

**Final numbers on v81's tables (steps_by_id_v81rule.log):** 33 bridged + 75 held body-frames on 8 ids (1:14, 6:5, 74:5,
166:25, 204:25, 198:1; 55/84/198 bridged); steps 5 (157 at 553-556, 212 at 602/605, v81's own), hops 0, census 0.92 ->
1.005 (the holds land on frames where the team already reads 11 or more -- a ghost elsewhere; the film says the held men
are there), vanish holes 9 -> 5, hole frames 160 -> 102, end frames 736 -> 661. Suite 1248 passed, 3 skipped.

**Measured and rejected on the way (each on the play window):**
- the hold with the same 0.6 m clearance: 501 held body-frames on 11 ids, census 0.92 -> 2.62;
- the hold stopped by any teammate within 1.5 m: never holds the centre (Thuney stands 1.3 m from him);
- the hold stopped by a teammate BORN within 8 frames within 1.5 m: still loses the centre (211 born 1.3 m away) and holds
  BAL 40 beside his own new id 198 (an OLD id at IoU 0.48 on his last box);
- a 40-frame hold cap: 166's endzone hold ran 20 frames past a Raven standing on its spot -- the last box is a stale image
  position and both cameras pan;
- the bridge without a hole cap: 166's 135-frame hole (406-542) bridged 116 body-frames of a ghost beside the centre,
  census 0.92 -> 1.19;
- the A/B whose three hold arms printed identical numbers: module constants bound as default arguments (TWIN_M again);
  the loader passes every knob at call time now -- memory probe-monkeypatch-default-args;
- **the centre's endzone ids folded into 204** (174 455-508, 166 507-546, 164 547-634, each stretch read on the film):
  the loader's beyond-span rule keeps him only 521-543 (500-520 dropped as more than 0.8 m from the join, which itself
  is 0.14 m), his placement slides 1.7 m over 524-528 (steps 0.32-0.39 x5), live steps 5 -> 10, census 0.92 -> 0.953,
  vanish end frames 736 -> 694. Two rulers worse for one better: tables restored to v81 (cmp against the .v81 copies).
  The sixteenth correction that lost. The endzone camera's play-time depth is what stops the endzone carrying a lost
  lineman -- open item (3), not a fold. A first, wider fold (166 on 472-562) was also wrong on the film: 166 is on the
  man beside Humphrey before ~505 and on the Raven in front of him after ~546.

**What the centre looks like now:** drawn 395-499 from his sideline track, held 500-524 at his last spot (the film has him
there), gone 525-541, back 542-568 as his endzone id 166 (542 detected, 543-568 held), gone after. Better than v81
(gone from 500), not whole: the remaining gap is the sideline detector's merge of two engaged men into one box and the
endzone pairing's three ids for one man.

**Tools:** `scratchpad/probe_end_boxes.py` (box coverage after every end), `hold_sheet.py` (film sheet per hold),
`zoom_strip.py` (a zoomed strip around a fixed image box, ZR/ZZ env for radius/zoom), `steps_by_id.py`.

**v83 rendered and film-checked (20:40 machine clock): `diag/play_001_v83_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` /
`_endzone_blend`.** 07l on 395-607: steps 5, hops 0, census 1.00 (KC 11.31 / BAL 11.06; v81 0.92). Film vs render at the
centre's spot (`diag/pocket/centre_v83_check.png`, 499-548): 499-524 the render matches the film frame for frame (the
Raven plus two red men); at 532 the film still has the centre locked with that Raven and the render has one red man
(the hold ended at 524); by 547 the pair has travelled a box-width. Note for the chain: 08y needs `--qb 80 --down 607
--snap 395` with `--from-film` (the first v83 chain ran it bare, wrote down None, and was killed before the render).

**The locked mode (v84).** The Raven the centre blocks (BAL 84) is tracked to 587, so the block carries him:
timeline.stand_still's hold gets a locked mode -- a man whose track ends while ENGAGED (an other-team box on his at
IoU >= 0.4 on 8 of his last 15 boxed frames), with one other-team box covering his last box at IoU >= 0.5 on the first
held frame and that opponent drawn and slow, follows the opponent's displacement for up to 90 frames until the opponent
moves more than 1.0 m over 10 frames (broke free), leaves, or a same-team body stands within 0.6 m of the followed spot.
The engagement history separates the cases: the centre had a Raven (13, then 84 -- the same man under two ids) on his
box at 0.41-0.96 over 483-499; BAL 1 had at most 0.23 before his end, Noah Gray's 0.77 came AFTER it (a walk-over).
On v81's tables: the centre 395-540 (locked 500-540, moving 1.1 m back with 84 as the film shows), then 166 542-568;
BAL 1 still 14; steps 5, hops 0, census 1.005 -> 1.014, vanishing end frames 661 -> 646. Rejected on the way: the lock
without the engagement test (BAL 1 followed Gray 83 frames, census 1.36); bounded by the stale box's cover (26 frames);
the cover on a box moved with the opponent's plus a 0.5 m block speed (24, and BAL 1 cut to 5); a box-successor test
inside the lock (Thuney's box drifting onto the centre's Raven at 0.41-0.46 ended it at 524 with his body 1.3 m off);
the moved-box cover inside the lock (the Raven's own box shrinking ended it at 526). Known seam: the followed spot at
540 and 166's endzone placement at 542 lie 1.29 m apart -- the endzone camera's depth wander, open item (3).
**v84 rendered and film-checked (21:35 machine clock): `diag/play_001_v84_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` /
`_endzone_blend`. CURRENT BEST.** 07l on 395-607: steps 5, hops 0, census 1.01 (KC 11.38 / BAL 11.06). Film vs render at the
centre's spot (`diag/pocket/centre_v84_check.png`, 516-568): 516-540 the render matches the film frame for frame -- the
Raven plus two red men, the pair moving together as the block is driven back; from 542 his endzone id 166 draws him,
1.3 m off the followed spot (the endzone depth wander), to 568; the rest of the pocket reads the same as v83. Commits
44e94e9 (the rule + the ruler), 181dff4 (HANDOFF), aa671dd (the locked mode). Open, in value order: (1) the sideline
detector merging two engaged men into one box (the centre after 499, Thuney's box on the pair from 524; a fragment 186
rides the pair 524-567 and is dropped as a rider); (2) the endzone camera's play-time depth wander (166's 1.3 m seam,
and what stopped the centre's endzone rows from carrying him); (3) the endzone pairing's three ids for one man
(174/166/164); (4) the pile's synthesised lying poses.

## 2026-09-19 (night): the endzone camera's depth is a BIAS, not a wander -- taken out of endzone-only placements (v85)

**Measured** (scratchpad/probe_ez_common_mode.py, a wrapper on play_timeline.ground_positions recording the raw per-camera
ground points; the play window 395-607): the median sideline-minus-endzone offset over each frame's two-view bodies is
+0.45 m along the field on EVERY frame (p10 +0.31, p50 +0.45, p90 +0.63; 80 of 213 frames above 0.5 m), its spread
(p75 of the residuals) 0.2-0.5 m before the catch and 0.5-1.1 m after; the across offset drifts from 0 to -0.9 m over
the last 60 frames as the camera pans. So what the 09-18 entry called a 1.4 m "wander" is mostly a constant bias of the
endzone camera's ground points along the field plus a pan-time drift across; a two-view body never shows it (the
sideline's point overrides), a body the endzone alone places carries it whole. That is the 1.29 m seam between the
centre's followed spot at 540 and his endzone id 166 at 542, and the reason the film-true fold of his endzone ids
slid (the 16th rejected correction): the endzone rows were placed 0.45 m short.

**The correction** (pair_rule.common_mode_shift, EZ_COMMON_MODE on, EZ_COMMON_MODE_MIN_PAIRS 4): every endzone-only
point in the merged ground moves by its frame's median sideline-minus-endzone vector over the ids both cameras place
(the play-wide median where a frame has fewer than 4 pairs), in the loader after the sideline's points override the
merged ground and before the hole hold. The same common mode MISPAIR_FRAME_M measured (and lost with, as a per-frame
veto: flips = steps), used as a correction: nothing flips.

**A/B on play 1** (probe_cm_ab.py, v81's tables, the stand-still rule on): the seam 1.29 -> 0.91 m; steps 5, hops 0;
census 1.014 -> 1.009; vanish hole frames 97 -> 87, end frames 646 -> 667; 6705 endzone-only body-frames shifted over
the whole clip, 503 frames with their own offset (the play-wide one is +0.23, +0.03 m over all 647 frames). The
sideline blend is the ruler for a shift along the field: `diag/pocket/centre_v85_check.png` against
`centre_v84b_check.png` (542-568) -- the endzone-drawn body moves toward the film's pair at every frame, the residual
being 166's own drift onto the Raven. Adopted; commit 4166c74; suite 1251 passed, 3 skipped. v85 chain launched
(render + both blends) -- numbers in the next entry.

**v85 rendered (23:20 machine clock): `diag/play_001_v85_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` / `_endzone_blend`.
CURRENT BEST.** 07l on 395-607: steps 5, hops 0, census 1.01 (KC 11.37 / BAL 11.05); 6705 endzone-only body-frames shifted.
Also checked on the film tonight: id 37's 43-frame hole (531-573) is NOT a vanishing -- the man is drawn as his twin id
211 throughout (`diag/pocket/sl_37_hole.png`), and 37's endzone point at 530 sits 3.5 m across from his sideline point
at 574 (a mispaired endzone row), which is why the vanishings ruler's straight line misses 211; the ruler's worst list
is contaminated by re-identifications (1 -> ?, 6 -> 78, 40 -> 198, 198 -> 206) whose successor bodies stand more than
0.6 m off the old spot. A successor-aware ruler is the next small step; the real remaining vanishing on the film is the
centre after 568 (his endzone id 164 carries him 547-634 but is beyond its own sideline span, join 330 frames back).

**Could the centre's endzone id 164 carry him past 568? Measured, parked (23:45).** probe_164_handover.py: 164's raw endzone
points with the frame's common mode sit 1.0-1.3 m from the lock's last spot (540) and ~1.0 m from 166's drawn points over
545-557, then walk off along the field (+x, Humphrey jogging after the catch: 2.0 m at 565, 3.1 m at 593). 164 is not in
the timeline at all on the play (its own sideline span ended at 216, so every endzone row is beyond-span and dropped). A
runtime handover (an endzone-only same-team id appearing within ~1.3 m of a lost man's last spot continues him, the seam
blended over a few frames) is the mechanism that would draw him to 607; it is the fold's seam problem in another coat and
needs the beyond-span join test to accept a join against the LOCKED spot, not the sideline's last box. Not tonight.

## 2026-09-26 01:10 -- hidden feet: the short-box rule measured and rejected; v120 = v119 + stands that rise

**Why Madubuike lands deep:** his sideline boxes at 572-590 are only his head and shoulders over #65 -- 33-46 px tall
where #65 and #74 beside him are 112-118 px -- so the "foot" row is ~80 px too high and the ground point lands deep
along the sideline ray. **The short-box rule** ($S/patch_short_box.py: a box shorter than 0.7 of the median height of
the boxes around it, not lying down, takes its foot from its top plus that median) moved 293 sideline boxes play-wide.
v119s: census 0.08 -> 0.16 -- #98 (id 81) drops out at 542-567 (his boxes merged with Thuney's are "short" and his
point slid 1.8 m, then deduped), the KC RG drops pre-snap at 220-227, and Madubuike still stands at y 2.2 (film:
between #65 at 1.1 and #74 at 1.6). With SPARE_MISSED too (v119sm): 0.19. Rejected; the rule reads every occluded or
merged box as hidden feet, and the man it was built for is barely moved. The next attempt should take hidden feet
from the man's OWN unoccluded box height near that frame, not the neighbours'.

**The stands (render.sky STANDS_MODE "bowl", caf7638):** the v119 hero's top band was a red/grey pixel mosaic (the
stands drawn flat on the ground). Now four planar banks rise as in the viewer (26 m over 42 m behind a 1.3 m wall
with a red ribbon board), seated spectators per 0.55 m seat and 0.9 m row, aisles, dimmer up the bank; "flat"
reproduces v119 byte for byte. v119's chain was stopped at the hero's 30th frame and restarted as **v120** = v119
tables + --shade + the bowl ($S/launch_v120.sh: hero 1080p, skycam 1080p, the sideline broadcast pose 720p).

## 2026-09-26 01:35 -- v121: Madubuike's depth read off the film; 11 v 11 on every frame from snap to whistle

**Read, not inferred.** Neither camera places Madubuike (id 4) along the sideline's line of sight at 552-596: feet
hidden behind #65 in the sideline view, no endzone box. His helmet read in the endzone film ($S/grid_crop.py gridded
crops; clip frame = f - 15) at 552/564/584/596 = (1130,537) (1092,528) (1052,560) (1040,615) px, triangulated with his
sideline box's top-centre: y 1.93 / 1.92 / 1.88 / 1.77 m, ray gaps 0.13 / 0.32 / 0.21 / 0.10 m. **<play>/film_reads.json**
carries the reads, the pixels and why; **depth_snap.apply_depth_reads** (065a23a) slides the man along his OWN sideline
ray to the read y after the snap (x stays the sideline's), ramped over 6 frames. No file, no change.

**Measured** (patch arm v119r, then the repo path v121 -- dumps identical): census live 0.08 -> **0.00** (KC 11.0,
BAL 11.0; 213 of 213 live frames exactly 11 v 11; the clip's 17 off frames are 215-234 pre-snap, 342-344 and 610-615
after the down), steps 20/0, hops 0, jitter unchanged; surges 4.4 % (v117b 4.8 %). **Film** ($S/mark_ids.py: each
drawn body as a turf-to-1.8 m stick on full-resolution crops of both films, diag/mark_v119r.png vs mark_v119.png):
Madubuike between #65 and #74 at 560/576/588 in the endzone film (v119: on #74 or on Ojabo's spot). **Cost:**
Ojabo's endzone point is 0.75 m from the corrected Madubuike, inside the 0.9 m teammate dedupe, so it is dropped and a
hold bridges him ~0.7 m wide of #90 (v119 drew him right at 560 and not at all at 570-586). Next if wanted: a
film-read man is not a duplicate of anyone (exempt his neighbours from the dedupe).

**v121 renders** ($S/launch_v121.sh): hero follow 1080p, skycam 1080p, the sideline broadcast pose 720p -- all with
--shade and the bowl stands. Viewer Version 35 (v121 joints). The v120 hero/skycam were stopped mid-render (superseded);
placeholder FILES at play_001/render_hifi_v120sc, render_view_v120 and render_view_v119 blocked the stopped chains'
next steps -- delete them.

## 2026-09-26 01:55 -- v122 = v121 + depth_snap.SPARE_MISSED on (f2d58ee): Ojabo on #90, the KC RG drawn pre-snap

SPARE_MISSED failed at 00:40 only because the man it freed (Madubuike) fell back to a sideline-only point 0.6 m too
deep; with his depth read off the film (v121) that failure is gone. Measured on top of v121 (with_flag arm v121s):
live census 0.00 either way, steps 20/0, hops 0, jitter p99 0.1628 -> 0.1666; clip frames exactly 11 v 11 384 -> 390
of 401 (the KC RG 76 at 218-234: no more pop-in a third of a second into every video); on both films
(diag/mark_v121s.png vs mark_v121.png) Ojabo stands on #90 at 552 and 572 (v121: a hold 0.5-0.9 m wide). Worse in one
place: Madubuike at 512 (before the read window) sits ~0.3 m further from the Raven on the turf. Surges 4.3 %.
Remaining off-count clip frames: 215-216 (KC 12), 342-344 (KC 10, the RG flicker), 610-615 (BAL 12 after the down:
sideline track 69 at 606-642 is a separate box left of Madubuike's track 45 -- unread).

Renders: $S/launch_v122.sh (hero, skycam, the sideline broadcast pose; --shade, bowl stands) queued after the v121
hero (kept as the fallback). Viewer Version 36 = v122 joints. Placeholder FILES blocking stopped chain steps:
play_001/render_hifi_v120sc, render_view_v120, render_view_v119, render_hifi_v121sc, render_view_v121 -- delete.
