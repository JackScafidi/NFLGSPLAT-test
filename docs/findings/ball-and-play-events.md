---
type: findings
topic: ball-and-play-events
period: 2026-09-17 to 2026-09-18
entries: 4
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Ball and play events

The snap, the release and the catch, the ball's path, and when the play is dead.

4 entries from 2026-09-17 to 2026-09-18, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Ball](../concepts/ball.md), [Play events](../concepts/play-events.md), [Hands](../concepts/hands.md), [Feet](../concepts/feet.md)

## 2026-09-17 (overnight): the clip ends when the play is dead; a gait for the legs

**Decisions taken by the user (04:00):** end the clip when the play is dead; build and test the gait
model; keep the loop running overnight, hypotheses -> tests -> footage.

**Play end (08x, commit feb29cd/b26fb91).** The share of moving bodies does not mark the death of the
play (scratch probe_play_end: 5-25 % of bodies move faster than 3 m/s DURING the play -- linemen
engaged, backs covering -- and 50-80 % after it, everyone jogging in). The ball carrier stopping does:
he is taken as the id that travels furthest from its snap position over the live window (play 1: id
9, 19.2 m), and the play is dead when he stops for 10 frames, his track ends, or the sideline last
sees him -- the 05q strip of 9 at 480-492 shows him wrapped and going down at 482-486 and on the turf
by 488, while the bridge kept a standing body on him to 493, so the last sighting caps it. 05k reads
<play-dir>/play_end.json and stops at end + a 30-frame tail; pipeline_play.sh runs 08x as a marked
stage before the rulers. Play 1: end 493 by the first rule, re-run with the last-sighting cap pending.

**Gait (render/gait.py, commit feb29cd; opt-in via 05k --gait / 05q --gait).** Where the pelvis
moves faster than 4.8 m/s the hip and knee rows of both legs are synthesised from a phase that
advances 2 pi per stride of travel along the body's forward axis (a backpedal cycles backwards):
stance with the foot planted by construction (the hip's forward reach runs linearly back over the
stance travel), a cosine swing with the knee to 1.3 rad, blended over 6 frames at the edges; the fit
keeps the torso and arms. First cut used the STEP length as the cycle (2.2 m at a sprint) and ran the
runner at 2.8 cycles/s, twice a sprinter's cadence -- the cycle is two steps, 4.6 m at 9 m/s, and the
ground share falls with speed (0.6 walking to 0.22 sprinting). Fixed before any footage. A/B on the
live play (skating ruler, sideline reprojection, jitter) running; render v51 = v50 + gait + the clip
end follows if it reads well.

Gait A/B, corrected stride (04:40, scratch probe_gait_ab; post-hoc on the live play): 18 ids get the
gait (the runner 148 frames / 3.8 cycles = 3 steps a second; 3, 6, 40, 74 ... for 15-30 frames each).
Skating ruler: slower ankle / pelvis p50 0.94 -> 0.88, planted 1 % -> 11 %. Sideline lower joints
9.9/16.2 -> 17.8/25.4 px (the legs no longer chase the noisy ankle keypoints; expected). Joint jitter
p90 0.062 -> 0.153 (a leg that really swings reverses hard at each end; the ruler was calibrated on
legs that did not). 11 % planted is short of a runner's ~50 %: diagnosing on the runner whether the
plant fails where the body moves across its fitted facing (43 deg median off the velocity on this
play) -- then the legs should swing along the velocity. v51 (gait as is + the clip ending at 523)
is rendering for the footage verdict regardless: a leg cycle that looks like running beats a ruler.

Play end, capped at the carrier's last confident keypoints (05:00): the box tracker outlives the
detector's pose (boxes on 9 to 493, keypoints to 483), so play_end.json now says end 483, clip to 513.
v51 went out under the earlier 523; the next render uses 513.

Plant diagnosis on the runner (scratch probe_gait_plant, 137 moving frames): where the fitted facing
is within 20 deg of the velocity (75 frames) the gait plants 24 % (ratio p50 0.75; the stance dips to
0.08-0.27 every ~15 frames, a 2-cycles-a-second sprint with 0.1-s stances -- physically right; the
< 0.3 criterion misses the stance edges, ~40 % is the ceiling at a sprinter's duty); where the facing
sits 45-90 deg off the velocity (53 frames, 39 % of his run) it plants 0 % -- the legs swung along
the fitted facing, sideways to the motion. The fitted yaw is the unreliable part (43 deg off the
velocity at the median on this play). Fix: the legs' plane turns onto the direction of motion
(`gait.leg_yaw`: a yaw about the pelvis's up axis composed with the hip flexion; a backpedal keeps the
plane and cycles backwards). Re-measuring.

Re-measured with the legs in the plane of the motion (05:20, commit 9f374ab): all moving bodies --
slower ankle / pelvis p50 0.94 -> 0.74, planted 1 % -> 21 %; sideline lower joints 9.9/16.2 ->
15.3/21.6 px (the facing-plane version cost 17.8/25.4: legs that swing where the man goes also sit
nearer his keypoints); joint jitter p90 0.062 -> 0.208 (the ruler now counts real swing reversals;
compare gait renders among themselves on it). The runner: planted 13 -> 27 %, and the stretch where
his fitted facing sat 45-90 deg off his velocity goes 0 -> 26 %. A sprinter's duty caps the
criterion near 40 %. v51 = the facing-plane gait (clip to 523), v52 = this one (clip to 513),
chained; the strips of the runner (326, 400, 470), 40, 0, 2, 6 and 38 decide.

**v51 delivered (15:36; the machine was off from ~05:30 to ~15:00 and the chain resumed): diag/
play_001_v51_hifi_720.mp4 = v50 + the facing-plane gait + the clip ending at 523 (255 rendered
frames, 69 after the play left out); legs synthesised on 2236 body-frames of 65 ids.** Strips: the
runner at 326-340 -- a stride cycle, one leg forward while the other drives back, the knee lifting in
swing, feet flat; at 400-414 the same with a forward lean; at 470-484 running into the tackle, then
wrapped. Id 40 (a Baltimore back) at 378-392 -- alternating legs with a high knee. At strip scale
the legs read as running, not gliding; the video is the user's to judge. v52 (legs along the motion,
clip to 513) is rendering; 07l gains --gait so the report scores what 05k --gait draws.

**07l v57 = v56's timeline with the gait applied (the v52 render's legs).** Skating p50 0.94 -> 0.75,
planted 1 -> 21 % of 244 moving frames; joints jitter p50/p90/p99 0.0106/0.0329/0.069 ->
0.0112/0.0501/0.263 and speed p90 0.085 -> 0.110 (legs that swing and reverse; from here the joint
rulers compare gait renders with gait renders); steps 5, hops 4, root jitter, census 1.19 unchanged
(the gait moves no pelvis).

Gait over the footage (05q --gait, scratch review_gait): the runner at 340-354 -- the synthesised
legs stride while the green keypoints sit within 10-20 px of them; running toward the camera the
swing leg projects as a sideways kick at mid-swing. Id 40 at 380-394 -- the legs stride hard (a
sprinter's 39 deg reach at 0.24 m/frame) on a body that stands the known metre off the man (the
endzone-only placement of 385-394), so the legs look right and the placement wrong. The gait is the
pipeline default from here (pipeline_play.sh: GAIT=0 draws the fitted legs; both 05k and 07l take
it), reversible with one variable.

Gait on the jogging band, measured and DENIED (16:05, scratch probe_gait_jog; RUN_M 0.08 -> 0.05 so
bodies at 3-5 m/s get the gait too): on those 545 live body-frames the fitted legs already plant 9 %
(the detector's legs are usable at a jog) and sit 8.5/14.6 px on the sideline keypoints; the gait
takes planted to 29 % but the legs to 21.4/37.3 px -- a synthesised walk over legs the footage
shows is a loss. RUN_M stays 0.08: the gait replaces legs only where the keypoints cannot carry
them (a sprint). Ankle rows level the stance foot from commit 2b9058b (v53 chained behind v52).

**v52 delivered (16:15): diag/play_001_v52_hifi_720.mp4 = v50 + the gait with the legs along the
motion + the clip ending at 513 (250 rendered frames, 8.3 s; 74 rendered frames after the play left
out).** Strips: the runner at 326-340 strides (334-340 one leg driving back while the other knee
comes up), id 40 at 378-392 strides with a sprinter's trailing leg at 390-392. The clip itself, tiled
every fourth frame from the pile break to the tackle: bodies run, the scene holds, the clip ends
with the pile forming. v53 (+ the levelled stance foot) is rendering. Next check: whether the fast
jog band (4.8-6 m/s) is better served by the fitted legs, which would move RUN_M to 0.1.

Fast-jog band alone (0.08-0.1 m/frame, 96 live frames, 16:40): the fitted legs skate there as at a
sprint (planted 1 %, ratio 0.89) and sit 7.5/15.8 px; the gait plants 17 % at 10.9/21.3 px. Against
the slower band (0.05-0.08: fitted legs plant 9 %, the gait costs 13 px), 0.08 is where the
keypoints stop carrying a stance and the gait starts paying for itself. RUN_M stays 0.08; the
threshold is measured on both sides now.

Arm swing on running bodies (16:50, scratch probe_arm_swing; frames where the gait is on): the
fitted wrists travel 0.4-0.6 m fore-aft per leg cycle (runner 9: 0.41 / 0.57 m, upper-arm flexion
range 16 deg; 6: 0.41 / 0.50; 19: 0.33 / 0.57 at 52 deg) against a sprinter's 0.8-1.0 m and 70-90
deg -- the arms pump at about half amplitude. Not the moonwalk: the fitted arms are on their
keypoints, and replacing them with an animation would trade footage for a guess, the same trade the
jog band lost. Recorded; a lighter temporal weight on the arms of sprinting ids is the fit-side
hypothesis if the video wants more pump.

**v53 delivered (16:49): diag/play_001_v53_hifi_720.mp4 = v52 + the stance foot levelled (250
frames, clip to 513).** The runner at 326-340: the stride with the stance boot flat on the turf; id
6 (a Baltimore back at 340-354, under 4.8 m/s so the fit's legs): a coverage shuffle, bent knees,
natural. v53 is the current best; v50 is the last fitted-legs render for a side-by-side.

Side by side for the video verdict: diag/play_001_v50_vs_v53_run.mp4 (the run, rendered frames
150-250 = timeline 300-500, v50's fitted legs left, v53's gait right, 960x540 each). The standing
directive of 2026-09-05 (play 1 only, no compute on other plays) stands until the user lifts it;
the next play was considered at 17:00 and not started.

## 2026-09-17 (evening): the snap was never at 300 -- RETRACTION of the live window and the clip end

**The footage, not a ruler, found it (17:20).** Full-frame overlays of both cameras (05q --frames 305
320 340 360 380 400 --cam both, diag/census_v53/) show play 1's formation still SET at sideline
frames 360 and 380 -- linemen crouched, the QB under centre -- and the line firing at 400. The snap is
~393-396, not the 300 that identity.roles.snap_frame wrote into identity_resolved.pkl and that
LIVE_LO, 08x, 07l and every "live window 300-460/483" number in this file inherited. Bodies moving
faster than 0.03 m/frame (1.8 m/s) per frame from the v53 timeline: at most 6 of 22 before 388 (the
man in motion, id 9, from 284; a shifting defence; two gliding fragments), 9-11 at 392-404, 18 of 24
at 416. The snap detector's 0.5 m/s "static" cut sits below the placement's own jitter, so "fewer
than 40 % static for 12 frames" fired 95 frames early.

**What that retracts.** (1) Every "live" ruler since 2026-09-13 ran on a window that was two-thirds
pre-snap: the census 1.19 "live", hops "live 4-5", the KC-at-the-snap deficit (300-344 = KC 9 drawn,
ids 37/38 arrive at 340/345 -- that IS pre-snap, the formation standing 50 frames before the ball
moves; two linemen missing from a set line for 0.8 s). The fixes judged on that window were also
judged on the footage strips, so they stand; their aggregate numbers do not mean what they said.
(2) The play is a PASS: the QB is in the pocket at 480 (endzone 465), the ball is downfield at 520,
the tackle is at ~640 by the 15-yard line, the source clip ends at 647. 08x's "ball carrier =
furthest traveller from his frame-300 position" picked the motion man (19 m, mostly pre-snap) and
"last seen" ended the play at 483 when he ran out of the sideline frame: **v51, v52 and v53 stop at
513, two seconds after the real snap, in the middle of the play.** The 16:49 "v53 delivered (clip to
513)" is withdrawn as a clip; the gait/unwrap/twin content of those renders is unaffected.

**The crowd is the ruler now (scripts/08x_play_end.py, rewritten).** snap = the frame from which at
least 0.4 of the drawn bodies (12+ drawn) move faster than 0.03 m/frame for 6 frames, less 4 (the
line fires a few frames after the ball moves); dead = that share under 0.4 for 30 frames from snap+60,
else the clip's end (NFL Pro cuts the All-22 at the whistle: the share never falls below 0.57 to the
last frame here). Play 1: snap 393, dead 660 (clip end), clip from 213 (START_BEFORE 180 = 3 s of
formation and motion). --carrier ID keeps the old stop rule for a named id; --end/--snap override.
07l's --lo/--hi now default to play_end.json's snap/end; 05k honours a "start". tests/test_play_end.py
(5). identity.roles.snap_frame is left as is (08n's pre-snap window [snap-130, snap-30] lands on
the same set formation either way on play 1) -- but it is wrong and must not be trusted on another
play; the 08x detector is the one to reuse. Memory: snap-frame-check-on-footage.md.

