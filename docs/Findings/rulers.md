---
type: findings
topic: rulers
period: 2026-09-09 to 2026-09-12
entries: 5
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Rulers (how results are measured)

The measurements used to judge a change: plausibility rulers, the count of bodies per team (census), overlays, and the footage as the final judge.

5 entries from 2026-09-09 to 2026-09-12, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Census](../Concepts/census.md), [Reprojection error](../Concepts/reprojection-error.md), [Plausibility rulers](../Concepts/plausibility-rulers.md), [Footage review](../Concepts/footage-review.md), [Referees](../Concepts/referees.md)

## The footage as the ruler (2026-09-09)

The user on v24: still jittery, arms all over the place, compare against
the All-22 footage. `scripts/05q_overlay_footage.py` projects the timeline's
bodies (the states 05k renders, placed the same way) through the sideline
camera onto the footage as skeletons, with the 2-D keypoints as dots;
`--player ID --start F --count N --step S` gives one body over consecutive
frames. `diag/overlay_v24/`. What it showed at once:

- Refit-placed bodies 1.5-3 m toward the camera on some frames (ids 2, 4:
  feet 50-76 px below the real ones): `place_from_refit` accepted a
  record's pelvis up to 3 m from the box point; MAX_REFIT_SHIFT_M is 1.0
  now (the box point sits 0.52 m from a right pelvis at the median).
  Median over all states: ankles 13 px above the box bottom, pelvis 0.24 m
  beyond it.
- A lineman in his stance (id 12, frames 130-151): the sideline keypoints
  do not move, the skeleton's torso and arms swing frame to frame. The
  fused refit reprojects into the sideline camera at p50 8.4 px, p90 15
  (arms p90 19) -- the triangulation's own level, 10 cm on a 140 px body
  -- and the 3-D fit follows every spike of it. The keypoints are the
  stable signal; fitting them directly in both cameras with the temporal
  term, instead of triangulate-then-refit, is the next step.
- The QB (id 5, frames 180-201, standing still in the shotgun): the
  keypoints sit on him, the skeleton's feet reach 40 px below his shoes --
  the two-view refit places him 0.2-0.5 m toward the camera, because the
  endzone track paired to him is Pacheco's (the pairing's ~1 m ambiguity
  between two backfield players), so both his triangulated pose and his
  placement mix two people. The one-view fit would put him on his own box
  point (unbiased against a right pelvis, 0.52 m at the median).

Two experiments, judged on the same rulers (sideline reprojection per
record, the merged cache's jitter, the boundary ruler, and the id 12 /
id 5 strips): `05p --two-view` (every two-camera player fitted straight
to both cameras' keypoints, 05f's records replaced; probe on ids 12 and 5:
sideline 8.1 px, endzone 8.5 -- the views disagree by that much through
the calibration, no fit hugs both) and `05p --one-view-only` (every body
from the sideline alone; the render camera sits on the sideline's side,
where the one-view depth error is foreshortened). Results:

- two-view direct fit (00:19-00:48): 23 players, only 1440 of 1976 frames
  under the 20 px gate (the two views disagree past it on a quarter of the
  frames), sideline 8.6 px / endzone 8.7 -- the same as 05f's chain; the
  id 12 strip is pixel-for-pixel the v24 one: the wobble is the two views'
  disagreement, and averaging the views cannot remove it. Not adopted.
- one-view only (00:48-01:18): 52 players, 5166 records, sideline
  reprojection p50 2.0 px, p90 4.8. The strips (`diag/overlay_oneview/`):
  the lineman's skeleton holds still on him, the QB stands on his own feet;
  a walking corner (id 2) still had his skeleton 60 px below his feet --
  the timeline placed him on the two-camera AVERAGE (1.9 m endzone offset
  on that pair) and refused the record's pelvis against it, and the fit
  itself let the reprojection drag the pelvis 0.38 m off the box point
  along the ray (place_weight 1). ADOPTED with two changes: the timeline
  places every id the sideline sees on the sideline's own point (100 % of
  records placed, median shift 0.38 -> ?), and place_weight 10 holds the
  pelvis on the box point (the run with it, 03:07-03:28: 5166 records at
  1.9 px p50 / 4.7 p90; the corner's skeleton now stands on his shoes,
  `diag/overlay_oneview2/player_2_f300.jpg`). Pipeline: ONE_VIEW=1
  (05p --one-view-only); the triangulation and 05f stay as the validation
  reference. The two-view depth is given up where the pair was right; the
  render camera on the sideline's side foreshortens that error.
- Even with the pelvis held, every skeleton's feet sat ~15 px below the
  shoes (the QB, the corner, the lineman alike). Measured: the detection
  box ends 16.7 px below the lower ankle keypoint at the median (138 px
  boxes); the ankle is 6 px above the sole, so 11 px is the detector's
  margin -- 0.078 of the box height -- and through the camera it is ~0.15
  m toward the lens for every body. `ground_positions` now takes the foot
  at bbox_y2 minus 0.078 of the box height (BOX_MARGIN_FRAC); the fit and
  the timeline share it. Run 3 (the fit on the corrected points, redone
  after a session death): 5166 records at 1.9 px; the corner's and the QB's
  skeletons now sit on their bodies with the feet on the shoes
  (`diag/overlay_oneview3/`). v25 (16:39, `diag/play_001_v25_hifi_720.mp4`,
  sent; strip against v24 `diag/p1_v24_v25_strip.jpg`): 24 bodies a frame,
  postures follow the footage, no arm arcs on the line. **v25 is the
  deliverable**; the pipeline reproduces it with ONE_VIEW=1 (default).

**The runner toward the camera** (2026-09-09 evening, strips on v25's
cache, `diag/overlay_v25b/player_9_f260.jpg`): id 9 running toward the
sideline camera gets a collapsed skeleton from frame 266, legs splayed at
the lens, while the keypoints on him look like a runner. One view cannot
tell short, foreshortened legs from legs pointed at the camera, and
nothing forbade the impossible angles. `pose.pose_bounds`: per-component
body_pose bounds at the 2nd/98th percentile of the two-camera refit
records (2963, 24 players); the one-view records sat outside them on 54 %
of components. As a soft prior (`bounds_weight`): weight 1 does not fix
the runner (the reprojection still wins), weight 10 neither: the legs
still splay (`diag/overlay_bounds_w10/`) -- the two-camera records the
bounds come from allow a hip abduction of 1.0 rad themselves (their own
noise), so the range forbids nothing that matters. Not adopted. The
principled fix is the second camera: the endzone sees motion along y
across its image, exactly where the sideline is blind; at a LOW weight it
would act only where the sideline's constraint is null. Measured (probes
on ids 9 and 12, strips in `diag/overlay_anat/`, `diag/overlay_ez0.3/`):
- anatomical joint limits (hips, knees, ankles, elbows; weight 10): the
  runner straighter for two frames, legs still out from frame 275.
  Insufficient alone.
- the endzone at weight 0.3 in the two-view fit: the runner's legs are
  UNDER him on every frame, the arms a little wide; the lineman holds
  still with legs and torso on the keypoints, but his head is drawn as a
  spike up and back -- the endzone's head keypoint (the back of a helmet)
  pulled it. Only 95 of 194 frames passed the combined 20 px gate (the
  endzone's residuals are 17 px by design at that weight). Two changes:
  the gate is the sideline's reprojection alone, and the second camera
  does not vote on the neck and head. Re-probe: PENDING.

**The keypoints themselves jump.** Sideline wrists (confident ones):
frame-to-frame motion p50 1.6 px, p90 7.5, p99 44 px, max 94 -- a
left/right swap or a miss for one frame -- and 30 % of wrists sit under
0.5 confidence (hips and knees never do). Every fit that follows the
keypoints throws the arm there and back. `pose.keypoint_filter.
reject_outliers`: a confident point further than 18 px from the median of
its neighbours' pairwise midpoints (constant motion of any speed sits on
every midpoint; a one-frame spike does not) gets confidence 0 -- the fit
ignores it and the prior holds the joint. Play 1: 1.4 % of confident
keypoints rejected (wrists 3.3 %), wrist p99 44 -> 17 px, max 94 -> 37.
Applied in 05p (both passes) and 05n.

## The endzone overlay, and what it showed (2026-09-11)

The user asked which camera the overlay uses. It used the SIDELINE alone, and
that is a blind ruler for the one axis that matters most: the sideline looks
down the line of scrimmage, so a body a metre too near or too far lines up in
its image exactly as a right one does. 05q now draws into either camera (the
endzone clip runs at f + clip_offset, so the label says which film frame it is)
and `--cam both` puts them side by side. Colours: GREEN the detector's 2-D
keypoints in that camera's film, RED a fitted Kansas City body, WHITE a fitted
Baltimore body, cyan the track id.

The first endzone frame showed three things the sideline overlay had hidden:

1. Two officials and a sideline marker are drawn as Baltimore players. All the
   drawn endzone-only ids are non-players: 85 and 89 and 108 are officials
   (85 wears 83 on his back, so the jersey reader gave him Baltimore's Qadir
   Ismail) and 109 is a marker. The frustum test in endzone_only_rule keeps
   endzone-only ids the sideline could not have seen, which is right for a wide
   receiver and wrong for the referee standing 14 m behind the ball.
2. The counts are wrong: the render draws a median of 9 Kansas City bodies and
   13 Baltimore ones, where the truth is 11 and 11. Bodies per team per frame is
   the sharpest ruler this project has had; it was never being looked at.
3. Several one-view bodies sit up to a metre off in depth, visible only here.

## Counting bodies per team: the ruler, and what it says (2026-09-11)

Eleven a side is the one number in this problem that is known without labelling
anything, and nothing was checking it. Per frame, from the snap onward, play 1
draws |KC - 11| + |BAL - 11| = 2.9 bodies wrong on average, and exactly eleven a
side on 2 frames of 361. The median hides two different faults pulling opposite
ways:

- AT THE SNAP Kansas City is three short. The sideline detector has 8 boxes for
  their 11 players; the endzone camera has 11. The men it loses are the linemen
  in the pile at the line of scrimmage. The render can only draw what the
  sideline tracks, so those three are simply absent.
- LATER IN THE PLAY both teams run one or two OVER, as the tracker re-acquires a
  player under a new id and both are drawn.

Tried and rejected (2026-09-11): keeping an id beyond its sideline span wherever
the sideline has no body within 1.2 m of it. It is the right idea for the first
fault -- four Kansas City players are seen by the endzone through a sideline gap
-- but it admits a ghost for every player it recovers: 2.93 -> 3.01. The
capability stays in endzone_only_rule (side_ground=), unused.

The honest read: the count is limited by the sideline DETECTOR's recall in the
trenches, which is upstream of everything in the render. That is the next place
to look, not the render's rules.

Measured there (2026-09-11, yolov8x at imgsz 1920 on play 1's sideline, twelve
frames): person boxes at the detector's 0.35 threshold against lower ones --

    frame   0.35  0.20  0.15  0.10
    160-400  19-23  19-26  19-26  19-27   (the play: 22 players + 2-4 officials)
    440-600  26-42  28-54  31-63  34-76   (the camera pans, the crowd enters)

At frame 300, the snap, the two boxes that appear only below 0.35 are a Kansas
City lineman half hidden behind another, at confidence 0.17 and 0.13 -- exactly
the men the census says are missing. But a blanket threshold drop is not the
answer: late in the play it triples the detections as the sideline crowd comes
into frame. The shape of the fix is to fill the GAPS OF EXISTING TRACKS: where a
track has no box on a frame inside its own life, look for a low-confidence
detection near where the track should be, and take it only there. That keeps the
threshold high everywhere else and creates no new identities.

## The census metric was scoring the aftermath (2026-09-12)

`|KC-11| + |BAL-11|` has been averaged from the snap to the END OF CLIP, and roughly half of it is the
post-play crowd rather than a defect:

    window                frames   KC mean   BAL mean   error   exactly 11/11
    current metric           360      11.5       12.0    2.82      10 of 360
    the play only (300-460)  160      11.1       11.7    1.98       9 of 160
      the snap  (280-340)     60       8.9       11.7    2.85       0 of  60
      the run   (340-460)    120      11.8       11.8    1.79       9 of 120
    after the whistle        100      12.8       12.6    3.46       1 of 100
    late (560-660)           100      11.0       11.7    3.52       0 of 100

So play 1's real body-count error is **1.98 a frame, not 2.84**, and every figure quoted above (2.95,
2.94, 2.84) includes 200 frames of players and staff walking onto the field after the whistle. Score the
play, not the aftermath. **The snap remains the one phase this does not explain away** -- KC 8.9 against
a truth of 11, 0 of 60 frames correct -- and that is the pile, whose only surviving route was a detector
that separates overlapping bodies in the sideline view.

**That route is closed too, and the film closed it.** Projecting the six Kansas City men the endzone
resolves in the line box but the sideline does not, onto the sideline plate at frame 300, and drawing
every box the detector actually found: **not one cross lands on bare grass.** id 74's falls on a lineman
already boxed twice; 38 and 22 land in the overlapping tangle of boxes 17, 25 and 82; 86 and 37 land on
bodies inside boxes 11 and 17; id 9's lands at the feet of a man the detector did find. The sideline
detector is not MISSING these men -- it is **merging** them, because from the sideline the line of
scrimmage is viewed edge-on and several players occupy one box. The endzone's extra resolution comes
from seeing that same pile face-on, not from a better detector.

So no detector threshold recovers them: separating bodies that overlap this completely needs instance
segmentation or a pose-driven split of a shared box, which is a different project, not a tuning change.

**The pose model was the cheap version of that split, and it does not reach them either.** 05m already
runs `yolov8x-pose.pt`, and a pose model returns one skeleton per person it finds, so a skeleton inside a
merged box would be the split for free. Tested per man at the snap: of the six Kansas City men the
endzone resolves and the sideline lacks, exactly **one** (id 38) has a pose skeleton nearer than any
existing box. No `-seg` weights are on disk, so true instance segmentation is a download plus rework of
every box-keyed stage downstream.

**A correction to my own first reading of that test.** The single-frame version appeared to show three of
the six "already inside a tracked box", which would have meant the men were detected and merely
unmatched -- a pairing problem, not a detection one. That was a pixel-versus-field artifact: it measured
to a box's bottom-centre in pixels, while a merged box yields **one** id and therefore **one** ground
point, so a cross can land inside a box with no separate body there at all. Repeating it on the field,
across frames 280-345: **69 of 72** missing-KC instances have no sideline body within 0.6 m under any id
or team, and only 3 do. The men really are absent from the sideline's body set, exactly as merging
predicts, and the closure stands.

**And the ghost rule is not what deletes them either -- measured and rejected 2026-09-13.**
`endzone_only_ids` drops an endzone-only id for its WHOLE life on a >= 50 % frustum vote, with no test of
whether the sideline actually has a body there, while its sibling `beyond_sideline_span` carries exactly
that test (`SAME_BODY_M = 1.2`). The asymmetry looked like the snap deficit's cause. It is not. Giving
`endzone_only_ids` the same-body test keeps 13 of 35 ghost ids back and the census gets WORSE on every
window: snap 2.82 -> 3.18, play 1.98 -> 2.23, run 1.79 -> 1.94, aftermath 3.44 -> 4.00, whole clip
2.89 -> 3.21. Kansas City at the snap does not move at all (8.89 either way), because none of the 13 kept
ids live at the snap: 11 of 13 are Baltimore, and the two Kansas City ones begin at frames 457 and 538,
after the play. They add surplus to a team already over eleven (BAL 11.70 -> 12.07). Eighth entry in
corrections-must-beat-what-they-correct.

The negative is the useful part: the six missing Kansas City linemen are NOT excluded as endzone-only
ghosts. Their endzone detections must reach the timeline under ids that also carry sideline rows, so no
endzone-only rule ever classifies them. The per-frame mechanisms that can still delete a body at the snap
are `beyond_sideline_span` (1680 body-frames left out on this play) and the timeline's own `dedupe_frames`:
a state the SIDELINE detected that frame is protected (the 2026-09-08 fix), but a state the ENDZONE alone
sees dedupes against every kept state inside an axis-aligned `ONE_VIEW_DEPTH_M` x `ONE_VIEW_ACROSS_M` =
4.0 x 1.5 m box in FIELD axes. On the line of scrimmage every lineman shares x and they stand about a
metre apart in y, which is inside that box -- the 7th correction-must-beat case recurring in the other
camera, since that fix protected only sideline-detected states. This also fits the 0.6 m number above
rather than contradicting it: a man 1.2 m from the merged body is genuinely "no sideline body within
0.6 m" and still inside the dedupe box.

**That dedupe hypothesis is measured and rejected too (same day).** The one-view box kills ZERO Kansas City
states in the snap window. Of 500 dedupe drops in the clip, 42 fall in 280-345 and every one is the
`interp` branch at `INTERP_DUP_M` = 0.4 m (35 Baltimore, 7 Kansas City) -- a second fragment id standing on
a body the sideline detected, which at 0.4 m is the same man. Sweeping the across-radius 1.5 -> 1.0 -> 0.8
-> 0.6 m changes the drop count not at all (500 every time) and every census window to the digit, so that
branch binds nowhere on this play. The reason is `_nearest_views`: an id with any sideline record within
`MAX_GAP_FRAMES` inherits "sideline" among its views and is then either protected as detected or deduped as
interpolated, so almost nothing reaches the one-view box. The instrument passed its own validity gate --
the instrumented copy of `dedupe_frames` reproduced the real run exactly (0 frames differing, identical id
sets, 500 drops both).

**Both exclusion routes are now closed, and what is left is bookkeeping.** The six men are in the endzone's
detections, are not endzone-only, are not excluded by any rule, and are not deduped -- so their endzone
rows hang off global ids whose SIDELINE rows belong to other men. Because `side_ground` overwrites `ground`
(play_timeline.py:327-329), such a body is drawn where the sideline puts its own man and the endzone's extra
detection adds no body at all: ten endzone men plus eight sideline bodies still render eight. That is the
bookkeeping figure already recorded -- 21 sideline ids and 24 endzone ids at frame 300 sharing only 12 --
and it is the pairing being locally wrong across a window where the track as a whole is right, which
`mispaired_ids` cannot see because it gates on the MEDIAN distance over a whole track and a 60-frame error
does not move a median. Next test: per frame at the snap, the gap between a global id's sideline and
endzone ground points; where it is large the endzone row is a different man and deserves an id of its own.

**THE SNAP DEFICIT IS RECOVERABLE, and two claims above are now wrong (2026-09-13).** Two rules were each
masking the other, which is why every single-rule measurement read as a no-op:

  - `beyond_sideline_span` drops ids 74/38/22 at the snap, so they never reach dedupe. Measuring dedupe
    alone therefore showed 0 Kansas City states killed by the one-view box and no sensitivity to its
    radius -- true of the shipped configuration, FALSE of the mechanism. The claim above that the box
    "binds nowhere on this play" holds only while the span rule deletes its inputs first.
  - Give the span rule its same-body test and those 751 body-frames reach dedupe, where the one-view box
    kills every one (id 74 by id 1 on 65 of 65 frames, id 38 by id 4, id 22 by id 13; `n_duplicates`
    500 -> 1585). That is why the span fix alone measured +0.00.

Corrected together, the census moves for the first time. Kansas City at the snap 8.9 -> 10.8, frames
exactly eleven-a-side at the snap 0 -> 23, and Baltimore never moves (11.7), so the change is targeted:

    configuration          snap   play    run  after   full
    baseline (shipped)     2.82   1.98   1.79   3.44   2.89
    span fix only          2.82   2.03   1.86   3.53   2.90
    span fix + across 1.0  1.20   1.73   2.00   3.57   2.52
    span fix + across 0.8  0.93   1.67   2.01   3.66   2.43

**The footage and a control group say ids 74 and 38 are real men, and 22 and 86 are not.** Paired Kansas
City ids agree between cameras at p50 **0.42 m** (n = 380 rows in 280-345). Ids 74 and 38 stand **1.44** and
**1.24 m** from the nearest sideline body, and the gap is mostly ACROSS the field (|dy| p50 1.19 m for
both), which is the direction a formation's linemen separate -- not along the endzone's blind depth axis.
Ids 22 and 86 come in at 0.65 m, inside the control distribution, and contributed only 1 and 10 frames.
Zoomed crops agree: box 12 plainly spans two to three Kansas City players with a single ground point inside
it, the merged box this document describes.

**NOT SHIPPED, because the fix as swept is a blanket threshold and it over-admits.** The run window
regresses 1.79 -> 2.01 with Kansas City at 12.1, over eleven: a smaller dedupe box recovers real men at the
line and admits copies once the players spread out. The principled form is the same-body test INSIDE the
one-view box -- an endzone-only state is a copy only where the sideline actually has a body -- rather than
a narrower box, which is the same lesson as `beyond_sideline_span` carrying `side_ground`. Measure that
before changing any constant.

**And that principled gate is measured and REJECTED -- it is worse than the blanket threshold (2026-09-13).**
Requiring the sideline to have a body within `same_body` before calling an endzone-only state a copy
regresses the run to 2.24-2.50 against a baseline of 1.79 (the blanket radius gave 2.00), and it breaks what
the blanket never touched: Baltimore goes 11.7 -> 12.7 at EVERY window, a whole extra body a frame, with
frames exactly eleven-a-side collapsing to 2-3 where the blanket at 0.8 gave 41. Whole clip 2.98-3.21
against 2.89 baseline, a net loss.

The reason, plain in hindsight: the gate replaced "near a kept state" with "the sideline has a body nearby",
so a state FAR from any sideline body is kept -- which is exactly the play-2 endzone ghosts strung along x
that `ONE_VIEW_DEPTH_M` was built to kill. The rule I called principled readmitted the precise failure the
box exists for. Ninth entry in corrections-must-beat-what-they-correct. A second tell, worth remembering:
`box AND sideline` and `sideline only` print identical numbers at every threshold, so once the same-body
test is added the 4.0 x 1.5 m box never binds -- the two conditions are not independent and pairing them
buys nothing.

So the only configuration that helps Kansas City without disturbing Baltimore is still the blanket
`span fix + across ~1.0`, and its run regression (1.79 -> 2.00) is the open question. Diagnose which bodies
that window gains before shipping anything: if they are copies, a discriminator exists; if the control test
calls them real men while truth is still eleven, something else is wrong.

