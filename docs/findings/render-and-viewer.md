---
type: findings
topic: render-and-viewer
period: 2026-09-20 to 2026-09-24
entries: 5
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Render and viewer

The 3D render and the browser viewer: first-person view, gear and the stadium backdrop.

5 entries from 2026-09-20 to 2026-09-24, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Render and viewer](../concepts/render-and-viewer.md), [Head](../concepts/head.md), [Feet](../concepts/feet.md), [Ball](../concepts/ball.md)

## 2026-09-20 (morning): the viewer, and the detector holes measured -- one new track, no missing Raven

**The viewer.** The user asked to see the play from any angle. 05k --export-joints / --no-render writes every drawn
body's 22 world joints per frame (the same poses, gait, throw, catch, carry and fall the render draws) plus the team,
the ball and the joint tree as JSON; viewer/play_room.html (three.js from cdnjs, no other dependency) draws capsule
bodies on the SMPL-X tree in team colours on a rulebook field with the line of scrimmage, camera presets (sideline,
endzone, overhead, pocket, follow ball), a free orbit, a scrubber with the snap/release/catch/down marks, and click-to-id.
Published as an artifact with the joints file beside it (data stays out of the repo): the "Play 001 Film Room".
Commit 1d7347f.

**The detector holes, measured (scratchpad/probe_redetect.py, then scripts/03e_redetect_missing.py).** YOLOv8x at
2560 px, conf 0.35, on the sideline play frames, a box counted new when no tracked box overlaps it (IoU < 0.15, centre
outside every box), its foot on the field through the camera (|x| < 57, |y| < 25.5 m -- without this gate the
benches and the crowd at the top edge gave 14-28 "new" men a frame), player height, linked over gaps of 3, runs of
15+: ONE new track on 395-607 -- the centre, 533-556, after his box merged into his neighbour's at 528
(`diag/pocket/redetect_new_tracks.png`). BAL 1 after 434 has no box in either camera. The Raven who read as
"missing" is nobody: every endzone-only Raven the timeline drops stands 0.2-0.9 m from a DRAWN Raven
(probe_ez_only_bal.py: 146 by 171/55, 112 by 40/212, 21 by 28, 187 by 180 -- the endzone camera's second ids), and
85, named a Raven by the OCR, is the referee (`diag/pocket/ez_full_470_605.jpg`). The tracks table boxes eleven
Ravens on the sideline frames I checked; the count's deficit is the twin rules and the loader's exclusions, id by
id, not a man no camera saw. So the "second detection pass" is additive and small: 03e adds new tracks from 900,
05m --ids/--append and 05c --ids (per-track resume) pose them alone, and nothing existing is renumbered.

**Applied.** 900 (the centre 533-556) -> keypoints -> sideline poses -> folded into 204; 166's Humphrey rows folded
into 204 too (507-539 and 540-562; the film had 166 on him from ~507). The loader's hole rule then filled the long
hole's ends by extrapolation and dropped its middle (514-524), and the bridge refused that 0.68 m gap because Thuney
stands 0.47-0.55 m off its line: STAND_CLEAR_M 0.6 -> 0.45 (twins stand 0.1-0.4 m). Tried and reverted first: a
"neighbour" exemption for the bridge (a teammate within 1.0 m at the hole's start) -- it re-admitted the twins the
twin rule had cut (bridged 38 -> 106, census 1.02 -> 1.20), because the twin IS a teammate within 1.0 m at the hole's
start. Also new in stand_still: a hole the bridge cannot take gets the hold/lock from its start (hold_or_lock, one
closure for holes and ends) with the tail slid onto the far end over STAND_SEAM_FRAMES (6; a 4-frame walk made a
0.29 m step, ten frames make 0.12), and a lock that ends early inside a hole falls back to the static hold.
endzone_only_rule.short_team_vouch (off) was written for the missing Raven and found nothing to vouch.

**Measured on play 1 (395-607):** the centre drawn 395-556 as one id (locked 500-528, walked onto his re-detected
boxes, two-view from 540), steps 5, hops 0, census 1.155 -> 1.023, vanishing holes 4/96 -> 3/61 (the ruler shares
STAND_CLEAR_M, so its end-frame count is not comparable across the change). v88 chain launched.

**v88 rendered and film-checked (2026-09-21, 00:40 machine clock): `diag/play_001_v88_hifi_720.mp4` + `_sideline_blend` /
`_sideline_sbs` / `_endzone_blend`. CURRENT BEST.** 07l on 395-607: steps 5, hops 0, census 1.02 (KC 11.24 / BAL 10.60).
Film vs render at the centre's spot (`diag/pocket/centre_v88_check.png`, 508-556): the Raven plus two red men at every
checked frame, the render matching frame for frame -- the centre is one body from the snap to 556 (locked 500-528, walked
onto his re-detected boxes, two-view from 540). Tables and pose caches snapshotted as `*.v88`. Commits 5779113 (03e, the
hole-lock, the seam, the clearance), 5f9ffed (HANDOFF), 1d7347f (the viewer). Open: BAL 1 after 434 (no box in either
camera; the count's deficit otherwise is the twin rules id by id), the pile's synthesised lying poses, the endzone
pairing's several ids per man (a fold per man on the film, as done for the centre).

## 2026-09-22 -- the user's next three asks: natural motion, gear/textures, first-person view

**First-person view (done, viewer):** click a body, "First person": the camera sits at his head joint (+0.10 m up, +0.08 m
forward), looks where his shoulders face (forward = up x (right shoulder - left shoulder), smoothed 0.25/frame), a
slight downward gaze, fov 80, near 0.12, his own body hidden; clicking another body switches eyes; drag/wheel leaves.
05k --export-joints now writes `names` ({pid: "15 Patrick Mahomes"} for named ids) and the pick line shows them.

**Motion naturalness -- two rulers over the exported joints (v95, 4396 body-frames per hinge):**
- hinge FLEXION is fine: elbows/knees over-bent (< 35 deg) or locked (> 178) on 2 body-frames in 17,584 (the hard
  hinge bounds work);
- knee-angle JERK > 25 deg/frame^2 on 55 body-frames (knees 24 + 31, elbows 7): snaps at speed changes (9 at 252-258
  pre-snap, 204 at 578, 30 at 494, 1 at 472-498) -- the gait blend and leg flips;
- the bend PLANE (|n . right|, 1 = swings forward-back, 0 = bends sideways): arms bent sideways (< 0.4) on 4% of left-arm
  and 11% of RIGHT-arm bent frames -- an asymmetry, the camera-far arm fitted into the frontal plane when occluded;
  legs 5-6%. Worst ids: 11 R arm (38), 5 L leg (33), 9 L leg (27), 80 R arm (25, the throw -- real), 74 R arm (21).
Plan, in order: (1) confidence-gated joint angles -- a joint whose 2D keypoint confidence is low is interpolated (slerp)
between its nearest confident frames instead of fitted; score on the two rulers here plus reprojection; (2) the endzone
camera's keypoints in the fit where it sees the man (the depth ambiguity behind sideways elbows); (3) a temporal 3D
lifter (MotionBERT-class) per track, SMPL-X fitted to the lifted joints; (4) a pose prior (VPoser or football joint
statistics) in the fit; (5) contacts (feet on turf, no interpenetration in piles).

**Gear and textures (plan):** the hifi render is flat colour + numbers + helmet spheres. Steps: a per-team UV texture on
the SMPL-X body (jersey with the number front/back, pants, socks, cleats, gloves), a helmet mesh with a facemask
(replaces the sphere), shoulder-pad silhouette via a small displacement on the shoulder vertices. The viewer draws
capsules; real meshes there are a later, heavier step (SMPL-X vertices per frame = 10k x 3 x 200 frames).
Trap (fixed in 05k): `--export-joints --no-render` into an out-dir whose PNGs exist wrote an EMPTY joints file -- the
export is filled inside the frame loop and resume skipped every frame. The export now forces --no-resume.

## 2026-09-22 (machine clock ~13:00-15:00) -- first-person gaze, the receiver's id, the motion rulers' first two mechanisms, gear

**The user's report on the first-person view:** the quarterback in the pocket "faces the sideline". Measured on the v95
joints: the fitted shoulder line's yaw at 400/440/480/500/520/540 = -68/26/83/97/45/176 deg (0 = +x, downfield for KC =
180) -- the single-camera fit's yaw is off by up to a right angle where the body faces the camera, and the neck-to-head
vector agrees with the shoulders (no independent gaze). Fixed in the VIEWER (artifact Version 11, d5ec371): the gaze
comes from the play -- moving > 1.5 m/s looks along the run; within 3 m of the line at the snap looks across it; the
carrier standing looks his team's way; everyone else looks at the ball. Fit-side (endzone keypoints in the refit, a
yaw prior from the run direction) not started.

**The user's report on the motion receiver "spawning a new player":** id 9 (KC, in motion) meets the Ravens defender id 6
at 480-493. The 09c track table + the sideline film strip (diag/wr_9_77_sideline.png): at 485-488 the detector merged
the two men into one box under id 9; at 489-493 id 9's box (cx 1089, bottom 262, h 94) sits on the WHITE defender while
6's own track ends 488 and his track 78 resumes 494 at the same box; at 494 track 77 is born on the red receiver. Fixed
on the tables (backups .pre_fold.64/65, .pre_drop.11): 77 folded into 9 (steps 2, hops 0, census 0.18 -> 0.16); then
on a copy of the play dir 9's 489-493 sideline rows folded into 6 (08z --cam sideline --track-id 9 --frames 489 493)
and 485-488 dropped (08za) -- rulers unchanged (2 / 0 / 0.16), film-true, ported. presence 9 = 395-628, 6 = 395-637.
Live tables = v96 (not yet snapshotted). Viewer Version 12 carries the v96 joints.

**Which models are ours (the user asked):** everything in play 1's loop is pretrained (YOLOv8x at 2560 px, BoT-SORT,
yolov8x-pose, SMPLest-X init, easyocr, SMPL-X, nerfstudio splatfacto) plus our geometry and rules; the models WE trained
(`data/weights/`: jersey CNN 25 %, ResNet18 jersey reader 42 %, ReID ResNet-18 below the ImageNet trunk at the linking
question) all lost their measurement and none is wired in; the landmark detector has scripts, no training run.