**Ghosts from the endzone lead-in, confirmed on the footage (17:05-17:40).** The census surplus on
Baltimore (11.53 on 300-483) is not kit-vs-label (only 37 of 5689 confident live detections
disagree with their id's team, all on endzone-only ids 91/42 that are never drawn). It is (a) the
30-frame reach before/after an id's sideline span, drawn from the endzone alone: id 198 at 453-482
stands on EMPTY TURF beside the tackle 2.4 m from its man (diag/census_v53/player_198_f453.jpg), id
40 at 368-396 a phantom defender 1-2.7 m beside the real one; the smoother turns the 2.4-2.7 m jump
at the join into a glide, so the hop ruler (3-frame excess) never saw it; and (b) fragments on men
already drawn under another id in the pile (194/40 at 0.20-0.25 m, 168/15, 84/13; 37/166 41 frames,
19/166, 19/37 in the KC line) -- real men, doubled, below the twin rule's 0.2 m / 8 frames; no radius
separates them from engaged linemen (thread open, the 09-13 finding stands). Held real men: 37 and
38 drawn 30 frames before their sideline spans join within 0.27-0.55 m and stand on their men.

**Rule (render/endzone_only_rule.py `hold_m`, HOLD_M).** For each side of a two-view id's sideline
span, the jump between the endzone's point at the frame adjacent to the span and the sideline's
own first (last) point for the man; over ``hold_m`` the whole side is dropped. First cut compared
every beyond frame to the join point and read a man's own running over a long lead-in as drift
(74: median 1.29 m over 314 frames, mostly his 125-390 pre-snap stretch) -- replaced by the join jump
before shipping. A/B on 300-483 with the per-frame cut, hold off -> 0.8 m: KC 10.82 -> 10.79, BAL
11.53 -> 11.21, frames at exactly 11/11 50 -> 69, frames with BAL >= 12 75 -> 33, pile pairs 9 -> 9,
live hops 5 -> 6 (74 at 418, 0.225 m: its lead-in now ends where the sideline starts). Join-jump A/B
below.

**Join-jump A/B (18:05), hold off -> 0.8 m on 300-483:** KC 10.82 -> 10.73, BAL 11.53 -> 11.36, exactly
11/11 50 -> 56 frames, BAL >= 12 75 -> 62, live hops 5 -> 4 (74's 0.228 m at 419 gone), pile pairs
9 -> 9. Dropped whole-play: 198 (jump 1.55 m, 43 frames, the ghost on the turf), 40 (1.55, 27: the
phantom defender's lead-in), 74 (1.14, 270: its pre-snap endzone stretch -- in the live window only
the 16 frames 366-369/409-420 that flickered between two old-rule drops, so KC -0.09 and one pop
fewer), 164 (1.22, 80), 170 (4.34, 58), 186/212/206. Held: 37 (0.31), 38 (0.50), 17 (0.41), 27, 30,
171. The per-frame cut dropped more (BAL 11.21, exact 69) by also dropping men for their own running;
the join jump is the honest version and ships: **HOLD_M = 0.8** (render/endzone_only_rule.py).

**v54 delivered (19:20): diag/play_001_v54_hifi_720.mp4 = v53 + the join-jump hold + the real snap
and the whole play (timeline 213-660 at stride 2, 224 frames, 7.5 s at 29.97).** The run sheet
(scratchpad/review_v54/run_sheet.png, 380-640) shows the line firing at 400, the pocket at 440-520,
the routes at 540-600 and a white body down on the turf at 640. Strips: 198 ABSENT at 452-480 (the
ghost on the turf is gone); the tackler 184 renders prone with arms forward at 640-652 and then
stands up at 654-658 while the footage still has him down; 55 dives plausibly at 604-638.

**The join-jump hold misses a GLIDING ghost (19:50).** Id 40's lead-in 368-397 is still drawn: its
lead-in joins the sideline within 0.67 m (kept), the 1.55 m jump the report showed was its TAIL
(527-553, dropped 27). The footage strip has 40 standing 1-1.5 m beside the real defender at
368-383 and on him at 398: the endzone's placement slides 2.7 m onto the man over the 30 frames,
and the join test only sees the last step. The per-frame test caught it and misread running men;
the join test passes it. What separates them is not metres at all: a real man is always under
SOME sideline detection box (even a merged one, as 37/38 were), empty turf never is -- the test
belongs in the sideline image (project the endzone point, ask whether a sideline box covers it).
Measured next.

**Bodies on the ground -- measured and NOT adopted (20:10).** Hypothesis: the tackled men are drawn
standing because the fit's tilt prior (weight 10 past 20 deg) forbids lying, so gate it by the box
(sideline h/w under 0.7: linemen's p5 is 0.87, the tackled men 0.46-0.58; 0.9 also caught crouched
linemen 4 and 17 pre-snap on 110 frames each). Built: Mono2DConfig.lying (the lean must be at least
60 deg), 05p --lying-aspect, timeline.lying_frames + build_timeline(lying=) skipping the tilt clamp,
tests/test_lying.py. Probe on ids 184/28/55 (55 has no fit at all: no keypoints pass the filter).
Same-recipe control vs lying prior, world tilt through the timeline, id 184 at 642-660: control
20-36 deg, lying 142/140/115/80/52/46/56 -- past horizontal, the pelvis inverted; the fit's own
upper-body reprojection 16.7 -> 21.2 px, lower unchanged; the footage strips (diag/lying_v54/) look
the same for both: a folded body along the man at 642-651, standing up at 654-657 while he is still
down. The shipped fit ALREADY renders the tackler prone (v54 strip 184 at 640-652) from a folded spine
at 24 deg of pelvis lean: the 24 deg I first read as "standing" was the pelvis, not the body. What
remains wrong is 654-660 (he rises early) in both. The prior ships opt-in (05p default 0); the
timeline's no-clamp on lying frames stays (it never fires on the shipped fits; a gate, not a change).
Also: a first per-frame tilt reading taken on the raw records (24 vs 102 deg) was in the cache's
frame, not the world's -- measure through the timeline's states.

**Box containment is not the ghost test either (20:00).** Endzone-placed lead-in frames projected
into the sideline image, "inside any sideline box dilated a quarter body sideways": 198 0.72 (it
stood beside KC 65 on empty turf: the neighbour's box covers it), 40 0.18, real men 37/38/17 1.00,
74 0.96, 164 0.94, 170 0.47. Nearest box bottom in body heights: ghosts 0.57-0.60, real 0.26-0.48
-- the same 1 m ambiguity as the metres. What does separate 40 is TIME: before the snap a set man
does not move, so a lead-in that stands 2.7 m from where the sideline finds him and slides in is
the endzone's error. Rule: before play_end.json's snap every beyond frame is measured against the
join point (per frame); from the snap on, the join jump. Test added; A/B below.

**Snap-aware hold A/B (20:45), 300-483, hold 0.8 m.** Join-jump only (v54): KC 10.73 / BAL 11.36,
exactly 11/11 on 56 frames, BAL >= 12 on 62, id 40 drawn on 30 of 360-397. Per frame before the
snap + join jump after: KC 10.73 / BAL 11.21 (pre-snap 10.32 / 11.00, live 11.14 / 11.42), exactly
11/11 on 69, BAL >= 12 on 33, id 40 on 1 of 360-397, live hops 4, pile pairs 9. KC pre-snap loses
half a man (74 and 164, real linemen whose endzone depth sat 1.1-1.3 m off their sideline join).
Tried "hold": keep those pre-snap frames AT the sideline's join point instead of dropping them (a
set man has not moved). Rejected: KC pre-snap 10.32 -> 10.39 only, BAL 11.00 -> 11.19, exactly
11/11 69 -> 54, and a new pile pair 1-40 (22 frames): 40's held lead-in lands on the man already
drawn as id 1 -- the lead-in was a second copy, and dropping it was right. PRESNAP = "drop" ships
(endzone_only_rule.PRESNAP; "hold" kept as the measured alternative). v55 launched 20:50 with it.

**The double body on KC 76 (37 + 166, 41 frames within 0.6 m) is a DEPTH error, not two boxes
(21:15).** Every pile id draws within 3-18 px of its OWN sideline hip keypoints (166 13 px, 37 3 px,
19 18, 204 9, 17 11, 1 7): both bodies sit on their detections in the sideline image, and those
detections are 88 px apart -- adjacent linemen stacked along the sideline's depth axis (field y).
The zoomed two-camera crop at 380 (diag/census_v53/line_zoom_380_400.jpg) shows it: in the
sideline 11, 166, 37 are three men in a row; in the endzone 37 is on 76 with keypoints and 166's
skeleton stands a metre beside 76 on turf with nobody under it. 166 is sideline-only there (its
endzone pairing is 472-562), so its y is the sideline's own foot-point depth, off by ~0.5 m in the
line cluster, which puts it inside 37's 0.6 m. Sideline box IoU (0.36) and keypoint distance (88 px)
cannot call it a duplicate because it is not one: it is a man drawn half a metre into his
neighbour. The fix is depth for one-view bodies in the line (an unpaired endzone id for the same
man is among the 68 endzone-only ids left out), i.e. the pairing thread of 09-08/09-10, not a
twin rule. Left open.

**The real baseline (21:30): 07l on the live window 393-660 (play_001_v55_plausibility.json,
the v54/v55 timeline).** steps > 0.25 m/frame live 114 (handovers 7), > 0.6 none; hops live 25 (the
old window said 4-5); skating: planted 13 % of 1207 moving body-frames (a runner plants ~50 %);
census live 2.55 (KC 11.04, BAL 11.49); joints (57 ids) jitter p50 0.026, p90 0.156, p99 0.58.
Every "floor" claimed on 300-460/483 was two-thirds pre-snap; the play itself has 25 hops and a
p99 joint jitter of 0.58 m/frame^2. This is the number to beat from here. 07l's window now comes
from play_end.json (a str/Path slip fixed 21:25).

**Hole hold (22:05): endzone-filled holes inside a sideline span follow the sideline's own line.**
The span rule holds a span's edges; inside a span the hole rule (HOLE_REACH 8) draws endzone-placed
frames, and the endzone's ground point is poor along the field: id 37 at 569-576 stepped 0.42-0.44 m
a frame for five frames -- the footage strip (diag/live_v55/player_37_f558.jpg) has him drawn on the
lineman two metres LEFT of the man the sideline resumes on at 573, who stood there throughout.
Rule (endzone_only_rule.hold_holes, HOLE_HOLD_M 0.8): a hole frame farther than 0.8 m from the
sideline's line between the hole's ends (holes up to 17 frames) or from the nearer end's point
carried at the sideline's own velocity over 4 frames (longer holes, the frames within reach 8 of an
end) takes that line. Live window 393-660: 110 frames held (median 1.31 m off, max 3.69); hops 25
-> 23, steps > 0.25 m/frame 114 -> 97, handovers 7 -> 4, KC 11.04 -> 11.10, BAL 11.49 -> 11.38; 37's
run of 0.4 m steps -> 0.03 (one 0.47/0.48 pair remains where the two ends' extrapolations meet
mid-hole). Shipped; v56 carries it.

**v55 delivered (22:35): diag/play_001_v55_hifi_720.mp4 = v54 + the snap-aware hold (id 40's pre-snap
phantom gone; 74's off-line pre-snap stretch gone).** Sheets over the live play at 6-frame steps
(scratchpad/review_v55/sheet_a.png 393-525, sheet_b.png 531-660): the line fires, the pocket holds
to ~520, routes to 600, the tackle at 639-657 with the tackler prone. Nothing standing alone on the
turf. A small black-clad figure deep at the top of 615-633 (an official or a teamless body) to check.

**Gait threshold re-tested on the real window, DENIED again (22:30, scratch probe_gait_runm).** RUN_M
0.08 (shipped): gait on 2135 body-frames, planted 14.2 %, ratio p50 0.79; 0.06: 3205, 18.5 %, 0.76;
0.05: 3860, 18.2 %, 0.78. Four points of planting for a thousand body-frames of synthetic legs on
bodies whose keypoints carry a jog (the 16:05 reprojection cost, 13 px, is unchanged by the window).
RUN_M stays 0.08.

**Next: the sideline's own double tracks.** Same-team id pairs whose SIDELINE boxes coincide (IoU
>= 0.6) on 8+ live frames -- one man, two tracker ids; the memory's "never by boxes" was about
engaged linemen at IoU ~0.4, these are 0.85-0.97 at the p90: 40-198 (27 frames 483-522: the
ghost's sideline track sits on 40's man), 61-64 (BAL, 27, p90 0.95), 197-186 (KC, 14, 0.96), 194-40
(13, 0.93), 12-170 (9, 0.87), 46-56 (9, 0.97), 194-198 (8, 0.85), 211-205 (14, 0.69). Footage strips
of 61/64 and 197/186 next, then a box-twin rule A/B on the live census.

**Box twins, measured and left opt-in (23:00).** timeline.box_twin_frames (same-team drawn ids whose
sideline boxes overlap IoU >= 0.6 on 8+ consecutive frames; the id with fewer sideline boxes loses
them), load_play_timeline(box_twin_iou=). Of the strong pairs, 61/64 and 46/56 are bench people at
the boundary (never drawn: diag/boxtwins/player_61_f578.jpg), so the rule reached 74 body-frames
whole play: 27 at 129-150, 195 at 181-205, 170 at 598-605, 198 at 489-509 (the ghost's sideline
track on 40's man). Live window 393-660: KC 11.10 -> 11.07, BAL 11.38 -> 11.31, exactly 11/11 34 ->
35, BAL >= 12 115 -> 109, pile pairs 18 -> 16 (289 -> 261 frames), hops 23 -> 25, steps > 0.25
97 -> 94. Real duplicates, a handful of frames, and two hops bought by the gaps it leaves.
BOX_TWIN_IOU = None (off); test in tests/test_timeline.py.

**An official drawn as a Baltimore player (23:20).** The small black figure at the top of v55's
615-633 is id 70: on the boundary line at the LOS for its whole 28-frame life (|y| 23.5-24.4,
x -25..-24, 611-638, kit margin -0.31, no jersey, no role), drawn 20 yards behind the play in its
fitted black-and-white appearance. The dweller rule's line was 23.5 m and 70 straddles it.
SIDELINE_M -> 23.0 (offfield_rule): among every id the v53 timeline draws, 70 is the only one with
half its frames beyond 23.0 (every roster-named player stays under 6 m median, none past 23.5).

**Despike (23:30): a median of the +-2 neighbours BEFORE the position Gaussian.** The hops the
rulers count on the live window are single-frame spikes the Gaussian spreads into a hop; a
median sees a spike as the odd one out and a real cut (every later frame moves the same way) as the
trend. timeline.despike_xy (excess DESPIKE_M, symmetric window only, holes left alone), applied in
build_timeline before smooth_xy; knob despike_m on load_play_timeline. Live window 393-660: hops 23
-> 2 (0.15) / 2 (0.25), steps > 0.25 m/frame 97 -> 63 / 65, handovers 4 -> 0, root jitter p90
0.050 -> 0.032 / 0.035; the two left: 79 at 544 (0.36 m) and 194 at 503. Second ruler (the bodies'
hips against their own sideline keypoints, off vs 0.15) below.
Second ruler (23:40): 3024 drawn body-frames with hip keypoints on 393-660, hips vs own keypoints:
off p50 7.3 / p90 16.0 / p99 40.0 px, 70 over 30 px; despike 0.15: 7.3 / 16.2 / 40.3, 68 over 30.
The spikes go and the bodies stay on their keypoints. **DESPIKE_M = 0.15 ships**; v57 carries it
with the dweller line.

**v56 delivered (23:50): diag/play_001_v56_hifi_720.mp4 = v55 + the hole hold.** Sheets as v55. But
id 37's strip (scratchpad/review_v56/strips/render_37_f558.png) flickers: absent 558, drawn 562-568,
absent 570, drawn from 574. Per frame in the current timeline: absent 545-559, drawn 560-568 on
endzone-only views with steps 0.30-0.46 m/frame, absent 569-573, sideline from 574. The hole is 29
frames; the hold moved the frames within reach 8 of the end (566-573) onto the sideline's line and
left 560-565 at the endzone's spot two metres away, so the glide moved rather than went, and the
held frames near the join were then deduped against the man's other id. Fix: in a long hole the
frames beyond reach of BOTH ends are left out (they were the endzone's blind depth with nothing to
hold to). v57 (launched 23:45, despike + dweller line) predates this; v58 carries it.
Measured (00:05, with the despike in): 110 held + 28 left out; live window hops 2, steps > 0.25
m/frame 63 -> 55, handovers 0, KC 11.10 -> 10.98 (the 28 blind frames), BAL 11.31; id 37 absent
until the sideline resumes at 574 and steady after (0.03 m/frame): no glide, no flicker. Ships;
v58 carries it after v57.

**Where the live joint jitter is (00:20).** 07l's "jitter p99 0.58" on 393-660 was measured WITH
the gait: the synthetic legs swing, and that swing is most of the p99 (the 09-16 note already had
0.263 for gait swings). Without the gait, the worst ids by 07l read: 212 p90 0.008, 206 0.000 (nothing
there), 185 0.10, 184 0.43 (the diving tackler at 655-658, interpolated between sparse records),
79 and 5 0.2 at 536-541 (a throw-side arm, real), and 66 0.84 at 581-582 -- a DEFAULT-POSED body
(no fit at all; 66 at 576-607 and 194 at 467-509 are the two on the play) whose heading comes from
its motion and started at the fallback 0 deg until the motion gate opened, then turned 104 deg in
one frame. Across the worst ids the jitter does not sit at view switches (p90 0.032 there vs 0.080
elsewhere) nor differ between record and interpolated frames (0.072 vs 0.081).
Fix: timeline.yaw_from_motion backfills the frames before the first known heading with it and
smooths the heading circularly over 5 frames (YAW_SMOOTH). Test added. Numbers below.
Measured (00:30): id 66 jitter max 0.84 -> 0.08, p90 0.21 -> 0.07; 194 unchanged (0.01). Ships;
v58 (queued behind v57) carries the long-hole fix and this.

**Box twins re-measured with the despike in, and SHIPPED (00:45).** Same rule, same pairs, live
window 393-660: KC 10.98 -> 10.95, BAL 11.31 -> 11.21, exactly 11/11 37 -> 41, BAL >= 12 109 -> 100,
pile pairs 18 -> 16 (285 -> 251 frames), hops 2 -> 2, steps > 0.25 55 -> 53; 82 body-frames left out
whole play (194 490-497 and 198 489-509 on 40's man, 170 598-605, 27 and 195 pre-clip). The two
hops it cost at 23:00 were spikes the despike now removes. BOX_TWIN_IOU = 0.6.

**v57 delivered (01:05): diag/play_001_v57_hifi_720.mp4 = v56 + the despike + the dweller line.** Id 70
(the official) absent on 611-638 (strip); 76 stays with the pile at 628-646 instead of sliding off
it; sheets as v56 otherwise. v58 (long-hole middles out, heading backfill, box twins) rendering.

**Bodies on the ground flail between sparse records: a wider pose Gaussian on lying frames (01:30).**
The one real flail left on the play was the diving tackler 184 at 655-658 (joint acceleration p90
0.43 m/frame^2, records on 7 of 19 frames). timeline.build_timeline: frames the box calls lying
(lying_frames, aspect 0.7) take the pose Gaussian at LYING_SIGMA_MULT x sigma, blended in over
LYING_BLEND 3 frames either side of a lying run. Without the blend, swapping the values on the
lying frames alone made a seam: id 1's isolated lying frames went p90 0.08 -> 0.55. With it, on
393-660 (55 lying body-frames, ids 1/28/34/35/36/55/82/184/206): lying p90 0.189 -> 0.079 (x3) /
0.031 (x5); 184 0.42 -> 0.09 / 0.03; 28 0.19 -> 0.02 / 0.04; 1 0.08 -> 0.15 / 0.19; all-frames p99
0.105 -> 0.098. LYING_SIGMA_MULT = 3.0 ships (the seam cost on 1 is the reason not 5). Footage strip
of 184 with it: diag/lying_smooth/player_184_f646.jpg.
The tackler's footage strip with the smoothing (01:40, diag/lying_smooth/player_184_f646.jpg): the
skeleton lies along the man from 646 to 660 -- he no longer rises at 654-658. v59 (queued behind
v58) carries it.

**Pre-snap per-frame hold only when the join is at the snap (01:55).** A join deep in the play is
where a man who has since run stands, and says nothing about where he stood set: 74 (join at
snap+28, 1.14 m off) and 164 were real linemen dropped for the whole pre-snap. PRESNAP_JOIN_MAX 10:
the per-frame test applies when the join is within 10 frames of the snap (40's phantom joins at
snap+5 and stays caught: 1 frame on 360-397), otherwise only the same-body test stands. Measured
on 300-483: KC pre-snap 10.32 -> 10.37, exactly 11/11 69 -> 68, BAL >= 12 33 -> 35, pile pairs 9,
hops 2 (0 live). A wash in numbers -- 74's pre-snap frames were mostly the OLD rule's (a sideline
body within 1.2 m in the line) -- kept because it is the right question to ask. Tests updated.

**v58 delivered (02:20): diag/play_001_v58_hifi_720.mp4 = v57 + long-hole middles out + heading
backfill + box twins.** Id 37's strip: absent 558-570, present from 574, no flicker, no glide
(scratchpad/review_v58/strips/render_37_f558.png); sheets as v57. v59 (lying-frame smoothing,
pre-snap join window) next.

**The evening against the 21:30 baseline (02:45), 07l on 393-660 with the gait, v59's timeline
(play_001_v59_plausibility.json):** steps > 0.25 m/frame 114 -> 53, hops 25 -> 2, handovers 7 -> 0,
skating planted 13 -> 17 %, census 2.55 -> 2.13 (KC 11.04 -> 10.95, BAL 11.49 -> 11.21), joints
jitter p50 0.026 -> 0.023, p90 0.156 -> 0.136, p99 0.58 -> 0.39 (the p99 is the gait's leg swing).
What did it: the despike (hops), the span/hole holds (steps, handovers), box twins and the dweller
line (census), the lying-frame smoothing and the heading backfill (jitter). What is left on the
play: two hops (79 at 544, 194 at 503), BAL +0.2 from fragments (201/177/75, strips in
diag/fragments_v59/), KC -0.05, the pile depth of 37/166.

**Short fragments with an unreadable kit wear a guessed team (03:10).** Footage strips
(diag/fragments_v59/): 201 (26 frames, kit margin -0.05, no jersey, no role) is a white skeleton
standing on Kansas City linemen's legs; 177 (36 frames, -0.10) the same on the lineman beside the
Baltimore rusher; 75 (49 frames, -0.30) is a real man. Rule (timeline.unreadable_kit_ids, WEAK_KIT_MARGIN
0.2, at most RIDER_MAX_FRAMES 40 frames, and identity gave the id neither a jersey nor a role): left
out. Live window: drops 23, 67, 158, 177, 201 (106 body-frames); KC 10.95 -> 10.86, BAL 11.21 ->
10.98, exactly 11/11 41 -> 49, BAL >= 12 100 -> 60, pile pairs 16 -> 15, hops 2, steps 53. Ships;
v60 carries it (v59 had loaded its timeline).
75's strip (03:15, diag/fragments_v59/player_75_f528.jpg) is NOT a real man after all: a white
skeleton on a red Kansas City player for 528-584, kit margin -0.30 -- under the kit module's own
carry bar (KIT_MARGIN 0.4, |margin| below it = unknown) but over this rule's 0.2, and 49 frames
against the 40-frame limit. Measuring 0.4 and 60 next, with strips of the ids they would add
(186 KC 47 frames -0.07; 66 KC 32 frames 0.23, the default-posed runner).
Measured (03:35): 0.2/40 (shipped) KC 10.86 / BAL 10.98, exactly 11/11 49; 0.4/40 drops 8, 66, 71,
185 as well (213 body-frames): KC 10.60, exactly 49 -> 44, and 66's strip shows a real red man under
the skeleton; 0.4/60 adds 75: BAL 10.79, exactly 45. The kit module's bar is too greedy here:
0.2/40 stays, 75 remains a known wrong-team fragment (49 frames).

**The 53 steps over 0.25 m/frame left on the play are real men sliding, not switches (03:55).**
Worst: 185 at 650-657 (0.33-0.40 for eight frames) is a Kansas City receiver sprinting along the
sideline with the skeleton on him throughout (diag/steps_v59/player_185_f639.jpg) -- his placement
slides three metres while he runs; 79 at 543-544 is the scrambling quarterback with a two-frame
jump. A rule for runs of impossible steps (timeline.impossible_runs, 0.2 m/frame for 4+ frames,
drop the frames) measured: steps 53 -> 3 and hops 2 -> 1, but 97 body-frames of ten ids go (5, 28,
38, 71, 78, 79, 157, 180, 185, 212), KC 10.86 -> 10.66, BAL 10.98 -> 10.82, exactly 11/11 49 -> 47:
it empties real bodies at the end of the play, where the camera pans and the depth is worst.
IMPOSSIBLE_M = None (opt-in). The slides themselves are a placement-depth problem for a later day.

**v59 delivered (04:10): diag/play_001_v59_hifi_720.mp4 = v58 + the lying-frame smoothing + the pre-snap
join window.** The tackler 184 stays prone 640-660 (scratchpad/review_v59/strips/render_184_f640.png),
the second Baltimore man 28 arrives lying at 654; sheets as v58. v60 (unreadable-kit fragments out)
next.

**Before the snap Kansas City has nine or ten men, and the quarterback is one of the missing (04:40).**
Census on 213-383 (the clip's first three seconds): KC 9.64 / BAL 11.00, exactly 11/11 on 32 of 171
frames, KC <= 10 on 132. The zoomed both-camera overlay at 260 (diag/presnap_v60/formation_260_zoom.jpg)
shows Mahomes (15) behind the centre with endzone keypoints and no body: the sideline camera sees
him on five frames (id 33, role QB, 281-288) behind the line, and his endzone-only ids are dropped
as ghosts because the spot is inside the sideline image. The line itself is drawn by fragments
that come and go (19, 31, 82, 166; 82 drawn 300-307) while every man stands still.
Rule tried: formation_hold (endzone_only_rule) -- a man whose pre-snap sideline points stay within
still_m of their median is drawn there from the clip start to snap-10 wherever the sideline missed
him. First cut (0.3 m): KC 9.64 -> 10.04 (33 held 166 frames: the QB), but BAL 11.00 -> 12.05 --
fragment 32, a rider on another man, held for 152 frames became a long duplicate the rider rule
no longer sees. Keeping the endzone-only ids on top added nothing (10.08 / 12.24, pops 14 -> 28).
Second cut: only an EMPTY spot is filled (no sideline body within 0.8 m that frame). Numbers below.
Measured (04:50): empty-spot hold at 0.3 / 0.5 m: KC 9.64 -> 9.64 (the QB's spot is 0.7 m behind the
centre, never "empty"), BAL 11.00 -> 11.79 (32, 34, 36, 171 still extended: fragments a metre from
the men they double), exactly 11/11 32 -> 0. REJECTED both ways; FORMATION_STILL_M = None (the code
stays as the measured alternative). The pre-snap deficit is the quarterback occluded from the
sideline plus a line drawn by fragments, and the honest fix is in identity/pairing (an endzone-only
id at the spot the roles call the QB's, paired to 33's five frames), not in the timeline.

**v60 delivered (05:15): diag/play_001_v60_hifi_720.mp4 = v59 + short unreadable-kit fragments out.
This is the current best.** 07l on 393-660 with the gait (play_001_v60_plausibility.json): steps >
0.25 m/frame 53 (0 handovers), hops 2, planted 17 % of 1069 moving body-frames, census 2.06 (KC
10.86, BAL 10.98), joints jitter p50 0.023 / p90 0.135 / p99 0.39 (54 ids). Against 21:30's
baseline on the same window: steps 114, hops 25, handovers 7, planted 13 %, census 2.55, jitter
p99 0.58. Side by side for the video verdict: diag/play_001_v53_vs_v60_snap.mp4 (timeline 393-513,
the snap to the throw; v53 left, v60 right; v53 is the last render the user was shown, cut at 513).

**Where play 1 stands (05:20).** Shipped tonight, each on a ruler and a strip: the crowd-motion snap
and clip end; the span-edge hold (per frame before the snap when the join is at the snap, the join
jump otherwise); the hole hold with long-hole middles out; the despike; the dweller line at 23.0;
the heading backfill; box twins; the lying-frame pose smoothing; unreadable-kit fragments out.
Measured and left opt-in: the lying fit prior, the jog-band gait, box containment, pre-snap
hold-at-join, impossible-speed runs, the formation hold, the 0.4 kit bar. Open, in order of what
the viewer sees: Kansas City is nine or ten men before the snap (the quarterback occluded from the
sideline, the line drawn by fragments -- identity/pairing work, not the timeline); real men slide
at the end of the play where the camera pans (53 steps over 0.25 m/frame); two ids on one lineman
by depth (37/166); 75, a 49-frame wrong-team fragment.

**The quarterback is five ids and none of them covers the snap (05:45).** Identity's QB role sits on
22 (sideline 14-171 + endzone 125-156: the walk to the line), 93 (endzone 197-237) and 95 (endzone
214-220), 33 (sideline 281-288, five frames behind the line) and 49 (sideline 509-639, after the
throw). Between 238 and 508 -- the set formation, the snap, the dropback and the pocket -- no id with
his role has a box in either camera. At endzone frame 245 (sideline 260) the boxes at his spot are
the centre 17 (bottom 638) and a second endzone track 164 (tid 22, 230-362, bottom 630, cx 922):
the QB under centre shares the centre's box bottom because his feet are hidden, so 164's ground
point IS the centre's spot, 1.2 m short of his own -- the very 1.22 m join jump the span hold
measured on 164 and dropped. The sideline never sees him behind the line (33's five frames are
the exception). This is an identity thread: link 22 -> 93/95 -> 164 -> 33 -> 49 as one man from the
formation (the endzone box above the centre, the role), and place him 1.2 m behind the centre
while he is under centre, then by the sideline once it has him. Not a timeline rule; next session.

**The quarterback before the snap cannot be drawn from data (06:05).** Role-restricted hold tried:
33 (role QB, five sideline frames) held 124 frames, drawn 51 after the span rule, KC pre-snap 9.64
-> 9.94 -- but 33 stands at y -5.3, five metres beside the centre (y 0.0), not behind him: the role
came from the formation rule, not from where he is. Endzone track 164, the only box at the centre's
spot besides the centre's, IS the centre (top 405 vs 397, bottom 628 vs 637, cx 922 vs 927, a second
track of one man), and no id has a keypoint at the quarterback's helmet at endzone 245: the
detector merged him into the centre's box in both cameras. A body there would be invented.
FORMATION_ROLE_STILL_M = None (the code stays, measured). The pre-snap deficit is now understood
and left: KC shows ten men for three seconds because the eleventh is inside another man's box.

**Despike window 3 measured and denied (06:20):** hops 2 -> 4 (new ones on 75, 79, 37), steps 53 -> 51,
hip reprojection unchanged. DESPIKE_HALF stays 2 (knob added).

**Next threads (06:25), all in identity/pairing, each with its evidence above:** (1) the pile depth
of sideline-only linemen (37/166: the sideline-only man drawn half a metre into his neighbour; the
endzone sees them a metre apart) -- a cross-view depth ruler for one-view body-frames first, then
whether a bias is correctable; (2) the end-of-play slides (53 steps > 0.25 m/frame on real men
while the sideline camera pans; the depth axis again); (3) 75, a 49-frame wrong-team fragment on a
Kansas City lineman (kit -0.30); (4) the quarterback before the snap is inside the centre's box in
both cameras and stays undrawn. The user's video verdict on v60 decides what matters first.

**One endzone body, one sideline body (06:45).** The depth snap slides every sideline body along its
ray to the nearest same-team endzone body; on the live window 116 of 4337 snaps had two claimants
(205/211 x10, 72/81 x10, 49/76 x13, 40/194/198 x9, 79/211 x8 ...) -- two sideline ids pulled onto one
man. depth_snap.EXCLUSIVE: the nearer ray keeps the body, the other stays at the sideline's own
point. A/B: hops 2 -> 0, steps > 0.25 m/frame 53 -> 45, but BAL 10.98 -> 11.10, exactly 11/11 49 ->
47, pile pairs 15 -> 17 (the unsnapped duplicate no longer lands on its man, so the twin rule's 0.2 m
misses it and it stands 0.3-0.6 m off). Motion better, count worse: not shipped, EXCLUSIVE = False
(knob exclusive on snap_ground; test added). 37/166 is not among the double claims -- that double
is 166's own foot point, not a snap.

## 2026-09-18 (morning): the ball, and the quarterback under centre

**User (08:00): "resume on the open items - you can now add in the ball as well - i want to see it
moving as well."**

**The quarterback under centre, drawn (08:40).** He is inside the centre's box in both cameras
until he steps back at the snap, and the sideline then has him 0.8 m behind the centre (id 80 at
377). A set man has not moved: endzone_only_rule.qb_hold holds the offence id whose track starts
within 25 frames before / 15 after the snap, 0.5-2.5 m behind the centre and within 1 m of his
line, at that first point from the clip start (QB_HOLD, on by default). Three things had to be
right: the centre is the lineman nearest the line's MEAN across (08n's y_centre named the guard,
half a metre off); the hold runs AFTER the span rule (else "beyond the span, a sideline body within
1.2 m"); and the dedupe treats the held frames as vouched for (build_timeline ``keep``: an
unanchored body 0.8 m from a detected one is otherwise a duplicate). Pre-snap 213-383: KC 9.64 ->
10.08, KC <= 10 on 132 -> 111 frames, exactly 11/11 32 -> 25 (the frames at 347-392 already had
eleven with the lineman fragments; now twelve -- the pile thread, not this one). 80 drawn 213-511.

**The ball (08:20-09:00).** No detector sees a football at this scale; the ball is placed from the
bodies and two events read off the film. scripts/08y_ball_path.py writes <play-dir>/ball.json:
before the snap at the centre's hand on the turf (0.35 m toward the line, z 0.15); at the snap it
rises over five frames into the hands of the id that steps back (80), travels at chest height with
the passer chain (80 -> 79 by nearest-body continuity; 79 is Mahomes after 511, his "OL" role is a
formation guess), winds up to 2.0 m over the last eight frames; from the release it flies a
ballistic arc (gravity only) from the hand to the receiver's hands (1.4 m) at the catch; then rides
at chest height with the carrier chain (77 -> 71) and drops to the turf when the chain ends or the
carrier's box is on the ground. Play 1 from the footage: release 527 (endzone frames 530/540: arm
forward, then the ball high over the line), catch 583 (sideline 578-586: the receiver has it and
meets 14 at 586). Flight 27.1 m in 0.93 s = 29.3 m/s (65 mph), apex 1.1 m above the chord -- a
laser; the plausibility bar is 30 m/s and 9 m. A first run with --qb 49 chained the passer to a
lineman at the snap (49 only exists from 509): the chain must start with the id that steps back.
render/ball.py draws it as gaussians on a 28 x 17 cm ellipsoid, brown with a lace line, pointed
along its velocity; 05k --ball. v61 launched 09:05 with both.

**A lead-in on another man's spot, inside the gap (09:40).** The span rule's same-body test (a
sideline body within 1.2 m) only ran beyond the 30-frame gap; inside it 37's endzone lead-in
(340-369) stood on the lineman the sideline already draws as 166 (the zoom at 380 had both
skeletons on 76). SAME_BODY_GAP_M = 0.8: inside the gap, a sideline body of another id within 0.8 m
means the sideline has the man. A/B (the QB hold in): 0.6 m missed 37 (0.55 was the smoothed
figure) and cost real frames (pre-snap exactly 11/11 25 -> 11); 0.8 m: 37 drawn from 370 not 340,
pre-snap KC 10.08 -> 9.75 (frames at twelve 35 -> 14, exactly 11/11 25 -> 28), live KC 10.86 -> 10.79,
BAL 10.98 -> 10.97, exactly 11/11 49 -> 59, hops 2, steps 53, pile pairs 15. Ships; v62 carries it.
First look at the ball in v61's early frames (09:50, scratchpad/review_v61/strips/render_ball_f214.png,
render_80_f214.png): a brown ellipsoid on the turf at the centre's hand, mostly hidden behind the
linemen from the follow camera (it sits behind the offence), and the held quarterback stands behind
the centre in his first fitted pose. Review tooling: render_strip.py takes ``--spec ball:START:COUNT:STEP``
(the crop follows the ball's projected position, its z from ball.json).

**v61 delivered (10:25): diag/play_001_v61_hifi_720.mp4 = v60 + the quarterback under centre + the
ball.** Ball strips (scratchpad/review_v61/strips/render_ball_f388/528/576.png): at the centre's
hand 388-392, rising into the quarterback's hands 394-396, then INSIDE his torso 398-402 (placed at
the body's centre); the flight 528-584 crosses the field alone, brown with its lace, apex 2.9 m,
and lands on the receiver at 584; then inside the receiver's torso 586-590. Fix: the carried ball
sits 0.3 m in front of the body along its facing (yaw_of), the release point 0.4 m in front; v62
relaunched with it (the first v62 had loaded the old path and was stopped). The held quarterback
stands behind the centre for the whole pre-snap (render_80_f214.png).

**The end-of-play slides are not the camera solve (01:10; RETRACTED below).** cameras.npz has the sideline solved on
every frame 213-660 (conf 1.00, no filled runs), and its pan is slow (yaw rate under 0.06 deg/frame
by the stored R). The 53 fast steps on real men at 560-660 are one-view depth on bodies 15-20 m
across the field from the camera's line (185, 78, 77 near the far sideline): the placement thread,
not calibration. 07l on v62's timeline: census 1.99 (KC 10.79, BAL 10.97), hops 2, steps 53,
planted 17 %, jitter p99 0.39.

**RETRACTION (01:30): the end-of-play slides ARE the sideline camera.** "conf 1.00 on every frame" says a
frame was solved, not solved well, and "0.06 deg/frame" is 8 px/frame at fx 7500 (units!). Three rulers
agree, all on the footage: (1) the solved paint drawn on the frames (scratchpad paint_overlay.py /
paint_full.py, diag/slides_v62/): on the paint at 500-530, off it at 636-660 (yard lines 35-64 px left,
hash rows 9-15 px, the far sideline ~108 px at 645); (2) probe_paint_rows.py (brightness search along the
projected rows/lines): yard-line offset 0-4 px through 630, then -18/-35/-64/-48/-55 px at 636-648 and
+33/+38 at 657-660; (3) the calibrator's own grid_distance_px: 3-7 px on 400-628, then 12, 14, 28, 37, 44,
61, 77, 46 px at 632-660. Every fast step on 393-660 lies along the camera's depth axis (probe_slides.py:
|along| share p50 0.98, 53/53), on 78 at 636-656, 185 at 643-658, 180 at 644-649 -- the drift window.
The camera is not "solved" at 632-660: 08e's refinement did not hold there. Fix thread: re-refine the
tail (chained from the last good frame), then the placement follows (the timeline places from the ankle
rays through cameras.npz at load time; the pose caches stay).

**v62 delivered (02:45): the ball moves.** Strips (scratchpad/review_v62/strips/render_ball_*.png): the ball
rides in front of the passer's chest 518-530, leaves at 532, comes down on the receiver's chest at 584 and
stays with him to 636; at the snap it sits in the pile at the quarterback's hands. 37's duplicate lead-in
(340-369) is gone. The carried ball floats a hand's width ahead of the body (0.3 m along the facing): the
avatar's arms do not hold it -- a hands pose is the next ball thread, not a placement one.

**The chained tail cameras (scratchpad refine_tail.py) were REJECTED on the second ruler (02:40).** Chained
rotation+focal refinement of 600-660 fits the yard lines to 2-3 px (shipped 5-77) and keeps the box-height
ratio at 1.05-1.15 (the shipped lens drifts to 1.52 by 660), but the timeline under it has 116 fast steps
(shipped 53): whole groups of bodies slide shallower together at 614-635. New ruler, "common-mode depth":
the median over all drawn bodies of the along-depth step per frame (a camera drift moves everyone at once;
men do not). Mid-play both tracks read 0.006 m/frame; on 600-660 the shipped reads 0.013 (p95 0.039), the
chained 0.105 (p95 0.127). The yard lines are a pencil of near-parallel lines: rotation about their
direction trades against the focal length (refine_paint's documented valley) and the chain walks along it
(the far-sideline row drifted 30/51/66 px at 620-628 while the yard lines stayed at 2 px). The fix needs a
ROW constraint per frame: the far sideline while it is in frame, the hash rows, and the players' common-mode
depth motion between frames. cameras.npz restored (backup cameras_pre_tail.npz).

**Tail cameras, attempt 2 (03:40): REJECTED on the timeline too.** refine_tail2.py chained from 628 with the zoom
scanned per frame (coarse 0.5 %, then 0.05 %) and chosen by the players' common-mode depth step on the box
bottoms (+ far sideline + box heights), the rotation refined to the yard lines with the focal fixed: per frame
the box common-mode reads 0.00-0.02 and the far sideline stays within 12 px to 640, but the timeline under it has
99 fast steps (53) and a whole-scene slide of -0.20/-0.29/-0.20 m/frame at 638-644. Two causes seen: the
far-sideline term picked the crowd at 642 (+60 px) once the line reached the image's top edge, and the 3-dof
rotation refit on the yard lines leaves the TILT free (a pencil of near-vertical lines pins pan, not tilt): the
smoothed track has a 0.127 deg step at 640 = 17 px at fx 8000 = 0.7 m of far-field depth in one frame. Next:
pan from the yard lines only (1-dof), zoom and tilt from the bodies' depth steps (their median and their slope
against depth), roll held; the far sideline as a check, not a term. cameras.npz restored.

**Id 75 is a real man (03:35).** diag/twin75/: the footage shows a white BAL rusher engaged with the red KC
lineman 48 from 528 to 592, 75's skeleton on the white jersey, 48's on the red one; their boxes overlap (IoU
p50 0.52, box bottoms 0 px apart) because they are locked together, not because they are one man. "75 = a
wrong-team fragment" is withdrawn; a cross-team box-twin rule would have deleted a real player. The census
already counted him right (BAL 10.97).

**v63 (03:30): the clip ends at the dead ball.** 08x has a third end rule between the carrier and the crowd:
the ball on the ground (08y's ball.json, its first ``down``/``ground`` frame after the release: play 1 = 639,
the receiver tackled) is the dead ball, and the clip runs DEAD_AFTER_BALL = 8 more frames for the tackle to
finish (play_end.json: end 639, tail 8, "ball down (08y)"). The crowd rule could not fire on play 1: the clip
ends 21 frames after the tackle and the rule needs 30. The user's standing instruction: "we can end the clip
when the play is dead". Effect: the camera-drift window 647-660 (grid 44-77 px) is no longer drawn at all,
632-647 (12-40 px) still is. 07l on the play (393-639): steps 23 (53 on 393-660), hops 2, census 1.40
(KC 11.39, BAL 11.12), planted 17 %, joints jitter p99 0.36. diag/play_001_v63_hifi_720.mp4 = v62's frames
to 647 (the frames are unchanged; no re-render). Next inside the play: the 632-639 camera drift (78's slide),
the carrier's hands on the ball, 37/166 depth.

**Hands on the ball (04:00, v64 rendering).** render/carry.py: 08y now names the ball's holder per frame in
ball.json (the passer chain 80 then 79, the carrier chain 77 then 71; nobody in flight, on the ground, or
BEFORE THE SNAP -- the centre's hand rests on a ball that stays on the turf, and the first cut marked him a
holder, which would have stood him up with the ball at his chest for 180 frames: caught on the launch
log's "5 holders" and fixed before the render). 05k turns the holder's shoulder and elbow rows toward a
carry pose solved on the real SMPL-X model (both hands in front of the chest a ball's width apart; the
conventions -- +x left, +y up, +z forward, a shoulder about -y swings the arm forward, about -z drops it --
are recorded in carry.py), ramping over 4 frames at each edge of a holding stretch, and draws the ball at the
posed wrists' midpoint + 6 cm along the facing. Smoke render 594-606: the ball sits in both hands at the
chest (scratchpad/review_smoke/render_ball_f594.png); v62 had it floating a hand's width ahead. Known seam:
the last two windup frames before the release use the path's rising z (a chest-to-shoulder pop at 525-527);
the throwing arm is the next ball thread. Also seen: the receiver's id changes 77 -> 71 at 624-628 (the same
man, 0.2 m apart, both drawn for 5 frames -- under the twins rule's 8), so the carrier chain's "hand-off" at
629 is an id change, not a fumble.

**The throw (04:25).** carry.py's second half: two key arm poses solved on the model (COCKED: the ball beside
the ear, the elbow out, the left arm pointing at the target; RELEASE: the throwing arm extended up and forward,
the left arm dropping across), a schedule around ball.json's release (the arms cock over 6 frames, swing over
8 with the release pose on the release frame, fade back to the fit over 8), the ball in the throwing hand
(the wrist + 8 cm along the forearm) until it flies; 05k --throw-hand R|L (default R; play 1's passer is
right-handed). Smoke render 512-532 (scratchpad/review_smoke/render_ball_f512.png): windup 514-518, the arm
up 520-524, release 526, flight after. The slerp from the carry to the cocked pose passes through a
straight-arm-out frame or two (the elbow's flexion axis turns from y to z) -- brief, left as is. The first
solve of the key poses sat in local minima (the arm never rose); seeds from the verified conventions fixed it.
v64 = v63 + carry + throw, rendering.

**The hidden linemen (04:45): pre-snap KC 9.75 -> 11.18.** The pre-snap deficit was never a missing
detection: the endzone camera, looking along the line, sees the guards side by side on every pre-snap frame
(38 on 169, 37 on 166, 74 on 162), while from the sideline they hide behind the centre and their tracks start
at 345/370. Their endzone-only bodies were deleted by the DEDUPE as copies of the centre (along the sideline's
depth axis they sit inside its box) -- the closed "dedupe-box" thread's inseparable case. What separates them
is the endzone's ACROSS axis: a ghost from the endzone shares its man's across position (the endzone measures
it well), a hidden lineman stands a body's width across from every sideline-backed teammate. New rule
endzone_only_rule.line_vouch (LINE_VOUCH_ACROSS_M 0.7, default on): on the pre-snap frames an endzone-only
body within 2 m along the field of the offence's side of the LOS with no sideline-backed teammate within
0.7 m across is vouched for to the dedupe (build_timeline keep, like the quarterback). Window 213-383: KC
9.75 -> 11.18, exact-eleven frames 28 -> 80, KC <= 10 frames 129 -> 30; 38 vouched 115 frames, 74 157, 86 87
(74 confirmed on the endzone footage, diag/vouch/overlay_f00300_both.jpg). The 61 frames at twelve are the
sideline's own twins that were there before (82/166 on one man 291-307, 204 on the quarterback's spot),
the next pre-snap thread. First tries recorded: a "formation spot hold" for two-view still ids held only two
BAL twins (171, 195: BAL 11.0 -> 11.63) because the guards are not two-view at all -- reverted.

**v64 delivered (04:50): ball in hand, the throw, the clip to the dead ball.** Strips
(scratchpad/review_v64/strips): at the snap the ball leaves the turf under the centre and rides in the
quarterback's hands as he drops (394-402); the throw cocks at 516-518 (the arm swings out wide for two frames
on the way to the ear -- the carry-to-cocked slerp passes through a straight arm), rises 520-524, releases at
526; the receiver's hands close on the ball at 584 and it stays at his chest. diag/play_001_v64_hifi_720.mp4
(218 frames, 213-647). v65 = v64 + the hidden linemen (line_vouch) is rendering.