**Measured: the run regression is NOT caused by the change, and the census is the broken instrument there
(2026-09-13).** The bodies that window gains under `span fix + across 1.0` come to 41 body-frames over 121
frames -- **0.34 a frame** -- and by the control test most are real men: id 74 for 33 frames at |gap| 1.40 m
with |dy| 1.30 (the same man the snap analysis found), plus ids 38, 54 and 19 for one or two frames each.
Only ids 11 and 25 are copies, 4 frames between them at 0.26 and 0.19 m, inside the control distribution.

The arithmetic that matters: baseline Kansas City in the run window is already **11.79** against a truth of
eleven, so roughly **0.8 phantom Kansas City bodies a frame exist before any change**. Adding 0.34
mostly-real men lifts |KC - 11| from 0.79 to 1.13, which reads as a regression while the render is getting
MORE correct. A census cannot referee a change that adds true bodies to a count that is already too high.

So the run is not a reason to withhold the dedupe fix -- but it is not yet a reason to ship it either,
because the pre-existing surplus is unexplained and could share a cause with the bodies being added. Find
the phantom first: which drawn Kansas City bodies in 340-460 stand within the control's 0.95 m of another
drawn Kansas City body, and whether any id labelled KC is misassigned. Note the surplus is phase-specific --
8.89 at the snap (a deficit), 11.07 over the play, 11.79 in the run -- so it grows as the players spread
out, which is the opposite of what a merged-box fault would do.

**First attempt at that measurement was invalid, in two ways worth recording.** It counted PAIRS of drawn
Kansas City bodies closer than 0.95 m and got 2.31 a frame, which cannot be compared with a 0.79 surplus:
pairs overlap -- (17, 25), (25, 33) and (19, 25) all share id 25 -- and the phantom count is bodies minus
CLUSTERS, not pairs. Second, 0.95 m was the p90 of the CROSS-CAMERA control (the same id seen by both
cameras), which is not a "two different teammates" radius at all; teammates legitimately stand about a metre
apart, so that test declares real players duplicates. It is the 0.6 m clustering artifact from earlier in
this document wearing a different hat. Any cluster radius here has to be one below which two real players
cannot both stand (~0.4-0.5 m), and even then same-team clustering during a run is a weak instrument.

**What does survive: fourteen ids are drawn as Kansas City in the run window.** Nine run near-continuously
(111-121 of 121 frames: ids 3, 5, 9, 12, 37, 11, 25, 38, 17) and five are partial -- 80 (84 frames), 33
(83), 19 (75), 39 (69), 74 (52). With truth at eleven, the surplus rides on the partial ids, which is the
signature of fragments rather than of a threshold.

Two leads, neither yet confirmed:
  - id 39 carries jersey 6 and a roster name that is a DEFENSIVE back. Kansas City has the ball on this
    play, so a safety cannot be on the field; if the roster confirms the position, that is 69 frames of a
    body that should not exist. Verify against the pipeline's roster rather than from memory.
  - id 74's "defence side of the line" flag is an artifact: its mean x is 0.69 m past the line of scrimmage,
    which is where a tight end on the line stands. Not evidence, and not a reason to doubt the footage and
    control-group verdict that id 74 is a real man.

**The run surplus is localised and it is an IDENTITY fault, not a geometry one (2026-09-13).** Counting
clusters rather than pairs: bodies 11.79 a frame, clusters 11.56 at 0.40 m and 11.29 at 0.50 m, so only
~0.2-0.5 of the surplus is one man counted twice and the rest stand genuinely apart. (At 0.95 m clusters
read **9.69**, below truth -- independent proof that radius merges real men and that the earlier pair-based
reading was invalid.) The surplus is not spread across the window either: frames 340-380 read 10-11 bodies,
correct, and it climbs to 13-14 across **390-430**. Two ids carry it: id 39 adds +1.41 bodies a frame when
present and id 80 adds +1.52, against 74 (+0.75), 19 (+0.50) and 33 (+0.26).

Checked against the 2024 roster, those ids' jerseys do not belong on the field:

    id 39  jersey  6  Bryan Cook          DB   -- defence, and Kansas City has the ball
    id 38  jersey 55  Uche / Bozeman      LB   -- defence (Bozeman is practice squad, status DEV)
    id 19  jersey 67  no Kansas City player wore 67 in 2024
    id 80  jersey  0  P80  -- NO jersey was read for this id at all (corrected below)
    id 74  jersey 83  Noah Gray           TE   -- correct
    id 25  jersey 76  Kingsley Suamataia  OL   -- correct
    id  5  jersey 10  Isiah Pacheco       RB   -- correct

**A wrong jersey does not make a body false, and the two failures need separating.** id 38 was validated as
a real man by the control group and the footage; what is wrong there is its identity, not its existence. But
a real body with a wrong TEAM label corrupts the census directly, because the census counts by team -- so
team labelling is now a third suspect instrument, alongside the pair-versus-cluster error and the borrowed
radius. Before trusting any census number by team again, establish how often the team label is wrong.

**Cross-team double-drawing is NOT the explanation, and the census-by-team survives (2026-09-13).** At frame
420 the id-39 cross sat beside Baltimore body id 4, which would mean one man drawn under two team labels --
inflating BOTH counts, matching KC 11.79 and BAL 11.84 both sitting over eleven, and invisible to a dedupe
that never looks at team. Measured over 380-440 it is false: id 39's nearest opposite-team body is **p50
1.89 m** (id 4 is its commonest neighbour but on 23 of 54 frames at ~1.9 m), and id 80's is **p50 3.16 m,
min 3.06 m** -- nowhere near a Baltimore body. The picture was single-frame proximity, not co-location.

Across the whole clip, cross-team pairs closer than 0.30 m are **1.0 %** of 14 397 drawn body-frames and
closer than 0.40 m **1.4 %**. That is not systemic, so every census-by-team figure in this document stands,
**including the snap 8.9 -> 10.8 result**. It also cannot explain a 0.79-a-frame surplus, which would need
~6.7 % of the Kansas City bodies.

What the same probe did find: **id 19's nearest SAME-team body is p50 0.58 m, min 0.17 m** -- inside the
control distribution, so that one is a genuine double. Accounting for the 0.79 surplus so far: same-team
near-duplicates account for ~0.2-0.5 of it (clusters 11.56 at 0.40 m, 11.29 at 0.50 m against 11.79 bodies),
leaving ~0.3-0.5 as bodies standing genuinely apart. The remaining candidate is officials or staff drawn as
players -- a failure mode already recorded on this play, where three officials and a field marker were drawn
as Baltimore players and one got a roster name.

**Where this leaves the dedupe fix.** Its two supporting rulers -- the cross-camera control group (paired ids
agree at p50 0.42 m, so ids 74 and 38 at 1.24-1.44 m with |dy| ~1.19 m are real men) and the footage -- are
both independent of team labels, so neither depends on the census being sound. The run regression is now
explained as a pre-existing census error the fix does not cause. `ONE_VIEW_ACROSS_M` also has a data-driven
justification rather than a census-fitted one: the same man reads <= 0.95 m across cameras, real separate men
read >= 1.19 m, so a radius of 1.0 m sits between the two populations.

**SHIPPED 2026-09-13.** `play_timeline` now passes `side_ground` to `beyond_sideline_span`, and
`ONE_VIEW_ACROSS_M` is 1.0 (was 1.5), set between the two measured populations -- same man across cameras
<= 0.95 m at the p90, separate men 1.19-1.30 m. Play 1: snap 2.82 -> 1.20, play 1.98 -> 1.73, whole clip
2.89 -> 2.52, frames exactly eleven-a-side 10 -> 33, Kansas City at the snap 8.9 -> 10.8 with Baltimore
unchanged. A test covers the dedupe half (an endzone-only state 1.2 m across is kept; it fails at 1.5).

Verified on the SHIPPED path rather than the prototype: every figure above came from probes that
monkeypatched `beyond_sideline_span` and rebuilt `side_ground`, while production passes the real local that
has been through `snap_ground`. An unpatched `load_play_timeline` reproduces every window exactly. The
discrimination is also sharper than the census alone shows -- body-frames drawn over 280-345 are
**{74: 66, 38: 39, 22: 0}**: the two ids the control group and footage called real men are drawn, and id 22,
which the same control called a copy at 0.65 m (inside the 0.95 m p90), is still dropped. The change admits
exactly what the two non-census rulers vouched for and nothing they rejected.

**The `ONE_VIEW_ACROSS_M` half was REVERTED within the hour: play 2 regresses.** Measured on play 2, of the
123 states 1.0 keeps that 1.5 drops, |dx| to the body they duplicate is **p50 2.87 m** (p90 3.52) -- id 2 on
53 frames at 3.46 m, id 34 at 2.90, id 1 at 2.87 -- the endzone's copy strung along its own depth axis,
exactly the failure that radius exists to prevent. Breaking play 2 to fix play 1 is the thing
corrections-must-beat-what-they-correct forbids, so the constant is back at 1.5 and the test now guards the
play 2 case instead. `side_ground` stays: it is the half that restores the bodies, and it harms nothing on
its own (play 1 +0.00, play 2 unaffected) -- it simply cannot pay off until dedupe stops eating what it
restores.

**But the same measurement hands over the discriminator.** In the marginal band (|dy| 1.0-1.5) the two
populations separate cleanly on |dx|, the axis nobody was looking at:

    play 2 ghosts          |dx| 2.4-3.5 m    the endzone's copy, displaced in DEPTH
    play 1 merged linemen  |dx| 0.38-0.79 m  a different man beside him, at the SAME depth

A copy is displaced along x; a separate man is displaced across y at the same depth. So the fix looked like a
depth-aware exception -- an endzone-only state beside a kept state (|dx| small) but clear of it across
(|dy| >= ~1.0) is a different player -- rather than a wider or narrower box.

**Measured on both plays, and REJECTED (2026-09-13), because the premise was my own measurement error.**
The exception does nothing on play 1: the snap census stays 2.82 at near_depth 0.8, 1.0 and 1.5, with id 74
drawn on 3 frames against 66 under the blanket radius; only 2.0 moves it at all (2.64, 14 frames). On play 2
it newly keeps 54 states at every setting (|dx| p50 0.29) -- the ghosts stay dead, but it is pure cost with
no benefit.

The premise was wrong: **|dx| 0.38-0.79 m was id 74's distance to the nearest SIDELINE BODY** (from the
offset-control probe), not its separation from the kept state that dedupe actually compares against, which
is id 1. Two different relationships; I carried the statistic from one into the other and built a rule on
it. Sixth instance this session of the same error family -- see the standing note about stating the
population before reading a number.

**Measured, and the line is CLOSED (2026-09-13).** Separation from each dropped state to the kept state that
actually kills it:

                     n    |dx| p50   p90     |dy| p50   p90
    play 1 (KC snap)   163     2.07    2.48       1.11    1.39
    play 2 (all)      1267     2.38    3.75       0.70    1.28

    |dx|      p10    p25    p50    p75    p90
    play 1   0.94   1.98   2.07   2.29   2.48
    play 2   0.09   0.77   2.38   3.22   3.75

Play 2's ghosts span 0.09-3.75 m and straddle play 1's entire 0.94-2.48 range, so **no threshold in
(|dx|, |dy|) keeps the linemen and drops the ghosts**. Narrowing the DEPTH reach instead fails for the same
reason: a quarter of play 2's ghosts sit inside 0.77 m.

This also corrects the framing above. id 74's killer is id 1 at **|dx| 2.03**, and id 38's is id 4 at 2.41 --
not a box-mate 0.38-0.79 m away, which was the distance to the nearest sideline BODY. The linemen are
deleted because a body sits ~2.4 m off in depth, so it is the box's 4.0 m depth reach that swallows them,
not the across radius I spent the evening adjusting.

**What would be needed is a different feature, not a better threshold** -- the pair's geometry does not carry
the answer. Candidates never attempted: appearance (do the two states look like the same player?), or
tracking which camera's detection is genuinely unpaired rather than inferring it from distance. Four
replacements for this rule are now measured and rejected. `side_ground` stays on main because it is
measured-neutral and a prerequisite for any future version; the snap gain does not ship.

Two caveats from the original entry, one now discharged. `ONE_VIEW_ACROSS_M` exists for PLAY 2's endzone
ghosts strung along x and only play 1 was measured -- if those ghosts return, this belongs behind a per-play setting rather than in the
constant. And no unit test guards the call-site wiring: a future edit could drop `side_ground` at
play_timeline.py:337 and only the constant's test would still pass.

**The run surplus is an identity fault, and it splits into two faults needing opposite fixes (2026-09-13).**
Of 17 jersey-carrying drawn ids on play 1, 11 are consistent with the play and 6 are not, covering **1798 of
14445 body-frames (12.4 %)**. Kansas City has the ball, so KC ids should carry offensive numbers:

    id 39  KC  jersey  6 = DB (Bryan Cook)      233 frames   nearest body p50 0.60 m, 70 % inside 0.95 -> DUPLICATE
    id 42  BAL jersey 76 = OL (Dalcourt)        196 frames   nearest body p50 0.60 m, 84 % inside      -> DUPLICATE
    id  3  KC  jersey 18 = not on the roster    623 frames   p50 2.72 m,  0 % inside                   -> distinct
    id 38  KC  jersey 55 = LB (Uche/Bozeman)    172 frames   p50 1.47 m, 15 % inside                   -> distinct
    id 78  BAL jersey  4 = WR (Zay Flowers)     167 frames   p50 4.17 m,  0 % inside                   -> distinct
    id 19  KC  jersey 67 = not on the roster    407 frames   p50 1.21 m, 41 % inside                   -> BIMODAL

A wrong jersey does not make a body false: the distinct ones are real men whose LABEL is wrong, and deleting
them would delete players. The two duplicates are extra bodies. Note `dedupe_frames` cannot remove them --
a state the sideline detected that frame is never a duplicate (the 2026-09-08 rule) and these are
sideline-detected -- so whatever fixes this is a different mechanism, not a radius.

**Two corrections to claims I already committed.** id 39 was called "a distinct real body, not a duplicate"
on the strength of the cross-team probe, which measured **frames 380-440 only** (nearest same-team 1.20 m);
over the whole clip it sits 0.60 m from something 70 % of the time. Same id, different window, opposite
answer. And id 19's "distinct" verdict is an artifact of reading a median: p50 1.21 m with 41 % of frames
inside 0.95 m is bimodal, not distinct. Seventh and eighth instances tonight of a number read without its
population.

**None of them is a duplicate: the "count fault" half is wrong and withdrawn (2026-09-13).** Asking WHICH
body each flagged id sits on, rather than how often something is near it:

    id 39  162 close frames  partners id 25 x74 (46 %), 80 x22, 42 x21, 84 x13   -> rotating
    id 42  164 close frames  partners id 25 x43 (26 %), 15 x37, 39 x35, 37 x20   -> rotating
    id 19  166 close frames  partners id 25 x79 (48 %), 33 x39, 20 x24           -> rotating
    id  3    0 close frames  p50 2.72 m from anything                            -> distinct
    id 78    0 close frames  p50 4.17 m from anything                            -> distinct

No twin tracks. The "70 % within 0.95 m" figure measured CONGESTION, not duplication -- id 25 (Suamataia, an
interior lineman) is the commonest neighbour of three different ids because everyone near the pile is near
him. The earlier "DUPLICATE (count fault)" verdict on ids 39 and 42 rested on a proximity share without ever
asking whether the neighbour was the same body, and it is withdrawn. Ninth instance tonight of a number read
without its population.

So all six flagged ids are **real bodies carrying wrong labels**, removing any of them deletes a man, and the
census cannot be improved by removal at all.

**What that sharpens.** id 3 is drawn on **623 of 647 frames** (KC, jersey 18, not on the 2024 roster)
standing p50 2.72 m clear of everyone, and id 19 on **407 frames** (KC, jersey 67, also not on the roster).
A near-permanent body that no roster number matches is the shape of an official or a staff member that
`sideline_dwellers` / `striped_ids` / `behind_the_offence` did not catch -- which would explain the run
surplus better than anything tested tonight, and would be a bounded fix rather than a threshold. The footage
decides it; proximity statistics demonstrably do not.

**The footage kills both remaining explanations: they are all real players (2026-09-13).** id 3 is a Kansas
City man in full uniform in a three-point stance at the line, on two separate frames -- so the "officials the
off-field rules missed" idea is dead, and the biggest flagged id (623 frames) is correctly counted with only
its jersey misread. Detection status settles the rest:

    id 19  drawn 407  detected 380  interpolated 27 (7 %)   frame 500 interpolated
    id 78  drawn 167  detected 167 (100 %)                  frame 500 DETECTED (sideline)
    id  3  drawn 623  detected 622                          frames 400 and 500 detected

**And my "phantom on empty grass" reading was a sampling error.** I cropped id 19 at frame 500 -- one of its
27 interpolated frames, 7 % of its life -- and read it as evidence about the id as a whole. id 78 is 100 %
detected including that frame, so its cross belongs to a real player in the crop (most likely the Baltimore
man above right) with the ground point placed low, not to a body on bare turf. Tenth instance tonight of
sampling the rare case and generalising from it.

So there are no phantoms and nothing to remove: **all six flagged ids are real detected bodies with wrong
labels**, and the count-fault half of the identity thread is dead alongside the officials idea.

**What is left is the one assumption never tested: that truth is eleven in that window.** If the whistle
falls before frame 460, the tail of the "run" window is people walking on -- exactly the error already
corrected once in this document, when the census was scoring 200 frames of aftermath. The end of the play
has never actually been located; it was assumed from the window bounds.

**The end of the play is still unlocated, and the probe built to find it was broken (2026-09-13).** Two
proxies, both useless, recorded so nobody rebuilds them:

  - **Runner speed.** Taking the FASTEST Kansas City body per frame reports 48.0 m/s at frame 430, 35.6 at
    500 and 24.6 at 465. A world-class sprinter peaks near 12. A max over all bodies is dominated by
    whichever id is glitching, so "fastest KC >= 4 m/s across 300-560" says the metric is noise, not that
    the play is live. Any speed signal here needs ONE identified carrier and a median filter.
  - **Bodies beyond the sideline.** Zero anywhere in 300-560 -- but the crowd-crossing evidence recorded
    earlier in this document is at frames **580-620**, outside the window I scanned. The signal was real and
    I looked in the wrong place.

Eleventh instrument error of the session. What the run does show is genuine: drawn bodies climb from 20-21
at frames 300-335 (Kansas City 9, the snap deficit), to 23 at 345 as the pile separates, to **25-26 with
Kansas City at 13-14 across 390-430**. The surplus is concentrated exactly where the play is most congested,
which fits neither "aftermath crowd" nor any removal route -- all six flagged ids being real detected
players. The end of the play needs settling on the FOOTAGE, since eyes have been reliable tonight and
derived proxies have not.

**The play is LIVE through frame 470, so the window was right and the census thread closes here
(2026-09-13).** At frame 425 (24 bodies, KC 13, BAL 11) players are running and engaged in blocks with a
carrier in the scrum; at frame 470 (25 bodies, KC 12, BAL 13) a tackle is still forming, and the people at
the top of the plate are off-field on the sideline. No whistle, no converging officials, nobody standing
around. The aftermath explanation for the run surplus is therefore dead too, and 340-460 is all live play.

**Where that leaves play 1's body count.** Every removal route is closed -- the ghost rule, dedupe, cross-team
double-drawing, duplicates, officials, phantoms, and now the window itself. All six odd ids are real detected
players carrying wrong labels. The surplus is genuine over-counting during the congested phase, of which the
cluster test accounts for only ~0.2-0.5 bodies a frame (clusters 11.56 at 0.40 m and 11.29 at 0.50 m against
11.79 bodies); the remainder is unexplained. **Census stands at 1.98 a frame over the play, where the session
found it.**

One discrepancy recorded rather than acted on: at frame 425 the census reads KC 13 while a count of red
shirts on the plate gives roughly 10-11, with a dense knot of Kansas City dots over some 4-5 players in the
pile. That looks like more duplication than the cluster test measured. Eyeballing a pile is precisely what
produced several of this session's errors, so the instrument stands until a better one is built -- but the
disagreement is real and is the first thing to re-measure, with a method that can count bodies in a pile
without a radius.

**And the obvious candidate for that method does not work.** Pose skeletons look like a radius-free counter
-- one skeleton per person by construction -- but `keypoints_2d.parquet` is
`[frame, cam, global_player_id, joint, x, y, conf]` with exactly 17 joints per id and **no per-detection
key**. Each skeleton IS an id, so counting skeletons recounts the very ids the census counts and arbitrates
nothing. (Consistent at frame 425: 20 sideline skeletons against 24 drawn bodies, the difference being
endzone-only and interpolated states.) A genuinely independent count needs a FRESH pose inference over the
crop, ungated by tracking -- a GPU build rather than a query. Recorded so nobody spends an hour rediscovering
that the keypoints are id-keyed.