**Motion, mechanism 1 -- the confidence-gated joints (built, measured, NO effect):** timeline.gate_low_confidence SLERPs a
rotation across keyframes whose driving keypoint (elbow for the shoulder, wrist for the elbow, knee for the hip, ankle
for the knee) scores under CONF_GATE_MIN 0.3 in runs up to CONF_GATE_MAX_RUN 30 frames; play_timeline.keypoint_confidence
builds the per-row confidence from keypoints_2d.parquet and every knob is passed at call time. The first arm was a
no-op: the loader filtered the keypoints on the refit's cam, which is "fused", not "sideline" -- 0 records, identical
arms (the log's count line is the tell; probe-monkeypatch memory, 3rd case). Wired (both cameras, best per keypoint):
15,261 (frame, id) records, 1,956 keyframe-joints slerped -- and 09d unmoved: jerk 57 -> 57, sideways R arm 11.0 -> 11.1 %,
L arm 5.7 -> 5.9 %, legs identical; 07l joint jitter p50 0.0231 -> 0.0229, skating 0.725 -> 0.727. The sideways bends
are not where the keypoints are unseen (or the SLERP lands in the same plane). Stays in the code, default to be set 0
unless a CONF_GATE_MIN 0.5 arm moves something.

**Motion, mechanism 2 -- the knee snaps are the GAIT's:** the same play exported with --gait off: leg jerk events 50 -> 2
(arms 7 either way). A synthetic run found one mechanism (constant speed: knee jerk max 16; speed flickering +-0.006
about RUN_M: 49, 10 of 58 samples over 25) and hysteresis + a minimum run (gait.on_flags, OFF_SHARE 0.75 / MIN_RUN 12)
fixed it there (49 -> 22) -- but on the PLAY it LOST: leg jerk 50 -> 51 and the legs bent sideways on 11.8 % of frames
against 7.9 % (the 3.6 m/s off-threshold re-admits the jogging band, where men shuffle and the gait's legs swing in the
motion plane across the body). Defaults reverted to the plain threshold (1.0 / 1); the code stays for the synthetic case.
The play's own mechanism, read off joints_v96a: 41 of the 50 leg events sit within 8 frames of a 4.8 m/s crossing --
the gait's switch-on / switch-off ramp (6 frames, linear, from the fit's legs to the gait's phase-zero legs). Arms in
flight: BLEND 16 linear, BLEND 16 smoothstep (gait.BLEND_SHAPE "smooth", C1 at both ends), BLEND 6 smoothstep.

**Gear (built, unit-tested, one close render checked from behind):** uniform.regions now carves a collar (jersey top,
front and sides), sleeve cuffs (the 7 cm of jersey before the elbow) and a pant stripe (the outer seam: |x| > 0.13 m,
|z| < 0.045 m) out of the jersey/pants, and Kit carries their colours plus the cleats (KC white collar/cuffs, red stripe
and cleats; BAL purple trim, black cleats); helmet.facemask_mask + wear_facemask push the lower front of the face 3 cm
proud of the shell in the team's cage colour (KC white, BAL black), applied by 05k under --helmets; --pads (existing,
shoulders out 3.5 cm and up 2 cm) goes into the v96 launch. Frontal check render pending.

**Mechanism 2 resolved -- the gait's blend (2026-09-22 ~16:30):** the first BLEND arm measured two identical arms because
gait_sequence bound BLEND as a default argument (probe-monkeypatch memory, 4th case; every gait knob is read at call time
now, with a monkeypatch test that the output changes). Wired, on play 1 v96 (09d, live play, gate off): BLEND 6 -> 57
jerk events (legs 50); BLEND 16 -> 11 (legs 4); BLEND 30 -> 11 (legs 4); BLEND 16 smoothstep -> 13. Sideways legs fell
with it (L 7.9 -> 7.0 %, R 5.0 -> 3.5 %); the 7 arm events are the fit's (the throw, 80 at 532; 84 at 430; 15 at 484).
BLEND 16 is the default (30 buys nothing and is 0.5 s of half-gait per edge). The synthetic flicker case is cured by 16
alone too (49 -> 18), so OFF_SHARE / MIN_RUN stay at the plain threshold. 07l's skating ratio with BLEND 16 pending.

**The gate's verdict and the blend's cost (~17:00):** CONF_GATE_MIN 0.5 (2,161 keyframe-joints, BLEND 16): arm jerk 7 -> 5,
sideways R arm 11.0 -> 10.8 %, L 7.0 -> 7.0 % -- noise; the gate is OFF by default (CONF_GATE_MAX_RUN 0), code and
loader wiring kept. 07l with BLEND 16: joint jitter p90 0.126 -> 0.066 and p99 1.06 -> 0.20 (the snaps), but the
skating ruler gives back half of what the gait bought: planted share of moving frames 22.6 % -> 6.7 %, ratio p50
0.725 -> 0.822 (the ramp is half-gait time). Arms in flight to keep both: BLEND 6 + MIN_RUN 12 (no brief crossings),
BLEND 10, and BLEND 6 + a sigma-3 Gaussian over the gait's own rows where it is on (gait.GAIT_SMOOTH_SIGMA, new).
Arms measured (~17:30): BLEND 6 + MIN_RUN 12 (no hysteresis) -> 56 events (legs 49), sideways legs 10.9 / 8.0 % -- filling the
off-gaps puts the gait on shufflers, rejected; BLEND 10 -> 22 (legs 15), sideways 7.1 / 4.0 %. The trade is blend
length against skating; the Gaussian-over-the-gait-rows arm (BLEND 6, sigma 3) is the attempt to have both.
BLEND 6 + GAIT_SMOOTH_SIGMA 3 (09d): 7 events, ALL the fit's arms (legs 50 -> 0), sideways legs 6.7 / 4.1 %; 07l skating
for it pending. 07l so far: BLEND 6 planted 22.6 % / jitter p99 1.06; BLEND 10 14 % / 0.26; BLEND 16 6.7 % / 0.20.
BLEND 6 + sigma 3 on 07l: planted 4 % (ratio 0.85), jitter p99 0.13 -- the Gaussian rounds the stance sweep that plants
the foot; REJECTED. Every ramp knob trades jerk against planting, so the next two attack the gap itself: MIN_ON (drop
on-runs shorter than 12 frames, no gap filling) and PHASE_MATCH (start each on-run at the phase whose hip flexions match
the fit's at the switch-on frame; gait.fit_hip_flexion / phase_match).
Gap arms (09d, BLEND 6, gate off, ~18:30): MIN_ON 12 alone -> 17 events (legs 10), sideways legs 7.3 / 5.3 %; PHASE_MATCH
alone -> 48 (legs 41): the hips matched, the knees not, and the fit's legs at a crossing are not gait-like; both -> 21
(legs 14). So the short crossings (nothing but ramp) were most of the play's leg jerk. In flight: 07l skating for
MIN_ON 12; MIN_ON 18; MIN_ON 12 + BLEND 10.
07l for MIN_ON 12 (BLEND 6): planted 14 %, ratio p50 0.89 (worse than 6's 0.725 -- the dropped short runs were planting
frames), jitter p99 0.23. The frontier so far (leg jerk events / planted %): BLEND 6 50 / 22.6; BLEND 10 15 / 14;
MIN_ON 12 10 / 14; BLEND 16 4 / 6.7; sigma 3 0 / 4. Nothing yet moves both the right way.
MIN_ON 18 (BLEND 6) -> 15 events (legs 8), sideways 7.2 / 4.7 %; BLEND 10 + MIN_ON 12 -> 14 (legs 7), 6.9 / 4.5 %, its 07l
skating in flight -- the candidate default if the planted share holds near 14 %.
07l for BLEND 10 + MIN_ON 12: planted 14 %, ratio p50 0.89, jitter p99 0.21 -- DEFAULT (gait.BLEND 10, MIN_ON 12): leg
jerk events 50 -> 7 for 22.6 -> 14 % planted; nothing measured moves both the right way, and the jerk is what the user
sees as odd angles. v96 chain launched (~19:15): v96 tables (snapshotted *.v96) + the gait defaults + the gear
(--pads on, facemask/collar/cuffs/stripe/cleats) + KC names; gate off.
Suite 1280 passed / 3 skipped with the final defaults; gait committed 162c500 (gear 3b9ca6f, gate 2d5e494, gaze d5ec371).
Next unit while v96 renders: scripts/09e_contact_links.py -- a link finder for track deaths/births through contact
(team kit, OCR votes, kinematics, box-overlap history, the other camera), validated on a v95 copy where the 9 -> 77
switch still exists (data/.../play_v95copy).

**RESUME HERE (power-off ~20:00, 2026-09-22).** Running when the machine went off: the v96 render chain
(`$S/chain_v96.sh`, log `$S/chain_v96.log`; relaunch with `nohup bash "$S/chain_v96.sh" > "$S/chain_v96.log" 2>&1 &`
-- Git Bash has no setsid; 08y/08x/dump/07l re-run, the render skips existing PNGs in render_hifi_v96). Then review:
catch_check strips, both blends, the 09d rulers on the render's own joints, the viewer (Version 13 already has the v96
joints). Then snapshot: MEMORY.md index still says v95 = current best.
The link finder (scripts/09e_contact_links.py, tracking/contact_links.py, tests) is committed. On the live tables it
proposes 4 links; the film says: 19 <- 162 = fragments of the snap pile, NOT a man (do not fold); 167 <- 139/153 = the
KC lineman on the pile, unverified; 1 <- 4 (track 45 from 528) = ONE man but the finder's DIRECTION is backwards --
the white Raven engaged with KC 65 (id 76) is id 4 at 412-442 and from 528 (sideline t45, endzone t45/t136 440-506
at the same spot), while id 1's sideline rows 500-526 (t45 <= 520, t40 522-526, h 70-116, y 3.7-4.9 = a metre across
from 4's y 2.5) are on him too; id 1's own track 40 runs 440-494 upfield (y 5-6.6) and the endzone's t112 (524-536,
y 2.4) sits on 4's spot. Likely fix (measure on a copy first, `data/.../play_copy` has the finder's own 1 <- 4 fold
applied -- rerun the copy from live before trying the reverse): give id 1's sideline rows 500-527 to id 4
(`08z --keep 4 --drop 1 --cam sideline --track-id 45 --frames 500 520`, `... --track-id 40 --frames 522 527`) and
the endzone t112 to 4, then look at where the real Ojabo (1) is after 494 on the film. Finder improvement to make:
when the born id has older rows or an other-camera presence at the spot, fold the dying id's TAIL into the born id
instead (a `direction` field), and never propose pairs whose death box is a merged pile box (h > 1.4x the track's
median height).
The copy trial of the finder's 1 <- 4 (track 45 from 528) measured: census 0.16 -> 0.43, id 4 vanishes 502-607 (106
frames), steps 2 / hops 0 -- REJECTED by the ruler as by the film (28th correction that lost). v96 chain reached the
render (loader rulers on v96: steps 2, hops 0, census 0.16; 1 frame rendered) when the machine went off.