**The quarterback's double (05:15).** With the guards back, the pre-snap frames at twelve were the sideline's
twins, and the biggest was the quarterback himself: id 204, a 159-px standing box on his spot on 90 of 180
pre-snap frames, is the quarterback under another id (his track switches to 80 at 377), and the QB hold drew
80 beside him. qb_hold now takes out a teammate within QB_SAME_M = 0.5 of the held spot who stands at least
0.3 m behind the centre (a first cut without the behind test took the centre out on 18 frames), so one body
with one pose stands there. Mean |KC - 11| a frame on 213-383: 0.602 -> 0.520; exact-eleven frames 80 -> 91;
at twelve or more 61 -> 34; at ten or fewer 30 -> 46 (204 stood alone on a few frames where 80's held body
is later dropped -- open). Box twins at IoU 0.5 change nothing pre-snap and 0.4 costs real men (exact 80 ->
55): 166 on 19's man (291-392, IoU p50 0.57) stays the remaining pre-snap twin. v66 = v65 + this.

**Pre-snap hole fill: measured and not adopted (05:40).** The left guard (82) is sideline-only with holes on
40 of its 91 pre-snap frames (a 69-px partial box on a man behind the centre; no endzone id -- the endzone
detection of that man carries 166's/82's labels but no separate track). hold_holes moves endzone-filled
frames and has nothing to move here, so endzone_only_rule.fill_presnap_holes draws the line between a set
man's sideline points across any pre-snap hole. It filled 82 on 36 frames but also every twin's holes
(19, 34, 195, 204 ...): |KC-11| 0.520 -> 0.538, exact-eleven 91 -> 82, twelve-or-more 34 -> 52. Opt-in
(PRESNAP_FILL False; loader presnap_fill=True). The pre-snap now stands at 10.9 a frame with the left guard
its remaining hole and 82/166's overlap (291-307) its remaining double.