**Tiled inference does NOT recover the merged players -- rejected on the footage, twice (2026-09-14).**
The full-frame pose pass finds 19-20 people where 22 players plus officials stand, so it under-detects, and
the obvious remedy was tiling: 3x2 overlapping tiles each resized to 1920, merged by NMS. The gate passed
perfectly (every full-frame person reproduced, none lost) and it "recovered" 7/6/9/26 extra people. All of
it collapsed under inspection:

  - **off-field contamination.** At f470, 14 of 26 recoveries are bench and staff at |y| ~26.8 m, which a
    2x resolution now resolves. Recovered is not recovered PLAYER.
  - **truncated boxes.** Recoveries at 0.03-0.14 m from an existing body are the same man re-detected: a
    partial box's bottom edge is at mid-torso, so back-projecting it to the ground lands metres beyond the
    player. The "0.6-1.6 m separation" I read as shoulder-to-shoulder lineman spacing was that artifact.
  - **the height test was necessary but not sufficient.** Back-projecting each box to an implied stature
    (gate: real full-frame boxes read p50 1.78-1.80 m, matching the project's 1.85 m) dropped the slivers at
    0.50-1.38 m and kept 2 per frame at 1.43-2.11 m. The footage then showed all four survivors are narrow
    FULL-HEIGHT strips down men who already have a box. Testing vertical extent never tested width.

So higher resolution yields duplicate boxes of the same men, not the merged ones. The earlier closure --
those bodies overlap genuinely in the image and need instance segmentation rather than more pixels -- now
rests on much stronger evidence, and a future session should not spend a GPU build rediscovering it.

**This also walks back the "pile over-count" reading, in the conservative direction.** The census drawing 24
bodies where the sideline detector sees 20 is NOT evidence of over-counting: the sideline merges 2-4 men and
the endzone legitimately supplies them. The "duplicates" found by matching drawn bodies to sideline skeletons
are that merging, which was already known, not extra bodies.

**The untried feature is cross-camera RAY MISS.** The one-view dedupe box cannot separate play 1's linemen
from play 2's ghosts in (|dx|, |dy|) -- but if an endzone-only state is truly the endzone's copy of a kept
sideline player, their two rays should nearly intersect, while two different men's rays miss by a metre or
more. 05u already computes that quantity and the dedupe rule has never used it.

**Cross-camera ray miss fails too, and backwards (2026-09-14).** The prediction was that an endzone GHOST is
the endzone's copy of a man the sideline also sees, so the two rays nearly intersect, while a merged LINEMAN
is a different man whose ray misses by a metre. Measured over every one-view-box kill on both plays:

    play 1 (merged linemen)  p10 0.28  p25 0.68  p50 0.75  p75 0.81  p90 0.84   under 1.0 m: 100 %
    play 2 (endzone ghosts)  p10 0.28  p25 0.75  p50 0.99  p75 1.31  p90 1.74   under 1.0 m:  51 %

Play 2 sits HIGHER than play 1, the p10s are identical and the sub-0.5 m shares are 14 % against 18 %. No
separation, and the sign is inverted. Two reasons it could never have worked, worth keeping: the
cross-camera control already showed the SAME man disagrees by 0.42 m, so a 0.4-0.5 m noise floor swamps a
signal of this size; and only 514 of 1089 kills on play 1 and 290 of 1267 on play 2 have ankle rays in both
cameras, so it would gate under half the cases even if it separated.

**That is the fifth rejected candidate and the (dx, dy)-style dedupe line is closed permanently** -- ghost
rule, blanket radius, depth-aware exception, any box at all, ray miss. No sixth variant of the same shape.

**What the failures point at is a COUNT, not a distance.** Every rule so far asks "is this endzone state near
a kept sideline state?". The mechanism is the other question: "does the endzone resolve TWO men where the
sideline sees ONE?" A merged lineman should show two endzone detections against one sideline body; a play 2
ghost should show one endzone detection duplicating one sideline man. That uses the endzone's own separation
as evidence, which no rule has done, and it is the last untried shape.

**The wide-killer-box rule is the first one that MECHANICALLY works, and still is not shippable
(2026-09-14).** Rule: in the one-view branch, a killing sideline box that is anomalously wide for its height
holds two men, so the state it would kill is the second man and survives. It measures merging rather than
inferring it from position, which the six earlier candidates all did.

    play 1  threshold   snap    play    run    full   11/11   watch 74/38/22
            off         2.82    2.03   1.86    2.90    10     0/1/0
            0.79        2.49    2.09   2.09    2.97     7     61/26/0
            0.90+       2.82    2.03   1.86    2.90    10     0/1/0     (exact no-op)

    play 2  off 35.10 | 0.79 35.15 | 0.90 35.14 | 0.96 35.14 | 1.05 35.13   bodies a frame

Two genuine firsts. **Play 2 is untouched at every threshold** (+0.03 to +0.05 bodies a frame) -- the first
candidate all session that does not pay for play 1 with play 2's ghosts. And at 0.79 it draws **ids 74 and
38** (61 and 26 frames at the snap), exactly the men the cross-camera control and the footage independently
validated as real.

Rejected as shippable on two pre-committed criteria. There is **no plateau**: only 0.79 acts, and 0.90 upward
are exact no-ops -- mechanically sensible, since skipping one wide killer merely lets a narrower kept body
kill the victim instead, so enough killers must be skipped, which makes the effect fragile. And it is **net
worse**: the snap improves 2.82 -> 2.49 while play, run, aftermath and the whole clip all regress
(2.90 -> 2.97), with exact eleven-a-side frames 10 -> 7.

**The reason is diagnostic, not fatal.** Kansas City rises 8.9 -> 10.2, toward truth. Baltimore rises
11.7 -> 12.7, away from it. The test is not team-aware and Baltimore's defensive linemen are merged in the
same pile, so it recovers real men on BOTH sides -- and Baltimore was already over eleven before any change
of mine. **Baltimore's baseline surplus is what stands between play 1 and a correct census**, and nothing
tonight has examined it: at the snap BAL reads 11.70 against a truth of 11. The relabel experiment cannot
explain it either, since all four flipped ids contribute zero body-frames at the snap.

**THE TELEPORTS -- what the user sees, and the census cannot (2026-09-15).** v38 shows players swapping,
teleporting and jittering; a Baltimore man standing in the Chiefs' O-line then snapping back to linebacker.
A plausibility ruler (per-id contiguous step; nobody exceeds 0.20 m/frame = 12 m/s) finds 487 of 14 384
body-frames over the sprint bound and a top speed of 73 m/s. I had this signal a day earlier -- a probe
reported the fastest body at 48 m/s -- and dismissed it as a noisy metric. It was the defect.

Three distinct mechanisms, each found by tracing raw per-camera positions through the pipeline stages:

  1. **A welded tail.** id 19 = a KC sideline track (14-430) with a Baltimore ENDZONE track (483-639)
     stitched onto the same global id. Its kit vote says BAL while the head says KC; three independent
     signals (73 m/s step, live-play colour flip 0.90 -> 0.20, tail's own kit majority) agree. Cut at 430
     -- the sideline span's end, NOT the teleport frame 493, which was interpolation racing toward the tail.
     **Verified: id 19's worst step 1.23 m -> 0.32 m** (74 -> 19 m/s). The tail (id 146, BAL) is
     endzone-only and the ghost rule drops it, correctly -- that linebacker has his own sideline id.
  2. **Interval mispairs.** A pairing right for most of a track and wrong for a stretch: id 17 carries four
     sideline frames (457-460) of a man 6.2 m from its endzone track; id 82's endzone rows from 315 begin
     5.9 m from where its sideline ended; id 5's endzone sits 6.2 m from context for 389-403. mispaired_ids
     misses all of it because it gates on the whole-track MEDIAN. Fix: per-frame cross-camera disagreement
     over the control's 0.95 m for >= 4 frames marks a bad run; the intruder camera is whichever is
     discontinuous with the id's own positions outside the run; its rows move to a fresh id with a team
     from its own kit colour. A margin (intruder >= 1.5 m and >= 2x the other camera) is essential -- without
     it 50 intervals fire, most coin-flips at 0.6 m vs 0.6 m. With it, 13 intervals, 187 rows, every one
     unambiguous. APPLIED; timeline verification running.
  3. **`smooth_xy` averaged ACROSS GAPS -- fixed.** id 21 moved 0.88 m/frame at 240-242 with NO raw
     detection in either camera from 244 to 320 and raw positions at 236/242 only 0.1 m apart. My first
     hypothesis was place_from_refit; the stage trace showed its shift was 0.00 on every detected frame. The
     jump appeared only between build_timeline's input and its states, and only in a segment's last FOUR
     frames -- the smoother's pad width. smooth_xy compacted every finite row into one array before
     convolving, so frame 243 sat beside frame 320 and the 9-frame mean blended one segment's tail with the
     next segment's head, 77 frames and metres away. Now smoothed within each contiguous run only.

  4. **Same-camera track switches** (scripts/08t_cut_track_switches.py). One camera's own track jumps to a
     different man across a short gap: id 82's sideline sat at x = -23.1 to frame 307 and resumed at 315 at
     x = -28.9 -- 5.9 m in 8 frames, which fill_gaps then drew as a body crossing the field. Both cameras
     agree on the NEW man afterwards, so no cross-camera test (08u) can see it. Two things made the detector
     usable: PERSISTENCE (the medians either side of the gap must stay apart -- the endzone's depth noise
     blips ~1 m every frame and fired 90+ times without it) and scoping to the LIVE play by --max-frame,
     because after the whistle tracks legitimately hop between milling bodies. Applied to play 1 with
     END_LIVE=470: 16 cuts, 3524 rows, frames 41-465.

**Progress on the timeline ruler** (contiguous steps over 0.6 m/frame, whole play): v38 **26** -> id 19 cut
22 -> 08u 14 -> smooth_xy fix 3 -> 08t (16 cuts) **1** (id 76 at 637, after the whistle). At the tighter
0.25 m/frame bound (15 m/s), which the corrected smoother makes necessary because it spreads a 4-frame ramp
over 9, 218 steps remain across 30 ids -- mostly 0.3-0.5 m and mostly after the whistle, plus a handover
artifact on fragment 161 at 47-50 where its endzone rows precede its sideline rows by three frames. Census
unchanged by all of it (play 2.01, full 2.90): the cuts moved men, they removed none.

**And 08v** (scripts/08v_remap_poses_after_relabel.py): the pose caches are keyed by global id, so every
fragment 08t/08u/08s creates rendered DEFAULT-POSED until now -- 29 fragments, 900 posed frames on play 1.
The mapping is exact by (cam, frame, track_id) between a snapshot and the result; a pose follows the
SIDELINE row's relabel, because that is where the timeline draws the body. Runs under PYS (numpy-1 pickles). All of it is now a pipeline stage (`switches`, after `pair` so 08c cannot erase the fragment
identities), with 08u and 08t carrying pure, tested planning functions.

Failed calibrations, so nobody rebuilds them: a ratio-to-own-median teleport test flags the STILLEST ids
(median 0.006 m/frame makes any motion a 40x outlier); a colour-flip test over the whole clip flags 21 ids
because the post-whistle crowd occludes torsos -- restricted to the live play it flags 2.

**Team colour is the identity to keep.** kit_margin in tracks.parquet is finite on 96 % of rows and
separates cleanly (BAL 0.09 / KC 0.88 positive share over 68 and 58 ids). Jersey OCR gave 3 of 13 Baltimore
ids a number and the roster path produced defenders drawn on offence. Every fragment created above takes its
team from its own kit majority, never inherited.

**THE JITTER IS IN THE LIMBS, NOT THE ROOT (2026-09-15).** Two hypotheses for the "super jittery" motion
were A/B'd on the drawn timeline (scratch probe_jitter_ab: root-xy second difference, m/frame^2, all
drawn body-frames, plus the census as the guard):

    config              | p50    p90    p99   | census play / full
    default             | 0.0028 0.0294 0.178 | 2.00 / 2.90
    no depth snap       | 0.0028 0.0258 0.157 | 1.98 / 2.94   (id 162 worse: 0.16 -> 0.44)
    no refit placement  | 0.0050 0.0540 0.249 | 2.14 / 2.97   (jitter DOUBLES: the refit pelvis is smoother than the box point)
    neither             | 0.0048 0.0379 0.171 | 2.22 / 3.02

Both rejected. The root's p50 is a real player's value (0.003); the p90 tail is five post-whistle ids
(169, 170, 76, 79 from 483+) and fragment 162. So the root is not what the user sees shaking.

The limbs are (scratch probe_pose_jitter: the renderer's own forward pass, pelvis-relative joints, live
play 300-460, 31 ids): joint jitter p90 **median 0.15 m/frame^2 across ids**, ten times a visible
twitch, with ids 162 / 165 / 9 / 4 at 0.7-0.9 and hands moving 0.4-0.6 m/frame (25-37 m/s) at the p90.
Every one of them is fused-posed, keyframes at **stride 2**, so the timeline is nearly the raw
per-frame fit; smooth_axis_angles (median 7, range-gated at 0.5 rad) keeps any component that turns
more than 0.5 rad in 7 frames RAW -- which is exactly what fit noise on a 5-pixel hand does. The
gate built to save a runner's arm swing also saves the noise. Next: per-joint breakdown (which limbs),
raw keyframes vs drawn (fit or smoother), and a smoother A/B on TWO rulers -- joint jitter and limb
reprojection onto the footage keypoints in both cameras (a frozen mannequin has zero jitter, so jitter
alone would crown the heaviest smoother).

The rulers are now code: `nfl_gsplat/render/motion_rulers.py` (contiguous step, root jitter, census,
joint jitter/speed, handover steps -- pure functions, tested) and `scripts/07l_measure_plausibility.py`
(builds the timeline as 05k renders it, prints one table, writes DIAG/<play>_<tag>_plausibility.json),
so v38 / v39 / v40 are one diff.

**The fix: a Gaussian on the limbs (2026-09-15, commit 5b46e9d).** Per joint the jitter sits at the
extremities (wrists 0.12, feet 0.11, ankles 0.09, elbows 0.07 m/frame^2 at the p90), and the raw stride-2
keyframes carry the same numbers as the drawn frames: the fit itself is noisy on every frame, and the
7-frame median (gated or not) cannot remove noise that is on every frame. Smoother A/B on TWO rulers,
live play, 30 ids -- joint jitter p50/p90/p99 and limb reprojection onto the footage keypoints (px,
sideline p50/p90, endzone p50/p90):

    raw               0.035/0.261/1.38   8.6/20.2   5.9/12.3
    median 7 gated    0.040/0.231/1.38   8.9/20.2   6.1/12.9    (the old default: nothing)
    median 15         0.035/0.159/0.89   9.7/21.0   7.2/15.5
    gauss sigma 2     0.019/0.109/0.69   9.0/20.9   6.4/14.2    <- adopted (POSE_SMOOTH_SIGMA)
    gauss sigma 4     0.013/0.078/0.53   9.9/21.7   7.3/16.7    smear: +1.3 px p50, +4.4 px endzone p90

Verified on the real timeline by 07l (tag v41 vs v40): joints p50 0.037 -> 0.018, p90 0.229 -> 0.108,
p99 1.35 -> 0.69; steps, root jitter and census identical. The reprojection ruler is biased toward the
raw fit (the fit followed the detector's per-frame noise, so any smoother scores slightly worse against
the same noisy keypoints) -- it still separates repair (sigma 2) from smear (sigma 4). The sigma sweep
and the per-joint split (arms heavier than legs) were then measured on both rulers, jitter p90 /
endzone reprojection p90 px: s1.5 0.138 / 13.4, s2 0.109 / 14.2, s2.5 0.098 / 14.7, s3 0.090 / 15.5,
s2 with arms s3 0.099 / 14.7, s2 with arms s4 0.093 / 15.5. One trade curve: each 0.01 of jitter costs
~0.3 px of endzone p90 wherever the sigma goes, so the split buys nothing and sigma 2 stays. CLOSED.

**Renders (`diag/play_001_vNN_hifi_720.mp4`) and the 07l report each carries.** v39 = cut 19 + 08u +
smooth_xy fix. v40 = + 08t (live scope) + 08v + the Gaussian limb smoother = report v41. v41 = + hinge
clamp + ankle anchor + snap veto = report v44. v42 = + 08t to a fixpoint over the whole clip = report
v45. v43 (after the whole-play refit with hard hinges) = report v46, if v46 wins. The report numbers
are the truth about each render; the mp4 is what the user watches.

**"Joints in weird positions" is measurable too (2026-09-15).** On the drawn live play (3676 body-frames,
33 ids, after the Gaussian), the hinges do the impossible: R_knee hyperextended (< -15 deg) on 3.0 % of
frames with a minimum of -104 deg, L_elbow on 5.9 % (min -136), and bent SIDEWAYS (> 35 deg off the hinge
axis) L_knee 11.9 %, R_elbow 14.2 %, L_elbow 7.3 %. Collars turn 146-176 deg at the p99 (a clavicle does
30); spine segments 116-126. It is concentrated on ids 4, 9, 165, 17, 11, 38 -- the same men whose limbs
jitter most, i.e. stretches where the fit is garbage rather than noisy. Hinge axes used: knee flexion
about +x, elbow about y (R +, L -) in SMPL-X's rest pose.

The clamp, measured before the Gaussian on both rulers (jitter p50/p90/p99; limb reprojection px
sideline p50/p90, endzone p50/p90; violation shares after):

    gauss s2 (no clamp)             0.019/0.114/0.73   9.0/20.9   6.4/14.2   2.8 % / 10.4 %
    hinges + collars, off 20        0.018/0.098/0.66   9.7/23.7   7.1/19.4   0 / 0
    hinges + collars, off 30        0.018/0.100/0.66   9.7/23.7   7.0/19.0   0 / 0
    hinges only, off 20             0.019/0.107/0.74   9.3/21.1   6.5/15.9   0 / 0     <- adopted (off 25)

The COLLAR clamp is the smear (+2.8 / +5.2 px at the p90): the regressor places the whole arm through
the clavicle, so a limit there moves the arm off the keypoints. Hinges alone cost +0.2 / +1.7 px at
the p90 with the p50 unchanged and take every backwards or sideways knee and elbow to zero -- a limb
that could not exist is worth two pixels at the tail. `timeline.clamp_hinges` runs before the
Gaussian (which rounds its kinks); `motion_rulers.hinge_violations` reports the shares in 07l. The
collars and spine stay as the fit made them: their repair belongs in the fit (a pose prior), not here.

**The 21 live-play hops: three mechanisms, traced by stage (2026-09-15).** None is a camera handover.
Stage trace on ids 1, 40, 161 (raw sideline, raw endzone, sideline after the depth snap, drawn):

  1. **id 1 at 415-420**: the raw sideline point sits still at y +5.9; at 420 the DEPTH SNAP slides it
     2.0 m along its ray to y +3.0 with no endzone row of its own -- a same-team body happened to lie
     on the ray -- and the smoother spreads that into a 12-frame ramp at 0.2-0.35 m/frame. The snap is
     decided per frame; the correction a body needs along its ray varies slowly.
  2. **id 40 at 384-396**: endzone-only frames before its sideline span; the endzone's ground point
     walks 2.6 m along x (its depth axis) in 12 frames, 13 m/s, then the sideline picks him up 0.7 m
     away. The endzone's depth noise, drawn as motion.
  3. **id 161 at 368-369**: the raw SIDELINE point hops 1.2 m when the ankle keypoints stop being
     confident and the box bottom takes over; at 375 an outlier box adds 1.6 m more.

Fixes measured on four rulers (live / whole-clip steps > 0.25 m/frame, root jitter, census, and the
drawn lower joints reprojected into the ENDZONE against its keypoints -- the sideline's depth axis is
that camera's lateral axis, so a slide along the ray shows there and nowhere else):

    baseline                       live 21   full 214   root p90 0.0294   census 2.00   endzone 8.8 / 15.2 px
    box anchored to ankles (3)     live 19   full 196   root p90 0.0286   census 1.94   endzone 8.8 / 15.2   ADOPTED
    temporal snap, median +-6 (1)  live 28   full 217   root p90 0.0289   census 1.96   endzone 8.9 / 16.3   REJECTED

The anchor (`play_timeline.anchor_boxes_to_ankles`): a box point takes the id's own median (ankle -
box) offset over its ankle frames within 15, with 3+ of them; 2462 box frames moved by p50 0.31 m
(exactly the box's known bias), p90 0.73. Better on every ruler, worse on none. The temporal-median
snap replaced every per-frame correction with a windowed median and filled unsnapped frames: the
piecewise medians step where the window's membership changes, and it moved bodies the per-frame
gates had rightly left alone. The veto-only variant -- keep every per-frame snap, drop the one more
than 1.0 m from the median of the same body's other snaps within +-6 frames (2+ of them), or alone
in its window and over 1.0 m -- was then measured on top of the anchor:

    anchor alone                   live 19   full 196 (1 over 0.6)   root p90 0.0286   census 1.94   endzone 8.9 / 15.1
    anchor + snap veto (1)         live 15   full 186 (0 over 0.6)   root p90 0.0278   census 1.94   endzone 8.9 / 15.1   ADOPTED

110 of 4635 snaps vetoed (2.4 %, the documented wrong-man share); the last step over 0.6 m in the
whole clip (id 76 at 637) goes with them. `depth_snap.veto_outlier_snaps`, VETO_WINDOW 6 / VETO_M 1.0.
One id pays: fragment 162 loses its lone snaps and its root jitter p90 goes 0.18 -> 0.44 (it was the
id the no-snap A/B had shown depends on the snap); the aggregates all improve, so it shipped.

The anchor's two knobs swept on the same four rulers (id 161's hop at 370 survived on one ankle
frame): w15 s2 = shipped; w15 s1 live 14 / full 188 / census 1.95; w30 s3 live 14 / full 182 / census
1.95 / endzone p90 15.3; w30 s1 live 13 / full 172 / root p90 0.0269 / census 1.96 / endzone p90 15.3.
Steps improve, both guards move the wrong way by a hair (+0.02 census, +0.2 px). Not adopted;
w15 s3 stays. CLOSED.

Mechanism 2, REJECTED: a Gaussian on x inside each id's endzone-only runs (sigma 4 and 8, 5869
frames touched) -- live 19 -> 19, full 196 -> 195, sigma 8 census 1.94 -> 1.97 and endzone p90 +0.3
px. The drift is a monotone 2.6 m ramp over 12 frames, which a smoother preserves by design; only a
velocity bound anchored at the sideline join could remove it, and it is two live steps on one id.

**Where the live play stands after all of it (07l, tag v44):** steps > 0.25 m/frame 15 (from 21;
none over 0.6 anywhere in the clip), root jitter p90 0.015, joint jitter p90 0.102 (from 0.229),
hinges 0 / 0, census 1.94. The largest remaining term is joint jitter on the ids whose fits are
garbage in stretches (162, 9, 4, 13, 17, 165 at 0.26-0.70) -- the case docs/PLAUSIBILITY.md reserves
for the local repair.