**Resumed (2026-09-22 ~21:45): the chain never died** -- the pause left the machine on; the hifi 720 finished 21:14, the
sideline blend/sbs 21:33, the endzone view is running. v96 film review (catch_check on the sideline blend): whole-field
420/500/580 counts and spots right; the receiver's contact 482-500 PLACED right (one red man, one white, no spawn) but
DRAWN LYING FLAT at 486-496 (neck-pelvis tilt 37 -> 90 -> 40 deg, the film has him upright and running); the catch
556-568 and the throw 528-532 right; the tackle 598-606 at the film's spot. Cause of the flat body: the pose caches
keep records for frames whose boxes were dropped or folded away after the fit -- id 9 has a regressor record at 488
(the merged two-man box I dropped) and a refit at 494 (track 77's first, wide box), the timeline interpolates through
them. Rule under test, alone: timeline.DROP_UNBOXED_POSES (a record whose (frame, id) has no tracks row in either
camera is dropped before interpolation), measured on the joints (tilt at 486-496, 09d) and the loader rulers.
Finder re-run with the two rules: 19 <- 162 REJECT (pile box h 201 vs 126), 1 <- 4 DIRECTION? (4 seen 53 frames in the
endzone before the death), 167 <- 139 / 153 still LINK (167 is itself a pile id at the KC line, 412's box h 206;
unverified, not applied).
DROP_UNBOXED_POSES measured alone: 812 records dropped; loader rulers unchanged (2 / 0 / 0.16); id 9's tilt at 486-496
51-94 -> 32-40 deg; bodies past 70 deg in the window 3 -> 2 (6 at 492, 15 at 576 remain: their rows exist); 09d 14 -> 12.
ADOPTED (default True). v97 = v96 tables + this rule, chain to launch when v96's endzone view finishes.
v96 endzone blend (frames ~489 and ~565): bodies on the film's men in depth, the pocket and the collapsed pocket both
right. v96 review complete: one defect (the receiver flat 486-496), fixed by DROP_UNBOXED_POSES; a second pose class
under test alone: DROP_MERGED_BOX_POSES (a record fitted on a sideline box over 1.3x the id's median height or 1.6x
its width is dropped; the defender 6 at 490-492 leans 84 deg on such a record): 199 records dropped, loader rulers
unchanged (2 / 0 / 0.16); joints export pending. v97 = v96 tables + both rules once measured.
DROP_MERGED_BOX_POSES measured alone (on top of the no-box rule): 09d jerk 12 -> 10, sideways legs 6.8 -> 6.4 / 4.6 -> 4.2 %,
arms 5.8 -> 5.6 / 11.2 -> 11.3 %; the trunk ruler UNCHANGED (6 at 490-492 84 deg, 15 at 574-576): the defender's last
own box (h 116 vs his median) is under the 1.3x ratio, so his record survives -- a different mechanism, open. Kept
(small net gain, rulers unmoved). v97 chain launched ~22:40 (v96 tables + both pose rules).
The defender's lean (6, 84 deg at 490-492) explained: no refit records for him there, only the one-view regressor's at
488 and 494, but the tilt limit is chosen PER PLAYER from his first record's source ("fused" -> 60 deg) so a one-view
record in a pile gets the two-view allowance. timeline.TILT_LIMIT_PER_FRAME (the nearest keyframe's source per frame)
built and unit-tested, default OFF while v97 renders (the chain re-imports the modules per stage); measured alone in
flight (joints export + loader rulers via with_flag).
TILT_LIMIT_PER_FRAME measured alone (with_flag, v96 tables + both pose rules): trunk past 70 deg 4 -> 0 body-frames (6 at
490-492 and 15 at 574-576 both clamped to the one-view limit their records deserve), 09d jerk 10 -> 10, sideways
unchanged, loader rulers unchanged (2 / 0 / 0.16). ADOPT after the v97 chain finishes (the chain re-imports the
modules per stage; flipping now would mix rules inside v97). Then v98 = v97 + this, or fold it into the next render.
A yaw ruler tried and found CONFOUNDED: for bodies over 3 m/s the fitted facing (up x (R shoulder - L shoulder)) is over
45 deg off the run direction on 61 % of 1,236 body-frames and past 90 on 35 % -- but the worst ids are the backpedalling
defenders (6, 0, 30, 5, 3, 2) and the motion man (9, who runs across while facing the ball): real. A facing ruler needs
the film's own evidence (the endzone camera sees the numbers) or the 2D keypoints' left/right; the FPV yaw stays with
the viewer's play-derived gaze for now.

**v97 rendered (2026-09-22 22:58): `diag/play_001_v97_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` / `_endzone_blend`.**
v96 tables + DROP_UNBOXED_POSES + DROP_MERGED_BOX_POSES. Film check at the receiver's contact: upright and engaged at
488 and 494 (v96 lay flat); the defender 6 behind him still flat at 488-492 (the per-player tilt-limit case).
TILT_LIMIT_PER_FRAME flipped ON after the chain; suite running for its commit; v98 chain launched ~23:05 (v96 tables +
all three pose rules).
09d on the WHOLE clip (v98 joints): pre-snap 215-394 has no hinge jerk at all and 276 trunk-past-70 body-frames that are
the linemen's three-point stances (4, 11, 84, 12, 17 at 78-79 deg: real); the tail's 74 at 100 deg 608-614 is the
tackle (real). The trunk ruler is clean only on the live play window, like the census. Viewer Version 15 = v98 joints.
Finder on the ENDZONE camera (395-607): 73 candidate pairs, 15 LINK (top: 80 <- 186 track 22 at 511/512 on one spot,
"jersey 7 agrees" = an OCR misread of 15; 156 <- 139 jersey 62; 7 <- 89; 192/202/210 on one BAL track 141 dying and
reborn three times at the line), 15 DIRECTION?, 43 REJECT. The endzone ids are the pairing's fragments the loader
already reconciles per frame; folding them by this table needs a film pass per pair -- not applied, kept as the
map of where the endzone tracker breaks (the line at 395-400, the pocket at 511-545).
v97 pre-snap (300 / 350 / 390, whole field): the formation, the motion man and the defenders' spots match the film.
v97 tail (604 / 608 / 612): the carrier 74 goes down with Hamilton (28) on him as on the film, but the film's SECOND Raven
on the pile is missing in the render: at the down only 28 is within 4 m of 74. The vanish list's one open entry (171
ends at 600) is that man -- a moving tackler the stand-still hold does not carry. Next: carry a body that ends within
N frames of the down and within reach of the carrier into the tackle (tackle.py TACKLER_M 1.5 acts only on drawn
bodies at the down frame).
tackle.lost_tacklers built + tested (other-team bodies lost within 12 frames before the down and 1.5 m of the carrier:
Roquan 171 at 599); the 05k wiring (add them to hold_to_end's `always`) waits for the v98 chain to finish, then v99.

**v98 rendered (2026-09-23 00:02): `diag/play_001_v98_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` / `_endzone_blend`.**
v96 tables + DROP_UNBOXED_POSES + DROP_MERGED_BOX_POSES + TILT_LIMIT_PER_FRAME. Loader rulers 2 / 0 / 0.16. Film check
of the lean sites pending; the lost-tackler wiring (05k, tackle.lost_tacklers) applied after the chain and measured
on the joints for v99.
v98 film check (488 / 492 / 574 / 576): the defender behind the receiver upright at both frames (84 deg in v97), the
catch-side bodies at 574-576 as on the film. v98 = CURRENT BEST (reviewed on the receiver's contact, both lean sites,
the catch, the throw, the pre-snap formation via v97 and the tackle spot). Open on it: the second tackler (v99).
Lost-tackler wiring measured on the joints: 171 held from 599 to the end, tacklers on the down frame [28, 171]; 09d jerk
10, trunk 0 (unchanged). v99 chain launched ~00:20 (v98 + the second tackler in the pile).

**RESUME HERE (power-off expected ~00:30, 2026-09-23).** The v99 chain is rendering (`$S/chain_v99.sh`, log
`$S/chain_v99.log`); relaunch with `nohup bash "$S/chain_v99.sh" > "$S/chain_v99.log" 2>&1 &` (frames resume). Then review
the tail 604-614 (both Ravens on the pile), record v99, snapshot the viewer. Then START THE IN-FILLER (the user's call):
a self-supervised joint in-filler on play 1 with the hold-out ruler (mask sure joints, measure recovery vs the Gaussian
+ SLERP), design in the 2026-09-23 chat and the pipeline write-up artifact ("All-22 to Avatars", to be kept current).

**In-filler built (2026-09-23 01:40, pose/infill.py, scripts/09f_infill.py, tests/test_infill.py).** Three synthetic
lessons, each measured: predict the correction over SLERP (rows outright lost 2.8 vs 1.1 deg); zero-init head +
validation early stopping (epoch 0 = SLERP); every unsure row reads as its SLERP fill in the input (3.7 vs 1.5 with true
values leaking as context); masks hide a LIMB over a run (single-joint masks taught a same-keyframe shortcut, 1.5 vs
1.45). Synthetic now: never worse on a 2-keyframe hole, better over an 8-keyframe hole on a curved stride. NEXT: the
play run (`PYS scripts/09f_infill.py --play-dir P --lo 395 --hi 607`) after v99, then the timeline hook only if the
hold-out ruler wins on the arms.
In-filler on the PLAY (395-607, 35 players, 1,633 keyframes, 34,293 rows: 13,833 sure, 423 unsure = 1.2 %): held-out
sure rows 527, model 10.2 deg mean / 22.7 p90 vs SLERP 5.9 / 15.1; arms 5.3 vs 4.0, legs 21.2 vs 10.2. LOST -- and the
early-stopping guard let it (best epoch 18): windows of neighbouring keyframes overlap on 8 of 9, so a per-window
validation split was a near copy of training. Validation now by player; one honest rerun, then the verdict.
In-filler VERDICT (player-wise validation): best epoch 0 -- the model is SLERP: 5.85 / 15.1 on 527 held-out rows, arms
3.95 = 3.95, legs 10.15 = 10.15. Unsure rows 423 of 34,293 (1.2 %), 196 runs, p50 1 keyframe, p90 4, max 16; L arm 260,
R arm 131, legs 32. Unseen joints are NOT the odd-arm mechanism. Code kept (hook off). NEXT: the 2D keypoint fine-tune
on two-view-consistent pseudo-labels (the label builder first, with its own hold-out ruler).

**2D fine-tune, step 1 (2026-09-23 ~02:40): pose/pseudo_labels.py + scripts/09g_pose_labels.py + tests.** Labels = the
fused fit's joints reprojected where a camera anchors them (conf >= 0.5 within 12 px); fit_cross (anchored only by
the other camera) is the new signal; det where only the detector is confident; unlabelled otherwise. Dataset under
<play-dir>/pose_ds (gitignored): every 5th sideline frame + its endzone frame = val. Building for play 1 now; the
counts (how many fit_cross labels, where) decide whether there is enough new signal to train on.
Dataset built (play 1, 214-616 stride 2, the cache's own keyframes -- a range from the odd 215 had missed every fit):
395 images (317 train / 78 val), 9,298 instances, 85,204 keypoint slots: fit_self 48.5 %, fit_cross 16.3 % (13,858:
endzone 12,382, sideline 1,476 -- the endzone detector is the weak one at 88 m; the sideline gets ~120 cross labels per
joint), det 13.4 %, unlabelled 21.8 %. 165 MB under <play-dir>/pose_ds (gitignored). scripts/09h_finetune_pose.py
written: baseline score, ultralytics fine-tune (freeze 10, imgsz 1920, batch 2, no mosaic), fine-tuned score by source.
Baseline detector vs the held-out labels (val frames): sideline det/fit_self PCK@10 100 / 98 %, median 0 / 2.5 px;
sideline fit_cross (n 281, detector conf 0.33) PCK@10 51 %, median 9.5 px -- the genuine unsure cases. ENDZONE fit_cross
(n 2,408, detector conf 0.90!) PCK@10 0.6 %, median 20 px: the endzone detector is confident and the fit disagrees by
20 px (~0.5 m at 88 m). Suspect: the endzone camera's depth wander, not the detector -- measuring the residual's
per-frame common mode before any training; a label rule change follows (the fit must never override a confident
detection in its own camera).
Residual fit - detection on confident joints (all frames): ENDZONE norm p50 12.7 px, per-frame COMMON MODE |du| 3.3 /
|dv| 8.0 px (p90 14), within-frame MAD 5-6 px, worst on hips (17 px) and shoulders; SIDELINE common mode 0.1 / 0.3 px,
MAD 1.0 / 1.7, norm 2.5 px. The endzone camera is off per frame (its known depth wander seen from the fit's side); the
fused refit is fitted against it. So the 2D fine-tune's endzone labels are camera error and the order changes: refine
the endzone camera per frame from the bodies (the sideline-anchored fit as 3D landmarks), refit, measure the residual
and 09d, THEN the fine-tune with clean labels.
The endzone common mode is SMOOTH in time (frame-to-frame p50 0.9 px, +3 to +18 px over the play) and grows with image
row: dv 3.9 px at the far end (rows < 400), 9.5, 12.4, 30 px at the near end (rows > 800) -- a per-frame zoom / depth
error of the endzone camera, not a tilt. Plan: scripts/09i_refine_endzone.py -- per frame, a 5-parameter correction
(small rotation, depth along the axis, focal scale) of the endzone pose fitted to the sideline-anchored 3D joints
against the confident endzone detections, smoothed over frames; then on a COPY: cameras_refined -> 05f refit -> the
residual, the loader rulers, 09d, the endzone blend.
09i first solve (5 params, unbounded): residual 13.4 -> 9.8 px p50 (p90 24.5 -> 14.8) with degenerate parameters (depth
shift to thousands of metres; depth along the axis and focal scale are collinear at 88 m). Bounded models compared next.
09i bounded models (residual p50 / p90 px, before 13.4 / 24.5): rot+focal 9.8 / 14.0; rot+depth 9.9 / 13.7 (dz p50 +0.45 m
= the known endzone depth bias); rot+height+depth 8.8 / 13.1 (dy at the -3 m bound on some frames). All at the endzone
detector's scatter floor. CARRY rot+depth ($S/cam_rot_depth.npz) downstream on a fresh copy after v99: cameras.npz
swapped -> 05n triangulate -> 05f refit -> loader rulers on the copy + joints export (09d, tilt) + the residual again.

**The refined endzone camera downstream, on the copy (2026-09-23 ~04:10):** 05n triangulated median reprojection 2.6 px,
05f refit joint rms 0.072 m. Residual fit - detection: ENDZONE norm 12.7 -> 6.7 px, common mode |dv| 8.0 -> 1.1 (p90 2.0);
SIDELINE 2.5 -> 5.5 px (the two views' disagreement now split between them: a camera weighting question, later).
09d on the copy's joints: sideways R arm 11.0 -> 6.9 %, L arm 5.6 -> 5.0, L leg 6.4 -> 2.2, R leg 4.2 -> 2.2 (!), trunk 0,
jerk 10 -> 12. THE ODD ARMS WERE THE ENDZONE CAMERA pulling the two-view fit. But the loader's placement LOST: steps 2 ->
13, census 0.16 -> 0.36, vanishings 8 -> 242 frames (167 421-607, 1 556-594, 17 475-488): the pair rule's +0.45 m
endzone common-mode compensation and the endzone-tuned holds now double-correct. Next: retire the compensation on the
copy (knob at call time), re-measure; the camera must win the placement rulers too before it is ported (18th case
memory: a camera refit that doubled the fast steps).
Split test (old camera in the loader, the corrected-camera refit for poses): steps 4, census 0.385, 167 still vanishes
421-607 and 17 475-490 -- so the placement break is in the NEW poses_refit.json, not the camera in the loader: 05f refit
28 players where the live refit has more (its --min-frame-frac 0.5 / --min-valid-joints 6 gates drop the pile ids).
Coverage: the LIVE poses_refit.json is a legacy file (65 ids, 5,885 records, from before the folds; the no-box rule drops
812 of them); a fresh 05n+05f on the current tables gives 28 ids / 4,891 records and only the frames BOTH cameras see
(id 9 271-391 against 14-620 live; 167 none) -- the loader's holds react to the missing records (167 vanishes). Testing
a MERGE on the copy: the corrected-camera refit where it has a record, the legacy record elsewhere (loader rulers +
09d). Open beyond that: a one-view refit (05p) for the frames the endzone does not see.

**v99 rendered (2026-09-23 05:41): `diag/play_001_v99_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` / `_endzone_blend`.**
v98 + the lost tackler held into the pile. Film check of the tail 600-612: two Ravens on the carrier at 600-604, the
pile flat with both on him at 608-612, as on the film. v99 = CURRENT BEST (tables *.v96). Viewer Version 16 = v99 joints.
Merge test (corrected-camera refit where present, legacy elsewhere; the OLD camera in the loader): steps 2, hops 0, census
0.343 (live 0.16); every twin / fragment / kit decision identical to live; the difference is stand_still (131 -> 162 hole
frames bridged, id 17 held 3 -> 33) and the census -- because place_from_refit puts every two-view frame on the refit's
pelvis, and the corrected camera moved those pelvises (the +0.45 m depth). The placement rules were tuned on the old
spots. Per-frame census diff against tl_v99.json next.
The merge changed COVERAGE: "placement from the refit" 4,938 body-frames live -> 7,425 merged (the fresh refit adds
records the legacy file lacks; each moves that frame's body from the box-bottom point to the refit pelvis). So the
census 0.34 is mostly the coverage change. Isolating the camera: a same-keys merge (only the legacy file's own
(pid, frame) records replaced by the corrected-camera poses) under test.
POPULATION ARTEFACT (2026-09-23 ~06:30): the "sideways R arm 11.0 -> 6.9 %" of the fresh refit was measured on a different
population -- the fresh 05n+05f only has records on two-view frames, so the remaining bodies were the well-fitted ones.
Merged with the legacy records (same coverage as live) the share is 10.8 % again, legs 5.5 / 4.7. The camera's own
effect is the same-keys merge (pending). The sideways arms live in the frames the endzone does not see (one-view
records of the legacy file), which no endzone correction can touch. State the population before the number (memory).
Split by record source on the merged copy: two-view frames (700 body-frames) sideways R arm 25.6 % (52 of them the QB's
throw), L arm 7.9, legs 3.5 / 2.7; legacy-only frames (1,660) R arm 8.3, L arm 6.5, legs 6.4 / 5.4. The arm ruler is
the throw and the carry; the LEGS are the clean signal, and the one-view records bend sideways twice as often.
Sideways R arm by id on the v99 joints (frames): 80 the QB 65 frames over 396-602 (the whole pocket, not just the throw
-- candidate fit error), 74 Gray 30 (456-606: run + carry), 204 Humphrey L arm 24 (blocking), 4 Madubuike 24, 37
Suamataia 24, 12 Taylor 18 (blocking), 17 16, 84 16, 15 Oweh 16, 9 15. Film check of the QB's arm in the pocket next.
Film check of the QB's right arm (v99, 420/450/480/500): REAL -- he holds the ball at his chest with both elbows out
(a frontal-plane bend); the blockers' hands and the carrier's ball arm are the same. The sideways-ARM ruler counts
football, not fits, and is retired as a target; the sideways-LEG ruler (6.4 / 4.2 % live; the one-view records twice
the two-view ones) stays. Coverage diff on the merged copy: 39 of 213 frames differ, almost all id 17 (a KC lineman)
drawn at 441-450 where the live does not (KC 12): the added records restore a twin -- the merge as such is not a port.

**Endzone camera VERDICT (2026-09-23 ~07:30): NOT PORTED.** Same-keys merge (the legacy file's own 5,885 records, 2,396
of them replaced by the corrected-camera poses; old camera in the loader): loader rulers identical to live (2 / 0 /
0.16, 4,938 refit placements); 09d L leg 6.4 -> 5.4 %, R leg 4.2 -> 4.8 %, arms 11.0 -> 10.5 / 5.8 -> 6.1, jerk 10 = 10,
trunk 0 -- a wash. With the corrected camera in the loader too: steps 13, census 0.19, vanishings 235 frames (167
421-607, 1 556-594): the holds and twin rules were tuned on the biased camera. The refinement (09i) is right by its
residual (13.4 -> 9.8 px, the detector's floor, +0.45 m depth) and stays as a tool: for the label builder (the copy's
labels have 3,175 endzone cross labels against 12,382 before) and for a future re-tune of the placement rules on a
corrected camera. play_copy restored to the original camera. Lesson recorded (29th).
NEXT UNIT running (~07:45): the one-view refit (05p, today's fit code with the hard hinges) for the endzone-blind frames on
the copy, swapped into the legacy file on its own keys only (two-view records untouched); loader rulers + 09d legs vs
live (6.4 / 4.2 %). The legacy one-view records predate the hard-hinge defaults (09-16); poses_refit.json's mtime is a
fold's relabel, not a refit.

**One-view refit PORTED (2026-09-23 ~08:05).** 05p with today's fit code (hard hinges, temporal weight 3) on the copy: 53
players, 2,591 one-view frames fitted, reprojection median 16.5 -> 3.0 px, body-frame joint speed p50 0.19 -> 0.39 m/s.
Swapped into the legacy cache on its own keys (2,588 records; two-view records untouched): loader rulers 2 / 0 / 0.16
unchanged; 09d jerk 10 -> 5, L leg 6.4 -> 5.8 %, R leg 4.2 -> 3.9 %, trunk 0 -> 2 (84 at 404-406, a rusher's stance
to check), arms 5.8 -> 8.3 / 11.0 -> 11.3 (the football ruler). Live poses_refit.json replaced (backups .v99 and
.pre_mono; the full 05p output kept as poses_refit_mono_2026-09-23.json). v100 chain launched. Film checks after:
the arms at 420-500, id 84 at 404-406, the tail.
Film check of id 84 at 400-410 (diag/lean_84_404.png): a Raven driving low into the KC line, bent ~70 deg -- REAL; the
new one-view records catch a lean the legacy ones missed. Viewer Version 17 = the v100 joints (the copy's export,
same config as live now).

**The first-person yaw, resolved on the film (2026-09-23 ~08:40):** the triangulated shoulders of the QB face 97 deg at
500 with a normal 0.38 m gap and match both cameras' left/right labels (sideline 9 px as-labelled vs 54 swapped;
endzone 34 vs 39, shoulders overlapping in that view). Film strips (diag/qb_shoulders_side.png, _end.png): the
sideline camera sees the "15" on his BACK at 470-500 and the endzone camera his profile -- his torso faces the far
sideline; his head turns downfield. The fit is right; the first-person camera needs a HEAD yaw, not a torso yaw.
Next: head yaw from the COCO face keypoints (nose against the ears' midpoint, one visible ear = a quarter turn) per
camera, into the export as a per-body gaze; the viewer uses it where present, the play-derived gaze elsewhere.
head_yaw on play 1: sideline 2,234 body-frames / 37 ids, endzone 6,786 (a coarse instrument: "away" = pi, one ear = 0.35
pi). QB: 103 deg (away from the sideline camera) at 480/520, -140 at 528, -180 at 540 (endzone) = downfield for the throw.
Next: 05k exports {pid: {frame: [heading, conf]}} as "gaze"; the viewer's first person uses it where conf >= 0.5, held
and smoothed, else the play-derived gaze.

**v100 rendered (machine clock 2026-09-23 07:04): `diag/play_001_v100_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs`
/ `_endzone_blend`.** v99 + the one-view refit with today's fit code on the endzone-blind frames. Film check: pocket
420-500 and whole field 420/500/580 as v99 (no regressions), the one-view bodies more articulated. v100 = CURRENT BEST
(tables *.v96; poses_refit.json = the same-keys merge, backups .v99 / .pre_mono). Next: the gaze export into the
viewer (Version 18), then the placement re-tune on the corrected endzone camera as the next unit.

**Head gaze from the face keypoints: measured, NOT wired (2026-09-23 ~09:45).** `pose/head_yaw.py` + 05k's `gaze` export
(27 ids, 6,417 readings on v100). Ruler: fast men (> 3 m/s) look where they run; 78 readings on both cameras. Heads
are 8 px (sideline) / 21 px (endzone) nose-to-ear and the keypoints sit on helmets: sideline one-ear 118 deg off
(median, n 28), endzone "both ears no nose = facing away" 94 deg off (n 18; a helmet's ear holes show from behind and
from the side); only the sideline facing-away (8 deg, n 14) and the endzone one-ear (26 deg, n 17) read. On the
quarterback (film strips both cameras 430-520): 430-450 is the PLAY-ACTION FAKE -- he faces his own end zone, the
endzone one-ear reading (63 deg, backward-right) is right and the play-derived gaze (attack direction) wrong; 480-520
he looks downfield and the sideline facing-away reading says the far sideline (103 deg) -- exactly the "faces the
sideline" the user reported, re-created. Net: the viewer keeps the play-derived gaze (Version 17 rule), the export
stays as raw material. Two cancelling sign errors fixed in head_yaw (world heading facing+yaw; the one-ear side): the
play's readings are unchanged, the three-point case (1 reading on the play) flips. Viewer Version 18 = v100 joints.

**Placement re-tune on the corrected endzone camera: CLOSED, no upside on play 1 (2026-09-23 ~10:40).** Three loader
arms on copies (A play_copy = live tables + original camera; B play_copy_b = the same tables + cam_rot_depth, the 09i
rot+depth refinement, +0.45 m; C = B with STAND_DEBUG_IDS). A reproduces live (steps 2 / hops 0 / census 0.16); B =
13 / 0 / 0.192, vanish 235. But the DRAWN BODIES DO NOT MOVE between A and B: on the 4,673 shared (pid, frame) keys
the median A->B move is 0.01 m (204: 0.07 m, 4: 0.05, 81: 0.03, everyone else <= 0.01) -- the common-mode shift
already takes the endzone bias out of endzone-only points per frame (play-wide +0.28 m under A, -0.22 m under B, the
per-frame offsets absorb both), and two-view points take x from the sideline and y from the endzone's lateral axis,
so an endzone depth bias never reaches them. B's 13 steps and 235 vanish frames are three RULE EDGES flipping on the
same positions: id 167 (a KC-kit fragment box on the 76/Raven pile at 411-420, film-checked) escapes the rider rule
(RIDER_M 0.6) for 10 frames and then "vanishes" for 187; BAL 1's hold ends at 556 under the successor test; BAL 4's
seam at 568-573. A new placement ruler (`$S/placement_residual.py`: every drawn body's ground point projected into
each camera against the detector's foot point, same keys, px): two-view bodies in the SIDELINE 21.1 -> 20.1 norm p50
(unchanged camera), in the ENDZONE 20.2 -> 26.8 (dv mean -6 -> -20 px: the corrected camera projects the
sideline-anchored bodies 14 px farther from their endzone feet). The old camera (paint + box height, 08l) stays; the
09i refinement fits the camera to the two-view fit's compromise, a circular ruler, and its pose gain was a wash on
the same keys (07:30 entry). Also dropped with it: camera weighting in the fit (belonged with the re-tune). The
endzone blend at 479 shows the drawn paint on the footage's yard lines. play_copy_b kept (28 MB, tables only).

**The jogging band (2.5-4.8 m/s), measured 2026-09-23 ~11:30 (v100 as rendered, 395-607).** 39 % of the play's
body-frames (1,845 of 4,682; > 4.8 m/s 24 %, < 1 m/s 10 %). As rendered (gait above 4.8): the slower ankle moves at
0.76 of the pelvis, planted (< 0.3) 9 %, (< 0.5) 26 % on 1,798 band body-frames. The sideline leg KEYPOINTS cycle on
every jogger (the left-minus-right ankle x: std 20-40 px, autocorrelation periods 24-37 frames = 1.6-2.5 Hz on ids 0,
74, 80, 30, 7), and the FIT follows them: band ankle residual p50 6.0 / p90 17.6 px, knee 6.2 / 15.0; the fitted
ankle's sweep about the hip 13.9 px std against the keypoints' 15.1, correlation 0.85-0.99 per id. So the fit is
not the skate. A strike-window probe (strikes = maxima of the hip flexion in the motion plane, stance = 0.45 of the
cycle): 41 windows on 19 ids, pelvis travel per stance 0.47 m, the ankle's world skate 0.53 m, sweep/travel 0.35 --
the sweep is a SINUSOID (a foot planted for an instant per cycle) where a stance is flat for 40 % of it. Remedy
built (`render/foot_lock.py` rhythm mode, commit 98f7a45, opt-in): the fit's own strikes, the ankle pinned at its
strike point for DUTY 0.40 of the cycle, the leg re-solved by the numpy-FK solve_leg, eased over 3 frames, released
0.45 m behind the hip. A/B running (`$S/jog_ab.py`): band planted share / ratio, the leg keypoint residual (must stay
near 6 px), joint jitter, then the film. The old dips mode's "no effect" (09-16) was the sprint band, where the legs
do not cycle; the gait owns that band now.

**Foot lock A/B, first arm (2026-09-23 ~12:00, `$S/jog_ab.py`, v100 as rendered, band 2.5-4.8 m/s = 1,798 body-frames
on 395-607).** A (as drawn): slower-ankle/pelvis ratio p50 0.76, planted (< 0.3) 9 %, (< 0.5) 26 %; band ankle
residual vs the sideline keypoints p50 6.0 / p90 17.3 px, knee 6.2 / 15.0; joint jitter p50 0.0170 / p90 0.0604 /
p99 0.183. B (rhythm lock, defaults: DUTY 0.40, EDGE 3, MAX_BACK 0.45, BAND_RULE window): 39 stances on 263 frames
of 16 ids, the foot moved p50 0.12 m / p90 0.31, solver miss p90 1 mm; ratio p50 0.75, planted 15 % (< 0.5 29 %);
ankle 6.6 / 19.3 px, knee 6.3 / 15.1; jitter p90 0.0688 / p99 0.192. A gain where it acts, at +0.6 px p50 on the
ankles and +14 % joint jitter p90 -- but it acts on 15 % of the band. Funnel (`$S/lock_funnel.py`): 376 strikes,
374 windows, 171 dropped for a frame at the gait's speed, 159 for a frame under 2.5 m/s, 39 kept, and the release
(0.45 m behind the hip) trimmed 271 of the kept 534 frames. BAND_RULE "strike" added (the strike in the band, no
frame at the gait's speed; a man slowing through 2.5 mid-stance still plants); two arms running: strike, and strike
with MAX_BACK 0.35.
Strike-rule arms (~12:40): BAND_RULE strike -- 72 stances / 518 frames on 20 ids, foot moved p50 0.11 / p90 0.32 m;
band ratio p50 0.72, planted 18 % (< 0.5 32 %); ankle 6.7 / 19.4 px, knee 6.3 / 15.2; joint jitter p90 0.0765 (+27 %
on A's 0.0604), p99 0.215. Strike + MAX_BACK 0.35 -- 69 / 435 frames; planted 16 %; ankle 6.5 / 19.0; jitter p90
0.0728. The planting gain is real and the keypoints hold (+0.5-0.7 px), the JITTER is the cost: on the frame after a
stance the foot jumped from its pin to the fit's mid-swing ankle (0.3 m in a frame). RELEASE 6 built (commit 64553b9:
the target eased from the pin back to the fitted ankle over six frames, smoothstep; EDGE 1); arm running.
Release arm (~13:05, strike + RELEASE 6, EDGE 1): 72 stances, 907 frames touched (stance + release) on 20 ids, foot
moved p50 0.16 / p90 0.43 m; band ratio p50 0.67 (A 0.76), planted 25 % (A 9 %; < 0.5 37 % vs 26 %); ankle 7.4 /
22.0 px (A 6.0 / 17.3), knee 6.3 / 15.8; joint jitter p90 0.0731 (A 0.0604, the snap arm 0.0765), p99 0.194 (A
0.183). The planting nearly triples; the ankle residual grows by the skate it removes (a pinned foot against a
sliding keypoint, 0.16 m = 13 px at the stance's end); the jitter is not the end snap alone -- a warm-started leg
solve (the previous locked frame's solution as the start, the pull still toward the fit) is next, with a probe
bucketing the jitter by role (strike / stance / end / release / untouched).
Warm start (commit aedf15a): NO EFFECT on the play (jitter p90 0.07315 = 0.07315): the solve was not hopping. The
jitter-by-role probe (`$S/jitter_where.py`, locked-leg joints, p50 / p90): stance interior 0.0103 / 0.0295 against
A's 0.0104 / 0.0237 -- the pinned stance is smooth; STRIKE 0.033 / 0.123 (A 0.0118 / 0.0315) and RELEASE 0.0397 /
0.1018 (A 0.0097 / 0.0241) carry it: the foot stops dead at the strike (from the fit's swing at ~0.1 m/frame) and
must catch the fit's swinging ankle over six frames after. A footfall is abrupt in life too; the release catch-up is
ours. Arms running: EDGE 3 + RELEASE 12, EDGE 2 + RELEASE 10 (strike rule). The film decides after.
Easing arms (~13:50): EDGE 3 + RELEASE 12 -- 1,225 frames touched, planted 18 %, ankle 8.0 / 24.6, jitter p90 0.0875,
p99 0.443; EDGE 2 + RELEASE 10 -- 1,129 frames, planted 22 %, ankle 7.9 / 23.8, jitter p90 0.0925, p99 0.430. Both
LOSE to EDGE 1 + RELEASE 6 on every ruler: a long release chases the fit's ankle into its next swing and the catch-up
is violent (p99 doubles); the in-ramp only lets the foot slide. Default arm stands (planted 25 %, ankle 7.4 / 22.0,
jitter p90 0.0731 / p99 0.194). v101 chain launched (~13:55) with the lock on through with_flag (MODE rhythm, BAND_RULE
strike; EDGE 1, RELEASE 6): 08y, 08x, dump, 07l, hifi, both blends. Film check next on stride-2 strips through one
stance per jogger (`$S/jog_strip.py`): id 15 R 458-470, id 0 R 584-594 / L 567-575, id 80 L 465-477, id 28 L 525-534.

**v101 rendered (machine clock 09:15): `diag/play_001_v101_*` (hifi, sideline/endzone blends) = v100 tables + the
foot lock (rhythm, strike rule, EDGE 1, RELEASE 6) through with_flag; 07l: 83 stances on 1,037 body-frames of 24 ids;
steps 2 / hops 0 / census 0.16 (unchanged).** Whole-scene check 450 / 500 / 562: bodies on the film's men, no
regression. FILM on the pinned stances (`$S/lock_diff_strip.py`: film | v100 | v101 | diff, zoomed on the man): the
open-field jogger (id 0, BAL 21, turning upfield 566-578) -- v101 keeps the left foot on the "2" numeral through
572-576 as the film does where v100 slid it; the release at 578 stretches the trailing leg a touch long. The ENGAGED
rusher (id 15 driving into his blocker, 458-470) -- v100's long drive stride matched the film, v101 compressed it: a
pushing man's feet DO slide, the stance model is wrong for him. The receiver 74 (542-552, being tackled) -- small leg
changes, undecidable. Also: the strike set depended on the run's start (id 0's R stance at 584-594 found on 395-607,
absent on the whole clip: the earlier-of-two-maxima rule). Fixes: ENGAGED_M 1.0 (no stance struck with an opponent
within a metre; engaged_flags from the timeline's teams) and the higher-of-two-maxima rule. v101 is NOT the best
(the rusher); v102 = the gated lock.
Gated arm (~machine 09:50; ENGAGED_M 1.0 + the higher-of-two-maxima strike rule, strike band rule, EDGE 1 / RELEASE 6):
61 stances / 764 frames on 19 ids (11 stances gated out), foot moved p50 0.17 / p90 0.41 m; band ratio p50 0.71,
planted 22 % (< 0.5 35 %); ankle 7.5 / 21.9 px, knee 6.3 / 15.6; joint jitter p90 0.0718 / p99 0.190 (A 0.0604 /
0.183; ungated 0.0731 / 0.194). Most of the gain kept, the engaged men left to the fit. v102 chain launched (the same
with_flag chain as v101; the gate and the strike rule are module defaults; 05k / 07l pass team_of, commit 6ed9e9a).
Film check next: id 15 (458-470) must now equal v100; id 0 (566-578) as v101; the whole scene at 450 / 500 / 562.

**v102 rendered (machine clock 10:26): `diag/play_001_v102_*`; 07l: 71 stances on 886 body-frames of 23 ids (12 gated
out); steps 2 / hops 0 / census 0.16.** Film: the DB (id 0, 566-578) as v101 (the foot held on the numeral); the
rusher (id 15, 458-470) UNCHANGED from v101 -- the gate missed him: his drawn distance to his blocker (37) is
1.36-1.55 m at 458-470 (the placement holds engaged men apart; at 525-548 they read 0.69-0.89 m and were gated) while
the film's boxes overlap. The ground-distance gate is the wrong instrument for contact; the film's boxes are: a stance
struck while an other-team SIDELINE box overlaps the man's (IoU >= 0.15) is not locked (ENGAGED_IOU), on top of the
distance gate. v102 is NOT the best; v103 = the box gate.
Box gate arm (ENGAGED_IOU 0.15 at the strike frame): 58 stances / 728 frames, planted 21 %, ratio 0.71, ankle 7.4 /
21.9, jitter p90 0.0715 -- and the rusher STILL locked: his strike frame 458 read IoU 0.136 with his blocker (37),
his engaged frames were 459-465 (side by side in the sideline view two men overlap 0.07-0.19 through a block). Fix
(commit after 54a0d05): the gate looks at every frame of the stance and counts touching boxes (ENGAGED_IOU 0.05).
Arm running; v103 after it.
Window box gate arm (ENGAGED_IOU 0.05 on any frame of the stance + ENGAGED_M 1.0; commit 1edd44f): 37 stances / 463
frames on 15 ids (the rusher 15 gated 456-471, the tackled receiver 74 540-553; ids 0 / 28 / 80 free); band ratio
p50 0.72, planted 17 % (A 9 %; ungated 25 %); ankle 6.8 / 20.6 px (A 6.0 / 17.3), knee 6.4 / 15.4; joint jitter
p90 0.0669 (A 0.0604, +11 %) / p99 0.188 (A 0.183). Half the gain of the ungated lock at a third of its cost, and
none of it on engaged men. v103 chain launched (machine ~11:05) with it; the film decides.

**v103 rendered (machine clock 11:34): `diag/play_001_v103_*` = v100 tables + the foot lock (rhythm, strike band rule,
ENGAGED_M 1.0 + ENGAGED_IOU 0.05 on any stance frame, EDGE 1, RELEASE 6). CURRENT BEST, film-checked.** 07l: 45
stances on 557 body-frames of 18 ids; steps 2 / hops 0 / census 0.16. Film (`$S/lock_diff_strip2.py`, film | v100 |
v103 | diff): the rusher 15 (458-470) identical to v100 (the gate holds); the DB 0 (566-578) keeps his left foot on
the numeral through 572-576 as the film does (v100 slid it), the trailing leg a touch long at 578; the linebacker 28
(522-536, a lateral shuffle then the turn) plants the left foot through 528-532 where v100 glided both feet; the
whole scene at 450 / 500 / 562 unchanged. Band rulers (gated arm): planted 9 -> 17 %, ratio 0.76 -> 0.72, ankle
residual 6.0 -> 6.8 px, joint jitter p90 +11 %. Module defaults now MODE "rhythm" + BAND_RULE "strike" (full suite
gate); the chains no longer need with_flag for it. Viewer Version 19 = v103 joints. Open on the lock: the release
stretch at the stance end (a shorter MAX_BACK or an earlier release, measured against the same strips); the
strike-event jitter is a real footfall.

**The release stretch, mechanism found (machine ~12:00, `$S/reach_probe.py` on the DB id 0, v103 lock):** through
the stance 567-575 the pin runs from +0.24 m ahead of the hip to -0.40 behind (the fit's own ankle -0.28), and over
the RELEASE 576-581 the target still blends toward the fixed pin while the pelvis moves on: the pin reads -0.47 ->
-0.65 m and drags the foot back (the fit's ankle sits at -0.31 -> -0.34) -- the stretch on the film at 578. Two more
of his "stances" (509-511, 515-518) began with the foot already 0.24-0.33 m BEHIND the hip along the motion (the
fit's flexion maximum with the foot behind the body): no strike, and the release then pulled them to -0.77. Fixes:
the released foot keeps its pelvis-relative offset from the stance's last frame and swings from there to the fit
(never farther behind than at the stance's end); a strike needs the foot at least MIN_REACH0 (0.0 m) ahead of the
hip. Arms MAX_BACK 0.35 / default control running for the record.
Release2 arm (the release from the stance-end offset + MIN_REACH0 0.0; commit 68f28ed / 9893301): 21 stances / 279
frames on 14 ids -- MIN_REACH0 refused 16 of 37 stances; band planted 14 % (A 9 %), ratio 0.74, ankle 6.4 / 19.3 px,
jitter p90 0.0632 (A 0.0604, +5 %) / p99 0.185. Cheaper and smaller. WHY so many strikes with the foot behind the
hip: the strike is the HIP FLEXION maximum, and at that moment the knee is still bent from the swing, so the ankle
sits under or behind the hip; the foot's true forward extreme (the strike) comes as the knee extends. Next: the
strike from the ANKLE's forward reach relative to the pelvis in the motion plane (ankle_world_xy, no flexion), the
stance from there -- the foot lands ahead by construction and the back-reach at the stance's end shrinks.
Reach-signal arm (the strike = the ankle's forward-reach maximum from the pelvis in the motion plane, MIN_SWEEP_M
0.15; run on a patched COPY of the module while the v104 chain held the repo's -- `$S/jog_ab_mod.py` +
FOOTLOCK_PATH): 28 stances / 421 frames on 12 ids (flexion + MIN_REACH0: 21 / 279); band planted 17 % (A 9 %), ratio
0.74, ankle 6.8 / 18.6 px (the best p90 of any arm; A 6.0 / 17.3), knee 6.4 / 15.0; jitter p90 0.0644 (A 0.0604,
+7 %) / p99 0.188. The foot lands ahead of the hip by construction; the stances survive. v105 = this, after v104
lands (module edits wait for the chain).

**v104 rendered (machine clock 12:49): the release from the stance-end offset + MIN_REACH0, flexion strikes; 07l: 22
stances on 298 body-frames.** Film (`$S/lock_diff_strip2.py --a v103 --b v104`, the DB id 0 566-580): the only change
is the release 576-580 -- the trailing leg no longer stretches at 578 (the foot sits under him as the film's does);
the stance 567-575 identical to v103; whole scene 450 / 500 / 562 unchanged. v104 is an improvement on v103's one
open defect but with fewer stances (the flexion strikes). v105 chain launched (machine ~13:00) with the reach-signal
strike (commit f5ef27e, 32 tests): the film decides between v103 / v104 / v105 -- v105 expected best (28 stances,
the foot ahead of the hip by construction, no stretch).
PAUSE (user powering off, machine ~13:20): the v105 chain was mid-render (`$S/chain_v105.sh`, log `$S/chain_v105.log`).
ON RESUME: re-run `nohup bash $S/chain_v105.sh > $S/chain_v105.log 2>&1 < /dev/null &` (05k resumes from existing
frames in render_hifi_v105 / render_view_v105 / render_ezview_v105), then the strips: id 0 561-577 + 583-597, id 2
541-557, id 30 447-463, id 28 521-537 (`lock_diff_strip2.py --a v103 --b v105`), the whole scene 450 / 500 / 562, then
the v105 verdict, the joints export + viewer, the write-up. Repo at f5ef27e (reach-signal strike default).

**Resume (machine ~15:50-16:20).** v105 chain relaunched after the power-off; the hifi + sideline blend finished, the
endzone view crawled (39 / 201) beside two of the user's `uv` Python 3.12 processes holding 11.9 of 12.3 GB; on the
user's word both were killed (pids 15600 / 54304) and the endzone view relaunched (05k resumes from its frames).
VPoser V02_05 (user's download) moved to `data/body_models/vposer/V02_05/` (snapshots epoch 08 / 13 ckpt + yaml;
gitignored). TRAP: `pip install git+human_body_prior` into smplx312 swapped torch for 2.13.0+cpu (CUDA gone; the
running endzone render died, exit 127); restored `torch==2.11.0 --index-url .../whl/cu128` (cuda True; the package
still imports under its version complaint). Next unit: the VPoser ruler (pose/pose_prior.py + 09j): the latent norm
per drawn body-frame as the plausibility score, the projection decode(encode(pose)) as the correction, gated on the
keypoint residual; scored on 09d / 07l / the film.

**v105 rendered (hifi + sideline blend machine ~16:05; the endzone blend re-rendering after the GPU clearing): v100
tables + the foot lock's final form -- reach-signal strikes, the release from the stance-end offset, the box +
distance engagement gate (commit f5ef27e; module defaults). CURRENT BEST, film-checked on the sideline.** 07l: 39
stances on 587 body-frames. Film (`--a v103 --b v105`): the DB id 0's second stance 584-596 holds the right foot on
the turf through 586-592 where v103 slid it, the swing at 594-596 as the film's; the backpedalling DB 30 (448-462)
and the shuffling LB 28 (522-536) read as planted steps where v103 glided; the whole scene 450 / 500 / 562
unchanged. Band rulers (gated, reach): planted 9 -> 17 %, ratio 0.76 -> 0.74, ankle 6.0 -> 6.8 / 17.3 -> 18.6 px,
jitter p90 +7 %. Viewer Version 20 = v105 joints (export running). The lock unit is CLOSED at this form; open
only if more plays show a new failure mode.

**VPoser ruler over play 1 as rendered (v105 lock; `$S/prior_ab.py`; 4,704 body-frames on 395-607; machine ~20:40):**
latent-norm score p50 4.22 / p90 6.71 / p99 15.9, 6.8 % over 8.0 (Gaussian-noise poses score 10-16, the rest pose
3.4); hinge-violation share 0 (the fit's hard hinges); the score barely correlates with the sideline keypoint residual
(0.06) -- it sees something the residual does not. Worst: id 9 (KC, the sprinting receiver) at 415-418 scoring
21-22, id 5 (KC) 526-542 at 17-18, then 19, 139; per-id p90: 5 16.5, 9 13.1, 19 10.4, 139 9.7, the rest under 8.
Film strips of those cut; the shift arm (--apply 8 12: blend toward the projection from score 8, fully at 12) running.
Shift arm (blend toward the projection from score 8, full at 12, per frame): 321 body-frames moved (138 fully), mean
joint move 0.16 rad; score p99 15.9 -> 9.7, over 8.0 6.8 -> 5.0 % (a projected pose does not land under 8: the decoder
is not idempotent); keypoint residual p50 6.3 -> 6.7, p90 14.0 -> 15.5 px; hinge-violation share 0 -> 0.002; joint
jitter p90 0.064 -> 0.062 but p99 0.185 -> 0.224 -- a per-frame weight makes edges between moved and unmoved frames.
Next: the weight smoothed along each man's run (pose_prior.shift_timeline, SHIFT_SIGMA 3), then a sideline-view
render with the shift for the film (the sprinter id 9 at 414-418: the film has an upright sprint with pumping arms,
the fit leans far forward with the arms flung back -- VPoser 22, the keypoint residual silent).
v105 endzone blend done (machine ~20:15; the render checked at the pocket: bodies on the footage's men). Viewer
Version 20 = v105 joints. The VPoser shift wired into 05k / 07l after the foot lock behind pose_prior.SHIFT (off;
commit 90cb916); the smoothed-weight arm (sigma 3) running; a sideline-view render with SHIFT on (with_flag) follows
for the film check of the sprinter id 9 (414-418) and id 5 (526-542).
Smoothed-weight arm (blend 8 -> 12, the weight Gaussian-smoothed along each man's run, sigma 3): 550 body-frames
moved (46 fully), mean joint move 0.093 rad; score p99 15.9 -> 9.8, over 8.0 6.8 -> 5.4 %; keypoint residual p50
6.3 -> 6.6, p90 14.0 -> 15.4 px; hinge-violation share 0.001; joint jitter p90 0.0644 -> 0.0599 and p99 0.185 -> 0.174
-- BOTH better than as drawn (the per-frame blend had p99 0.224). Three rulers up, the keypoints down a little; the
film decides (the sideline-view probe render v106p with SHIFT on is running).
Film on the ruler's tail (v105 strips): id 9 (KC 1, the sprinter) 414-418 -- the film has an upright sprint with
pumping arms, the fit leans far forward with both arms flung back: a REAL defect the keypoint residual never
flagged (VPoser 21-22). id 5 (the KC back) 450-462 -- a low pass-protection crouch beside the quarterback, on its
keypoints; VPoser 11 because crouches are rare in mocap: a legitimate posture the shift would straighten. So the
shift needs the film's say: pose_prior.support_weights -- a body-frame whose sideline keypoint residual is under
8 px is not moved, over 16 px moved in full, linear between, no keypoints = full (SUPPORT_LO / HI; shift_timeline
takes ``support`` {(pid, frame): px}). Arm running (--support).
Support-gated arm (blend 8 -> 12, sigma 3, the body's median sideline residual as the support): 509 body-frames
moved, none fully, mean move 0.038 rad; score p99 15.9 -> 14.9 (the sprinter 22 -> 18 only: his body-median residual
sits under 16 px because the legs are on their keypoints and the median hides the arms), over 8.0 6.4 %; keypoint
resid 6.3 -> 6.4 / 14.0 -> 14.5; jitter p90 0.0644 -> 0.0612, p99 0.185 -> 0.180 (both better than as drawn); the
back's crouch kept (right). Next form: the support PER JOINT ROW -- each body_pose row gated by the residual of the
joint at the end of its bone (shoulder row <- elbow, elbow <- wrist, hip <- knee, knee <- ankle; the spine / neck /
collar rows take the body median), so the sprinter's arms move while his legs stay.
**Probe render v106p (sideline view, the shift ungated, sigma 3; 1,491 body-frames moved of 13,510) on film:** the
sprinter id 9 at 410-422 stands up with the arms carried forward and bent -- the film's upright sprint with pumping
arms, where v105 leaned 60 deg with both arms flung back (a win, if a touch too upright); the back id 5 at 450-462
is straightened out of his real low crouch (a loss: the film has him bent over in pass protection). The per-row
support gate is the form for both; `scripts/09j_pose_support.py` writes `<play-dir>/pose_support.json` (per body-frame
the 21-row residuals through each bone's child keypoint + the VPoser score) and 05k / 07l read it under SHIFT.
Per-row support arm (blend 8 -> 12, sigma 3, each body_pose row gated by its bone's child keypoint residual): 718
body-frames moved (4 fully), mean move 0.030 rad; score p99 15.9 -> 14.7 (the sprinter 22 -> 18: his arm rows move
part way, the wrist / elbow residuals sit in the 8-16 px ramp); keypoint residual p50 6.3 = 6.3, p90 14.0 -> 14.5;
jitter p90 0.0644 -> 0.0608, p99 0.185 -> 0.180 (both better than as drawn); the back's crouch kept. 09j
(pose_support.json) running; then the row-gated probe render v107p and the film.
09j on the play (215-615): 5,890 of 8,818 body-frames carry sideline keypoints (the rest -- endzone-only men, low
confidence -- get the ungated weight). The sprinter's arm rows at 414-418: L shoulder 1.5-8 px, R shoulder 12-22,
L elbow 15-20, R elbow 4-28 -- his LEFT shoulder reads film-supported while the arm is visibly flung back: the
detector's elbow keypoint sits on the flung-back position (motion blur on a 100-px sprinter's arms; the fit followed
the detector, the detector was wrong). So the per-row gate frees the right arm and holds the left; the film on
v107p decides; if it reads odd, the arm rows take a looser ramp than the legs (the arm keypoints are the least
reliable on blurred sprinters) or the plausibility score alone judges the arms.

**2D fine-tune baseline (09h --score-only, the pretrained yolov8x-pose on the held-out frames of pose_ds; machine
~20:45):** endzone -- det n 1,285 pck10 0.991 / pck20 0.992 / 0.4 px (the labels ARE the detector there), fit_self
n 2,085 0.832 / 1.000 / 6.7 px, fit_cross n 2,435 0.008 / 0.483 / 20.4 px; sideline -- det n 971 0.969 / 0.978 /
0.5 px, fit_self n 6,164 0.971 / 0.994 / 2.7 px, fit_cross n 277 0.505 / 0.830 / 9.6 px. fit_cross is the target
class (labels the detector could not have produced, anchored by the other camera); on the endzone it sits 20 px off
the detector (the endzone's +8 px common mode is inside that number). The training run (30 epochs, imgsz 1920,
batch 2, backbone frozen 10 layers) starts when the GPU is free of the v107p probe render.
**Probe v107p (the shift row-gated by pose_support.json; 1,873 body-frames moved, 176 fully, mean 0.060 rad) on
film:** the back id 5 keeps his crouch (450-462 as v105: right). The sprinter id 9 (410-422) sits between v105 and
the ungated v106p: the lean eased, the RIGHT arm brought forward and bent, the LEFT arm still trailing back -- its
shoulder row read film-supported (elbow residual 1.5-8 px) because the detector's blurred elbow keypoint sat on the
flung-back position. Arm keypoints on a 100-px sprinter are the least reliable joints; next: per-row-class ramps
(arms 4 -> 10 px, legs 8 -> 16) or the keypoint confidence folded into the support.
Arm-ramp arm (row gate, arms 4 -> 10 px, body 8 -> 16; commit af6bf8a): 718 body-frames moved (5 fully), mean
0.036 rad; score p99 14.5 (the sprinter 18.7 at 416: his arms only part-freed, the elbow residual 1.5-8 px lands at
weights 0-0.7); keypoint resid 6.4 / 14.5; jitter p90 0.0608 / p99 0.180 (as the plain row gate; both better than
as drawn). The aggregate rulers cannot see one man's arms; the film can, after the GPU frees (the 2D fine-tune is
at epoch 5 / 30, ~75 min). The two threads meet there: the sprinter's flung arms are a DETECTOR error on blurred
arms (the fit followed it); if the fine-tune's cross-camera labels fix the arm keypoints, a re-detect + refit fixes
the fit itself and the shift has less to do.

**2D fine-tune trained (09h, 30 epochs in 40 min, imgsz 1920, batch 2, backbone frozen 10 layers; machine ~22:15):**
held-out frames, PCK@10 / median px, baseline -> fine-tuned -- endzone: det 99.1 -> 93.1 % / 0.4 -> 1.6 px,
fit_self 83.2 -> 90.4 % / 6.7 -> 4.4, fit_cross 0.8 -> 72.4 % / 20.4 -> 5.8; sideline: det 96.9 -> 93.0 % / 0.5 -> 1.5,
fit_self 97.1 -> 96.3 % / 2.7 -> 2.2, fit_cross 50.5 -> 85.8 % / 9.6 -> 3.9. The target class (labels the detector
could not have produced) moves from 20 to 6 px on the endzone; "det" slips 1-1.5 px because those labels ARE the old
detector's points. Caveat: the held-out frames are frames of the same play (same men, light, camera), so this is
the fit's own projection learned back in part; the honest test is downstream: re-detect on the play copy
(`05m --weights pose_ft/train/weights/best.pt`) -> triangulate -> refit (05f, 05p same-keys merge, the v100 recipe)
-> 09d / 07l / VPoser rulers + the film (the sprinter's arms at 414-418 first). Weights: pose_ft/train/weights/best.pt.
Re-detect on the copy with the fine-tuned weights (05m, imgsz 1920): sideline 14,129 detections matched / 918
unmatched, endzone 11,527 / 676, 25,656 person-frames (the live detector's table kept as keypoints_2d.parquet.v105).
05n on them: 29 players triangulated, valid joints 52 % of all / 77 % of the COCO-observable, median reprojection
1.2 px. The downstream chain (`$S/copy_ft_chain.sh`: 05f two-view refit -> the live cache's records replaced on their
own keys (`$S/merge_samekeys.py`) -> 05p one-view refit merged on its keys -> loader rulers, 09d, VPoser scores) is
running on the copy; the arm-ramp gated shift probe render v108p on the GPU beside it.
**Probe v108p (row-gated shift with the arm ramps 4 -> 10 px; 1,903 body-frames moved, 176 fully, mean 0.062 rad)
on film:** as v107p to the eye -- the sprinter's lean eased and his right arm carried forward, the left arm still
trailing (its blurred elbow keypoint at 1.5-8 px still reads as partial support); the back's crouch kept; the whole
scene at 450 / 500 / 562 unchanged. The gated shift is a mild, safe improvement; whether it ships waits for the
fine-tuned detector's refit (running on the copy): if the new arm keypoints put the sprinter right in the fit
itself, the shift has less to do and its gate reads truer support.
PAUSE (user powering off, machine ~21:50): the fine-tune downstream chain on the copy was at the 05p one-view refit
(05n done: 1.2 px median reprojection; 05f done; same-keys merge done: 5,885 base records, 2,361 replaced, 2,411 new
records outside the base keys left out -> play_copy/poses_refit_step.json). ON RESUME: rerun only the tail --
  05p: `python scripts/05p_refit_mono.py --play-dir play_copy --refit play_copy/poses_refit_step.json --out play_copy/poses_refit.json`
  then the rest of `$S/copy_ft_chain.sh` from "loader rulers" on (probe_copy 9 5 0, the joints export + 09d, prior_ab arm A on the copy);
  then the film: a sideline-view render of the copy (launch_view with P=play_copy) and strips of the sprinter id 9
  at 410-422 against v105. Decide: port the fine-tuned keypoints (05m on play_001 with pose_ft/train/weights/best.pt +
  the same recipe) and ship the row-gated VPoser shift (pose_prior.SHIFT True) on the film's say. Repo at 2bc0484.

**Resume (2026-09-24 morning). The fine-tune chain had finished before the power-off.** On the copy: 05f two-view
refit 29 players / 458 frames, median joint rms 0.050 m; same-keys merge 2,361 of 5,885 records replaced; 05p
one-view refit 2,647 / 2,647 frames on 48 players, reprojection median 15.0 -> 2.1 px (against the fine-tuned
keypoints). POSE rulers (09d on the export, 395-607): hinge jerk 9 (L leg 1, R leg 5, R arm 3; v105 5), sideways
bends none listed, trunk 2 (id 9 -- the sprinter's lean); VPoser score p50 / p90 / p99 3.71 / 5.67 / 9.47 (v105 4.22 /
6.71 / 15.9), over 8.0 2.8 % (6.8 %), the sprinter's 414-418 out of the tail (his worst now 15 at 395-397); jitter
p90 0.0553 (0.0644) / p99 0.214 (0.185). But the PLACEMENT broke: loader steps 6 / hops 2 / census 0.465 (live 2 /
0 / 0.16), vanishings 395 frames (17 gone 424-607, 167 421-607, 4 474-519): the loader reads keypoints_2d.parquet
for ankle anchoring, the twin rays and the depth snap, and its rules were tuned on the old detector's points (the
corrected-camera story again). So the split: the fine-tuned keypoints feed the FIT only; the loader keeps the live
table. On the copy: keypoints_2d.parquet <- .v105 (the fine-tuned table kept as keypoints_2d_ft.parquet), the new
poses_refit.json kept; rulers + the film again.
**VPoser inside the fit built (commit df9bd77):** Mono2DConfig / SMPLXFitConfig.vposer_weight (0 = off), the residual
sqrt(w) * z(body_pose) next to the L2 prior; the encoder re-implemented in numpy (pose_prior.NumpyEncoder, 1e-4 of
torch) so the numeric Jacobian is cheap; 05p / 05f --vposer-weight. Test: an implausible target fitted with the term
scores lower on VPoser within 3 px of the plain fit. Two 05p arms on the copy (the fine-tuned keypoints, base
poses_refit_step.json): --vposer-weight 0.003 -> poses_refit_vp0.003.json, 0.01 -> poses_refit_vp0.01.json; each then
measured by swapping it in as the copy's poses_refit.json for the loader rulers, 09d and the VPoser scores
(`$S/rulers_for_refit.sh FILE TAG`). Units: the reprojection residual is px / 10, the L2 prior sqrt(0.02) * |bp|
(~0.3), a normal pose's latent norm 4-6 -> w 0.003-0.01 pulls about as hard as the L2.
**The fine-tuned fit on film (the copy's sideline-view render `vft`, fine-tuned poses + the live keypoint table for
the loader):** the sprinter id 9 at 410-422 is an UPRIGHT sprint with both arms bent and pumping -- the film's man;
v105 had him at 60 deg with the arms flung back and the VPoser shift probes fixed only one arm. The fit itself is
right now: the detector was the error. The back id 5 keeps his crouch. Loader rulers with the split tables: steps
2 / hops 0 but census 0.385 (live 0.16), vanish 211 (167 421-607 -- the KC-kit fragment admitted again, as under the
corrected camera; 17 475-490; 171 600-607); 09d hinge jerk 10 (v105 5), trunk 2 (id 9). Per-frame census diff next:
which ids the copy draws that live does not.

## 2026-09-24 16:45 -- first-person POV (the user: "can we figure out how we can do POVs better?") + a 05p bug

**The POV rule, measured.** The viewer's first-person gaze was a play rule (faster than 1.5 m/s: along the run;
lineman / carrier: the attack direction; else: at the ball) that ignored the drawn body. Census over the live
window (2,346 body-frames, $S/pov_census.py): more than 90 deg from the drawn torso on 39 %; 30 % are men moving
BACKWARD relative to their torso (safeties backpedalling, tackles in pass sets, the QB's drop), where it looked
behind them. Film ruler ($S/pov_ruler.py: arrows from the helmet on both broadcast cameras, 24 cases): the drawn
torso matched the helmet on every backward case (safeties 2/30, CBs 0/6, LBs 7/171, the tackle 12, the centre 204);
the QB in the pocket (486-526) has his torso to the far sideline (the sideline camera sees his back number) and his
head downfield -- the old rule was right there, the torso 90 deg off.

**render.gaze (new, 8 tests): look = the torso heading + a bounded head turn toward what he watches.** Passer:
downfield, then his receiver for the last 30 frames before the release; defence: the ball; everyone off the line:
the ball in flight; OL, the offence's other players, the carrier after the catch: no turn. Clamp 75 deg; a target
more than 125 deg off the chest is not watched (the QB's play-action fake at 420-440 otherwise looked over his
shoulder; the endzone film has his face to his backfield). Pitch follows the ball when it is the target, else -8.
05k --export-joints writes "look" and "eye"; the viewer's first person reads them (fallback: the old rule; a jump
in time snaps instead of swinging). On v107: look vs torso p50 8 / p90 56 deg, over 90 on 0.3 % (old: 39 %).
Previews of what the camera shows ($S/pov_preview.py): the backpedalling safety sees the offence instead of an empty
field, the tackle sees his rusher instead of turf, the QB in the pocket sees downfield in both.

**The 05p bug found on the way (fixed, test_refit_mono_base).** An explicit --refit holding one-view records was
silently swapped for <play-dir>/poses_refit_fused.json: every chain today (ft2, ft3, ft4, the VPoser arms) merged
its new two-view records into the live cache (which carries "mono"), so 05p dropped them -- 0 of 4,834 fine-tuned
two-view records reached v106/v107 (their two-view keys hold the 09-09 fused records), and frames the old backup
did not cover were one-view-fitted from the sideline alone. Visible defect: the receiver 74 turned his back on the
ball at the catch in v106/v107 (heading 170 at 550/556; v105 -35, the endzone film square to the ball) -- the
sideline strips I judged v106 on cannot show a front/back flip. Now: base_cache() refuses such a --refit without
--fused-base; the play-dir backup is rewritten only for an in-place run. Every "fine-tuned fit" number today that went
through 05p (lkft2/3/4, the VPoser-in-fit arms) measured the one-view refit over the OLD two-view records.

**v108 = v107 + lkft2c** (05p on the ft2 two-view fit, merged onto the live keys): the receiver faces the ball
through the catch (-3 -> -44 deg, 538-570; film confirmed with pov_ruler), the sprinter's upright run kept (trunk lean
28-32 deg vs v107 36-42), knees 130.6. Copy rulers: steps 2 / hops 0 / census 0.169; jerk 3 (v107 2); VPoser p99 10.7
(= v107), over-8 0.027 (0.022), hinge share 0.002 (0.000: 05f's two-view fit has no hard hinges); jitter .062/.216
(.059/.211). Mixed and small on the rulers; the catch is decisive on film. Chain running; film next (both cameras).

## 2026-09-24 18:40 -- v109: the first-person spins were the bodies' (two pose-record rules), the eye, own arms

**What the POV still did wrong after the look model (08bc22a).** $S/pov_steady.py on v108: the look turned more than
20 deg per exported step (1/30 s) on 2.9 % of live steps, p99 32 deg; the worst were whole-body spins -- id 6 at
470-496 (+276 deg) and 568-598 (-345 deg), id 15 at 568-594, id 9 at 492-506. The film ($S/facing_strip.py: the
drawn torso arrow projected on both cameras' footage, --skel for the skeleton; $S/box_crops.py: the raw box zoomed)
says none of those spins happened. The look was right to follow the torso; the torso was wrong.

**Cause 1, stale refit records.** id 6's 12 refit records at 578-589 have no keypoints for him in either camera in
ANY version of the keypoint tables (sideline box 45x80 px, no pose detection in it; no endzone rows after 304):
a two-view fit from an old pairing, carried onto him by 08v. They face away from the sideline camera; the film has his
number and face toward it. $S/orphan_records.py: 27 % of the live window's refit records have no keypoints for their
id within +-1 frame, but nearly all sit on ids no longer drawn; on drawn bodies: id 6 578-589, id 17 438-440, id 204
600. Rule: timeline.drop_unkeyed_poses (a refit record needs a keypoint over 0.3 for its id within 1 frame in
keypoints_2d or keypoints_2d_ft2; regressor records stay).

**Cause 2, single records facing the wrong way.** The regressor agrees with the keypoint fit on front/back 96 % of
the time (84 % on boxes under 90 px; $S/regressor_frontback.py), and a one-view fit of a man seen side-on flips too
(id 9 at 494 and 504, both 05f records). One such record between agreeing neighbours makes the SLERP turn the man the
long way round. Rule: timeline.drop_flipped_keyframes (fewer than half of the records within 12 frames either side,
at least 3, face within 90 deg: dropped worst first, regressor before fit on a tie, re-counted after each drop).
Tests: a clean half turn and a 720 deg/s spin sampled every 2 frames lose nothing.

**Rejected before building: face where you run.** The drawn bodies running backward fast are, on the film, safeties
backpedalling (id 30, id 0, id 6 at 436-440) and linemen in pass sets (17, 204, 12) -- the torso right every time --
plus placement speed glitches (the QB at 548); only id 9 was wrong. A motion prior would have broken the correct
ones. MISTAKE on the way: $S/backward_by_speed.py and pov_jumps.py divided 60 fps frame gaps by 30 fps, so every
speed they printed is HALF the real one; no conclusion rests on them (the film decided each case), but do not quote
them.

**A/B on the live export** ($S/ab_flip.sh, knobs via with_flag at call time): A (both off) reproduces v108's joints
exactly. Both on: drawn torso steps over 20 deg 4.2 % -> 2.1 % (max 173 -> 70); the look as the viewer shows it p99
30 -> 19 deg per step, over 20 deg 2.1 % -> 0.6 %. Film, rules on better in every judged stretch: id 6 (476-494,
572-596), id 1 (482-494), id 28 (544-550), id 15 (494-510), id 9 (494-506; 482-490 still wrong in both: the fits
there face him right), id 139 = Thuney: the endzone film has his back to that camera, turned toward his rusher, arms
reaching for him; v108 drew him facing the other way with his arms raised. 07l unchanged (steps 2 / hops 0 / census
0.17), planted 13 -> 14 %. 09d worse and read on the film: jerk 3 -> 5 (id 84 at 594), R arm sideways 11.8 -> 13.4 %
(Thuney's pass-block arms, right on the film). Committed 5162ce2 (defaults on).

**The eye.** SMPL-X's own eye joints (23/24) sit 4.1-4.5 cm above and 6.5-6.8 cm ahead of the head joint over
statures 1.62-1.87 m; render.gaze had 8 / 9 cm (a guess), now 4.5 / 6.5. Eye height p50 1.58 -> 1.54 m.

**Own arms in first person** (dc2eb63, viewer Version 25): only the helmet, the neck bone and the upper chest are
hidden; the receiver sees his hands reach for the ball at 560, Thuney his arms on the rusher. $S/pov_preview2.py
previews it (hiding the neck alone left a 13 cm chest capsule filling the bottom of the view).

v109 = v108 + the two rules + the eye. Render chain launched 18:37 ($S/chain_v109.sh); film review next.