**Pre-snap hole fill, second cut, ADOPTED (06:00).** The rejected fill filled the twins' holes; the vouched
guard 38 meanwhile flickered in v65 (drawn in seven runs, holes of 3-24 frames: strips render_38_f240.png
"absent" at 240/280/340). fill_presnap_holes now (a) fills a VOUCHED id's holes between its vouched frames
(the filled frames vouched too), then (b) fills any id's pre-snap holes only where the line point is EMPTY --
no same-team body within 0.7 m across and 2 m along (a twin's hole is its man's frame). |KC-11| a frame on
213-383: 0.520 -> 0.462 (a) -> 0.427 (a+b); exact-eleven frames 91 -> 96 -> 102; frames at ten or fewer
46 -> 28; at twelve or more 34 -> 41 (the sideline twins 82/166 and small fragments 98/172 fill too). v67 =
v66 + this. The pre-snap thread stands at |KC-11| 0.43 from 1.25 this morning (9.75 a frame).

**Lower-ankle placement: measured, not adopted (06:15).** Hypothesis: the mean of the two ankle keypoints is
pulled up the image by a lifted foot (a runner, a thrower stepping into the throw), placing the body deeper
for a frame -- 79's 1.5 m depth excursion after the release (526-547) looked like that. play_timeline
ANKLE_PICK "lower" (the ankle lowest in the image = the planted foot): steps > 0.25 m/frame on 393-639
23 -> 15, hops 2 -> 2, but census 1.40 -> 1.53 (KC 11.39 -> 11.49, BAL 11.12 -> 11.30) and root jitter p90
0.030 -> 0.034 (the pick hops between feet). Opt-in constant, default "mean".