**08t to a fixpoint over the WHOLE clip (2026-09-15, 07l v44 -> v45).** Two things were wrong with
the first 08t pass: it reports one cut per id (the earliest), so the fragments it creates carry
switches of their own -- a dry run over the full clip found 25 more cuts, six of them INSIDE the live
play on first-pass fragments (165 @131, 167 @420, 169 @229, 173 @334, 161 @51, 175 @273) -- and it
was scoped to the live play on the argument that post-whistle hops are not worth fragmenting, while
four of the post-whistle switches were CROSS-TEAM tails (a KC id turning into a BAL man at 609, 615,
623, 566) drawn in the head's colour. Applied to a fixpoint (25 + 8 + 4 + 0 cuts, 3701 rows, 37 new
ids; 08v carried 378 fused + 203 sideline posed frames):

    v44 (live scope, one pass)   live 15   full 186   census live 1.94   root p90 0.0278
    v45 (whole clip, fixpoint)   live  9   full 150   census live 1.66   root p90 0.0265   joints unchanged

The pipeline's `switches` stage now loops 08t until a pass cuts nothing, over the whole clip
(CUT_TO_FRAME narrows it); END_LIVE is only 07l's window now. 08t and 08v back up with a counter
(`tracking.relabel.backup_path`) -- the second apply had overwritten the first pass's `.pre08t`, the
only copy before any cut, and a manual `.pre08t_full` snapshot saved it.

**Hard hinge bounds INSIDE the fit beat the post-hoc clamp (2026-09-15, commit after 94b0be9).** The
soft range prior had lost to the reprojection twice; a box bound on the optimiser's parameters
(scipy trf `bounds`: knees/elbows flexion [-5, 150] deg, off-axis +-25) cannot. A/B on play 1's six
worst ids (9, 4, 165, 17, 13, 162; 05p --one-view-only, same keypoints, 993 frames each), scored on the
392 live keyframes -- violations on the RAW fits, jitter and reprojection after the shipped clamp +
Gaussian (px, sideline p50/p90; the endzone column is the one-view fit's own placement, ~60 px for
both, and only its direction counts):

    A shipped fit         hyperext 3.8 %  off-axis 27.7 %   jit 0.033/0.221/0.77   spd p90 0.27   side 13.4/23.9   end 64.9/95.2
    B hard hinges         hyperext 0.0 %  off-axis  3.7 %   jit 0.031/0.187/0.72   spd p90 0.24   side  9.4/18.8   end 53.5/94.1

Better on every ruler, INCLUDING the sideline reprojection by 4-5 px: a legal pose fits the keypoints
better than an illegal one clamped afterwards, because the other joints compensate while the fit
runs. `Mono2DConfig.hard_hinges` defaults to True (05p --no-hard-hinges to disable); the render-side
clamp stays as a belt for caches fitted before it. The whole play is being refitted with it
(poses_refit.json.pre_hard is the cache before).

**The whole-play hard-hinge refit: limbs win, root loses (07l v45 -> v46, 2026-09-15 20:43).** 5182
frames on 69 players in 26 min, reprojection median 16.4 -> 2.7 px. On the timeline: joint jitter p90
0.102 -> 0.090, p99 0.69 -> 0.55, speed p90 0.152 -> 0.135, hinges 0 / 0, census 1.66 -> 1.65 -- and
live steps > 0.25 m/frame 9 -> 19, root jitter live p50 0.0021 -> 0.0038, p90 0.0137 -> 0.0210 (id 11
walks 1.6 m over 403-407). Mechanism: place_from_refit moves each body to the refit's per-frame
pelvis, and the bounded fit's pelvis is noisier from frame to frame -- transl is solved per frame with
no memory, while a root moves smoothly. Not shipped as is: the pose gain must not ride on a root loss.
Being measured: per-id Gaussian on the refit's transl along its keyframe runs (s2, s4), an outlier
veto (> 0.5 m from the +-6-frame median), and placement off, on the four placement rulers.

**Scored where the render places it, the one-view hard-hinge cache LOSES (2026-09-15 21:05).** The
refit A/B had placed bodies at the fit's own transl (~60 px off in the endzone) and could not see this.
Same eight worst ids, live window, bodies at the TIMELINE's xy, both cameras (scratch
probe_cache_in_timeline):

    shipped (pre_hard)   hinges 6.4 % / 23.0 %   joint jit p90 0.34   root p90 0.022   endzone lower 16.4 / 32.1 px   sideline limbs 16.7 / 33.2
    hard1 one-view       hinges 0.0 % /  3.7 %   joint jit p90 0.27   root p90 0.033   endzone lower 52.5 / 70.1 px   sideline limbs 10.2 / 18.9

A bounded knee cannot fake the foreshortening a leg pointed at the sideline camera produces, so the
fit lays the leg along the ray instead -- invisible to the sideline, three times worse in the endzone.
The pelvis itself moved only 0.06 m (p50) between caches; it is the legs. "Place off" leaves the
endzone at 22 / 53 px, so no placement smoothing fixes it. poses_refit.json is back to the v45 cache
(the hard-hinge one kept as poses_refit.json.hard1). The bound stays on by default in the FIT because
the same experiment with the endzone in the objective (05p --two-view --endzone-weight 0.3, refit C)
is the one that can resolve the along-ray ambiguity; it is being scored the same way. If C loses too,
hard_hinges goes back to opt-in.