**v66 delivered (06:30) = v65 + the quarterback alone on his spot.** The waiter launched it before the catch
code landed, so the catch's first visual check is v67 (queued: + pre-snap hole fill + catch). Strips: the
ball leaves the turf at the snap into 80's hands; 620-638 the carrier holds it at the chest; at 639 it drops
to the turf where the chain lost him (the "ground" segment) and lies there to 647. Footage check of the
surplus KC ids in the pocket after the throw (diag/surplus/): 211 and 170 are both real red-shirted linemen
blocking Baltimore's 99 and 98 -- the play-window KC 11.4 is crowding and near-doubles in the pocket (12/76
0.3 m apart, 79/170 0.7 m, 205/211 0.8 m), the closed "no removal route" thread, not wrong-team labels.

**The in-play fast steps were the depth snap onto the wrong man (06:40 machine clock).** Tracing id 28's
fast steps (584-587, 0.3 m/frame across the field): no ankle keypoints there, the box point moves 1.1 m
over ten frames, the timeline 2.5 m -- depth_snap.snap_ground moved him +2.0 m along his ray at 588 (and
+1.8, +1.7, +1.2 after) onto a teammate's endzone row (28 has none of his own; the footage shows him
engaged with a red blocker beside 75/48), and id 157 -2.0 m at 548. The outlier veto compares a snap with
the body's OTHER snaps, and a run onto the wrong man agrees with itself. New veto_jumps (JUMP_M 1.0,
default on): a snap whose result lies more than 1 m from the body's point on the previous drawn frame,
while the raw point lies within 1 m of it, is undone, frames walked in order. Play window 393-639: steps
23 -> 11, hops 2 -> 0, root jitter p90 0.0301 -> 0.0284 / p99 0.0908 -> 0.0721, census 1.397 -> 1.409;
0.6 m: steps 10 but census 1.47 (right snaps refused). v68 = v67 + this.

**v67 delivered (07:15 machine clock) = v66 + pre-snap hole fill + the catch + the quarterback stance.**
Strips (scratchpad/review_v67/strips): the receiver's arms rise to the ball at 580-582 and close on it at
584 (v66: arms at his sides, the ball on his chest); guard 38 stands on every pre-snap frame (v65: absent
at 240/280/340); the pre-snap sheet shows a full red line. v68 = v67 + the depth snap's jump veto + the
throw's lift waypoint, rendering.

**There was no tackle (07:00 machine clock).** The footage (diag/tackle/): the receiver runs alone along the
far sideline and steps out of bounds at ~639; no Baltimore body is within 7 m of him on the timeline from 612
on. His track ends at 638, the carrier chain lost him, 08y wrote the ball to the "ground" there and the
render dropped both man and ball on the frame the play ended. Two changes: (a) 08y keeps the ball in the
lost carrier's hands ("held", the holder stays him) unless he was seen on the ground; 08x's dead-ball rule
counts "held" (a carrier the tracker loses is a dead ball: out of bounds or under a pile) -- play 1 still
ends at 639, clip to 647; (b) timeline.hold_to_end, applied by 05k after loading (NOT in the loader: a first
cut there fed the held body back into the ball chain, the ball was "carried" to 647, no dead ball was found
and the clip ran to 660 again): a body drawn within 3 frames of the dead ball keeps its last state through
the tail, so the receiver stands at the sideline with the ball while the clip ends. The lying body drawn at
640-647 (184) is a fallen man near the pocket, 12 m away, not a tackler. v69 = v68 + this.

**v68 delivered (07:35 machine clock) = v67 + the depth snap's jump veto + the throw's lift waypoint.** Strips
(scratchpad/review_v68/strips): the throw's windup keeps the arm in front (516: the ball at the shoulder, elbow
bent; v66 had it out at arm's length to the side); id 28 moves smoothly with his blocker through 578-592 where
he used to jump 2 m deeper at 588; 157 likewise at 546-556. v69 = v68 + the aftermath (the receiver keeps the
ball and stands through the tail), queued.

**v69 delivered (08:20 machine clock) = v68 + the aftermath.** Strip render_ball_f632 (scratchpad/review_v69):
the receiver keeps the ball at his chest and stands at the sideline through 646 where v68 dropped him and the
ball at 639; the late fragment 185 (a red body, 639-660) walks in beside him from 640 -- check whether he is a
teammate arriving or a ghost before touching him. diag/play_001_v69_hifi_720.mp4 is the current best.
Rulers on the play window 393-639 (v68's timeline; the aftermath acts after it): steps 11, hops 0, census 1.41,
root jitter p99 0.072, joints jitter p99 0.36; pre-snap |KC-11| 0.43. Threads left open: the far-field camera
drift 632-647 (78 slides), pocket near-doubles after the throw, 212's alternating box (a pair under one id),
the gait's arm swing (opt-in, strip pending).

**Runners' arm swing: measured, left opt-in (08:40).** gait.arm_rotvecs pumps the arms opposite the legs where
the gait is on (ARMS / 05k --gait-arms). 07l's joint jitter does not move (p90 0.122, p99 0.356 either way: that
ruler is orientation and leg-phase jitter), and the strips of runners 3 and 9 at 440-454 (review_v69 vs
review_smoke_arms) are a wash from the follow camera behind them -- both show arms at the sides, the gait's a
little more regular. Neither ruler moves, so the flag stays off; re-judge on a play with a side-on runner.

**The receiver drawn twice after stepping out (08:50).** v69's tail strip showed a second red body beside
the held receiver from 640: id 185, born at 639 two to three metres from where his track ended -- the same man
re-identified (footage diag/tackle/player_185_f640.jpg: one red man at the sideline). hold_to_end now takes
the teams and drops a same-team track born at or after the dead ball within 3 m of a held body's spot on the
held frames, so the held body owns the spot and keeps the ball. v70 = v69 + this.

**v71 delivered (10:05 machine clock) = v70 + twins 0.4 + the 4 m re-identification radius. CURRENT BEST:**
diag/play_001_v71_hifi_720.mp4 (218 frames, 213-647). Strips/sheets (scratchpad/review_v71): the receiver
alone with the ball through 646; the pre-snap line full; the play from the snap to the sideline coherent, the
ball visible in flight 537-561. Rulers on this timeline: play window 393-639 steps 11, hops 0, census 1.29
(KC 11.10, BAL 11.06), root jitter p99 0.072, joints jitter p99 0.36 (the gait's own foot strikes; yaw jitter
median p90 0.66 deg/frame^2); pre-snap 213-383 |KC-11| 0.345, exact-eleven frames 112 of 171. Open threads, in
order of what a viewer sees: the far-field slides 632-647 (the sideline camera's drift; two re-solves rejected),
the pocket's near-doubles after the throw (real men crowding, no removal route), the left guard's pre-snap holes
234-263 (his sideline id 82 is a partial box that may be the quarterback's upper body early on; no endzone id
of his own), the runners' arm swing (opt-in, a wash on strips).

**The left guard's endzone body, revived and not adopted (10:40 machine clock).** He was never missing from the
endzone: id 86, endzone-only, at his spot on all 180 pre-snap frames, passes the vouch on 87 of them (82's partial
box blocks 32, 19/37/166/9 the rest) -- and endzone_only_ids leaves the whole id out as a ghost before the vouch
can matter. A revival (the id kept, drawn on its vouched frames only, LINE_VOUCH_REVIVE_MIN 30) draws him on every
frame (KC at ten or fewer 40 -> 4) but the fragments that stood in his slot -- 166 on 19, 204, his own sideline
partial box 82 at 0.55 m, 31 -- now count as extras: exact-eleven 112 -> 103, |KC-11| 0.345 -> 0.433, and the
Baltimore ghost 92 (22 vouched frames) came with it until the 30-frame gate. Opt-in (None). The step that would
make it pay: fold 82 into 86 (one man, the sideline's upper-body box and the endzone's full body).
Folding his sideline fragment (82, within 0.8 m) into the revived 86 on his frames folded 13 body-frames and
moved nothing the right way (exact-eleven 101, |KC-11| 0.444): the extras are 166 on 19, 204 and 31, not 82.
Both revival and fold stay opt-in.

**A side-by-side for the eye (10:55 machine clock).** diag/play_001_v71_vs_footage.mp4: the sideline footage at
the render's frames (213-647, every second frame, 1280x720) on the left, v71 on the right, 218 frames at 29.97.
Time-aligned, not viewpoint-aligned (the render's follow camera sits behind the offence). Built with ffmpeg
(select between(n,213,647) and even offsets, setpts, hstack); diag/play_001_footage_213_647_720.mp4 is the
footage half. Next: a render from the broadcast camera's own solved pose (cameras.npz sideline K/R/t per frame)
so the two halves compare frame for frame.

**The blend ruler (11:40 machine clock).** 05k --view-camera sideline renders the timeline from the broadcast
camera's own solved pose (K/R/t per frame, K scaled to the output), so the render overlays the footage frame for
frame. diag/play_001_v71_sideline_view_720.mp4 (the render), diag/play_001_v71_sideline_sbs.mp4 (footage | render),
diag/play_001_v71_sideline_blend.mp4 (50/50 blend); scratchpad/launch_view_v71.sh builds all three. What the
blend shows that the strips and sheets could not: at the snap (394) every avatar sits on its player and the paint
on the paint; at 533 (after the release) and 583 (the catch) the avatars sit on their players except one red body
near the 30 with no player under it; at 639 the held receiver's avatar stands on empty grass at the far left
(placed 8-9 m inside the sideline he stepped over: the far-field depth of a one-view body under the drifting
camera) while the footage has a white-on-red pile mid-field (184 on 76, a block that ended on the ground, not the
receiver). Every version from here gets the blend; it is the footage-versus-render comparison the user asked for.

**Placement checked against the keypoints through the broadcast camera (12:20 machine clock).** A "feet vs box"
ruler read every body 0.12 box heights too deep and was WRONG: the detector's box bottom lies well below the
shoes, so its ankle line is not bottom minus 0.078 h. Against the keypoint ankles themselves (COCO 15/16, conf
> 0.5, 285 body-frames sampled every 20 frames) the timeline's ground point projects 1.4 px above the keypoint
ankle at the median and the rendered ankle 4.5 px (|dv| p50 5.0, p90 14.1; |du| p50 0.9): the posed feet sit
0.15 m (p50) ahead of the pelvis on the ground, a lean, not a bias. Two-view (fused) bodies read the same as
one-view ones once measured this way. The pelvis-vs-box ruler's 11 px pre-snap was the linemen's crouch.

**Correction (12:40 machine clock): the receiver scores, he does not step out.** His x at 638 is -45.3 m; the
goal line is at -45.72 (50 yards), and the footage at 640 (diag/tackle/crop640.png) has him 7 m inside the far
sideline beside the goal-line pylons, ball tucked, crossing into the end zone -- the timeline's (x, y) is right
and the "8 m inside the sideline" worry was correct and harmless. The tracker loses him in the end zone (his
track ends at 638, id 185 picks him up at 639); the dead-ball rule read that as the play's end, which it is: a
touchdown. HANDOFF entries above that say "steps out of bounds" mean this. The held body through the tail is a
small lie (he keeps running); the ball stays with him, as it should.

**The ankle ruler through the sideline camera measures depth disagreement, not error (13:00 machine clock).**
A ground point moving along the sideline's line of sight moves up and down the IMAGE (a near-vertical line at
this camera height), so the rendered-ankle-minus-keypoint-ankle row offset is the sideline's blind axis: the
pocket bodies 76 and 211 read 26-33 px because the two-view placement puts them ~1 m from where the sideline's
own ankle ray does, which is the fusion doing its job or not -- this ruler cannot say. An across-ray gate on
the refit placement (place_from_refit max_across_m; opt-in, MAX_REFIT_ACROSS_M None) changes nothing at 0.5 m
and hurts at 0.3 m (13 jumps to 41 px). The depth ruler for the pocket is the ENDZONE camera: a render from
its pose blended with the endzone footage (frames offset -15). Launching that as the second blend.

**The endzone blend's first frame (13:20 machine clock).** diag/ez_blend_214.png (render from the endzone pose
over endzone frame 199): the running back and the quarterback sit on their players, but several linemen's
avatars stand half a body-width beside theirs ACROSS the field -- the axis the sideline camera cannot measure.
ground_positions averages the two cameras' ground points, which halves the sideline's depth error instead of
removing it. Under test: FUSE_AXIS (x from the sideline, y from the endzone on two-view frames), judged by ankle
rulers through BOTH cameras (the endzone's du is the field's y) and the motion rulers.