**Hypothesis under test: a stronger per-camera pose model (NLF, NeurIPS'24) instead of the regressor
we refit from (2026-09-15, evening).** Of the multi-camera toolkits the user listed (Pose2Sim, Anipose,
MVPose, VoxelPose, EasyMocap, OpenCap, MeTRAbs...), only two touch what is still wrong on play 1: a
learned pose prior in the fit (EasyMocap's VPoser route; the weights are licence-gated and not on
disk) and a better per-camera 3D initialiser (MeTRAbs/NLF). The rest re-do triangulation and
association, whose ceilings are measured (geometry 0.15 m with identity given, the endzone's 4-6 deg
lens, a 1 m pairing ambiguity in a formation), or are trained on people 2-5 m from the camera.

NLF-L (`data/models/nlf/nlf_l_multi_0.3.2.patch4.torchscript`, 521 MB, noncommercial research
licence, loads under smplx312's torch 2.11 after `import torchvision`) takes OUR boxes and OUR camera
(`estimate_smpl_batched(images, [boxes xywh], intrinsic_matrix, extrinsic_matrix in mm,
world_up_vector, model_name="smplx")`) and returns SMPL-X pose (165), betas, trans, joints3d in world
millimetres, joints2d and per-joint uncertainties. First frame ran: 15 s per box on CPU. One box per
call -- a batch with one degenerate crop went non-finite inside its fitter. Probe
(scratch probe_nlf.py) scores hinge violations, limb reprojection onto the YOLO keypoints and
stride-4 joint jitter on the worst ids against the shipped refit (3.8 % / 27.7 % violations,
13.4 / 23.9 px) and the hard-hinge refit (0 / 3.7 %, 9.4 / 18.8 px). Runs on the GPU after v42.

Session note: the previous session died with three jobs running (v42 at frame 61, the whole-play
hard-hinge refit, the suite); v42 resumed, the refit restarted from scratch (its
`PermissionError: [WinError 5]` was the pool losing its parent, not a bug), the suite is queued.

**NLF, scored the same way: REJECTED as a pose source (2026-09-15 21:05).** On the GPU it is fast
(188 boxes in 69 s after warm-up) and good on the visible men in its own camera (id 4 6.0 px, 9 9.0, 13
8.8 at the p50 against the YOLO keypoints), garbage exactly where ours is (id 17 in the pile: 57 px,
its own uncertainty 1.5 m), and 4.3 % hyperextended knees. At the timeline's placement its legs are
WORSE in the endzone than the shipped fit (lower joints 29.6 / 69.5 px vs 14.5 / 34.0) and no better
in the sideline (17.9 vs 16.3). Same lesson as the hard-hinge cache: a monocular pose at 140 px lays
the legs along the camera ray, and only the other camera can say where they are. Kept as a possible
INIT for the fit (not measured); not a replacement for it.

**Pairing by formation position (the user's question, 2026-09-15 21:15).** It is what 08r does. At the
snap (frames 296-304, median ground points, same team) 13 of 22 are already paired at 0.43 m p50 and
every one of them is CLEAR by position alone (best <= 1 m, runner-up >= 2x further); position finds ONE
more, BAL sideline 4 <- endzone 198 (0.42 m, clear both ways), which 08r rejects as a re-pairing
(endzone 4 already holds a track on 29 of those frames -- --allow-repairing --give-up-incumbent would
apply it). Everything else is the KC interior (9, 19, 37, 38, 74, 86, 97, 164, 166, 204 at x -22..-23,
y -5..5): ratios 1.0-1.3 at 0.5-1.5 m -- the line stacked along the sideline's depth axis, where each
camera's blind-axis error (0.3-0.5 m sideline, ~1 m endzone) exceeds the spacing. No label changes
that. Scratch probe_snap_pairing.py.

**Refit C, two-view + hard hinges, WINS at the timeline's placement (2026-09-15 21:18, last result
before shutdown).** Eight worst ids, live window, bodies at the timeline's xy, both cameras:

    shipped (pre_hard)   hinges 6.4 % / 23.0 %   joint jit p90 0.341   root p90 0.0219   endzone lower 16.4 / 32.1   sideline limbs 16.7 / 33.2
    hard1 one-view       hinges 0.0 % /  3.7 %   joint jit p90 0.271   root p90 0.0334   endzone lower 52.5 / 70.1   sideline limbs 10.2 / 18.9
    C two-view ez0.3     hinges 0.0 % /  2.0 %   joint jit p90 0.204   root p90 0.0174   endzone lower 20.0 / 28.7   sideline limbs  9.5 / 20.7

With the endzone in the objective the bound stops laying legs along the sideline ray: joint jitter
-40 %, root jitter -20 %, sideline limbs -7 px, endzone p90 -3.4 px, for +3.6 px on the endzone p50
(inside the endzone keypoint noise on 60-px bodies). Ship it. hard_hinges stays default on.

**v47 = the whole play refitted two-view (endzone 0.3) with hard hinges (2026-09-16 01:50; 96 min,
2244 two-view frames on 29 players at sideline 2.5 / endzone 12.1 px, 2865 one-view records on 65).**
Against v45 on the timeline: joints p90 0.102 -> 0.090, p99 0.69 -> 0.44, speed p90 0.152 -> 0.127;
root jitter live p90 0.0137 -> 0.0128, p99 0.097 -> 0.081; census 1.66 -> 1.65; hinges 0 / 0; live
steps 9 -> 11 and whole clip 150 -> 154, every new one on fragment 162 (root jitter p90 0.30 -- the
26-frame tail of track 19 that sits 0.07-0.6 m from id 165/196/204 and the ankle-ray twin test cannot
see). Ships if the cross-view scorer agrees (running); 162 is the next thing to remove, not a reason
to hold the cache.

A "short fragment riding another body" rule was measured for 162 and found nothing to drop: at
<= 40 drawn frames, nearest same-team body under 0.6 m on >= 70 % of frames, no id qualifies (162: 53 %,
median 0.57 m to id 11; 39, 153, 167: 0-38 %). Loosening it to catch 162 alone is a rule for one id.
Not built. (scratch probe_short_fragments.py)

**v47 SHIPS (2026-09-16 02:25).** The full two-view cache reproduces C's cross-view numbers on the
worst ids exactly (hinges 0 / 2.0 %, joint jit p90 0.204, root 0.0174, endzone lower 20.0 / 28.7,
sideline limbs 9.5 / 20.7). poses_refit.json = the two-view hard-hinge cache (v45's kept as
.pre_twoview); the pipeline's ENDZONE_WEIGHT default is 0.3; render v43 = report v47.

**Handover level-match REJECTED (2026-09-16 02:30).** Shifting each endzone-only run by the
(sideline - endzone) offset at its join (62 runs, 415 frames; blended when both ends touch): whole-clip
steps 154 -> 154 (handovers 11 -> 7), live 11 -> 12, root p90 0.0257 -> 0.0267, census 1.65, and the
shifted bodies' endzone lower-joint reprojection p90 60 -> 92 px -- the run leaves the endzone's own
view of the man to meet the sideline. The handover jump is the two cameras' honest disagreement; a
constant shift trades a step for a wrong placement. (scratch probe_handover_level.py)

**Bodies per sideline box -- the pile counted without a radius (2026-09-16 02:32).** Every drawn
body's pelvis projected into the sideline image and assigned to the smallest detection box holding it:
same-team bodies per box {1: 2890, 2: 251, 3: 40, 4: 9} over the live play, 148 of 161 frames with a
doubled box, 390 surplus body-frames, the surplus ids the KC interior (166, 19, 37, 38, 11, 204).
Removing the surplus takes KC 11.06 -> 8.89 (census 1.65 -> 2.47): the doubled boxes hold two REAL
men, a lineman behind another in the sideline's merged box. So the census's open lead ("KC 13 at f425
while ~10-11 on the plate") is not duplication the box test can find; the drawn count is right within
the box merging. CLOSED. (scratch probe_bodies_per_box.py)

**The orientation gets its Gaussian too (2026-09-16 02:50, 07l v47 -> v48).** global_orient had kept
the 7-frame median after body_pose got sigma 2 -- never measured. A/B on the drawn live play, all ids
(joint jitter max over joints; yaw second difference; limbs reprojected in both cameras):

    median 7 (shipped)     joint jit 0.019 / 0.090 / 0.44   yaw jit p90 2.73 deg   side limbs 6.8 / 15.0   endzone lower 11.3 / 18.8
    gauss sigma 2          0.013 / 0.062 / 0.41   1.32   6.8 / 15.6   11.3 / 19.6
    gauss sigma 4          0.013 / 0.058 / 0.27   0.53   7.1 / 16.0   11.4 / 19.9     <- ORIENT_SMOOTH_SIGMA
    median 7 + gauss 2     0.013 / 0.063 / 0.41   1.15   6.8 / 15.7   11.3 / 19.4

Same trade curve as the limbs (~0.3 px of p90 per 0.01 of jitter), and the p99 -- where the twitching
lives -- drops 38 % at sigma 4 for ~1 px on either camera's p90 with the p50s untouched. Whole
timeline (v48): joints p50 0.019 -> 0.013, p90 0.090 -> 0.058, p99 0.44 -> 0.27; steps, root jitter,
census and hinges identical. Render v43 (in flight) carries v47; the next render carries this.

**The post-whistle steps have no single mechanism (2026-09-16 02:55).** 141 steps over 0.25 m/frame
after frame 470; the top 30 traced by stage: gap fill / endzone-only 9, raw sideline hop 9 (the box
point itself moving 0.4-1.1 m/frame in the crowd -- the detector's box sliding between milling men),
placement / smoothing 7, handover 4, snap toggle 1 -- in five clusters (170 @515-521, 37 @569-577,
185 @651-656, 79 @542-544, 212 @602). Nothing generic to fix; every one is the crowd after the play.
The clean product decision is to END THE RENDER at the tackle (~frame 500 on play 1: the play is
over, the crowd's artefacts are the worst in the clip) -- not taken unilaterally; the whole clip is
still rendered. (scratch probe_postwhistle_steps.py)

**Fit sweeps at the timeline's placement, eight worst ids, live window (2026-09-16 03:00).** Endzone
weight (timeline with the median orientation): 0.3 jitter p90 0.204 / endzone 20.0-28.7 / sideline
9.5-20.7; 0.5 0.260 / 16.2-25.9 / 10.3-22.0; 1.0 0.246 / 13.5-23.9 / 11.4-25.6. More endzone buys
endzone reprojection by selling the sideline and adding jitter (its keypoints are noisier); the render
camera sits on the sideline's side, so the sideline is the better proxy for what is seen. 0.3 stays.
CLOSED. Temporal weight (timeline with the orientation Gaussian): 0.3 jitter p90 0.144 / endzone
19.8-28.0 / sideline 9.8-22.2; 1.0 0.095 / 19.9-30.4 / 10.0-22.8; 3.0 0.079, off-axis 2.0 -> 0.5 % /
19.9-29.7 / 10.1-24.0. Minus 45 % of jitter for ~1.8 px at either p90 with the p50s unchanged: the
pull toward the previous frame is the term that holds a limb where the keypoints are noisy.
Candidate default 3.0, to be confirmed on the whole play before it ships.

Session note (2026-09-16 09:30): the machine went quiet ~03:30 with the v44 render at frame 101, the
whole-play temporal-weight-3.0 refit unfinished (poses_refit.json untouched = the v47 cache) and the knob
scorer short of its three new rows. All three relaunched 09:30 (05k resumes from its frames on disk).

**Three fit knobs at the timeline's placement, same recipe (two-view 0.3, bounds, temporal 0.3), eight
worst ids (2026-09-16 09:45).** C baseline: jitter p90 0.144 / endzone lower 19.8-28.0 / sideline limbs
9.8-22.2. `--unseen-temporal-mult 5` (a limb no camera sees holds its pose): 0.114 / 19.8-27.9 / 9.7-21.6
-- 21 % less jitter at no cost on either camera, ADOPT. `--lr-symmetric`: 0.148, off-axis 2.0 -> 5.6 %,
sideline 15.9-35.4, endzone p90 33.3 -- with the hinges boxed the mirrored assignment is not realisable
and the residual picks a bad mix; REJECTED. `--joint-reject-px 15`: 0.140 / 22.7-35.7 / 10.0-22.8 --
drops keypoints the endzone needed; REJECTED. Next: temporal 3.0 + unseen 5 together on the worst ids,
then the whole play with the winner.

**Footage review of v44 (2026-09-16 16:10-16:50, the loop's first pass).** Strips (05q, drawn body over
the real player with the detector's keypoints): id 9 (the runner, 340-354) shows the arms held out and
straight; frame by frame the drawn arms sit within 2-15 px of the detector's keypoints at every
KEYFRAME -- the arms are out in the footage -- and the excursions are the in-between frames (337:
30-55 px, a SLERP swing between two keyframes whose arm rotations differ wildly) and the keyframes
whose arm keypoints the temporal outlier filter removed (354: 29-51 px, nothing held the arm). Both are
what temporal weight 3.0 tightens. id 162's strip: its detections flip between a Chiefs lineman and
the Baltimore man beside him -- a duplicate under 08t's floor; `timeline.rider_ids` drops it (a short
fragment within 0.6 m of a teammate on half its frames; one instance on play 1, thresholds to be
re-measured on play 2). id 13 and id 4 (bent linemen) track their keypoints well; their spine past
90 deg is a real crouch, so the torso bound leaves 90 deg total. The Chiefs lineman drawn as
Baltimore is id 82 (kit vote 0.44, 1 m inside the KC line pre-snap): 08w re-teams him by the
formation. Two new rulers from this pass: limb speed on slow bodies (flailing: 5.5 % of standing
body-frames) and spine/collar angle shares (37 % / 36 %), scratch probe_flail.py.

**Torso bounds on top of temporal 3.0, at the timeline's placement, eight worst ids (2026-09-16 17:05):**
tw3 alone jitter p90 0.079 / endzone 19.9-29.7 / sideline 9.9-24.0; tw3 + hard torso 0.055 / 19.8-30.8 /
10.0-23.2, root unchanged, collars past 40 deg 12.4 % -> 0.1 % on the raw records. FINAL RECIPE:
`--two-view --endzone-weight 0.3 --temporal-weight 3.0 --hard-torso`; the whole play is being refitted
with it (poses_refit.json.pre_final = the v47 cache before). Render v45 (in flight) = the v47 cache +
id 82 re-teamed + the rider rule (162 gone) + the orientation Gaussian; v46 will carry the refit.
Review both with strips before any claim. Strip of id 82 after 08w (frames 220-276): drawn red over
the Chiefs lineman he is, keypoints matching where the detector sees him, the stance held through the
pile -- affirmed on the footage.

**Keyframe turns -- the ruler for the in-between-frame swing (2026-09-16 17:20).** Per joint, the
rotation between ADJACENT keyframes (stride 2) on the live play (scratch probe_keyframe_swings.py):
shipped cache p50 1.3 deg / p90 8.8 / p99 27.4, over 45 deg 0.25 % (id 9 carries 37 of them: elbows,
shoulders); the final-recipe partial cache (tw 3.0 + hard torso, eight worst ids) p50 0.4 / p90 2.5 /
p99 10.5, over 45 deg 0.03 %, over 90 none. A real joint turns at most ~20 deg in two frames, so the
shipped tail was fits disagreeing frame to frame, not motion; the recipe removes the cause of the
SLERP swing rather than guarding the interpolation. Whole play with the recipe (16:47, 2244
two-view frames at sideline 2.9 / endzone 12.4 px, joint speed p90 3.05 -> 2.04 m/s): p50 0.7 /
p90 4.9 / p99 14.4, over 45 deg 0.03 % -- the partial result holds across all 35 ids.

**v49 = the final recipe on the whole play + 08w + the rider rule (2026-09-16 17:00).** Against v48:

    live steps > 0.25    11 -> 7      whole clip 154 -> 141, none over 0.6
    root jitter live     p90 0.0128 -> 0.0119, p99 0.081 -> 0.062
    joints (live)        p50 0.013 -> 0.011, p90 0.058 -> 0.035, p99 0.27 -> 0.11; speed p90 0.121 -> 0.091
    hinges               0 / 0
    census               live 1.65 -> 1.50, whole clip 2.88 -> 2.51

The rider rule took ten short fragments across the clip (24, 29, 32, 59, 60, 72, 158, 162, 163, 194; 177
body-frames) and the census improved at both windows with them gone: they were copies. Render v46 =
this cache (chained behind v45). Cross-view scorer and the flail / torso rulers on the same cache are
the last gate before Mono2DConfig's defaults move to temporal 3.0 + hard torso. Flail / torso rulers on
it: flailing 5.5 -> 3.0 % of standing body-frames, a collar past 40 deg 1302 -> 0 frames, the spine
past 90 deg 1349 -> 1062 (the +-30 deg box lets a segment reach 52; a 20 deg box is being measured on
the worst ids, with the bent linemen's strips as the check that real crouches survive).

**Strips under the recipe (2026-09-16 17:25; cache = temporal 3.0 + torso, spine box 20 on the worst ids).**
Runner id 9 (340-354): the drawn arms follow the pumping keypoints in all eight frames, legs on theirs --
the v44 held-out arms are gone ON THE FOOTAGE, not only on the rulers. Bent linemen 13 (400-414) and 4
(360-374): the crouch survives the 20 deg spine box exactly as under 30 (the fold is at the hips) and
both track their keypoints. So the tighter spine box costs nothing visible; its numbers: spine total
p90 95 -> 87 deg, max 142 -> 101, past 90 on 11.0 -> 8.2 % of records, +0.2 px on the fit's own
reprojection. Cross-view scorer pending; if it holds, spine_max_deg 20 becomes the default.

**Spine box 20 DENIED by the cross-view scorer (2026-09-16 17:30).** Same six worst ids, scored at the
timeline's placement in both cameras (off-axis hinge share; joint jitter p90; endzone lower joints
p50/p90; sideline limbs p50/p90):

    temporal 3.0 + torso 30 (shipped)   0.9 %   0.0554   19.8 / 30.8   10.0 / 23.2
    + spine box 20                      3.3 %   0.0652   19.9 / 36.8   10.9 / 26.9

Worse on every column: with the spine boxed at 20 the fit fakes the crouch with the hinges (off-axis
0.9 -> 3.3 %) and the legs lie 6 px worse in the endzone. The strips were right that the crouch
survives; the scorer says the rest of the body pays for it. The fit's own +0.2 px understated the cost
by 30x -- the third time the fit's own reprojection has hidden what the other camera sees (memory
corrections-must-beat-what-they-correct, case 10). Mono2DConfig.spine_max_deg stays 30. The spine past
90 deg on 8-11 % of records is left as real crouching until a strip shows one that is not.

**v45 delivered (2026-09-16 17:25):** the pre-snap line crop from the rendered frame 74 (scratch
review_v45/line_30.png) shows every red shirt on the Kansas City side and no white one inside their
line -- id 82 (08w) is red on the footage, affirmed. 720p clip in diag as play_001_v45_hifi_720.mp4.

**FOUND ON THE FOOTAGE: the smoothers break at a half turn (2026-09-16 17:50).** The loop's first
footage-first pass on the two flailers the ruler still names (ids 0 and 38, 18-19 % of their standing
frames with a hand or foot past 0.10 m/frame) went: flail frames listed per id (scratch
probe_flail_frames) -> 05q strips at those frames -> the drawn legs leave confident keypoints. Id 0
(BAL 21, standing still at the snap, sideline keypoints at confidence 1.0 on every leg joint, no endzone
view): drawn legs splayed 45 deg on frames 302-312 and again 366-374 while the CACHE's own legs
reproject 3-5 px onto the same keypoints (scratch probe_id_legs: lower joints p50/p90/max 3.8/4.5/4.7
px over 280-340; 3.1/6.4/8.2 over 356-390). Id 38 (KC 55, a lineman): drawn legs collapse on 446-458,
cache 4.4-6.5 px. So the damage is made AFTER the fit, in the timeline, and it is smooth.

Mechanism: a body with its back to the sideline camera has |global_orient| near pi (id 0: 2.99 ->
3.19 rad over 286-322, crossing pi at 302-308). The keyframe SLERP (interp_axis_angle) returns
scipy's canonical vectors (|v| <= pi), so the vector FLIPS SIGN at the crossing, and the component-wise
orientation Gaussian (sigma 4, shipped v48) averages antipodal vectors: the timeline's |go| collapses
3.1 -> 0.64 and the yaw swings 87 -> -53 -> 178 -> 125 -> 90 deg over 300-314 (scratch
probe_orient_flip), sideline lower joints 30 px / upper 45 px against 3-5 px either side. The
body_pose Gaussian is exposed the same way in principle (joints never near pi in practice). The jitter
ruler cannot see it (a smooth 14-frame sweep), the hinge ruler cannot (the pose is fine, the frame is
wrong), the census cannot; only the footage and the sideline reprojection at the timeline's placement
did. Exposure on the whole clip (scratch count on the cache, keyframes canonicalised as the SLERP
does): 12.4 % of keyframes within 0.3 rad of pi, 46 sign flips; the three ids with the most flips are
9 (the runner, 11), 0 (10) and 38 (7) -- exactly the runner's flailing arms of v44 and the two flailers
left in v49. Each flip corrupts ~2 sigma frames either side.

Fix (commit 6d4c898): timeline.unwrap_axis_angles re-expresses each row as the representation
nearer the previous row (a rotation by a about u is a rotation by 2 pi - a about -u; the rotations are
unchanged) and build_timeline applies it to global_orient AND body_pose before the smoothers
(unwrap=True; False = v49). Tests: a sweep through a half turn is continuous after unwrapping; the
plain Gaussian on it is off by > 30 deg (negative control), the unwrapped one < 2 deg. A/B at the
timeline's placement on ids 0 / 38 and the play-wide rulers: below. Also seen in the cache: the fit's
own free vectors reach |go| = 1289 rad (205 turns, harmless to the rotation) and 14 keyframe pairs jump
> 3 rad in the raw vector (the two-view seed's representation vs the chain's; the temporal term at 3.0
fights those) -- a fit-side hypothesis for later, small population.

**Unwrap A/B at the timeline's placement (2026-09-16 18:05; scratch probe_orient_flip2) -- ADOPTED.**
Sideline reprojection of the drawn body (lower joints / upper limbs, px) and its yaw, v49 timeline
(no_unwrap) vs the fix (unwrap), on the frames the strips showed:

    id 0, 300-314   no_unwrap lower 5 -> 31 -> 6, upper 6 -> 45 -> 4, yaw 76 -> -53 -> 178 -> 90
                    unwrap    lower 3.0-4.8, upper 1.7-2.8, yaw 83-88 throughout
    id 0, 364-380   no_unwrap lower 8 -> 37 -> 8, yaw 89 -> -180 -> -53 -> 67
                    unwrap    lower 4.6-9.8, yaw 82 -> 71 (a real slow turn)
    id 38, 446-460  no_unwrap lower 12 -> 44 -> 36, upper 6 -> 48 -> 20, yaw 131 -> 171 -> -118 -> 44
                    unwrap    lower 4.9-9.6, upper 2.8-8.7, yaw 117 -> 96

Play-wide, every drawn body on 300-460 (n 3176): joint jitter p90 0.0352 -> 0.0326, sideline limbs
p50/p90 7.3/16.3 -> 7.1/15.0, endzone lower joints p50/p90 51.8/128.7 -> 51.8/129.5 (unchanged; that
ruler counts every body against whatever the endzone has under its id, so its level is not the six-id
scorer's). Better on every ruler the change can reach, neutral on the other camera: shipped as the
default (commit 6d4c898). 07l v50 and render v47 (chained behind v46; v46 is the v49 timeline and is
the before-footage) follow; the strips of ids 0, 38 and 9 from v47 are the affirm/deny.

Retracted (18:00, twenty minutes after writing it): I wrote here that the keyframe-turn ruler
(scratch probe_keyframe_swings, "turns > 45 deg 0.25 -> 0.03 %") differenced raw vectors and so
counted representation flips as 360 deg turns. Reading the probe: it measures body_pose joints as the
RELATIVE rotation's magnitude (ra.inv() * rb), representation-free, and never touches global_orient.
The temporal-weight number stands as measured. The lesson stays for any ruler that does difference
raw vectors; none of the shipped ones do.

Spine past 90 deg -- who and where (cache, live play, 18:20): every id with more than 11 such
keyframes stands within 2.3 m of the line of scrimmage (11, 12, 3, 17, 19, 166 on the Kansas City
side at 1.1-2.3 m; 13, 4, 1 on the Baltimore side at 0.6-1.0 m; 84) -- the two lines, crouching for
real, as the 13 / 4 strips showed. Off the line: the runner 9 (11 keyframes at 100-114 deg around the
handoff and the tackle) and 5 (two frames). The "29 % of frames past 90 deg" is the linemen; the
non-lineman spine hypothesis is DENIED by the population and closed.

Fit-side exposure (scratch probe_raw_jumps): 14 keyframe pairs on the clip jump > 3 rad in the raw
global_orient vector; 11 of them are pure representation jumps (|dv| ~ 6.28 = 2 pi, relative rotation
0-4 deg, the fit's own sideline error 3-8 px either side: the data term won and the temporal term's
2 pi residual cost nothing visible). The exceptions: the runner 9 at 326-338 (three jumps, sideline
13-18 px around them against 3 px outside), 28 at 472-474 (9 -> 27 px, post-whistle), 78 at 642-660
(a broken post-whistle track, hundreds of px, |go| 14 rad). A geodesic temporal residual (the relative
rotation's angle instead of p - prev) would remove the artefact; small population, needs a whole-play
refit and the cross-view scorer -- queued behind the v47 review.

**07l v50 = v49 + the unwrap (2026-09-16 18:15).** Only the joint rulers can move (the unwrap touches
rotations, not placement): jitter p50/p90/p99 0.0106/0.0354/0.112 -> 0.0104/0.0326/0.069, speed p90/p99
0.091/0.218 -> 0.085/0.141; steps (live 7, none over 0.6), root jitter, census 1.50 / 2.51, hinges 0/0
all unchanged. The p99s are the number to watch: a third of the worst joint motion on the live play
was the half-turn artefact.

Flail ruler under the unwrap (scratch probe_flail, v49 -> v50): standing body-frames with a hand or
foot past 0.10 m/frame 80 -> 48 of 2680 (3.0 -> 1.8 %); id 38 19 -> 7, id 0 28 -> 10, the runner's 2
gone; spine > 90 deg 1062 unchanged (the linemen), collars 0. What is left: 0 (10), 13 (8), 38 (7),
166 / 3 / 204 (4 each) -- next strips.

Strips under the unwrap (05q, sideline, scratch review_v50; the same frames as the v49 strips): id 0
at 300-314 -- the drawn skeleton sits on the keypoints in all eight frames, legs straight, the splay
gone; id 0 at 370-377 (frame by frame) -- the skeleton follows a real quick step with a teammate
crossing behind him, the drawn left leg a few px off the green at 372-376 and nothing like the
45 deg kick of v49. The two v49 flail windows of id 0 are AFFIRMED fixed on the footage. What the
flail ruler still counts on him (373-378 ankle 0.11-0.24 m/frame; 388-391 wrist 0.10-0.13) is that
step and a hand; on 38 and 13 the remaining wrist flags are 0.10-0.14 m/frame (3-4 m/s) hand-fighting
at the line, which the 410-424 strip of 38 already showed following the keypoints. The 0.10 m/frame
threshold now sits at the level of real hands; the flail ruler has done its job on this play.

Review tools promoted from the scratchpad (2026-09-16 18:15): `scripts/05v_render_strips.py` cuts
per-id strips from the RENDERED frames through the render's own follow camera (`--spec PID:START:COUNT:STEP`,
pass the 05k eye offset / fov) and contact sheets (`--sheet FRAMES`); `scripts/07m_measure_fit_reprojection.py`
prints a pose cache's own per-frame reprojection of one id (lower joints / upper limbs px, knee angles) --
read it beside the 05q strip of the same frames: if the cache is on the keypoints and the drawing is not,
the timeline made the damage. Tests in tests/test_review_tools.py. The loop per flagged id is now: flail /
07l names the id and frames -> 07m (is the fit right?) -> 05q strip (footage) -> 05v strip (render) ->
affirm/deny.

**Geodesic temporal residual: measured, NO EFFECT, closed (18:20).** Ids 9 / 0 / 38 / 28 refitted with
`--temporal-geodesic` (505 records) against the shipped cache, cross-view scorer at the timeline's
placement: joint jitter p90 0.0448 vs 0.0449, endzone lower p50/p90 13.8/20.4 vs 13.7/20.3, sideline
limbs 7.6/15.2 vs 7.7/15.4; the runner's own sideline error on 316-344 identical frame by frame (07m).
The 2 pi residual was harmless because the data term wins it every time. `Mono2DConfig.temporal_geodesic`
stays False; the raw jumps stay in the cache as a curiosity.

**v47 delivered and AFFIRMED on the render (19:15).** v46 = the v49 recipe (07l v50's cache, the
v49 timeline), v47 = the same cache with the half-turn unwrap; 720p clips in diag. Per-id strips cut
from both renders through the follow camera (scripts/05v, scratch review_v46 / review_v47/strips):
id 0 (Baltimore 21) at 300-314 -- v46 spins him through a full garbage turn over twelve frames
(side-on, bent double, crouched, back again), v47 shows a man standing with his back to the camera
in all eight frames. Id 38 (Kansas City 55) at 444-458 -- v46 has him collapse to the turf and lie
with his legs up, v47 has him upright in a blocking stance stepping sideways. These are the two
bodies the user's "funky angles, flailing" would have named on this stretch, and the fix is on the
footage, not only on the rulers.

The runner at the handoff (05q strips 322-336, both cameras): sideline -- the drawn body follows the
keypoints with a whole-body offset of ~15 px on 324-334 (a motion-blurred 100-px body between the
linemen); endzone -- id 9 has endzone rows on 322-324 only, and there the green keypoints sit on a
BLURRED figure passing between two linemen (the runner at speed, half-hidden), then nothing until 336
where his placement projects behind the quarterback. Hypothesis: the endzone term (weight 0.3) on those
two blurred endzone frames, carried by the temporal chain, is the 13-19 px; test = refit id 9 one-view
only and read 07m on 316-344 (running).

Result (18:30): one-view only, the runner's own sideline error on 324-336 drops 13-19 -> 3.5-9 px (lower)
and 4-17 -> 1.5-4.5 (upper) -- but his knees go 62-115 deg -> 3-27 deg: a sprinter drawn with straight
legs laid along the sideline ray, the one-view failure the cross-view scorer closed on 09-15. The endzone
has two blurred frames here and nothing to score the legs against. Neither cache oscillates the knees
stride by stride, so both are the 2D ambiguity; the two-view stays (its legs bend, its 15 px is the
price). NOT adopted; the runner at the handoff is left as it is.

**Live hops on the footage (05q strips at 07l v50's two worst live steps, 18:25).** Id 40 (BAL) at
387-394: the drawn body stands on EMPTY TURF between two Baltimore men with no green keypoints -- the
sideline has no detection of him on those frames (scratch probe_unseen_frames: seen by the endzone
only), so his ground point is the endzone's own foot point, which is blind along the field's long
axis (x) at 88 m; the hop (0.30 m/frame at 390-394) is that point wandering. Id 203 at 366-373: an
eight-frame fragment on the Kansas City line with NO TEAM (drawn in the default kit -- yellow in 05q),
sideline-only, its skeleton offset from the pile. Population on the live play: 3615 body-frames, 153
endzone-only (ids 40: 33, 37: 36, 38: 30, 17: 18, 74: 16, 198: 8, 15: 5), 8 teamless (203 only), 93
drawn with no detection in either camera (gap fill; the long ones are 153 gliding 3.15 m over 435-454
and 4 gliding 2.13 m over 444-457 in the pile, both under the 30-frame bridge). None of the six worst
live steps is on an unseen frame: they are endzone-only (40) and sideline-only fragment (203) frames.
Hypotheses: (a) on endzone-only frames slide the endzone point along the ENDZONE's own ray to the x
interpolated from the id's sideline-seen frames (its projection into the endzone is unchanged, the
blind axis comes from the camera that sees it) -- rulers: live steps, endzone lower joints (must not
move), census (must not move), metres moved; (b) a teamless fragment shorter than the rider length is
not drawn; (c) the gap bridge 30 -> 10 frames for the two gliders (measure the census cost).

(a) built as `render/blind_axis.hold_blind_axis` (slide along the endzone's own ground ray to the
sideline-interpolated x; the endzone image of the body is unchanged by construction), wired into
load_play_timeline (`blind_axis=`), unit-tested. First A/B (18:35, per-frame cap 4 m, one-sided hold
within the 30-frame window): 635 body-frames slid on the clip (median 0.60 m, max 3.27); live steps
7 -> 9 -- WORSE; census 1.50 -> 1.50 with both teams nearer eleven (KC 10.98 -> 11.08, BAL 11.42 ->
11.32); endzone lower p50 51.8 -> 51.3, sideline and jitter unchanged. What happened: id 40's
387-395 ghost is GONE -- slid onto the man he is, the dedupe box then takes him as the copy he was
(a twelfth Baltimore body), which is the census gain; but a per-frame cap let an eight-frame
endzone-only fragment (198, 453-456) flicker on and off the slide at 0.4 m/frame, and a one-sided
hold pinned it to a sighting a second old. Rebuilt: a run of endzone-only frames slides whole or not
at all (its median slide against the cap) and a one-sided hold reaches 6 frames, not 30; re-measuring.
(b) built as `timeline.orphan_ids` (a teamless id drawn on <= 40 frames is dropped; census unaffected
by construction), unit-tested, wired after the rider rule; measured with (a)'s rerun.

Rerun (18:50): with (b) in both arms, the per-run hold still LOSES -- live steps 5 -> 7, census
1.50 -> 1.60 (KC 10.98 -> 11.09), endzone/sideline/jitter unchanged, 611 body-frames slid -- and id
40's path on 385-395 moves by only 0.1-0.3 m: the endzone's own x drift there (-27.1 -> -25.2 in ten
frames) agrees with the sideline sightings on both sides, so he is RUNNING at 6 m/s and the ghost on
the strip is a lateral offset the hold cannot touch. (a) REJECTED, kept opt-in
(`load_play_timeline(blind_axis=True)`) with its numbers in the module. (b) ADOPTED: live steps
7 -> 5 (203's two gone), census unchanged. Commit 6cb2a1a.

The absolute step ruler counts sprinters: four of the five live steps left are id 40's strides at
0.26-0.33 m/frame (8-10 m/s, a defensive back in coverage) and none of the five is a step that
disagrees with its neighbours. New ruler `motion_rulers.jerk_steps` (commit c299ddb): a contiguous
step more than 0.15 m longer than the median of its neighbouring steps (3 each side) -- a hop, not a
stride; 07l prints it beside the absolute count (which stays for teleports). 07l v51 (orphan rule in)
follows; the hop count on the live play is the number to carry from here.

**07l v51 = v50 + the orphan rule (18:55).** Live steps > 0.25: 7 -> 5 (203's two gone), every other
ruler identical to v50 (root jitter live p90 0.0119, census 1.50 / 2.51, hinges 0/0, joints p90 0.0326,
p99 0.069). With the hop ruler: hops full 38, LIVE 4 -- id 37 0.27 m (+0.21 over its neighbours) @376,
166 0.25 (+0.18) @300 (the snap), 74 0.23 (+0.17) @419, 17 0.18 (+0.15) @414; id 40's strides are
not among them. Those four frames are the next strips.

Id 40 on the footage, three windows (19:00). Sideline 377-384 (no sideline detection either): the
drawn body stands ~1 m along the field from the real man in every frame. Sideline 395-400: at 395-396
still off him; from 398 the sideline sees him and the body sits on him. ENDZONE 386-393 (where he IS
detected): the green keypoints are on the man and the drawn body is offset ~40 px up-left of them --
further along the endzone's depth and a little across -- so the endzone-only placement does not even
land on the endzone's own keypoints. The ~1 m is made somewhere between the endzone foot point and the
drawn body: the refit placement (place_from_refit, 1 m reach), the run smoother (smooth_xy over a run
that mixes endzone-only and sideline frames), or the foot point itself (a running man's lifted foot).
Measuring per frame at the timeline (both cameras' lower joints, default vs no refit placement).

Result (19:00, scratch probe_id_timeline_reproj): id 40's lower joints reproject 86-112 px off the
ENDZONE keypoints on every frame 374-400, endzone-only and two-view frames alike, and turning the
refit placement off changes nothing (identical to the pixel) -- the offset is in the ground point
itself or the run smoother, not the refit. Isolating placement from the legs' pose next: the drawn
pelvis against the keypoints' hip centre, per camera (scratch probe_pelvis_offset, ids 40 / 37 / 74 / 17).

The four live hops on the footage (05q strips, 19:00): 37 at 372-379 -- a lineman in the pile, the
sideline keypoints steady on him while the drawn body sits 30-40 px off and drifts, the hop at 376
is the drawing moving, not the man (a two-camera id: 41 both / 44 sideline / 36 endzone frames).
74 at 415-422 -- drawn ~60 px left of the pile with no sideline keypoints until 421, then still
60 px off them: an endzone-only stretch handed to the sideline with its offset. 166 at 297-304 -- the
snap, a lineman firing off with the sideline keypoints gone; the body shifts a little. 17 at 410-417
-- keypoints on him to 413, then none; the crop jump at 415 is 05q switching from the box to the
projection for its crop centre, the body moves 0.18 m. All four are placement offsets of 0.2-0.3 m
at camera-source transitions in the line or the pile: the hop population is now four frames of 3600
on the live play, none over 0.3 m. The thread worth pulling is the OFFSET: bodies drawn 30-60 px
off their own sideline keypoints on frames that have them, next to unseen stretches (37, 74). A
population probe is running: sideline-seen body-frames' lower-joint px at the timeline placement,
binned by distance to the id's nearest unseen frame.

Result (19:05, scratch probe_seen_offset; 3185 sideline-seen body-frames on the live play, lower
joints px at the timeline's placement):

    distance to the id's nearest unseen frame    n     p50    p90
    0-2 frames                                  216    10.1   22.7
    3-6                                         231     8.7   14.8
    7-15                                        285     7.9   12.8
    16+                                        1342     6.3   14.1
    the id is never unseen on the play         1111     4.6    8.5

The two frames beside an unseen stretch are twice as far off their own keypoints as a frame of a
body every camera always saw, and the error decays with distance: something carries the unseen
frames' offset into the seen ones. Suspects, in order: the run smoother (timeline.smooth_xy, window
9, averaging seen with unseen points), the gap fill, the ankle anchor window (15). A/B running with
the smoother replaced by the identity (bins, root jitter, hops, census).

Placement alone (19:10, scratch probe_pelvis_offset: the drawn pelvis against the keypoints' hip
centre, px, drawn minus keypoints): id 40 in the ENDZONE is 70-78 px ABOVE his own hips on every
endzone-only frame 374-396 (further along that camera's depth) and still 34-38 px above, 55 px left,
on the two-view frames 398-400 -- the depth snap inherits it. Id 37 (two-view, the hop at 376/377):
endzone dx jumps 32 -> 67 px across the image between 376 and 377 while the sideline dy goes 20 -> 12
-- the body moved ~0.7 m along the sideline's depth in one frame: the depth snap changing its answer.
Id 74: endzone 45-50 px BELOW his hips (nearer the endzone camera) and 66 px right on 414-417, the
sideline 12 px below on 421-424. Id 17 (in the line, both cameras): 2-6 px, fine.

So the endzone-derived depth is off by ~1-2 m in both directions on running and piled men, and the
depth snap carries it onto the sideline's ray. Mechanism hypothesis: the endzone ground point is
the ANKLE keypoints' ray met with the ankle plane (ankle_ground, z = ANKLE_Z_M). That camera sits
low behind the goal line (~6 deg elevation at 88 m), so a foot lifted 0.4 m in a stride puts its
ground point ~3 m too deep, and a foot in a pile the other way; the sideline at ~24 deg is four
times less sensitive. The HIPS sit at ~0.95 m running or standing -- a 0.1 m spread -- so an
endzone ground point from the hip centre met with the hip plane would err ~1 m at worst instead of
3. Test: endzone target points from the hips (z = HIP_Z_M) instead of the ankles, everything else
unchanged; rulers = the endzone pelvis offset over every frame with endzone hips (p50/p90, the
population ruler of this defect), the sideline pelvis offset (must not move), live hops, census,
root jitter.

Smoother A/B (19:15, scratch probe_seen_offset_ab): with timeline.smooth_xy replaced by the identity
the bins barely move (0-2 frames: p50 10.1 -> 9.3, p90 22.7 -> 21.3; never-unseen 4.6 -> 4.7) while
root jitter live p90 goes 0.012 -> 0.043 and live hops 4 -> 67. The smoother is NOT what carries
the offset -- the ground points beside an unseen stretch are already off before smoothing, which
is what the endzone-depth hypothesis predicts (a two-view frame beside an endzone-only stretch
takes its depth from the same endzone foot point). DENIED; the smoother stays.

Lowest-ankle foot point A/B (19:25, scratch probe_lowest_ankle; the defect's own ruler = the drawn
pelvis against the endzone keypoint hips over every live frame that has them, n 1889): shipped mean of
both ankles |d| p50/p90 43.4/121.6 px; lowest ankle for the endzone 43.9/121.6; for both cameras
43.4/121.6 -- NOTHING moves, and census / root jitter get a hair worse (1.50 -> 1.53/1.55, p90 0.0120
-> 0.0126/0.0129). DENIED: the lifted stride foot is not the mechanism. The population number is the
finding: the drawn bodies sit 43 px from their own endzone hips at the median and 122 at p90, against
4.3 / 9.9 in the sideline -- a general endzone misplacement, not a few running men. Next: is it a
BIAS (one direction: the endzone camera itself, or a systematic depth rule) or scatter (per body)?
Vector statistics by views / team / depth band / id running.

Bias vs scatter (19:35, scratch probe_endzone_bias, 1889 live body-frames with endzone hips): the
overall median vector is small (dx -15, dy +6 px) but only 29 % of frames are within 20 px and 47 %
within 40 -- scatter, not one bias. It is structured: by team Baltimore dx -34 / Kansas City -1; by
field position the Baltimore side of the line (x < -26) dx -45 to -50 while the Kansas City side
(-26..-22) is +1 -- a horizontal shift in the endzone image is a y error in the field (the sideline's
DEPTH axis), so bodies on the defence's side stand ~1 m off along the sideline's depth while their
sideline hips match at 4-6 px. Two-view frames (n 1616) carry it (dx -17.5, |d| p50 42.5), so the
depth snap is not curing it there. Per id: 9 is 528 px off in the endzone (its endzone rows are
another man -- a mispair), 74 / 40 / 0 / 7 / 2 at 54-88 px with sideline 3-6 px; 3 / 11 / 5 / 13 / 15
at 8-17 px are fine. Next ruler: triangulate the hip centre on two-view frames (both cameras' hip
keypoints) and compare with the timeline's xy in field metres, by team and band -- if the y
disagreement is the ~1 m, the sideline's depth (foot point + snap) is the mechanism and the
triangulated hips are the fix for paired frames.

Gap bridge A/B (19:35, scratch probe_gap_bridge): bridge 30 (shipped) drawn 3607 live body-frames,
93 unseen by either camera; bridge 10: 3561 / 53, live hops 4 -> 4, steps 5 -> 5, census 1.50 ->
1.32, root jitter p90 0.0120 -> 0.0116; bridge 4: hops 6, steps 12, census 1.36 -- too short. Bridge
10 wins on every ruler measured; the ruler it lacks is POPS (a body vanishing and reappearing),
which no ruler counts yet -- counting them for 30 vs 10 before adopting.

Pops (19:50, scratch probe_pops; an id drawn, absent 1-30 frames, drawn again, live play): bridge 30
= 34, bridge 10 = 32. Not worse on the one ruler it lacked, better on census, jitter and unseen
body-frames, equal on hops and steps: bridge 10 ADOPTED as `timeline.FILL_GAP_FRAMES` (commit
a11555b; the span and anchoring rules keep MAX_GAP_FRAMES 30). Goes into 07l v52 with whatever the
hip A/B decides.

**Hip triangulation vs the timeline (19:45, scratch probe_tri_hips).** 1717 live two-view frames
have a confident hip pair in both cameras; the hip centre triangulated from the two rays lands at
0.77 m (p10 0.60, p90 0.92 -- crouching to standing), the rays pass within 0.13 m of each other at
the median, and the point reprojects onto the hips at 5.3 px (sideline) / 8.4 px (endzone). 1541
(90 %) pass a ray gap < 0.5 m and hip height 0.5-1.4 m. The timeline's point against them, field
metres: dx +0.04 (|dx| p50 0.07, p90 0.18), dy -0.10 (|dy| p50 0.20, p90 0.58); by side of the
line, Baltimore's side dy -0.33 to -0.38 (x < -26), Kansas City's +0.01; worst ids 74 +0.62, 0 -0.49,
7 -0.48, 2 -0.34. So the geometry is fine and the sideline foot point + depth snap is what stands
0.2-0.6 m off along the sideline's depth, one way on the defence's side. Built: render/tri_hips
(triangulated_hips with the two gates, place_on_triangulated_hips), wired into load_play_timeline
behind `tri_hips=` (off until measured), tests. A/B next: endzone pelvis offset (the defect's ruler,
expect 42 -> ~10 px on paired frames), sideline pelvis offset (control), endzone lower joints,
hops, steps, census, root jitter.

First A/B (20:00, scratch probe_tri_ab): 4483 body-frames placed on triangulated hips (median move
0.15 m, p90 0.34) -- and the endzone pelvis offset does NOT move (43.4 -> 43.6 px p50, 121.6 p90),
sideline 4.3 -> 4.3, while live hops go 4 -> 2 and root jitter p90 0.0120 -> 0.0117, census equal.
The ground point is not what is drawn: place_from_refit then replaces it with the refit record's
own transl on every fitted frame within 1 m (5038 body-frames on the clip), and the two-view fit's
transl is what stands 43 px off the endzone hips -- its endzone weight is 0.3 and its place term
pulls toward the OLD ground point it was fitted with. So the triangulated hips only reach the render
where the refit is absent. Next: keep the triangulated point on its frames (skip the refit
placement there) and measure again; the memory says the refit placement halves root jitter, so
that ruler decides with the endzone offset.

Second A/B (20:10, the triangulated point kept through the refit placement; both arms on the new
10-frame bridge): endzone pelvis |d| 43.4 -> 44.2 px (p90 121.6 -> 123.5), sideline 4.3 -> 4.9,
live hops 4 -> 7, steps 5 -> 9, census 1.32 -> 1.43, root jitter p90 0.0116 -> 0.0217. REJECTED
hard: 4483 frames on the triangulated hips beside 2853 on the refit's transl, the two sources 0.2-0.6
m apart, so the run alternates between them wherever a hip pair's confidence dips -- jitter doubles,
and the endzone number cannot fall while half the frames are still the old point and the smoother
blends the halves. Same shape as the ankle-vs-box switching of 09-15, same remedy: not the points but
a windowed MEDIAN offset (triangulated minus placed) per id, applied to every frame
(`tri_hips.anchor_ground_to_tri`, window 15, support 3), after the refit placement. Measuring.

Third A/B (20:25, the anchor): 5872 body-frames shifted by a MEDIAN OF 0.04 m (p90 0.09) -- and the
endzone pelvis offset is still 44.3 px, sideline 4.3 -> 4.9, hops 4 -> 6, steps 5 -> 9, census 1.32
-> 1.40, jitter 0.0116 -> 0.0122. REJECTED (three forms of tri_hips lost; the flag stays off). The
number that matters is the 0.04 m: at the point where the anchor acts (after the depth snap and the
refit placement), the placed ground points already agree with the triangulated hips to 4 cm at the
median -- yet the drawn bodies end 0.2-0.6 m from those hips. So the divergence is made AFTER that
point, inside build_timeline (gap fill, the run smoother, the dedupe) or in how the state's xy is
turned into a drawn pelvis. Capturing the ground handed to build_timeline and comparing it per frame
with the final xy and the triangulated hips for ids 7, 2, 0, 74 (running).

**RETRACTION (20:35): the endzone side of every scratch ruler written tonight was half a second off.**
The probe found ground -> final xy 0.01 m (build_timeline moves nothing) and ground -> triangulated
hip +0.29 m for id 7, i.e. the placed point was already "0.3 m off" -- and the anchor had said 0.04 m.
Reading the frame arithmetic: the trusted tools (05t, 05q, the cross-view scorer probe_cache_in_timeline)
take endzone clip frame = timeline frame + offset (offset = -15); the probes written tonight from
probe_orient_flip2 onward used timeline frame - offset, thirty frames (0.5 s at 59.94 fps) the other
way. A man moving 2 m/s is a metre from where those keypoints say, a standing lineman is not -- which
is exactly the "structure" I read as a defence-side depth bias. INVALID: the endzone columns of the
unwrap A/B and the blind-axis A/Bs (their sideline / jitter / hops / census columns and the render
strips stand), the pelvis-offset table (id 40 "70 px deep"), the bias-vs-scatter analysis, the hip
triangulation and all three tri_hips A/Bs (they compared a body with keypoints from another instant;
the "0.2-0.6 m" was the man's own motion), the lowest-ankle A/B's endzone column, the
id_timeline_reproj endzone column. VALID: the unwrap (sideline, jitter, strips, render), the orphan
rule, the fill bridge, the blind-axis rejection (steps and census), the geodesic and spine-20
decisions (the cross-view scorer indexes correctly), the seen-frame offset bins (sideline only).
Re-measuring with frame + offset: the pelvis offsets, the bias table, the triangulation. The lowest
ankle is re-measured too (its ruler was the broken one). tri_hips stays off and its docstring is
corrected once the numbers are real.

**Corrected numbers (20:50, frame + offset).** Endzone pelvis offset over 2062 live body-frames with
endzone hips: |d| p50 9.8 px, p90 19.0, 92 % within 20 px, 97 % within 40; two-view frames 9.5 / 18.2,
endzone-only frames 15.8 / 60.3 (n 133); no team or field-side structure (dx 0.4, dy 7.4 overall).
Hip triangulation on 1883 two-view frames (all pass the gates): rays meet within 0.06 m, hip height
0.84 m, reprojection 2.6 / 4.1 px, and the timeline's placement is 0.04 m (x) / 0.02 m (y) from it
at the median, 0.08 / 0.05 at p90, no id above 0.10. THE PAIRED PLACEMENT IS RIGHT. The endzone-depth
thread is closed; what remains of it is the endzone-only stretches (133 body-frames, p90 60 px, id
198's eight frames at 67 px), a population too small to chase before play 2. render/tri_hips is kept
as a ruler (the triangulation and its gates, docstring rewritten with these numbers); its placement,
keep-set and anchor code are deleted (commit below). The lowest-ankle A/B is re-run on the corrected
ruler for completeness.

Unwrap A/B re-measured on the corrected ruler (20:55): endzone lower joints p50/p90 12.4 / 21.4 (v49
timeline) -> 12.4 / 20.8 (unwrap), sideline limbs 7.2 / 16.2 -> 7.1 / 15.0, joint jitter p90 0.0354 ->
0.0327 (n 3169 body-frames). The unwrap is better on every valid column, the other camera included;
the earlier "endzone unchanged at 51.8 / 129" was the broken index (its level alone should have
said so: 129 px at p90 is a body length).

**07l v52 = v51 + the 10-frame fill bridge (21:00; the v48 render's timeline).** Live steps 5, hops
4 (37 @376, 166 @300, 74 @419, 17 @414), root jitter live p90 0.0119 -> 0.0115, census live 1.50 ->
1.32 (KC 10.78, BAL 11.34), whole clip 2.51 -> 2.42, hinges 0/0, joints p50/p90/p99 0.0106 / 0.0327 /
0.0689 unchanged, 13958 body-frames drawn (v51 14127). Render v48 = this timeline on the same cache,
strips auto-cut to scratch review_v48.

**Pops, classified (21:05, scratch probe_pop_classes).** The 32 pops on the live play are all GAP pops
within one id -- absent for 2 frames at the median, back 0.17 m away -- and not one is a fragment
handover (no id end is followed within 6 frames and 1 m by another id's start). They sit on ids in
the line and the pile (166: 5, 40: 4, 11 / 13 / 204: 3 each). Separately, 12 ids START mid-play with
no predecessor (37 @340, 38 @345, 74 @366, 40 @368, 80 @377, 39 @384, 167 @411, 197 @435, 84 @437,
198 @453 ...) and 7 END with no successor -- bodies appearing from nowhere and vanishing for good,
the rules admitting an id late (span, endzone-only, edge) or a fragment ending. A two-frame
absence with the body 0.17 m away is not a detection gap (the bridge is 10 frames): a timeline rule
removes the body on those frames -- the dedupe box when two bodies pass within DUPLICATE_M is the
suspect. Probing which rule and how close the nearest other body stood.

Lowest-ankle foot point on the corrected ruler (21:10): endzone pelvis |d| 9.8 / 19.0 (mean of both
ankles, shipped) -> 10.1 / 20.1 (lowest, endzone) / 10.1 / 19.8 (both cameras); census 1.32 -> 1.37,
root jitter p90 0.0116 -> 0.0122 / 0.0125; hops 4 -> 3, steps 5 -> 4 / 3. Worse on the ruler it was
built for and on census and jitter, better on two counts of small hops: DENIED for good. The mean of
both ankles stays.

Pop cause (21:15, scratch probe_pop_cause; the ground handed to build_timeline captured, then the
drawn states): two classes. (A) 18 pops where the id is NOT in the ground on the missing frames and
both neighbours are sideline-only (1, 11, 13, 19, 195, 82, 166 x5, 167, 197): a 1-5 frame hole in a
long-lived sideline id's detections; the bridge fills it, then dedupe_frames deletes the filled
frame because it is unanchored (no sideline detection of this id on that frame) and another body
stands inside DUPLICATE_M -- the rule built for fragment tails (a second id riding a detected man)
firing on a momentary dropout of the man himself. (B) 14 pops where the id IS in the ground and the
nearest other drawn body is 0.06-0.44 m away on the missing frames (204, 171 for 8 frames, 40, 17):
two ids on one man, the box killing this one on the frames it is filled and sparing it where it is
detected -- twin flicker. Remedy for (A): a filled frame whose id has a sideline detection within a
few frames on BOTH sides is a hole, not a tail, and stays anchored. Remedy for (B) is the twin
question (08o folds twins on the tracks; a stretch-consistent dedupe in the timeline would be the
render-side answer). Building (A) first; rulers = pops, census, hops, steps.

(A) built as `timeline._holes_by_frame` + `dedupe_frames(holes=)` (HOLE_REACH, commit c59c01b): an
interpolated state whose id the sideline detected within 6 frames on both sides is kept outright.
A/B on the live play (21:30, scratch probe_hole_ab): pops 32 -> 10, drawn body-frames 3561 -> 3601,
live hops 4 -> 4, steps 5 -> 5, census 1.32 -> 1.32 (KC 10.78 -> 10.96, BAL 11.34 -> 11.41), root
jitter p90 0.0116 -> 0.0129, p99 0.0606 -> 0.0692, duplicates dropped 1251 -> 1042; reach 12 takes
pops to 4 but the census to 1.45. ADOPTED at 6: twenty-two fewer vanish-and-reappear events per
live play for 1.3 mm/frame^2 of root jitter at p90. 07l v53 and render v49 (chained behind v48)
carry it. The 10 pops left are class (B), the twins.

**07l v53 = v52 + the hole rule (21:40; the v49 render's timeline).** Live steps 5, hops 4 (same
four), root jitter live p90 0.0115 -> 0.0125 (p99 0.0607 -> 0.0680), census live 1.32 (KC 10.96,
BAL 11.41), whole clip 2.42 -> 2.46, hinges 0/0, joints p50/p90/p99 0.0107 / 0.0329 / 0.0689,
14131 body-frames drawn (+173 over v52). The jitter cost is the readmitted filled frames; pops are
the number that moved (32 -> 10) and 07l does not print them yet -- probe_pops does.

**Twins on the live play (21:45, scratch probe_twins; drawn pairs within 0.45 m on >= 5 frames).**
Ten pairs. Two are twins beyond doubt: 166-204 (KC/KC, 23 frames 406-431 at 0.15 m, both sideline-
detected on 11 of them) and 1-40 (BAL/BAL, 19 frames 396-415 at 0.13 m, both detected on 9) -- two
sideline boxes 0.13-0.15 m apart on one man for twenty frames, each drawn as a body. The rest sit
at 0.27-0.43 m in the pile (19-166, 197-204, 19-37, 13-197, 82-166, 4-167, 17-204, 37-166), where two
real men can stand that close. 08o folds twins found by ankle rays at 0.03-0.11 m; these two are just
above it. Render-side rule to measure: a same-team pair within 0.2 m on >= 8 consecutive live frames
is one man, and the id with fewer drawn frames loses the stretch (the rider rule for long ids);
rulers = pops, census (a twin was a ghost in the count), hops, drawn body-frames.

A/B post-hoc on the v53 timeline (scratch probe_twins_ab; clock 20:25 -- the timestamps written into
this file since "18:05" ran ahead of the real clock by 60-80 minutes, I estimated instead of reading
`date`; the order of events is right): twin 0.2 m / 8 frames drops 111 body-frames on the clip (live:
40 at 399-413, 166 at 417-431 -- the two verified twins -- plus 21, 82 pre-snap and 60 / 75 / 197 /
205 after the whistle): census live 1.32 -> 1.20 (KC 10.96 -> 10.84, BAL 11.41 -> 11.32), live hops
4 -> 4, steps 5 -> 5, pops 10 -> 11 (the loser vanishes for its stretch and returns), drawn 3601 ->
3567. 0.25 m also takes 196 pre-snap (152 frames, census 1.19); 0.2 / 5 adds 168, 171 (139 frames).
ADOPTED at 0.2 / 8 (`timeline.TWIN_M`, `TWIN_MIN_RUN`, wired after the orphan rule): a body drawn twice
on one man for fifteen frames is worse than that copy vanishing. 07l v54 = v53 + twins; the v49 render
starts after v48 and picks this up, so v49 = v54's timeline.

**07l v54 = v53 + twins (clock 20:40).** Live steps 5, hops 4 (unchanged four), census live 1.32 ->
1.20 (KC 10.84, BAL 11.32), whole clip 2.46 -> 2.44, joints unchanged (p99 0.069); 111 twin body-frames
out (40 399-413, 166 417-431 on the live play).

**Ids starting mid-play, characterised (scratch probe_late_starts; team count over the five frames
before and after the start, nearest same-team body at the start).** Hole-fillers: 37 @340 (KC 9 -> 10)
and 38 @345 (KC 10 -> 11), both admitted by the endzone after the sideline lost them in the line --
right. Twins at birth: 171 @331 (0.13 m from a teammate), 84 @437 (0.12 m), 80 @377 (0.23 m), 197 @435
(0.30 m) -- they start on top of a drawn teammate and drift apart, too briefly for the 0.2 m / 8-frame
twin rule. Twelfth men: 40 @368 (BAL 11 -> 12, 1.7 m from anyone), 74 @366 (KC 11 -> 11.8), 39 @384
(25 frames), 167 @411 (10 frames, KC -> 13), 198 @453 (BAL 11 -> 12, endzone-only) -- real detected
players under a label the count already has, the run-surplus thread the census memory closed on
09-13 (no removal route that does not delete a real man). Recorded as the population; not pursued.

**v48 delivered (20:42): diag/play_001_v48_hifi_720.mp4 = v47 + the orphan rule + the 10-frame
bridge (07l v52's timeline).** Run sheet 344-454 (scratch review_v48/run_sheet.png): eleven white
and eleven red bodies through the run, the pile forming at 404-424 and breaking up by 444, nothing
floating, nothing lying down. v49 (+ hole rule + twins, 07l v54) started 20:44; its six strips and
a second review batch (ids 2, 7, 12, 3, 15, 30, 74, 37, 17, 40, 4, 11 and a 5-frame-stride sheet of
the whole live play) cut automatically when it lands.

**v49 delivered (21:33): diag/play_001_v49_hifi_720.mp4 = v48 + the hole rule + the twin stretch
rule (07l v54's timeline); the render log shows both firing (203's nine frames, 111 twin frames).**
Phase sheets (scratch review_v49/phases): pre-snap 100-300 -- the formation holds through the
cadence, a deep safety top-left, the Kansas City line in stances, the two split receivers, no white
body in the red line, the line filling in at 260-300 as the men set; post-whistle 460-640 -- the
crowd bunching bottom-right, lone bodies walking, a white body down at 640; nothing floating or
lying down on the play itself. Id 166 (a KC lineman) at 330-344: in a block, the line seen from the
side so the linemen overlap in the image (the camera's angle, not a defect). Whole-play sheet at
5-frame stride and twelve more per-id strips are cutting (review_v49/more).

v49 read (21:40, scratch review_v49/more): the 33-frame sheet of the live play at 5-frame stride --
the line holds 300-396, the pile forms 400-420, the play breaks to the near sideline 420-460, no
body floats, no team swaps, nothing lies down before the tackle. Id 2 (a Baltimore defender, 330-358):
standing then a natural arm raise, smooth. Id 74 (KC, 410-424): in a tackle scrum under two white
bodies, plausible. Id 40 (BAL, 380-394): running with bent knees and swinging arms -- and a second
white body drawn ON him at 380-386, the 1-40 twin before the stretch the 0.2 m rule takes (396-415):
the twins at 0.2-0.45 m still draw two bodies on one man for a few frames. Measuring TWIN_M 0.3 /
0.35 post-hoc (census decides: at 0.3 the pile pairs 19-166, 197-204, 19-37 come into reach, and
those may be two men).

Wider twin radii, post-hoc on the v54 timeline (21:50): 0.3 / 8 drops 51 more body-frames, 0.35 / 8
87, 0.3 / 12 43 -- ALL of them pre-snap (21 197-212, 196 132-209) or after the whistle (205, 76, 168,
198); on the live play nothing changes (drawn 3567, census 1.20, pops 11). The 1-40 double at 380-386
is not a within-0.3-m-for-8-frames case: they touch and part. TWIN_M stays 0.2 / 8; that double is
recorded as the residue.

Id 11 on the v49 strip (420-434) still vanishes on 422 and 428. Trace (scratch probe_id11_hole): the
sideline sees him 410-420 and again from 429 -- an eight-frame hole, one past HOLE_REACH 6, so the
bridge fills 421-428 but the dedupe deletes 422 and 427 as unanchored interpolated bodies near a
detected one, and 428 (endzone-only) falls to the one-view box (13 stands 1.49 m across). Measuring
reach 8 and 10 against 6 (reach 12 cost census 1.32 -> 1.45 earlier).

Reach A/B with the twin rule in (22:00): reach 6 pops 11 / census 1.20 / jitter p90 0.0122; reach 8
pops 7 / 1.19 / 0.0124; reach 10 pops 5 / 1.21 / 0.0126; hops 4 and steps 5 throughout. Eight wins
on pops and census: HOLE_REACH 6 -> 8. 07l v55 and render v50 (with a strip of id 11 at 420) follow.

**07l v55 = v54 + reach 8 (22:10; the v50 render's timeline).** Live steps 5, hops 4, root jitter live
p90 0.0120 (p99 0.069), census live 1.19 (KC 10.86, BAL 11.32), whole clip 2.47, joints p99 0.069.

**Facing vs motion, a new ruler (22:15, scratch probe_facing):** on the 260 live body-frames with
root speed > 0.1 m/frame, the angle between the body's forward and its velocity is 43 deg at the
median, past 90 on 17.7 %, past 135 on 3.5 %. Who runs "backwards": 6 (a Baltimore back, 12 frames
at 135 -- a backpedal), 166 / 19 / 5 (Kansas City linemen at 93-116 -- pass sets, retreating
squared up), 13 at 72; the runner 9 faces his motion at 13 deg over 132 frames, 3 / 11 / 204 / 74 /
40 under 60. Every past-90 case is a man who really moves backwards or sideways. No defect; the
ruler stays as a check for other plays.

**THE FEET SKATE (22:25, scratch probe_skating -- a new ruler).** On the 244 live body-frames where a
body moves faster than 0.1 m/frame, the slower ankle's WORLD speed is 0.94 of the pelvis speed at the
median and a foot is planted (under 0.3 of it) on 1 % of frames. A real runner plants one foot about
half the time: the foot stands still on the turf while the body passes over it. Every moving body on
the play glides with its legs cycling too little -- the runner 9 (132 frames, ratio 0.93, planted
2 %), 40 (1.00), 19 / 166 / 74 (1.00), 3 (0.86), 11 (0.56 -- the least bad). This is the "moonwalk"
of fitted motion and a viewer sees it without a ruler. Where is the plant lost? Either the sideline
keypoints themselves never plant (the detector on a 100-px blurred sprinter) or they do and the
pipeline damps the legs (the fit's temporal term at 3.0, the stride-2 keyframes with SLERP between,
the sigma-2 Gaussian). Measuring on the runner: each ankle keypoint's image speed against the hips'
image speed, beside the same for the drawn body (scratch probe_plant).

Result on the runner (322-372, 49 frames): the ankle KEYPOINTS' slower foot moves at 0.91 of the hips'
image speed (planted under 0.3 on 8 % of frames); the drawn body's at 0.77 (4 %). The keypoint ankles
jump 0.2 -> 15 px/frame from one frame to the next on a body whose hips move 3-6 px/frame: the
detector's ankles on a blurred 100-px sprinter carry no stance phase, so the fit cannot have one,
and the smoothers do not add or remove one. The skating is a DETECTOR LIMIT of the 2D keypoints;
the remedy is on the gait side: detect stance from the fitted leg cycle (the drawn ankle's world
speed dips to 0.3-0.4 of the pelvis speed every 8-15 frames on the runner) and lock the planted
foot to the turf with a two-bone leg IK while the pelvis keeps its smoothed path -- the leg then
extends behind the body as it passes over the foot, which is what running looks like. Cost to
measure: the sideline lower joints (the locked foot leaves its noisy keypoint by the skate distance,
0.1-0.3 m = 8-24 px), joint jitter; gain: the planted share (1 % -> ~40 %) and the render strip of
the runner. Building it opt-in.

Built (`render/foot_lock.py`, commit fba3c97: stance = the drawn ankle under half the pelvis speed for
2-8 frames, the foot pinned to the segment's median xy, hip and knee re-solved by a numpy-FK
least-squares; tests pass) and measured post-hoc on the live play (scratch probe_footlock_ab): 22
stance segments over all ids, 90 frames, the pinned feet moved 1-6 cm at the median (10 cm at most),
planted share 1 % -> 2 %, ratio p50 0.94 -> 0.94, sideline lower joints 9.9/16.2 -> 9.9/16.2, joint
jitter p90 0.062 -> 0.068. NO EFFECT: the criterion reads stances off dips the drawn legs do not
have -- they hardly cycle -- so it finds a few shallow ones and moves a foot a few centimetres. The
lock is left opt-in as a tool (it does what it says when a stance exists); the defect needs a stance
the data does not contain. That is a gait model: cadence from the body's speed (about 2 Hz at 8 m/s),
alternating stance phases, and leg motion synthesised to plant each foot -- motion synthesis over the
fit, which is a product decision (fitted legs that skate vs animated legs that plant) and a day of
work. Recorded as the next hypothesis class; the skating share goes into 07l as a standing ruler.

07l v56 (same timeline as v55, the skating ruler added to the report, commit 16261e5): skating p50 0.94,
planted 1 % of 244 moving frames; everything else as v55.

**Two decisions for the user (both product, both recorded, neither taken):**
1. Post-whistle: the render runs to frame 647; after ~500 the bodies are the crowd and the pile
   with no mechanism left to fix (the steps over 0.4 m are all after 500). Ending the clip at the
   tackle (05k `--limit` or a frame cap) is one flag.
2. Skating: fitted legs glide (planted 1 % vs ~50 % real). The only fix is a gait model over the
   fit -- cadence from speed, alternating stances, legs synthesised to plant, blended below the
   hips -- i.e. animated legs on fitted bodies. A day's work, and a different kind of footage
   (the legs would no longer follow the detector). Not started without a yes.

**v50 delivered (22:35): diag/play_001_v50_hifi_720.mp4 = v49 + HOLE_REACH 8 (07l v55/v56's
timeline).** Id 11 at 418-432 on the render strip: present on every frame, moving through the scrum
-- the two vanishes of v49 (422, 428) are gone on the footage. AFFIRMED. Delivered clips tonight:
v45 (82 re-teamed, rider rule), v46 (the v49 recipe, the before-footage), v47 (+ the half-turn
unwrap), v48 (+ orphan rule, 10-frame bridge), v49 (+ hole rule, twins), v50 (+ reach 8).

Twins at birth, measured post-hoc (22:45, scratch probe_birth_twins; an id whose first frame stands
within 0.3 m of a same-team body loses its frames while it stays on him): 6 body-frames (80 one
frame, 84 five), census 1.19 -> 1.15, pops 7, hops 4; at 0.4 m 16 frames (197 too), census 1.17.
Measured and NOT adopted: six frames is below what a viewer can see and not worth a rule; revisit
if play 2 shows the class at scale.

**Where the loop stands at 22:45.** Every mechanism the footage named tonight that had a
measurable fix is shipped and affirmed on the render (v47-v50); the rulers that remain on the live
play -- steps 5, hops 4 (all 0.18-0.27 m at source transitions), pops 7, census 1.19, joints p99
0.069, flails 1.8 % (real hands) -- are at the floor of what the rules can reach. What is left is
the two product decisions above (clip end, gait model), the runner's handoff 15 px (ambiguous
between two fits), and the twelfth-man thread (closed 09-13). Next play is the next signal.

**RESUME PLAN (machine off 2026-09-16 ~10:10; nothing running that matters).** Shipped state on disk:
poses_refit.json = the two-view hard-hinge cache (v47; .pre_tw3 is its copy), timeline with Gaussian
sigma 2 on body_pose and sigma 4 on orientation (report v48), renders v39..v44 in diag. Scratch caches
for the eight worst ids in `scratch/`: refit_tw3.0.json (temporal 3.0), refit_unseen5.json (unseen-limb
hold 5), refit_tw3u5.json (both).
  1. DONE before the shutdown (10:12): the combination scorer landed. At the timeline's placement,
     eight worst ids: C 0.144 / endzone 19.8-28.0 / sideline 9.8-22.2; temporal 3.0 0.079, off-axis
     0.5 % / 19.9-29.7 / 10.1-24.0; unseen 5 0.114 / 19.8-27.9 / 9.7-21.6; BOTH 0.079 / 19.9-29.7 /
     10.1-24.0 -- identical to temporal 3.0 alone: at that weight the temporal pull already holds an
     unseen limb, and the extra multiplier adds nothing. Winner: `--temporal-weight 3.0` alone.
  2. Whole-play refit with the winner: `PYS scripts/05p_refit_mono.py --play-dir P --two-view
     --endzone-weight 0.3 --temporal-weight 3.0 --workers 6` (~100 min; back
     up poses_refit.json first). Then `07l --tag v49 --joints` and the cross-view scorer with the new
     poses_refit.json as the extra argument; ship if joints improve with steps / root / census / endzone
     not worse than v48 (live 11, root live p90 0.0128, 1.65, endzone lower 19.8 / 28.0 on the worst ids).
  3. If shipped: set Mono2DConfig.temporal_weight default to 3.0 (unseen_temporal_mult stays 1.0),
     commit with the table, render v45 (`scratch/launch_v44.sh` with v45 substituted).
  4. Open product decision for the user: end the render at the tackle (~frame 500); post-whistle steps
     are the crowd and have no mechanism to fix.

**Local repair step 1, hold-through, measured and REJECTED as a default (2026-09-15).** Stretches
where the raw fit's max joint speed exceeds 0.25 m/frame (merged within 3 frames, padded 2): 85 on
the live play. Replacing a stretch's body_pose by the SLERP between its clean boundary poses, then the
shipped clamp + Gaussian (jitter p50/p90/p99; reprojection sideline p50/p90, endzone p50/p90):

    shipped              0.019/0.144/1.11   9.2/21.0   6.5/15.9   0 frames
    hold <= 12 frames    0.018/0.132/1.11   9.3/21.1   6.5/16.8   418 frames, 31 stretches too long
    hold <= 24           0.018/0.120/1.13   9.4/22.0   6.5/17.3   626, 18 skipped
    hold <= 48           0.018/0.118/1.08   9.4/22.3   6.5/17.5   664, 17 skipped

The same trade curve as the sigma sweep (0.01 of jitter for ~0.5 px), and the p99 does not move: the
garbage is in the LONG stretches (17 of 85 run past 48 frames), where holding is a mannequin. A
post-hoc repair cannot make a good pose from a bad one; the fix belongs in the fit -- a temporal term
across neighbouring keyframes and joint limits inside the optimiser, so the pose that matches the
keypoints is also one a body can hold. That is the next build, not another smoother.

**A false bug report avoided, worth recording.** I suspected this 2024 play had been resolved against the
2025 roster, because `roster.py` reads names only from a `player_name` column (the 2025 schema) while the
2024 file stores them under `full_name`, and yet identities carry names. The check disproved it: "Swayze
Bozeman" is in the 2024 table (KC 55, LB, DEV). My query had printed `player_name` for both files, so the
2024 names were never displayed at all. The schema difference is real; the conclusion drawn from it was not.

Worth recording separately: the probe's baseline census reproduces the ad-hoc figures recorded for v38
(snap 2.82 vs 2.85, play 1.98 vs 1.98, run 1.79 vs 1.79, aftermath 3.44 vs 3.46), so the two instruments
agree and the census numbers in this document are reproducible rather than one-off.

**The sideline DETECTOR's share of the deficit is closed**: those men cannot be separated in that view.
What is not closed -- and what an earlier version of this section asserted too broadly -- is that the last
geometric route is gone. A render can also delete a body it already holds, which is a different mechanism
from a camera that never resolved one, and `dedupe_frames` above is exactly that and still unmeasured.
Play 1's honest body-count error is 1.98 a frame over the play.

**And the "worst body-frame" is not a fit or pairing fault at all.** id 17 has records on only frames 458
and 460 in that entire stretch: an isolated two-frame island where the sideline ground point (-26.3,
+3.9) sits **4 m** from the endzone's (-22.9, -1.2), with the cached translation matching the sideline
exactly. The sideline track produced a ground point on those two frames only, and produced a wrong one.
A tracking artifact, already excluded from the ruler by the 0.6 m ray-miss gate -- not something the
fits or the joins can repair.

Three times now the geometry has proposed something the footage refused -- a body supposedly drawn on
the camera rig (it was a drone in the plate), players supposedly cut off by the sideline crop (nothing
was clipped), and now the endzone supposedly over-segmenting the line. **Look at the frame before
believing a count.**

Baltimore's 15-18 is the other half, and two new faults sit in it. **Officials are voted onto a team**: id 85
stands motionless at (-10.1, +5.2) through frames 300-400, 8.6 m from any sideline body, and id 87 at
(-51.7, -0.4) is 17.7 m behind everyone -- officials wear white, so the saturation vote reads them as
Baltimore. And **one body can carry different teams in the two cameras**: endzone id 86 (KC) is sideline id
82 (BAL) at 0.55 m, endzone 99 (KC) is sideline 6 (BAL) at 0.49 m, endzone 91 (BAL) is sideline 3 (KC) at
0.68 m. The kit vote is per camera and per id, so nothing forces the two views of one man to agree; the vote
belongs on the merged id, after pairing, not before it.

**The cause is the two-view gate.** Simulating `two_view_pass`'s filters per player showed the
cross-view error is monotone in the fraction of a player's frames that got the triangulated ankle
anchor:

    id 12  187 frames reach the two-view fit, 180 anchored (96 %)  ->  endzone   9.3 px
    id  5  118                              , 116         (98 %)  ->  endzone  16.2
    id 17   62                              ,  31         (50 %)  ->  endzone  20.1
    id 25   34                              ,  12         (35 %)  ->  endzone  14.5
    id 19   93                              ,   4         ( 4 %)  ->  endzone 142.2

But id 19 *did* reach the two-view fit on 93 frames, and the fit is innocent: on these five players
its own medians were **sideline 14.6 px and endzone 4.9 px** -- better in the second view than the
first. `_two_view_job` gated validity on `first_rms`, the fitted camera alone, at
`--reproj-px-max 20`. 126 of 328 frames failed that sideline gate with excellent endzone error, and
**not one of id 19's 93 frames survived it**, so all 170 of his frames fell through to the one-view
pass, which reported `id 19: 170/170 frames, reproj 13.1 -> 4.0 px`. That four-fold "improvement" IS
the defect: `merge_into_refit` skips a frame whose `valid` is False, so it is absent from the cache,
counts as uncovered, and the one-view pass refits it to the sideline alone -- where 4 px is trivially
reachable by sliding the body along the ray that camera cannot see. The gate's own comment records
the original reasoning ("a weak second view's residuals are large by design, endzone 17 px at weight
0.3"), which inverted when the endzone became an equal partner at weight 1.0. Nobody re-measured the
rule when its premise changed.

`--two-view-gate first|worst|mean` now exposes it, default unchanged. Note that **`worst` is
stricter and would reject id 19 too**; `mean` is the setting that keeps a frame whose second view is
good. And pixels are not comparable between these cameras -- the endzone's px per metre differs from
the sideline's, so 4.9 px there may be metrically better than 14.6 px here -- which means the
principled form of this gate is metric, not pixel. The deeper fix may be simpler still: a frame the
two-view pass attempted should never be handed to the one-view pass, because a one-view fit is
strictly worse in 3-D whatever its pixels say.

**Measured, on five players, with the harness validated first.** The baseline arm (`--refit
<nonexistent>`, otherwise v34's invocation) reproduces the v34 cache under 05t to the last digit, so
a difference in any arm belongs to the flag. Then:

    five players, 05t                     baseline   --anchor-max-miss 0.6   --two-view-px-max 40
    two-view frames kept                   202/328          201/328               327/328
    frames anchored on the ankles          179/328          290/328               179/328
    endzone p50 / p90 / p99 (px)      17.4/150.8/382.6   17.4/150.9/382.7      16.2/ 24.9/153.7
    endzone frames over 100 px          118 (34.8 %)     118 (34.9 %)            15 ( 4.3 %)
    id 19 endzone p50 (px)                 142.2            142.2                  16.5
    sideline p50 / p90 (px)              3.8 / 13.8       3.8 / 13.8            5.6 / 30.5

`--anchor-max-miss 0.6` is a **null result** and an instructive one: it anchored 111 more frames on
the point both cameras agree about and moved nothing that survives -- the anchor decides how often a
player is exposed to the gate, not what the gate does. `--two-view-px-max 40` collapses the
catastrophic tail, and the sideline pixels rise, which is the correct trade rather than a cost: that
number was never evidence, it was the symptom of a body placed to satisfy one camera.

**The second ruler, in metres, is unambiguous** -- gap from the point both cameras put the feet:

    id (ankle miss)   along-ray p50 base -> px40     across-ray p50
    id 19 (0.36 m)        1.04 m  ->  0.05 m          0.02 -> 0.01
    id  5 (0.19 m)        0.02    ->  0.02            0.00 -> 0.00
    id 17 (0.16 m)        0.25    ->  0.25            0.13 -> 0.13
    id 25 (0.34 m)        0.06    ->  0.06            0.03 -> 0.03
    id 37 (0.19 m)        0.02    ->  0.02            0.02 -> 0.01
    pooled                p50 0.07 -> 0.04, p90 1.12 -> 0.23

The broken player improves twentyfold and **not one other player moves a centimetre**, which is the
adoption test passed: beaten on a ruler that is not the one being optimised, with no regression
elsewhere. v35 applies it to the whole play and re-scores with 05t, the census and both overlays.

**v35, the whole play, and it holds.** The two-view pass now keeps **1787 of 1793 frames across 24
players** (its own medians: sideline 6.7 px, endzone 4.3) instead of throwing the informative ones to a
one-view refit:

    whole play, ~1820 body-frames both cameras see     v34        v35
    endzone p50 / p90 / p99                        8.7/25.3/341.3   8.8/16.7/140.3
    endzone frames over  20 px                       197 (10.9 %)     92 ( 5.0 %)
    endzone frames over  30 px                       178 ( 9.8 %)     55 ( 3.0 %)
    endzone frames over 100 px                       129 ( 7.1 %)     24 ( 1.3 %)
    sideline p50 / p90                                3.4 / 11.0      3.4 / 12.7
    sideline frames over 20 px                         6 ( 0.3 %)    147 ( 8.1 %)

and in metres, over 1680 paired body-frames on 23 players: |along-ray| **p90 0.21 -> 0.05 m, p99
2.51 -> 0.34 m**, id 19 1.04 -> 0.05, and **0 of 23 players worse by more than 0.10 m** -- every other
player identical to the centimetre. The catastrophic tail is cut fivefold, nothing regresses in metres,
and the sideline's own pixels get worse, which is the trade rather than the cost. `TWO_VIEW_PX_MAX = 40`
is now the default in 05p and carries these numbers in its comment.

(08f declined to re-split the teams on the new cache -- "no clear two-way split: largest gap 9 at 189,
123 below, 2 above; refusing" -- so the labels are v34's. Refusing beats guessing, and it is the same
one-sided saturation histogram the kit work has hit before.)

**The census did not move, and that is the useful part.** v35 scores `|KC-11| + |BAL-11| = 3.02` bodies
a frame from the snap against v34's 2.95, with KC mean 11.7 and BAL 12.0 and only 4 frames of 361
exactly eleven and eleven. Placement improved fivefold on its own ruler and the body count got very
slightly worse, which settles that these are independent axes: the two-view bound fixes where a body
stands, not whether the right bodies exist. **The census is now the binding problem.** What the render
threw away on the way to that number:

    frames beyond an id's sideline span left out   2110
    endzone-only ids left out                        34
    edge-clipped one-view ids left out               25
    sideline dwellers left out                       20
    bodies behind the offence (officials)            ids 85, 88, 106, 107

which corrects something written above: the officials that the kit vote labels Baltimore are **already
excluded from the drawn bodies** -- id 85, the motionless referee at (-10.1, +5.2), is in that list. The
vote is still wrong about them (white stripes read as Baltimore) and that wrong label still reaches
anything reading `identity_resolved.pkl` directly, but they were never inflating the census. The surplus
of 15-18 "distinct places" for Baltimore is a count of RAW ids, before these rules.

Note also `endzone-only ids left out: 34` sitting beside the finding above that 2-4 endzone-only ids a
frame are men no sideline body is within 1.5 m of -- the occluded linemen. The rule that drops them is
the same one protecting the count from double-drawing unpaired duplicates, which is exactly why the fix
has to be pairing (join the ids by ankle-ray agreement) rather than relaxing the rule.

**The depth snap is exonerated and re-measured as a win.** It is not the source of the along-ray
error: it never moves id 19 (1.09 m before, 1.09 m after; worse on 3 frames of 107, better on 1).
Where it fires it is strongly right -- id 5 0.40 m -> 0.05 m of along-ray error (better on 115 of
117 frames), id 25 0.60 m -> 0.11 m (better on 19 of 33).

**Two hypotheses killed, and a trap.** `two_view_pass` takes its endzone offset from
`poses_tri.json` rather than `clip_offset`; a disagreement would silently mis-pair every player, and
they agree (both -15). The edge cross-fade of `global_orient` did not fire on the records in question
(the anchor it would blend toward sits at 71 deg while the cache holds -172). And 05p's resume path
reads: if `poses_refit.json` holds "mono", start again from `poses_refit_fused.json` -- a backup only
written when `poses_refit.json` existed at the start, which the pipeline deletes first, so the file
on disk is from 09-09 and a plain re-run would build on a two-day-old two-view cache computed with
the old endzone camera. **Check that backup's mtime before trusting it**; pass `--refit
<nonexistent>` to reproduce the pipeline's empty-blob state.

**Pose, place or facing: how to tell.** `05s` holds a record's `body_pose` and re-solves only what
you allow to move. On id 9's frames 258-270 (rms px): cache 18.7/25.1/29.5/22.9, translation-only
12.2/19.6/26.2/19.1, `global_orient`+translation **3.2/3.2/3.3/3.6**, and a 180 deg turn 28-39. The
limbs were never wrong -- the heading was, drifting +80 deg across twelve frames while the man ran
straight. This is local: only 16 of 5099 frames exceed 20 px in the sideline.

**Measured and rejected before building it:** a velocity-heading prior. 51 % of 1778 body-frames over
1.5 m/s face more than 90 deg from their own travel direction, which looks like a catastrophe and is
mostly correct football -- turning those bodies 180 deg beats the cache on 0-1 % of them. id 12 holds
163 deg while sliding at 85 deg (7.6 px as cached, 49.5 px flipped) because he is a lineman blocking,
and defensive backs backpedal the same way. Such a prior would wreck exactly the players it appears
to save.

## The ruler was blind, and the gate preferred it (2026-09-12)

Every placement ruler used so far scores a body against the keypoints of the camera it was fitted
to. That is blind by construction: depth along the camera ray and rotation about it are exactly what
one view cannot constrain, so the number cannot rise however wrong the 3-D is. `05t`
(`scripts/05t_cross_view_error.py`) scores the same cached bodies in the OTHER camera and is now the
standing ruler for placement.

    v34 cache, the same 1812 body-frames both cameras see     sideline (fitted)   endzone
    rms p50                                                          7.6 px        8.7 px
    rms p90                                                         14.3          25.8
    rms p99                                                          --          341.5
    over  20 px                                                       6 (0.3 %)   197 (10.9 %)
    over 100 px                                                       0           129 ( 7.1 %)

Across all 5099 sideline body-frames the cache reads p50 3.4 px, p90 11.0, 0.3 % over 20 px. By the
fitted camera's ruler play 1 is finished; by the other camera 7 % of it is over 100 px wrong. **The
sideline footage overlay (05q) shares this blindness** -- red skeletons sit on green keypoints while
the body stands a metre downrange -- so it cannot show what a free-viewpoint render will.

**The worst player, and a second ruler in metres.** id 19: 4.0 px sideline, 142.2 px endzone (p90
339.5) over 107 paired frames, his hips 149 px sideways from his own endzone box and 16 px down.
Sideways in the endzone is depth along the sideline ray, so the defect was measured again in metres
against where the two cameras' ankle rays actually cross:

    id (ankle-ray miss p50)   gap from the triangulated feet   along the ray   across it
    id 30 (0.03 m)                      0.01-0.03 m               -0.01 m       0.02 m
    id  5 (0.17-0.22 m)                 0.01-0.03 m               +0.02 m       0.00 m
    id 19 (0.33-0.38 m)                 0.89-1.10 m               +0.89..+1.10  0.02 m

Nine sampled frames of id 19, every one a metre out along the ray and 2 cm across it. A pure depth
slide is the signature of a body placed by one camera.

**That decomposition is also an identity test, and it clears the pairing.** Splitting every paired
body's gap from the triangulated crossing into along-ray and across-ray over the whole cache -- 23
players with 15+ paired frames -- gives |along| p50 **0.01 m** and |across| p50 **0.02 m**. Not one
player exceeds 0.25 m ACROSS the ray (the worst is id 6 at 0.16 m), which is what a wrong-man pairing
would look like, so no mis-pairing survives among the paired ids. Exactly one player exceeds 0.5 m
along it: id 19 at 1.04 m, the next worst being id 17 at 0.25 m. The entire metric placement defect
of the paired population is one man -- which is why the endzone p99 of 341 px reads like carnage: it
is his 107 frames.

**And the blind spot this ruler cannot reach.** Only 1832 of the cache's 5103 body-frames have a
second view on that frame. 3271 (64 %) are sideline-only, and 1165 of those belong to ids the endzone
never sees at all. Their depth is not unconstrained -- an ankle ray meets the turf at exactly one
point, so one camera plus the ground plane does fix a position -- it carries the error of the
feet-on-ground assumption, and that error is **smaller than it looks**: measured against the
triangulated feet on the 1719 frames where truth exists, the ankle-turf depth is out by **p50 0.19 m,
p90 0.56 m**. (An earlier line here said ~0.4 m; that was id 5's pre-snap figure, one player, and the
population number is half it.) The depth snap reached 610 of the 3271 sideline-only body-frames
(moving them p50 0.25 m, p90 0.95, max 2.46 against its 2.5 m cap), leaving 2661 (52 % of the cache)
on the turf estimate alone -- which is decent, not dire.

**A ruler for those frames was designed, calibrated and thrown away the same hour.** A player's
standing height is fixed by his build (the 51 ids span 1.75-1.96 m, p50 1.87), so his box height in
pixels measures his range independently of the ankle ray, and two disagreeing estimates would localise
a bad placement with no second camera at all. It does not work, and the numbers say why:

    1719 paired frames, error against the triangulated feet   p50      p90
    ankle ray meets the turf (what the fit uses)              0.19 m   0.56 m
    box height against known standing height                  6.73 m  59.44 m
    the same, upright boxes only (857 frames)                  3.27 m  10.08 m

and the disagreement between the two carries no information: bucketing by it, from under 0.5 m to
over 5 m, |ankle - truth| stays flat at 0.13-0.21 m p50. The cause is geometry, not implementation:
at the median range of **112 m**, depth from apparent size inherits the box's RELATIVE error, so ten
pixels of slop on a 140 px box is eight metres of depth. Intersecting a ray with the turf is far
better conditioned. Do not re-propose depth-from-apparent-size at All-22 ranges; it is unusable
whatever the pose gating.

**So why does the depth snap reach so few of the blind bodies?** Its own docstring measures it firing
on 69 % of frames, but that was the PAIRED population; on the bodies that actually need it, it fires
on 19 %. Counting the refusals by reason:

    reason                                          paired (1907)   blind (3196)
    SNAPPED                                          1260 (66 %)     614 (19 %)
    no endzone bodies that frame at all                  0          1278 (40 %)
    no endzone body within LATERAL_M 0.6 m of the ray   112           492 (15 %)
    a body is on the ray but beyond MAX_MOVE_M 2.5 m     86           433 (14 %)
    two candidates within MARGIN_M: refused            449 (24 %)    379 (12 %)
    the team gate left no candidate                      0             0

A suspicion of mine died here: `snap_ground` filters candidates to `teams.get(q) == side`, which
drops a candidate whose team is UNKNOWN whenever the sideline body's team is known (the docstring
only promises leniency for an unknown sideline id). It costs nothing on play 1 -- all 90 endzone ids
carry a team label, 0 candidate-slots were dropped for an unknown team, and that bucket is empty in
both populations.

The largest bucket is not a gate. **1278 of the 3196 blind body-frames (40 %) have no endzone ground
points at that instant**, because the endzone camera is solved on 510 frames (sideline 140-649) while
the play is rendered over roughly 14-660: before frame ~140 there is no second view by construction.
That is calibration coverage, not a threshold, and it is the ceiling on everything two-view --
including 05t's own reach. Nor is loosening the gates attractive: the blind bodies' nearest candidate
sits p50 0.28 m and p90 1.44 m off the ray against 0.16 m and 0.51 m for paired ones, so the endzone
track frequently does not hold that man at all (the same fragmentation as the census problem) and a
wider `LATERAL_M` would mostly buy wrong matches. With the turf estimate already at 0.19 m p50 the
snap's remaining upside is small. The two levers that are left are extending the endzone camera solve
and fixing fragmentation -- not tuning this rule.

**And "fragmentation" turns out to be the wrong word for the census problem.** The v34 entry below
reads the 32 Kansas City and 51 Baltimore sideline ids as a player being lost and re-acquired under a
new id, which would be repaired by stitching the pieces back together. It is not that. Pairing every
id with its most plausible continuation (a later id starting within 90 frames of its end, close enough
that the join needs no more than 9 m/s) and chaining greedily leaves **KC 32 -> 28 chains and BAL
51 -> 40**: only 4 and 11 ids respectively have any successor at all. The ids are not sequential
pieces of one man. Many of them start at frame 14 and run for hundreds of frames side by side
(3[14-636], 5[14-628], 11[14-660], 12[14-638]), and where they coexist they stand in **different
places**: 11.2 concurrent KC ids occupy 10.4 distinct positions at 0.5 m single linkage, 14.2 BAL ids
occupy 13.8. They are separate people, so neither stitching nor the twin merge (08o, which only folds
ids sharing one body) has much left to take.

Two more things the count exposes. `entity_type` cannot be used to exclude non-players: it types only
**6 of 83** sideline ids as `player` and the other 77 as `other`. And the raw tracked population is
wildly phase-dependent -- at the snap 21 ids in 20 places, every one on the field (|y| <= 9.5 m),
against 36-37 ids in 30-36 places by frames 580-620 with **12-14 of them beyond the sideline**
(|y| > 24.4 m) and x spreading from -43.8 to -10.8. That late crowd is staff and players arriving after
the play is over. The drawing rules filter most of it (the census counts timeline states, not raw
tracks), but it means any census averaged from the snap to the end of the clip is scoring the aftermath
as much as the play, and the phase split already in the v34 entry (a deficit at the snap, a surplus
during and after the run) is the real signal.

The snap itself is the sharpest number: **21 bodies for 22 players, split KC 9 / BAL 12** by the kit
vote, in 20 distinct places. So two Kansas City players are never tracked at all at the snap, and one
Baltimore pair is a duplicate -- 9 + 11 real men + 1 duplicate = 21.

**The kit vote is not the problem, and I nearly recorded that it was.** Wanting a team ruler
independent of colour, I checked every body clear of the line against which side of the line of
scrimmage it stands on, and got **13 disagreements out of 13** -- which I first read as a labelling
catastrophe. Thirteen of thirteen is not a defect, it is an inverted convention: I had assumed the
offence stands at `sign * (x - LOS) < 0`, and play 1 has every KC body at +1.6 to +7.1 m and every BAL
body at -2.1 to -10.4 m. Read the right way round the two rulers agree on **13 of 13 bodies with no
exceptions**, deep safeties (BAL ids 2 and 30, ten metres off the line) and the KC back seven metres
into his own backfield included. The kit vote from torso saturation is sound at the snap; so is
`line_of_scrimmage`. When a check fails on literally every sample, suspect the check.

**Then the footage settled what the geometry could not.** I had a promising theory that the ball-following
All-22 sideline crop simply does not frame the whole field, which would make "eleven a side" unreachable
and part of the census error not a defect at all. The visible ground footprint is real enough -- at the
line of scrimmage the sideline frames y = -12 to +24 m of a +-24.4 m field and the endzone only -6 to +7,
about 25 % and 21 % of the ground around the ball -- but the theory is **wrong for the snap**. Looking at
sideline frame 300 itself: nothing is clipped at either edge (the leftmost body sits at x 250 px, the
Kansas City receiver split widest at x 1765), and a human count gives 11 Baltimore in white against 9-10
Kansas City in red. The 21 tracked boxes match what is actually visible. Kansas City's missing men are not
out of frame and are not missed by the detector -- **the sideline views the line of scrimmage nearly
end-on, so the offensive line overlaps into one mass**. Endzone frame 285 shows exactly those men
separately (76, 62, 65, 74, 83, with the passer 15 and the back 10 behind them).

**So the snap deficit is a cross-camera bookkeeping failure.** At frame 300 the sideline holds 21 ids and
the endzone 24, and only **12 of them share an id**: 12 endzone-only, 9 sideline-only, a union of KC 14 and
BAL 19 against a truth of 11 and 11, while the v34 cache draws 19 bodies (KC 8, BAL 11). The five
endzone-only Kansas City ids (22, 37, 38, 74, 86) stand at x -22.7 to -24.2, on the line: the occluded
linemen, tracked perfectly well by the camera that can see them and never joined to the sideline. Admitting
them wholesale would overshoot badly, because some endzone-only ids are the same men as sideline ids that
were never paired -- which of the two they are is the number that picks the fix.

**Measured, by asking each endzone-only id how far the nearest sideline body is** (frames 300-400):

    of the 12-14 endzone-only ids per frame
      5-7  stand 0.14-0.70 m from a sideline body: the SAME MAN under two ids -- a pairing miss
      2-4  have no sideline body within 1.5 m: genuinely unseen there (the occluded linemen, and officials)
      rest ambiguous at 0.7-1.5 m
    both cameras pooled, 45 ids fall in 26-28 distinct places: KC 11-12, BAL 15-18 (truth 11 and 11)

Kansas City's pooled count is **right**. The two cameras together do see all eleven; the snap deficit is
pure bookkeeping, and the repair is to join the ids rather than to admit more bodies. Ground-point distance
alone cannot do that joining -- 0.7 m folded two real men once before (the passer and the lineman beside him
at 0.29 m) -- and the obvious alternative, the cameras' ankle RAYS, **does not work per frame either**.
Tested over 137 (frame, endzone id) pairs at frames 300-420: only **10** gave a confident join (best miss
<= 0.30 m and at least 0.30 m clear of the runner-up), **113 were close but ambiguous** and 14 had no
sideline body agreeing at all. The runner-up typically sits 0.03-0.05 m behind the best, because at ~100 m
the rays to a neighbour standing a metre away miss by almost as little as the rays to the right man. The
"0.20 m against 1.11 m" separation quoted for twins was a grossly mis-paired case, not adjacent players,
and it does not generalise to picking one man out of a formation.

The signal is real but thin: where a pair is already correct (ids 2, 3, 5, 9, 12, 15, 30) the true partner
does come out best. So the form that can work is not a per-frame threshold but a **one-to-one assignment
per frame accumulated over the whole play** -- the ambiguity is mostly two endzone ids competing for one
sideline id, which a global assignment resolves, and per-frame noise averages out over hundreds of frames.

Tried, as a Hungarian assignment on the ray-miss matrix over 124 frames. The first run gave 9 of 31 ids a
partner winning 60 % of their frames and several plainly wrong winners, including cross-team ones -- but
two of those failures were the measurement's, not the method's: nothing forbade a cross-team assignment,
and the "share" divided by every frame the endzone id appears in, including frames where its true partner
was not detected at all, which penalises exactly the intermittent tracks this is meant to repair. With a
team gate and the share taken over co-present frames, **14 of 28** ids have a partner winning at least
60 %, and seven are joins the pipeline does not currently make:

    89 -> 7 (82 %, 89 frames)   5 -> 19 (74 %, 50)   38 -> 17 (71 %, 34)   45 -> 4 (71 %, 31)
    101 -> 5 (71 %, 34)         22 -> 80 (69 %, 29)  17 -> 25 (61 %, 33)

all same-team, and two of them (45->4 and 89->7) were independently flagged as the same man at 0.33 m by
the ground-point test above -- two instruments agreeing. **Not adopted, and checking each one against the pairing it
would replace is why:**

    endzone -> sideline   ray miss proposed/current   ground gap proposed/current   verdict
      5 -> 19                 0.33 / 0.19 m               6.44 / 0.48 m             WRONG, six metres apart
     38 -> 17                 0.30 / 0.10                 1.27 / 0.54               wrong
     17 -> 25                 0.14 / 0.18                 0.96 / 0.71               ambiguous, rulers disagree
     22 -> 80                 0.17 / 0.22                 0.71 / 0.45               ambiguous, rulers disagree
     45 ->  4                 0.11 / 0.90 (1 frame)       0.59 / 1.17               good
     89 ->  7                 0.08 (179 frames) / --      0.36 / --                 good, no current pairing
    101 ->  5                 0.25 (71) / --              0.89 / --                 plausible, no current pairing

The suspicion about `5 -> 19` was right and worse than expected: those two bodies stand **6.44 m apart**,
so a 74 %-confidence vote would have welded together two men at opposite ends of the formation. The
Hungarian one-to-one competition manufactures that -- when the true partner is undetected on a frame, the
assignment must still give the id to somebody. Two of seven candidates are flatly wrong and two more have
the two rulers disagreeing, which is far too high a false-positive rate to apply automatically; a wrong
merge costs more than a merge not made, as the 0.35 m twin threshold proved when it folded a passer into
the lineman beside him. Three survive an independent ruler (45->4, 89->7 at 0.08 m over 179 frames, and
101->5), and 89->7 in particular is a man the two cameras have never had under one id. The route forward
is the vote as a CANDIDATE GENERATOR with the ground-gap check as the gate, not the vote as a decision.

`scripts/08r_pair_by_rays.py` is that, and it proposes only -- on play 1, 254 frames, 13 candidates clear
the vote and the gate throws out seven, including `85 -> 84` at **14.24 m** (the referee, at 91 % vote
confidence) and `5 -> 19` at 6.44 m. But the six survivors are not all applyable, because a union may not
put two tracks of one camera under one id at the same time:

    97 -> 11   CLEAN addition (endzone 11 has no track at all)      102 -> 0   CLEAN addition
    89 ->  7   81 endzone frames collide                             45 -> 4   53 endzone + 14 sideline
    101 -> 5   17 endzone frames collide                             27 -> 14  41 sideline frames collide

**Four of six are re-pairings, not additions.** Sideline 7 already carries an endzone track under id 7 on
81 of the same frames, so joining endzone 89 to it means unpairing endzone 7 first -- a different and
riskier operation. The evidence does favour 89 (the existing (7,7) pairing has *zero* frames with
confident ankles in both cameras, while (89,7) has 184 at 0.08 m), but that is a decision to state
explicitly rather than smuggle inside a merge, so 08r proposes clean additions by default and needs
`--allow-repairing` for the rest. Applying any of them must route through
`pair_by_appearance.global_ids_checked`, which refuses the union outright.

**And then the two clean additions turned out not to be worth applying, which is the most useful thing
this thread produced.** Checking what `97 -> 11` would buy: over its 30 frames the one-view cache stands
p50 0.34 m but p90 8.38 m and max 10.27 m along the ray from the two-camera point, with 0.01 m across it.
That looks like a body wandering ten metres in depth. It is not. The 12 frames with over a metre of error
have a ray miss of **p50 1.65 m**, against **0.06 m** for the other 18 -- they are the frames where endzone
97 is not sideline 11's man at all. At frames 360-380 the cached body stands still at (-22.9, -4.5) while
the "two-camera point" walks from (-24.4, +2.5) to (-25.0, +5.5): two different people. Where the rays do
agree (468-510, 628-638, miss 0.02-0.14 m) the one-view placement is **already** 0.04-0.36 m accurate.

So the join buys almost nothing, and the 67 % vote share means something worse than "probably right": the
pairing is **time-localised**, valid over some stretches of the track and wrong over others. A whole-id
merge is therefore the wrong granularity -- it would weld the correct frames together and actively corrupt
the rest by fitting one man's body against another man's keypoints, which is exactly the failure the
two-view work spent this session repairing. Any future version of this has to join per interval, with the
ray miss deciding frame by frame where the join holds, and 08r's `share` must not be read as confidence in
a whole-track identity. The honest state: the cross-camera bookkeeping is real (12 shared ids of 21 and 24
at the snap) but neither ankle rays nor an accumulated assignment can fix it at track granularity, and the
placement upside for the bodies it would join is a fifth of a metre.

**Then the generator got better, and two of its own rules were wrong.** 08r now builds candidates from ONE
global assignment on per-pair MEDIANS -- the median ray miss over every frame two ids share -- instead of
accumulating per-frame votes. A single frame cannot separate neighbours, and votes fail in a way a summary
hides: when the true partner is undetected the assignment must still give the id to somebody, which is how
a referee got proposed onto a player 14.24 m away at 91 % confidence. The median version is validated by
what it leaves alone -- of 25 pairs it keeps **16** exactly as the pipeline has them, including every
pairing independently confirmed good -- and it corroborates six candidates that two other methods found
separately. It still cannot be trusted as a decision, because a complete matching displaces a chain into
worse slots (22 -> 38 at 0.45 m against its current 0.22), so the gate remains what decides.

The second wrong rule was mine: **a relabel is not a union.** A global id spans both cameras, so joining
endzone 19 to sideline 11 can either relabel the endzone track onto 11 -- leaving sideline 19's man, a
different person, alone -- or union ids 11 and 19, which sweeps him in. Only a collision in the OTHER
camera means a track must be given up; an own-camera collision merely dictates that the join is a relabel.
Classifying on the own-camera overlap had rejected `sideline 11 <- endzone 19` (0.14 m over 150 frames) for
"370 sideline frames collide" when its endzone collision was zero. Four candidates now survive on play 1:

    0 <- 102  (0.13 m rays, 0.44 m turf,  35 frames, union)    11 <- 19  (0.14, 0.38, 150, relabel)
   28 <-  21  (0.08 m rays, 0.44 m turf, 138 frames, relabel)  80 <- 22  (0.17, 0.64,  59, union)

held back as re-pairings: `4 <- 45`, `7 <- 89`, `33 <- 37`, `37 <- 139`. The one that hurts is **`7 <- 89`,
0.08 m over 184 frames** -- the strongest pairing evidence in the play -- because taking it means giving up
endzone 7, whose pairing with sideline 7 has *zero* frames with confident ankles in both cameras. That is
very likely right and still needs a deliberate decision. Nothing is merged: applying is a separate step and
its ruler is 05t plus the along-ray gap, never the sideline's own pixels.