**The endzone blend (13:50 machine clock).** diag/play_001_v71_endzone_blend.mp4 (render from the endzone pose
over the endzone footage, frames 198-620, i.e. sideline 213-635; diag/play_001_v71_endzone_view_720.mp4 the
render alone; scratchpad/launch_endzone_view.sh vNN builds them). Frames at 3.0/4.45/5.87 s: the avatars sit on
their players to within about half a body-width ACROSS the field; the worst are in the pocket after the throw.
The endzone-camera ankle ruler (rendered ankle vs endzone keypoint ankle, du = the field's y): pre-snap p50 5.4
px / p90 16.7, the play p50 6.7 / p90 57.9. Ranked by id over the play: 212 (-307 px: its endzone rows are
another man's), 170 (p90 190 at 555-567), 206 (114), 198 (-71 p50), 76 (p90 114 at 577-585), 81, 37 (74 at the
snap), 40, 211, 168 -- mispairings on a handful of ids, not a bias (74 alone carries a steady +19 px). Two
blends now bracket the placement: the sideline's for x and counts, the endzone's for y.

**PAUSED (14:00 machine clock, user's request).** Tree clean, everything pushed, suite green, no render running.
Current best: v71 (diag/play_001_v71_hifi_720.mp4; the follow-camera clip), with the review clips
diag/play_001_v71_sideline_blend.mp4 / _sideline_sbs.mp4 / _endzone_blend.mp4. Resume point: a per-frame
MISPAIR veto in the loader after place_from_refit (play_timeline.py ~line 693-703): for every (frame, id) whose
views include the endzone, project ground[f][pid] at ankle height through the endzone camera at f + offset and
compare with that id's endzone ankle keypoints (kdf, cam endzone, already shifted to sideline frames); when |du|
exceeds MISPAIR_PX (try 100, then 60) the endzone rows are another man's -- fall back to side_ground[f][pid] and
drop "endzone" from views[f][pid]. Rulers: scratchpad/probe_mispair_ab.py (endzone ankle ruler p90 57.9 -> ?,
sideline ruler unchanged, steps 11 / hops 0 / census 1.29). Then v72 with both blends. Play 1 only, as ever.

## 2026-09-18 (afternoon): the ball went to the WRONG MAN -- RETRACTION of "receiver 77", "out of bounds", "touchdown"

**What the user saw (16:00 machine clock).** "In this play the ball didn't go to the endzone / score a touchdown -
it went to the tight end in the middle for a smaller gain (first down) - why did your pipeline not catch this?
Why is the ball tracking going to the wrong player?" He is right. Every line above that says the receiver is
77, that he steps out of bounds at 639, or that the play is a touchdown, is wrong.

**What the film shows (diag/catch/, raw sideline frames 520-631 tiled at full resolution).** Mahomes (#15)
throws at 527 (sheet_qb_520_535.png: the arm comes forward 525-527, extended at 528). The ball is a 10 px
brown blur crossing the pocket at 532-540 (sheet_release_528_541.png) and flying flat over the middle
(sheet_flight_524_564.png). The catch is at ~562 by the red body at the near hash between the far 10 and 20
numerals (sheet_catch_556_571.png: he reaches at 560-563, tucks by 564). BAL 14 (Hamilton) wraps him at
584-596, he is dragged and down at 607, the pile lies still to the clip's end (sheet_tackle_584_631.png).
The 05q overlay of the timeline's ids on those frames (sheet_overlay_sl.png) names the receiver: id 48 at
560-583, then nobody -- and 77, the man I had typed as the receiver, is the far-sideline receiver 13 m away
who never had the ball. The gain is x -24.1 -> ~-33: about nine yards, the first down the user describes.

**Why the pipeline had no way to catch it.** (1) No ball detector: 08y builds the ball from three HAND-TYPED
inputs (release, catch, receiver). (2) I typed them from RENDER strips and then checked the constructed ball
against the render -- a closed loop that cannot fail. (3) The receiver's track was in three pieces, which is
the normal state of a man in a pile: 74 (Noah Gray, jersey 83 read by OCR, sideline 421-520; the timeline
even had him "fused" to 527), then 48 (508-588, unnamed, given an OL build and 315 lb by 08n's role rule),
then 75 (528-602, labelled BAL on an unreadable kit, the "real man engaged with 48" of the cross-team twin
note above -- he WAS 48). Even 08y's "nearest offence body" chain would have lost him at 588 to a man wearing
the other team's colour. (4) The dead-ball rule then read the chain loss as the play's end and the story
built itself: "tackle at 640" -> "out of bounds" -> "touchdown", each a reading of the render, none of the film.

**Fix (all committed).** `scripts/08z_fold_ids.py --keep 74 --drop 48 75` (nfl_gsplat/tracking/fold.py): an
explicit fold in the GLOBAL id space, track ids untouched, the weaker of two boxes on one frame dropped (41),
keypoints follow, 08v carries the pose caches, identity loses 48/75 (74 = Noah Gray keeps his real build).
Not via 08o's merge_map: it works in the tracker-id space and rewrites every row's global id from its track
id, and a fifth of play 1's rows differ since the pairing stages -- that path relabels unrelated men. Then
`08y --release 527 --catch 562 --qb 80 --receiver 74 --down 607` (flight 13.8 m in 0.58 s = 23.7 m/s;
carried 563-602, held 603-606, down 607+); 08x's dead_from_ball now takes the carrier's DOWN frame over the
chain loss ("held" is the weakest signal); play_end.json = snap 395, end 607, clip 215-615.
timeline.hold_to_end(always={carrier}) keeps the carrier drawn from wherever the detector lost him (602) to
the end, so the ball does not float over empty turf. Timeline after the fold: 74 KC drawn 213-602, one body
at the catch spot with BAL 28 and 55 beside him; 48 and 75 gone. v72 rendering with both blends.

**Rule for every play from now on (also in memory ball-from-events).** Read the events off RAW frames, not
render strips; overlay the ids on those frames (05q) to name the receiver; check that his id spans the catch
to the tackle in tracks.parquet and fold the pieces (08z) when it does not; verify the render's catch against
the raw frames, never against the render. The user's eyes were the ruler that caught this; the film was
available the whole time.

**v72 delivered and checked against the film (18:10 machine clock).** diag/play_001_v72_hifi_720.mp4 (the
follow-camera clip, 215-615), diag/play_001_v72_sideline_blend.mp4 / _sideline_sbs.mp4 / _endzone_blend.mp4 (the
blend launchers now cut the footage to play_end.json's own frames, so the streams are aligned). The check that
matters, diag/catch/catch_check_v72.png (film | render from the sideline camera's pose | blend at 528, 544, 556,
562, 570, 590, 606, 614): the receiver's avatar sits on the film's receiver from the route through the catch to
the pile, the rendered ball is beside him at 556 and in his hands from 562, the tackle forms on the film's spot.
The endzone camera (diag/catch/ez_catch_v72.png, the depth axis) shows the film's receiver wearing 83 -- Noah
Gray, the id the fold named -- with the avatar half a body-width to his left at 556 and on him by 570; the ball
in the film's air at 556 and in his hands at 562 where the render puts it. Render strips (review_v72/strips):
the flight 540-556, the reach and catch 560-562, the carry, the wrap at 584-606. One flaw seen and fixed for
v73: at the down frame the ball dropped to the turf beside the still-standing held body (08y wrote GROUND_Z on
"down") and read as a fumble; 08y now keeps the holder and the carry height on held and down frames (05k draws
the ball between the holder's wrists). Known and open: the pile is drawn standing (the detector loses the men on
the ground, so the last standing pose is held; a lying pose for a tackled carrier is new work); the ball renders
dark from the endzone pose (lighting), fine from the follow camera.

**A fourth fragment of the receiver before the snap.** 74 is drawn 213-380 from the endzone track alone, then
vanishes 381-393: id 39 (sideline 384-408, named "Bryan Cook" by a jersey vote) stands on his exact spot and the
dedupe rightly keeps the sideline-backed body -- 39 is Noah Gray's sideline fragment before his own sideline track
begins at 421 (the "odd id 39" of the census note above). 167 (411-420) is a merged two-man box (207 px tall) and
41 a 23 px speck; neither is folded. v73 chain (scratchpad/chain_v73.sh, running): 08z --keep 74 --drop 39, 08y
with --snap 395 (play_end's snap moved 393 -> 395 after the first fold), 08x, render + both blends.

**The ball read off the film (18:35 machine clock): scripts/09a_ball_in_film.py, nfl_gsplat/tracking/ball_film.py.**
The hypothesis: the ball in flight is a 10-20 px blob that moves against the camera-compensated background,
outside every player's box, along a near-straight image line. Tested on the raw sideline frames 500-615:
per frame pair an ECC affine alignment (the pan is 3-6 px a frame), absolute difference, threshold 28, blobs
of 8-120 px outside the dilated boxes and the graphics -- the ball shows on 7 of the 36 flight frames
(539, 550-558; behind the pocket's boxes and at the hands it is inside a box and invisible to this). A RANSAC
line grown along a quadratic through them, kept only when dense (a third of its span seen, no gap over 12
frames) and anchored in a box at each end (a far-field runner without a box beat the real flight on inliers
alone; a junk line through blobs 80 frames apart scored 7), then walked into the boxes: leaves 79 at 530,
enters 74 at 562 with 55's box on the same point (the passer's teammate is the receiver). Sheet:
diag/catch/ball_in_film_v73.png (the fitted track over the film 528-564). Against the corrected ball.json:
release, catch and receiver AGREE. Against the day-old wrong one (ball_v62.json, --ball): "receiver DISAGREES:
the film's flight enters id 74, ball.json says 77; at 583 the receiver typed is 270 px from the track; catch
DISAGREES (562 vs 583)". That is the check the pipeline lacked; it runs from the boxes and the film alone.
Next: 08y --from-film takes its inputs from 09a's ball_film.json so the hand-typing goes away.

**v73 note.** The v73 render (chain_v73.sh) loaded 05k after the tackle edit landed, so v73 = the fold of 39
+ the ball kept in the carrier's hands on the down frames + the CARRIER's fall (render/tackle.py); the
tacklers' fall (the other-team bodies within 1.5 m of him on the down frame fall onto him, committed in
ecf91d8 with the carrier's) is v74. Both chains are queued after the v72 blends, each with its blends.

**v73 delivered (18:50 machine clock).** diag/play_001_v73_hifi_720.mp4 (215-615). = v72 + the pre-snap fragment 39
folded into the receiver (he is now drawn in the formation through the snap, review_v73/strips/render_74_f380.png)
+ 08y at snap 395 + the ball kept in the carrier's hands on the down frames + the carrier's fall (render/tackle.py:
600-607 he pitches forward and lies face down along the way he ran, the run sheet at 610-614 shows him on the turf
under two standing tacklers). Rulers on the play window 395-607 (07l v73, gait on): live steps 5, hops 0, census
1.25 (KC 11.41 / BAL 10.80), root jitter p99 0.069, joints jitter p99 0.37, planted 19 %. A probe of the fallen
carrier (scratchpad/probe_fall_ball.py: the hold weight stays 1 through 615, pelvis 0.33 m, wrists 0.05 m) puts the
ball between his wrists on the turf under his chest -- out of sight under the body, as under a real pile; the
brown patch beside the yellow marker on the 608-614 strip is a tackler's hands, not the ball. v74 (queued after
v73's blends) adds the tacklers' fall onto him (28 and 55 stand 0.1 and 0.5 m from him on the down frame).

**The endzone camera wanders in depth during the play (19:00 machine clock; scratchpad/probe_mispair_dist.py).** For
every (frame, id) with rows in both cameras, the sideline's ankle-ground point against the endzone's: pre-snap
d p50 0.40 m (|dx| 0.23, |dy| 0.23); the play p50 0.98 m, |dx| p50 0.81, |dy| p50 0.32, and the x offset is a
COMMON-MODE bias that walks with time: dx (endzone minus sideline) -0.6 m at the snap, -1.1 m over 435-515, +0.2 at
515-545, +1.4 at 545-575, +0.9 to the end -- the same for the slow bodies (< 1.2 m/s) as for the fast ones in every
bin, so it is not a time offset (a time error gives a still body no offset; the whole-play slope of dx on velocity
is confounded by the bins) but the endzone camera's pose: its depth axis is the field's x, and while it pans the
paint solve walks along its tilt-zoom valley by up to 1.4 m (conf 1.0 throughout, as with the sideline's tail).
The sideline's x is trusted (the sideline blend puts every avatar on its player to a few px), and the loader lets the
sideline's point override on two-view frames, so the damage is confined to the endzone-only bodies (placed up to
1.4 m off in x on those frames), the endzone ankle ruler used above to rank "mispairs" (contaminated in dv), and
whatever the two-view refit's pelvis inherits. The y disagreements are smaller and id-specific: 211 (+0.91 m over
523-607), 40 (-0.87), 11 (+0.71), 37 (+0.68), 81 (+0.57), 76 (+0.53) -- each either a mispaired endzone row or the
sideline's blind-axis error, which only the film can say; 05q overlays of the pocket frames (diag/pocket/) are
running to adjudicate before any veto is written. A per-frame common-mode x correction of the endzone ground
points from the two-view bodies (the players as the ruler, as for the sideline's lens) is the candidate fix for the
endzone-only placements.

**The pocket on the film (19:05 machine clock; diag/pocket/, 05q overlays on both cameras at 480-600).** Through
the endzone camera the fitted skeletons sit on their players in the pocket through the throw; at 540 two red
skeletons stand around Mahomes: 79 (his id after 511) half a body-width to his left and 170 on him. The per-id
offsets say why: 170's endzone rows are another man's (endzone minus sideline +2 to +3 m in x over 520-568, far
beyond the frame's common mode of +0.2 to +1.4), and 79 has NO endzone rows after the throw at all, so his y is
the sideline's blind axis with nothing to correct it. The receiver's endzone skeleton is on number 83 at
500-580, and the v73 endzone catch sheet (diag/catch/ez_catch_v73.png) has the avatar on him by 562. The
SkyCam is in the endzone footage (the black cable camera between the pocket and the receiver): the "dark ball
with spikes" noted on the v72 endzone blend was it, not the render's ball.

**Per-frame endzone-row veto (pair_rule.mispaired_frames, MISPAIR_FRAME_M 1.0; under A/B, not yet adopted).** For
each (frame, id) in both cameras the endzone-minus-sideline vector less the frame's median over its pairs (the
camera's wander) is the row's own disagreement; over 1.0 m the endzone row is dropped for that frame and the
refit's pelvis is not used there (place_from_refit skip). Tests in test_pair_rule. A/B (scratchpad/
probe_mispair_frames_ab.py: None / 1.0 / 0.7 on the play-window motion rulers and the ankle rulers through both
cameras) is running; v74 (the tacklers' fall) loaded the loader with the veto on by default -- if the A/B rejects
it, the constant goes to None and v75 re-renders.

**Per-frame veto: MEASURED AND REJECTED (19:20 machine clock).** A/B on the play window 395-607, three loads of the
loader (scratchpad/probe_mispair_frames_ab.py): off -> endzone ankle ruler du p50 35.3 / p90 104.2 px, sideline
1.7 / 9.4, steps 5, hops 0, census 1.254; MISPAIR_FRAME_M 1.0 -> endzone 35.4 / 102.1 (unmoved), steps 15, census
1.277. Vetoing frame by frame flips a body between its two-view and its sideline-only placement and every flip is
a step along the sideline's depth. The thirteenth correction that lost to what it corrected (memory). The constant
is None (opt-in), the code and tests stay. NOTE on the ruler: the endzone ankle ruler keyed on the TIMELINE frame
(the keypoints table's endzone rows already sit on the timeline clock) reads 35 px at p50 -- about half a body-width
across, what the endzone blend shows -- where the earlier probe (keyed 15 frames off) read 6.7 px; the earlier
number was the wrong ruler. v74 (rendering) loaded the loader with the veto ON; v75 is queued behind it with the
veto off and is the candidate for current best; v74 serves only the tacklers' review.

**The quarterback after the throw has no endzone rows (scratchpad/probe_qb_endzone.py).** 80's endzone track ends at
496; 79 (511-657) has none. The nearest endzone-only KC id to 79 after 512 is 164 (0.85-2.7 m, consistent with
the camera's wander), but 164's own track stands on the CENTRE's spot pre-snap (x -23.6..-22.8, y 0 over 220-360),
is absent 380-500, and reappears in the pocket at 520 -- an endzone track that switched men. 08z --frames LO HI
exists now to fold such a stretch alone; not applied: the film has not named 164's post-520 rows as Mahomes and
the QB's half-body-width y error after the throw is a secondary figure once the ball is gone. Open.
Third arm, MISPAIR_FRAME_M 0.7: endzone 35.9 / 105.4, steps 15, census 1.352 -- worse again (703 body-frames vetoed on 33
ids; at 1.0 m 367 on 32, most on 170, 9, 2, 27, 40). Closed.
Id 170 is a chimera (probe_qb_endzone.py, third block): its sideline point is 197's twin at 524 (0.3 m), then walks
to the quarterback's area by 604 (1.4 m from 79 -- a third man, since the sideline sees x well), while its endzone
rows sit on someone at x -18.8..-18.1 over 524-540 (the quarterback's spot, 2-3 m from 170's own sideline point)
and on 170's own man from 556. Neither a fold nor a veto describes that; a per-stretch identity check against the
film is the tool it needs. Open; the pocket after the throw is a secondary figure once the ball is gone.

**v74 reviewed against the film (19:45 machine clock; diag/catch/tackle_check_v74.png, review_v74/strips).** The
tacklers' fall works: 28 and 55 (within 1.5 m of the carrier on the down frame) pitch onto him and the three lie
in a pile on the film's spot, extended the film's way, at 608-614. The timing was early: the render is flat at 604
where the film's three are still upright, going down at 608 and flat by 610 -- "down" as read off the film (the
knee or the body first touching, 08y --down 607) is mid-fall. render/tackle.py FALL_SETTLE 3: the fall ends three
frames after the down frame (committed, tests updated). v74 also carried the rejected per-frame veto (steps 15),
so it is not a candidate; v75 = the tacklers + the settled fall + the veto off, rendering with its sideline blend.

**v75 = CURRENT BEST (20:30 machine clock).** diag/play_001_v75_hifi_720.mp4 (215-615) with diag/play_001_v75_sideline_blend.mp4
/ _sideline_sbs.mp4. = v73's timeline (the veto off) + the tackle: the carrier and the two tacklers within 1.5 m
of him go to the turf with the fall ending three frames after the down frame. Against the film through the
sideline camera (diag/catch/tackle_check_v75.png at 590-614): upright wrap at 590-604 like the film, going down
at 608 with the film, flat on the film's spot and along the film's direction at 612-614. The whole-clip check
(diag/catch/catch_check_v75.png at 300, 420, 528, 562): the formation, the snap, the throw and the catch on
their players. Rulers are v73's (same timeline): play window 395-607 steps 5, hops 0, census 1.25. Suite 1241
passed. The endzone-only body-frames during the play are 150 of 4731 (3.2 %, at most 17 on any id), so the
common-mode correction of the endzone camera's wander would touch little; not built.

**Where the day ends.** The user's question is answered and fixed: the ball goes to Noah Gray, and the film reader
(09a) would now flag a wrong receiver on its own. Open, in value order: (1) the pocket after the throw -- the
quarterback has no endzone rows after 511 and 170 is a chimera (a per-stretch identity check against the film);
(2) the endzone camera's depth wander while panning (a players-as-ruler refit of its pose during the play);
(3) the far-sideline receiver 77's twins after 624 (outside the clip now); (4) the pile's lying poses are
synthesised, not fitted (the detector loses the men on the ground).

**The quarterback's endzone rows, named by the film (20:45 machine clock; diag/pocket/ez_boxes_qb.png).** The endzone
BOXES of the candidates drawn on the endzone frames: 170's box is on number 15 (Mahomes) at 524, 532, 540, 556,
572 and 600 (on a lineman at 500); 164's box is on him at 516 and drifts onto number 52 (Humphrey) by 556; 139 is
Thuney (62) throughout. So 170's endzone track becomes Mahomes at about 516 -- the "chimera" of the last entry is
an endzone track switch, not a sideline one -- and the fix is a range fold: `08z --keep 79 --drop 170 --frames
516 634` (both cameras; 170's sideline rows on frames where 79 has its own are the lineman twin and are dropped,
where 79 has none they are his). Running as chain_v76.sh: the fold, 09a, 08y --from-film, 08x, the dump, 07l, 05q
overlays of 520-580 on both cameras (diag/pocket_v76/), then v76 with its sideline blend. The check: 79's endzone
skeleton on number 15 at 540 with the depth the endzone gives, and the rulers not worse than v73's (steps 5, hops
0, census 1.25).

**The quarterback wears a lineman's build after 511 (20:55 machine clock).** identity_resolved: 80 (377-511) is
'P80' with the default build; 79 (511-657) is 'P79' with role OL and 08n's OL build, 1.96 m / 315 lb -- Mahomes
rendered as a tackle for the second half of the play. Two endzone-only fragments carry his name from the endzone
OCR of number 15: 93 (197-237) and 95 (214-220), with the roster build. Queued as chain_v77.sh after v76: 79
folded into 80 (one quarterback id, no passer chain: 08y --qb 80), 80's identity replaced by 93's (Patrick
Mahomes, 15, the roster build; the OL role dropped), then 08x, the dump, 07l, v77 and its blend. Not folding
93/95's rows in: they sit pre-snap where qb_hold draws him, and a track that "starts" at 197 would silence that rule.

**v76 is INVALID: the film reader fed a junk flight into the render (21:40 machine clock).** After the 170 -> 79 fold
the film reader named "release 520 from 197, catch 557 by 79" -- a 2.1 m, 4 m/s "flight" from a lineman's box into
the quarterback's own -- and 08y --from-film took it, so v76's ball goes to the quarterback. Why: the fold dropped
170's sideline boxes on 74 frames (the lineman twin), which had been masking a region beside the quarterback; the
slow blobs there (3-5 px/frame, a wandering cloud over 521-567) grew into 15-24-inlier tracks with a box at each
end and outscored the real flight (7 inliers, 353 px) on inliers. Fixes (tracking/ball_film.py, 08y): a grown
track keeps only if its own speed is a ball's (6-60 px/frame); a flight must cover MIN_LENGTH_PX 100; with a box
at each end the LONGEST track wins, then inliers; and 08y refuses a flight under MIN_SPEED 8 m/s. On the current
data the reader now picks 540-558 (353 px) -> 79/80 to 74 again. The lesson is the same as the day's: a reader
that names a receiver must be gated on what a pass IS (long, fast, hand to hand), not on how many blobs agree.
v77 (chain_v77b.sh, running) = v75 + the quarterback's endzone rows + one quarterback id with Mahomes' identity and
build + the ball from the corrected reader; v76 is discarded.

**The reader's second failure and fix (22:05 machine clock).** With the length ranking the reader found the right
flight again (540-558, 353 px) but walked its start into BAL 198's box (Madubuike leaning into the pocket, a
smaller box than the quarterback's at 530) and, by the passer's-teammate rule, named BAL 55 the receiver -- the
defender draped on 74. Fix: name_ends takes the offence (09a: the team with the most linemen by 08n's roles, KC 11
to BAL 1 on play 1) and both ends prefer an offence box within the walk; 08y refuses a receiver who is not on the
offence. Now: leaves 80 at 530, enters 74 at 562 (55 also at the point). v77 chain relaunched (chain_v77b.sh):
09a, 08y --from-film, 08x, dump, 07l, render, sideline blend.

**v77 = CURRENT BEST (22:55 machine clock).** diag/play_001_v77_hifi_720.mp4 (215-615) with _sideline_blend.mp4 /
_sideline_sbs.mp4; the endzone view and blend rendering. = v75 + the quarterback's endzone rows after the throw
(170's from 516, film-named) + one quarterback id for the play (79 folded into 80) wearing Mahomes' identity and
build (jersey 15, 1.87 m, 212 lb, from the endzone OCR fragment 93; the OL build of P79 is gone) + the ball from the
film reader with its gates (release 530, catch 562, passer 80, receiver 74; 25.8 m/s; no passer chain). Rulers on
395-607: steps 5, hops 0, census 1.12 (KC 11.08 / BAL 10.80; v73/v75 read 1.25 -- the quarterback's twin is gone),
root jitter p90 0.027. Film checks: diag/catch/pocket_check_v77.png (the pocket 500-560 through the sideline camera:
the quarterback's avatar on number 15 through the throw) and catch_check_v77.png (528-614: route, catch, wrap, pile
as in v75). Two reader failures were caught on the way and gated (above); v76 was discarded.

**v77 from the endzone camera (23:10 machine clock; diag/catch/ez_pocket_v77.png, diag/play_001_v77_endzone_blend.mp4).**
The quarterback's avatar sits on number 15 at 500, 520, 540 and 560 -- the half-body-width offset of v72-v75 at 540
is gone, which is what the 170 -> 79 -> 80 folds were for. What remains in the pocket from this camera: the linemen
and a BAL rusher half a body-width ACROSS at 500-520 (the sideline-only bodies' blind axis: Thuney's endzone track
139 has no sideline partner, so his sideline id is drawn without depth) -- the pairing thread, per stretch, is the
next placement lead; 08r_pair_by_rays exists and could be re-run now that the pocket ids are cleaner.

**Thuney, named by both films (23:20 machine clock; diag/pocket/sl_boxes_linemen.png, ez_boxes_qb.png).** 08r's
one rejected candidate that mattered was "sideline 197 <- endzone 139, rays 0.31 m" (its gate is 0.30, and the
endzone camera's wander is in that number). The sideline film: 197's box is on number 62 through 500-560 (the
jersey reads inside the box at 520; identity had him as "Bryan Cook" from a misread). The endzone film: 139's box
is on number 62 at 500-540 and identity names it Joe Thuney from the endzone OCR. Same man, two cameras, never
paired. v78 chain (chain_v78.sh, running): `08z --keep 139 --drop 197` (no overlap: one camera each; 139's
identity and roster build survive), 08x, dump, 07l, render, both blends. 86 (Thuney's pre-snap endzone track,
125-377) is left alone: a two-view id with endzone-only pre-snap rows would be drawn from the endzone alone there
and double the sideline's lineman. 211 (Suamataia by OCR) has its sideline box on a white jersey at 520 -- another
identity mess in the pocket, unchased.

**v78 delivered (00:15 machine clock, 2026-09-19).** diag/play_001_v78_hifi_720.mp4 + _sideline_blend / _endzone_blend.
= v77 + Thuney (139 <- 197). From the endzone camera (diag/catch/ez_pocket_v78.png) the left guard's avatar now
sits ON number 62 at 500-560 where v77 had it half a body-width to his right; the quarterback stays on 15. The
film reader AGREES with ball.json on all three (release 530, catch 562, receiver 74). Rulers 395-607: steps 5,
hops 0, census 1.18 (KC 11.23, up from 11.08 in v77): 197's sideline track ends at 565 and 139 is then drawn from
the endzone alone to ~590 while the sideline ids 157 (566-572, 1.2-1.4 m off) and 37 (578-608, 1.4-1.7 m off,
the camera's +1 m wander inside those numbers) stand near him -- one of them may be Thuney's later sideline
fragment and the other a neighbour; the sideline film decides (diag/pocket/sl_boxes_thuney_tail.png).
The sideline film after 565 (diag/pocket/sl_boxes_thuney_tail.png): Thuney (the red lineman engaged with BAL 98) has NO
sideline box at 572-614 -- 157, 37, 205 and 211 sit on other red men. So 139 drawn from the endzone alone on 566-590
is right, not a twin; v77 was missing him there. The KC 11.23 surplus is elsewhere and the film, id by id, is the
only ruler for it. **v78 = CURRENT BEST.** Suite 1243 passed; tree clean; everything pushed.

**The KC surplus, id by id on the film (00:40 machine clock; diag/pocket/kc_boxes_play.png, sl_boxes_66_49.png).** Frames
with 12 or more KC bodies: 61 of 213, all after the throw. The KC sideline boxes drawn on the film at 460/500/540/580:
every box on a red man except (a) 66, a 21-row fragment whose boxes sit at x 1913 -- the frame's right edge -- with
kit votes against KC (a stranger clipped at the border; the edge rule let it through), and (b) 12, whose late boxes
(581-609) sit on the same lineman as 76's (both boxes on one man at 590 and 604; 12's box is the upper part). 49 and
76 are two men (checked at 576). The bench people 51/47/52 carry KC labels but the off-field rules already drop them.
v79 chain (chain_v79.sh, running): 66 teamless (the loader drops teamless fragments), `08z --keep 76 --drop 12
--frames 581 609`, 08x, dump, 07l, render, sideline blend. Expected: census KC 11.23 -> about 11.0.

**v79 = CURRENT BEST (02:45 machine clock).** diag/play_001_v79_hifi_720.mp4 + _sideline_blend.mp4. = v78 + 66 dropped
(teamless) + 12 folded into 76 on 581-609. Rulers 395-607: steps 5, hops 0, census 0.99 (KC 10.93 / BAL 10.80) --
under 1.0 for the first time. Film checks (diag/catch/pocket_check_v79.png at 540/580/600, catch_check_v79.png at
562/608/614): every avatar on its man, Thuney beside 98 at 580, the pile as before; the reader agrees with ball.json.
The KC count by frame: 11 on 112 frames, 12 on 44 (395-434, right after the snap: 3 5 9 11 12 17 19 37 38 74 80 204
-- 17 the centre ends at 420 while 204 runs on, so the two are twins over 395-420; 19 and 166 are 6- and 8-frame
fragments), 10 on 51 and 9 on 5 (runs 435-442, 455-474, 501-508, 534-547, 602-607: a KC man missing). Next, in
this order, each against the film: 17/204 at the snap, the 19/166 fragments, then who is missing on the under-11 runs.

**The centre's post-snap twins (03:00 machine clock; diag/pocket/sl_boxes_centre.png).** At 396, 408 and 420 the boxes
of 17 (the centre, sideline to 420), 204 (sideline 210-499; pre-snap he is the quarterback's twin that qb_hold takes
out) and 166 (sideline 291-431) all sit on the same red lineman -- the centre after the snap; at 440 only 204 is
left on him. 19 (to 400) is the neighbouring lineman's fragment. v80 chain (chain_v80.sh, running): `08z --keep 17
--drop 204 --frames 395 499` and `--drop 166 --frames 395 431` (17 keeps the centre's identity and 08y's centre pick
at the snap), 08x, dump, 07l, render, blend. Expected: the 12-KC frames right after the snap go to 11.

**v80 REJECTED and reverted (03:45 machine clock).** The centre folds (204 and 166 into 17) are true on the film, but the
rulers went the wrong way: live steps 5 -> 11 (139 at 453-457, "handover"), census KC 10.93 -> 10.87, the 12-KC
frames after the snap 44 -> 40 only. What happened: with 17 now the long id through 435-499, the twin-stretch rule
(the shorter-lived of two same-team bodies within 0.4 m loses the stretch) dropped Thuney 139 on 435-442 instead
of the centre 204 on 435-474, and 139's re-entry made the steps. The rule's loser choice is the wound: two
engaged linemen stand 0.4-0.5 m apart on the turf and the depth error pulls them inside 0.4, so whichever is
shorter-lived vanishes for a stretch. The sideline box-overlap gate (TWIN_BOX_IOU_MIN 0.3 / 0.15, A/B on the v80
data: census 0.991 -> 0.981 -> 0.991, steps 11 unchanged) does not separate them either -- a guard and the
centre overlap in the sideline image because they sit at different depths on the same line of sight. Kept
opt-in (None). The fourteenth correction that lost to what it corrected. Restored tracks / keypoints / identity /
pose caches to the v79 state (the .pre_fold.6 and matching .pre08v backups); v79 stays CURRENT BEST. The
right fix is a twin rule that asks the FILM per frame (two boxes, two jersey reads) rather than a distance; until
then the 12-count frames after the snap (395-434) stay.
Restored state re-measured (07l v79r): steps 5, hops 0, census 1.04 (KC 10.88) against v79's 0.99 (KC 10.93) -- the
loader's drop lists match to one frame (204 435-475 vs 435-474), the 11 body-frames of difference sit in the pose
caches restored from the backup taken one remap later; the tables and identity are v79's. Current best stays v79 as
rendered. A two-camera box-overlap gate for the twin-stretch rule (TWIN_BOX_IOU_MIN: any camera seeing the pair's
boxes apart keeps both men -- two engaged linemen overlap in the sideline image but not in the endzone's) is
committed opt-in and under A/B (scratchpad/probe_twinbox_ab.py, None vs 0.3).

**ADOPTED: the twin-stretch rule asks both cameras (04:30 machine clock).** TWIN_BOX_IOU_MIN 0.3: a same-team pair
within 0.4 m is left alone when either camera has boxes for both that overlap less than 0.3. A/B on the v79 data
(scratchpad/probe_twinbox_ab.py): census 1.042 -> 0.920 with steps 5, hops 0, jitter and both ankle rulers
unchanged; the centre 204 is back on 435-475 and 166 keeps 392-409. The sideline-only version had done nothing
(0.991 -> 0.981) because a guard and the centre overlap in that image at different depths; the endzone camera
sees them side by side. Full suite gating the commit; v81 chain (dump, 07l, render, both blends) follows.

**v81 = CURRENT BEST (04:10 machine clock).** diag/play_001_v81_hifi_720.mp4 + _sideline_blend / _sideline_sbs /
_endzone_blend. = v79's data + the two-camera twin gate. Rulers 395-607: steps 5, hops 0, census 0.92 (KC 11.05 /
BAL 10.81), root jitter p90 0.026; the film reader agrees with ball.json. Film checks: diag/catch/line_check_v81.png
(sideline camera, 440/456/472: the engaged line, Kelce 87 and 65 on their players, the centre's cluster whole) and
ez_line_v81.png (endzone camera, 440-500: 62, 52 and 15 on their numbers). Suite 1245 passed, everything pushed.

**The BAL deficit, id by id on the film (04:25 machine clock; diag/pocket/bal_boxes_play.png; yellow boxes drawn,
red boxes not).** BAL counts 395-607: 11 on 126 frames, 10 on 43, 9 on 15, 12 on 26. The under-eleven runs: 489-495
(198 not drawn -- rightly, its box coincides with 40's and 194's on one rusher, IoU 0.66-0.75), 530-563 (171 dropped
as 55's twin over 331-566 -- one man, the defender on the receiver), 588-599 (84, 206). At 492 the sideline film
shows eleven Ravens and the timeline's ten drawn ids sit on ten distinct men: the eleventh has NO sideline box at
all -- a rusher hidden behind a lineman in the pocket. At 546 the same: 180 dropped at the far numeral (a hole rule)
and an unboxed rusher at the pocket's edge. So the BAL deficit is mostly DETECTION (occlusion in the pocket), not
identity. The endzone camera sees the pocket rushers side by side; the pre-snap line_vouch (an endzone-only body on
the line with no sideline-backed teammate within 0.7 m across is drawn) is the shape of the fix for the play
window: vouch an endzone-only body in the pocket region during the play when no sideline-backed body of its team
stands within the across radius. Next experiment, measured on the census and the film.

**Pocket vouch: MEASURED AND REJECTED (05:00 machine clock).** endzone_only_rule.pocket_vouch (line_vouch's test on the
play frames in the pocket region, a revival at 10 vouched frames) on v81's data: across 0.7 m -> census 0.92 -> 1.085
(263 body-frames vouched on 25 ids, revived 111, 112, 113, 140, 145, 170 -- KC copies among them: 170's endzone rows
are Mahomes', 111 is a lineman's second endzone id -- so Kansas City gains ghosts while the unboxed Raven is still
not among the endzone ids that survive the region test); across 1.0 m -> 0.93, revived 112, 145, 170, nothing gained.
Steps 5 and hops 0 either way. The fifteenth correction that lost. The constant stays None; the code and test stay.
The eleventh Raven at 492 and 546 is a DETECTION hole in the pocket: the fix is a detector that finds a man behind
another (or the endzone rows paired to their men, so the two-view id carries him), not a rule on the timeline.

**State at the end of the night (05:00 machine clock, 2026-09-19).** CURRENT BEST v81: diag/play_001_v81_hifi_720.mp4
with _sideline_blend / _sideline_sbs / _endzone_blend. Play window 395-607: steps 5, hops 0, census 0.92 (KC 11.05 /
BAL 10.81). Suite 1245 passed. Tree clean, everything pushed. Since the user's question: the ball to the right man
(three ids folded), the film reader (09a) with its gates and 08y --from-film, the tackle (carrier and tacklers), the
quarterback's endzone rows and identity, Thuney paired across cameras, the edge fragment and a late twin out, the
twin-stretch rule asking both cameras. Rejected with numbers: the per-frame endzone veto, the centre fold (until
the twin rule is fixed for it), the pocket vouch. Open, in value order: (1) the sideline detector's occlusion in the
pocket (a Raven unboxed at 492 and 546); (2) the 12-KC frames right after the snap (17/204/166 are one man; fold
them once the twin rule's loser choice cannot punish the neighbour -- re-measure now that the two-camera gate is in);
(3) the endzone camera's play-time depth wander; (4) the pile's lying poses are synthesised.

**The centre fold re-tried with the two-camera gate: still rejected (04:30 machine clock).** chain_v82.sh folded 204
(395-499) and 166 (395-431) into 17 on v81's data, measured, and restored on its own gate: live steps 5 -> 11 (two
handovers: the joins at 395 and 431, where 204's box and 17's box on the same man sit a few tenths apart and the
fold makes that offset a step), census 0.92 -> 0.94 (KC 11.05 -> 10.92: the 12-count frames after the snap are
gone, but the loss of the joins' frames and the twin rule's other drops leave him under). The gate no longer
punishes the neighbour (139 is not in the twin list), so what remains is the join itself: a fold of two ids on one
man needs the boxes reconciled at the seam (an offset blend over a few frames), not a cut. Tables restored to v81.
Note: with the two-camera twin gate on, 08x's motion-detected snap reads 393 (v79's tables read 395 without it -- the
drawn set at the line changed by two frames); v81 was rendered on snap 395 / start 215 and ball.json's snap segment
is 395, so play_end.json is pinned back with `08x --snap 395` to keep the state coherent with v81.
