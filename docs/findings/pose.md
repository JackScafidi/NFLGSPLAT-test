---
type: findings
topic: pose
period: 2026-09-07 to 2026-09-25
entries: 9
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Pose

Each body's joints: 2D keypoints, triangulation, SMPL-X refits, priors and fine-tuned detectors.

9 entries from 2026-09-07 to 2026-09-25, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Pose](../concepts/pose.md), [Player body](../concepts/player-body.md), [Hands](../concepts/hands.md), [Feet](../concepts/feet.md), [Head](../concepts/head.md), [Reprojection error](../concepts/reprojection-error.md)

**Decisions:** [0006: Don't pair cameras by the regressor's body pose](../decisions/0006-regressor-pose-is-not-a-pairing-cue.md)

## The 42 % triangulation figure has a structural ceiling (2026-09-07)

On play 1 v9 (58 two-view players, 104k joint-frames): 8 of the 22 SMPL-X
body joints (spine x3, collars x2, feet x2; the head only through the
face, 37 % confident) have no COCO-17 keypoint and never triangulate, so
the raw share tops out near 64 %. Over the 14 observable joints: 61 % are
confident (>= 0.3) in both views and 68 % of those reproject within 20 px
(median 13 px, p75 23, p90 37) -- 13 px at these focals is 0.15 m at the
player, keypoint noise not camera error. So the triangulation passes 66 %
of what is observable; `05n` now prints both shares. The endzone track
change moved neither (v8 42 %, v9 43 %). Chasing this further means better
2-D keypoints on 140 px people, not geometry.

## v15: the one-view bodies refit to the keypoints (2026-09-08)

Half of the rendered bodies are one-view (the sideline alone) and took the
monocular regressor's pose, which sits near the mean pose: measured on v14,
their joints move 0.21 m/s in the body frame (pose only, orient and transl
zeroed, `fit_mono2d.body_frame_speeds`) against 1.0 m/s for the
triangulated bodies -- mannequins gliding across the turf. The 2-D
keypoints (05m) exist for every tracked person and carry the articulation.
`pose.fit_mono2d` + `scripts/05p_refit_mono.py` (stage `refit_mono`, after
`refit`): per frame, least squares over SMPL-X (body_pose, orient, transl)
to the sideline keypoints through that frame's camera, the lower ankle on
the turf (the depth one view cannot see), the pelvis over the box-bottom
ground point, an L2 prior, a pull to the regressor's pose, a temporal
term; started from the regressor's pose and HEADING (a 12-heading search
picked the mirrored heading on a symmetric body and the fit then extended
the arm toward the camera instead of raising it: 0.31 px vs the truth's
1.09, wrong by 0.5 m -- the synthetic test in `tests/test_fit_mono2d.py`).
Records merge into 05f's cache; the fused record wins; the 05f cache is
kept as `poses_refit_fused.json` and a re-run starts from it. A frame
whose fit reprojects over 20 px keeps the regressor's pose.

Probe (ids 0 and 8, 343 frames): reprojection of the regressor's placed
pose 34 px -> 2.5 px; body-frame joint speed p50 0.21 -> 0.55 m/s (p90 1.3
-> 2.3). Cost 0.6 s a frame (least_squares max_nfev had been max_iter x 10
and a noisy frame ran 400 iterations); stride 2 (the timeline interpolates
axis-angles between records, 05k renders at stride 2), 6 workers.
Full run on v14's caches (04:32-04:43): 42 players with sideline keypoints
outside the fused refit, 3718 of 3721 frames fit (stride 2; 3 over the 20 px
gate); reprojection median 35.6 -> 3.3 px; body-frame joint speed p50 0.17
-> 0.56 m/s (p90 1.34 -> 2.98). The one-view bodies now move about half as
much as the triangulated ones instead of a sixth. The unobserved joints
(spine, collars, feet: 8 of 22) sit on the prior and pull the median down;
the reprojection is the keypoints' own noise at 130 px bodies.
`diag/play_001_v15_hifi_720.mp4` = v14 + this stage (nothing else changed).
Jitter (body-frame joint series, median second difference over median
first difference between records): fused refit 2.16 at step 1 and 2.16 at
step 2, one-view refit 1.70 at step 2 -- the one-view fits are no rougher
than the triangulated ones (both are noise-dominated at 8-15 mm a record),
so no extra smoothing on the mono records.
Validated against the fused refit (`05p --validate`: the mono fit run on
the frames the triangulation covers, scored against it; 365 frames at
stride 8): pelvis-aligned joint error p50 0.18 m for the regressor's pose
AND 0.19 m for the mono fit -- the reference's own noise floor (the fused
refit's rms to the triangulated joints is 0.087 m and those joints carry
~0.1-0.2 m at 8 px from 100 m), so the 3-D ruler cannot rank the two; the
mono fit's measured gains are 2-D (43 -> 3 px on those frames) and, with
the tilt prior, the lean. Without the prior the one-view fits leaned 34
deg (p50) against the truth's 16 (one view trades lean against depth);
`tilt_weight` 3 -> 21 deg, 10 -> 20 deg (|diff| 7, none past 60, p90 joint
error 0.31 -> 0.26 m), adopted at 10 past 20 deg. The pelvis of a one-view
body sits 0.46 m (median) from where the two-view fit puts it: the
box-bottom ground point against the triangulated pelvis -- the placement
ambiguity of one view, not the pose. HONEST CORRECTION to the motivation
above: the fused bodies' 1.0 m/s "body-frame motion" is mostly per-frame
jitter (8 mm a frame, second differences twice the first), so the
regressor's 0.17 m/s was not a sixth of real articulation; what the
keypoint fit adds is what the stills show -- strides, bent arms -- and the
2-D agreement, not a 3-D number.
On the real one-view set the prior is a wall: 3718 records lean p50 20,
p90 21, p99 21 deg (the fit wants more lean everywhere and stops at the
free angle), where the fused bodies spread 16 / 39. The lean points toward
the sideline camera 40 % of the time (cos > 0.5; fused 23 %) and away 21 %
(fused 12 %): a camera-ward bias, the depth ambiguity, not a travel lean
(cos with the travel > 0.5: 40 % vs 29 %). Untried: a quadratic prior from
zero tuned to the fused spread instead of a free angle and a wall.
Heading (`--validate`, 365 two-view frames, the fit's facing against the
fused fit's on the ground plane): |diff| p50 21 deg, p90 51, facing the
wrong way (over 90 deg) 3 % -- the regressor's heading prior plus the fit
gets the facing right on 97 % of frames; with the tilt prior the
pelvis-aligned joint error is 0.16 m against the regressor's 0.17.
Render (05:21): 69 posed players (v14 55), 3 default-posed, 16 bodies a
frame as before. Stills against v14 (`diag/p1_v14_v15_strip.jpg`, temporal
crops `diag/p1_v14_v15_motion.jpg`): the one-view bodies articulate --
running strides, bent arms -- where v14's walked upright; no flailing, no
broken bodies. v15 is the deliverable.

## v18: the two-view bodies shook; the fused refit damped (2026-09-08)

Ruler: second differences of the refit's world joints per frame (a smooth
motion has them far below the first differences). The fused refit (05f,
plain per-frame least squares, warm start only) came out p50 19 mm, p90
101, p99 717, hands/feet p90 319 mm a frame -- limbs jumping a third of a
metre between frames at the p90 -- from triangulated joints (05n) at p50
18 / p90 62 / p99 293: the fit AMPLIFIED the input's spikes. Two causes in
`fuse_smplx.fit_single_frame`: no temporal term, and soft_l1 at f_scale
1.0 m, which is plain least squares for anything under a metre. Now
`SMPLXFitConfig.temporal_weight` (pull of body_pose and orient toward the
previous frame's solution, consecutive frames only) and `f_scale`; 05f
defaults 0.3 / 0.1 (the library's defaults stay 0 / 1.0). Play 1 sweep:

| refit | p50 | p90 | p99 | hands/feet p90 | rms to the joints |
|---|---|---|---|---|---|
| plain (v14-v17) | 19 mm | 101 | 717 | 319 | 0.087 m |
| temporal 0.3, f_scale 0.1 | 17 | 65 | 255 | 102 | 0.096 |
| temporal 1.0, f_scale 0.1 | 16 | 59 | 182 | 77 | 0.102 |

The rms rises because the damped fit no longer follows the spikes it is
scored against; the p90 lands at the input's own level (the fit stops
amplifying). Synthetic: a 0.40 m one-frame wrist spike followed 0.28 by
the plain fit, 0.16 damped; a real 0.40 m step followed to 0.26 within
four frames. v18 = v17 + this (05f then 05p re-run) + the identity rules
(08:07, `diag/play_001_v18_hifi_720.mp4`): 22 bodies a frame, 68 tilt
clamps, stills against v17 (`diag/p1_v17_v18_strip.jpg`) identical in
formation, #21 the only visible number either way; the damping is a
motion property, judge it on the clip.

## v19: the one-view fill-in popped at every triangulation gap (2026-09-08)

Ruler: consecutive records (within 3 frames) of one player where the kind
changes between fused and one-view. Play 1 v18's cache: 22 players carry
both kinds, 577 one-view records sit inside a fused span (frames the
triangulation dropped), 187 boundaries, and at a boundary the pelvis jumps
0.43 m (p90 1.27), the orientation 35 deg (p90 122), body_pose 3.0 rad --
a two-view avatar pops half a metre and spins whenever the triangulation
blinks. The one-view fit placed the pelvis on the box-bottom point and
started from the regressor's pose, agreeing with neither fused block. Now
(05p, fit_mono2d.prev_seq): inside the span the ground point is the fused
pelvis interpolated, the start pose the nearest fused record's, the warm
start at a block boundary the fused params; beyond the span the box point
carries the end's offset, decayed. Measured: 0.43 -> 0.37 m (p90 1.27 ->
0.78), 35 -> 18 deg; with strong inside-span weights (place 10, init 1.0)
0.36 m (p90 0.43), 18 deg -- the pelvis holds, the pose does not. The
decisive ruler: second differences at triples mixing fused and one-view
records against fused-only triples of the same players: 227 mm vs 18
(hands/feet p90 778 vs 140), whatever the weights. One view's keypoints
disagree with the two-view pose along the camera's depth and no weight
settles it; for a gap of a few frames the interpolated two-view pose is
the answer. The gaps: 132 inside spans, p50 3 frames, 77 % under 12. Now
05p leaves one-view frames inside a fused gap of <= max_gap (12) frames to
the timeline's interpolation and fills only the long gaps, and
`place_from_refit` interpolates the refit translation across such gaps.
Play 1 re-run: 105 one-view frames left to the interpolation, boundaries
187 -> 71 (long-gap edges and span ends), the merged cache's jitter p99
763 -> 412 mm and hands/feet p90 144 -> 110 (the fused-only cache: 102).
At the remaining edges the pelvis still jumps 0.36 m: the placement pull
beyond the span was the default 1.0; it now follows the decayed offset
(10 at the edge, 1 five max-gaps out).

## 2026-09-24 05:30 -- the copy's census loss explained: the fine-tune's confidence head collapsed on the endzone

Per-frame diff of the drawn ids (copy vs v105): the copy draws id 17 (the centre) 442-474 and id 167 412-420, live
neither; that is the whole census 0.16 -> 0.385. Both are body-frames whose pose RECORDS the copy's refit cache lacks
(live's cache has 17 at 432-486 and 167 at 416/420; the copy's has none): with a record present the loader's rules
drop those bodies, with no record it draws them. The records are missing because the fine-tuned detector's ENDZONE
keypoints came out with median confidence 0.01 (live 0.95; every joint), so 05n/05f/05p rejected them: endzone
body-frames with median confidence >= 0.3 went 9306 -> 5193, and the "fine-tuned fit" was mostly a one-view
sideline fit (which is also why the back's crouch straightened). The sideline body joints are fine (0.79 p50,
3.1 px p50 from the live detector's points) but its face joints collapsed too (0.00-0.02).

Cause, in the dataset: 09g wrote every tracked box without a fit record as a box-only instance with all 17
keypoints at visibility 0 -- 54 % of the endzone instances (2373 of 4398), 40 % of the sideline's -- and
ultralytics' keypoint-objectness loss (loss.py: `kpt_mask = gt_kpt[..., 2] != 0`, `bce(pred_kpt[..., 2], kpt_mask)`)
trains the confidence head toward 0 on every v=0 joint. The face joints are v=0 in 73-96 % of instances for the
same reason (the fit has no face; the detector's helmet face is under 0.5). Also 20 endzone images were dropped by
ultralytics as corrupt (a box or joint outside the image, written unclipped). Fix: box-only instances take the
detector's own confident keypoints (pseudo_labels.detector_labels; fewer than 4 -> left out), the YOLO line clips
the box and drops out-of-image joints; dataset rebuilt as pose_ds2, retrain as pose_ft2, then the copy chain again
with --keypoints. Meanwhile the three refit arms (fine-tuned fit, VPoser weight 0.003 / 0.01) are being measured
on the LIVE cache's keys (content only, coverage held): $S/livekeys_rulers.log.

**06:40 -- the dataset rebuilt and retraining; the VPoser ruler's wrapped-rotation artefact.** pose_ds2 (09g with
--lo 214 --hi 616 --stride 2, after cc4512c / cb57c04 / 1d6578c): 395 images, 6,764 instances, no all-unlabelled
instance, no out-of-bounds coordinate, body-joint v=0 share 0.07 (was 0.54 endzone / 0.40 sideline); fit_cross
13,841 as before. pose_ft2 training (30 epochs, ~40 min); then $S/ft2_chain.sh on the copy: 05m -> the confidence
table gate ($S/conf_table.py; endzone body-frames >= 0.3 must reach 85 % of live's 9,306) -> 05n/05f/05p with
--keypoints -> merged onto the live keys -> rulers. The three earlier refit arms measured on the LIVE cache's keys
(content only; $S/livekeys_rulers.log, but its steps/census lines were stale -- read steps_copy_<tag>.log): the
fine-tuned fit lkft steps 2 / hops 0 / census 0.16 / vanish 171 only (= v105), 09d jerk 6 (v105 5), trunk 0
(v105 2); VPoser weight 0.003 in the fit (lkvp0003) the same placement, jerk 4, VPoser share over 8 0.044 vs 0.054,
jitter p99 0.230 vs 0.253; weight 0.01 pending. Both arms' VPoser p99 read 25.9 from ONE body: id 139 held
556-596 with a left-hip rotation vector of norm 5.62 -- the timeline unwraps rotvecs for continuity and holds the
last record forward, and VPoser (trained on canonical vectors) scored the wrapped form 27.3 where the same rotation
reads 6.3. Fixed f8ca9e7: pose_prior.canonical folds every vector under pi at every entry (encode, the numpy
encoder in the fit, blend). Every earlier VPoser number (live p99 15.9, the probes) carries the artefact on held
bodies past a half-turn; the live reference and the arms are being rescored ($S/prior_*_canon.log).

**07:00 -- canonical VPoser rescoring.** Live (v105 config): p50/p90/p99 4.22/6.71/15.87, over 8: 0.068 -- the
artefact barely touched live (15.94 before); its tail is real: the sprinter id 9 at 415-418 (22.5) and the back id 5
at 526-542 (17.9, the crouch); per-id p90: 5 16.5, 9 13.1, 19 10.4, 139 9.5. The fine-tuned fit on live keys
(lkft): 3.60/5.61/9.66, over 8: 0.024; worst 9 at 395-396 (14.9) and 489-490 (12.4), 28 at 495-498 (9.3); id 5
p90 16.5 -> 5.1 (the crouch straightened: a LOSS on film, the endzone camera was gone from that fit). Jitter p90
0.0644 -> 0.0604 but p99 0.1851 -> 0.2534: the one-view fits shake more at the tail. Keypoint residual 8.7 px is
against the LIVE detector's points, not this fit's, so it is not a ruler here; the film and the cross-view are.

**07:20 -- the VPoser term in the fit, weight 0.01, on the first fine-tune's keypoints (lkvp001, live keys,
canonical ruler):** steps 2 / hops 0 / census 0.16 / vanish 171 only; 09d jerk 3 (v105 5, lkft 6, weight 0.003: 4),
trunk 0; VPoser p50/p90/p99 3.42/5.07/7.68, over 8: 0.009 (lkft 0.024, live 0.068); jitter p90/p99 0.0602/0.229
(lkft 0.253, live 0.185). Worst: the sprinter 9 at 406-409 (9.8), 28 at 495-498 (9.3), 139 at 453-458 (9.2).
Sideways-leg share 3.9 % with id 5 (the back) at 20 frames -- new; the prior may be pulling his crouch legs. The
prior in the fit wins every pose ruler at 0.01; its film is owed (the sprinter, the back) once the GPU is free.
Queued after the ft2 chain and film: the same term on the RETRAINED detector's keypoints ($S/after_ft2.sh ->
lkft2vp), the real candidate.

**07:45 -- the four arms on the live keys, canonical ruler (play window 395-607, n 4704 body-frames):**

| arm | VPoser p50/p90/p99 | over 8 | 09d jerk | trunk | jitter p90/p99 | steps/hops/census |
|---|---|---|---|---|---|---|
| live v105 | 4.22/6.71/15.87 | 0.068 | 5 | 2 | 0.0644/0.185 | 2/0/0.16 |
| fine-tuned fit (lkft) | 3.60/5.61/9.66 | 0.024 | 6 | 0 | 0.0604/0.253 | 2/0/0.16 |
| + prior in the fit 0.003 | 3.53/5.42/8.56 | 0.015 | 4 | 0 | 0.0594/0.230 | 2/0/0.16 |
| + prior in the fit 0.01 | 3.42/5.07/7.68 | 0.009 | 3 | 0 | 0.0602/0.229 | 2/0/0.16 |

Monotone in the prior's weight on every pose ruler; placement untouched (same keys, same rules); the jitter p99
stays above live in every fine-tuned arm (the one-view sideline fits shake at the tail). All three use the FIRST
fine-tune's keypoints (endzone lost); the same arms on the retrained detector's keypoints are the decision.

**08:05 -- pose_ft2 trained (30 epochs, 0.69 h) on the fixed dataset.** Held-out, PCK@10 pretrained -> fine-tuned
(first fine-tune in brackets): endzone fit_cross 0.7 -> 66.1 % (72.4), median 20.4 -> 7.3 px; endzone fit_self 83.2
-> 92.3 (90.4); sideline fit_cross 50.7 -> 87.5 (85.8), 9.6 -> 4.1 px; sideline fit_self 97.0 -> 96.9; the det
classes lose 4-8 points as before (the label IS the pretrained point there). Same label-ruler gains as the first;
the decision is the confidence table on the re-detected copy, then the refit and the film ($S/ft2_chain.log).

**08:10 -- the confidence gate PASSES on pose_ft2.** Re-detected copy (keypoints_2d_ft2.parquet): endzone
body-frames with median confidence >= 0.3: 9,347 (pretrained 9,306; the first fine-tune 5,193); per-joint median
confidence on the body joints 0.93-1.00 (pretrained 0.82-1.00), the ears 0.83-0.93 (0.62-0.69), the nose and eyes
0.01-0.02 (helmets: the head now says "not visible" instead of guessing). Sideline the same: body joints 0.96-1.00
(0.79-0.99), 10,371 body-frames >= 0.3 (10,302). The dataset defect was the whole story of the endzone collapse.
Chain continues: 05n -> 05f -> 05p on the ft2 keypoints, onto the live keys, rulers, film.

**08:45 -- pose_ft2 downstream on the copy (lkft2 = the ft2 refit on the live keys).** 05n: 28 players
triangulated, 90 % of the observable joints, 1.6 px (the endzone is back); 05f 28 players / 489 frames, rms
0.051 m; 05p 2,596 one-view records, reprojection 14.7 -> 2.1 px. Rulers: steps 2 / hops 0 / census 0.207 (v105
0.16), vanish 167 421-607 + 171; 09d jerk 2 (v105 5), trunk 0 (v105 2), sideways legs L 4.7 % (id 5 45 frames);
VPoser p50/p90/p99 3.61/5.81/11.94, over 8: 0.024 (live 0.068), worst 167 at 411-414 (31) and 9 at 395-397 (18);
jitter p90/p99 0.0609/0.245 (live 0.0644/0.185). FILM (vft2diff_id9/id5, vft2_check): the sprinter id 9 410-422
upright with the arms pumping = the film (v105 leans 60 deg, arms flung back) -- the first fine-tune's win kept;
the back id 5 450-462 keeps his crouch behind the quarterback (the first fine-tune had straightened him: the
endzone was gone) -- the loss undone; whole scene at 450/500/562 on the film. The census 0.207 is one id: 167, the
KC-kit fragment, whose live records the loader drops as "riding another body" but whose ft2 records (garbage in
both caches: score 31 / 19, rotation vectors of norm 13-14) place him 0.1 m elsewhere and the rider test flips.

**06:10 (machine clock; the stamps above from 05:30 on ran ahead of it by up to two hours) -- the prior in the
fit on the RETRAINED keypoints (lkft2vp = ft2 two-view + 05p --vposer-weight 0.01, live keys):** VPoser
p50/p90/p99 3.41/5.11/8.77, over 8: 0.014 (lkft2 11.94 / 0.024, but lkft2's tail is id 167's garbage records at
31); worst 9 at 395 (14.0) and 458-459 (13.2); 09d jerk 4 (lkft2 2), trunk 0; jitter p90/p99 0.0583/0.280 (lkft2
0.0609/0.245); sideways legs L 5.1 % (id 5 44); steps 2 / hops 0 / census 0.207 (167 again). Mixed: the tail
better, jerk and jitter p99 worse. The plain ft2 fit (lkft2) is the port candidate; the prior term stays a
measured option (film not cut). Next: the rider rule's box condition (167), measured on the copy and on live, then
the port of lkft2 and the v106 chain.

**06:20 -- the rider rule asks the boxes (timeline.RIDER_BOX_CONT 0.5).** Id 167 = 8 sideline boxes at 411-420,
57-98 % inside KC 76's or BAL 4's boxes (two engaged men), and the distance test read him 0.46-0.67 m from 76:
dropped under the live records' pelvis, kept under ft2's (a 10 cm shift). With the refit placement forced off he
is kept too, so the live verdict was luck. A frame now also counts as riding when the fragment's own sideline box
lies half inside another drawn id's box, either team. Measured: the copy with the ft2 cache census 0.207 -> 0.16
(167 gone), live 0.16 -> 0.16, steps 2 / hops 0 both; the rider list grew by 8, 25, 165 (clip-edge sideline
fragments never drawn) and 23, 158, 177 (moved over from the unreadable-kit rule). Nothing drawn was lost.
PORT: play_001/poses_refit.json <- the copy's poses_refit_lkft2.json (the ft2 two-view + one-view refit on the
live keys; the previous cache saved as poses_refit.json.v105; keypoints_2d_ft2.parquet beside the live table, the
loader keeps keypoints_2d.parquet); chain v106 = v105 tables + this cache + the rider box rule.

**06:40 -- v106 chain (v105 tables + the ft2 refit cache on the live keys + the rider box rule), 07l:** steps 2 /
hops 0 / census 0.16 (KC 11.02, BAL 11.06), planted 11 % of 713 moving frames (v105 12 %), full-clip steps 42 (v105
42). Placement equal to v105; the pose rulers and the film follow from the hifi render and the view locks.
v106 09d (joints_v106, 395-607): hinge jerk 2 (v105 5), trunk 0 (v105 2), sideways legs L 4.6 % / R 3.0 % (v105
6.2 / 3.9; id 5's crouch reads sideways in both, 45 vs 40 frames), arms 7.9 / 9.8 % (football, unchanged).

**07:10 -- v106 = CURRENT BEST, film-checked.** Strips against v105 from the sideline-view render: the sprinter
id 9 410-422 upright with the arms pumping (v105 leaned 60 deg, arms flung back) -- the fine-tune's win, now in
the play; the back id 5 450-462 keeps his crouch behind the quarterback; the receiver 74 at the catch 556-568
reaches up for the ball at 556 and gathers it at 560 (v105 held the arms at the waist); whole scene at 450/500/562
on the film, counts right. Rulers: steps 2 / hops 0 / census 0.16 / planted 11 % (= v105); 09d jerk 2 (5), trunk 0
(2), sideways legs 4.6 / 3.0 % (6.2 / 3.9). Renders: diag/play_001_v106_hifi_720.mp4, _sideline_blend.mp4,
_sideline_sbs.mp4; the endzone view lock finishing. What v106 is: v105 tables + the pose cache from the RETRAINED
per-play 2D detector (pose_ft2: 05n/05f/05p on its keypoints, merged onto the live keys) + the rider rule's box
condition. Not shipped: the VPoser shift (SHIFT off) and the prior inside the fit (measured mixed on ft2 keypoints).
Open: jitter p99 0.245 vs v105 0.185 (the one-view fits' tail); the fine-tune port recipe for the next play
(09g --lo even, 09h, the confidence gate, 05m --out ft table, 05n/05p --keypoints, merge onto the live keys).
v106 endzone blend at 450/500/562 = v105's (depth unchanged; the pile bodies on the film). The jitter p99 rise
(0.185 -> 0.245) is ONE id: the sprinter 9, joint jitter p90 0.135 -> 0.228 with joint speed p90 0.218 -> 0.330
(07l's per-id table); every other id flat or better (3: 0.109 -> 0.112, 17: 0.099 -> 0.103). His arms now pump
(v105 held them flung back, still): fast real motion or a one-view zigzag -- the per-frame wrist trace decides
($S/wrist_trace.py).
Wrist trace 405-425 (per frame, pelvis-relative): v106's arms swing smoothly (left wrist +0.25 -> +0.30 -> +0.14
-> +0.38 m over 20 frames, no zigzag); the jitter spikes are single frames at the FEET (joints 7/8/10/11) in both
versions, and in this window v105 has 12 frames over 0.1 against v106's 4. The sprinter's p90 rise must sit
elsewhere in his run; the whole-run trace is being read ($S/wrist_v10{5,6}_full.log).
**Shift probe on v106 (row-gated, 8-12, sigma 3):** 191 body-frames moved (none fully), mean joint move 0.056 rad;
VPoser p99 10.95 -> 9.42, over-8 share 0.022 -> 0.021, jitter p99 0.245 -> 0.268 (worse); the tail is the sprinter
alone (per-id p90 13.9 -> 10.8; 395-397 at 18 = his stance at the snap, 441 at 16). SHIFT stays OFF: with the
fine-tuned fit the prior has nothing left to correct that the film would notice, and it costs jitter.

**08:00 -- the sprinter's jitter, located.** Whole-run trace of id 9 (395-607): v105 jitter p50/p90/p99 0.057 /
0.135 / 0.186 (17 frames over 0.15), v106 0.063 / 0.227 / 1.255 (46). Two events, neither the arms' pumping: (1)
490-494 the LEGS SWAP -- the right ankle goes from -0.62 to -0.18 m (pelvis-relative height) in one frame while
the left drops, then back four frames later: second differences 1.25-1.38 m/frame^2 on joint 8; the sideline
detector barely sees his ankles there (2-3 ankle keypoints at 484-498 in BOTH tables), so the legs are the gait's,
and the gait's phase flips; v105 is smooth there (-0.47 -> -0.34 -> -0.65). (2) The right wrist 446-466 and
471-483 swings +0.39 -> +0.83 -> +0.26 m with second differences 0.2-0.47 (41 frames over 0.1 on joint 21): the
detector's right wrist on the small blurred sprinter jumps 50 px at p90 and up to 139 px frame to frame in both
tables (fine-tuned p50 conf 0.69, pretrained 0.78), and the one-view fit follows it. Next: the leg swap on film
(strip 488-494) and the gait's phase continuity.
**The leg swap's mechanism (08:20):** not the fit's legs (with the gait off the ankles are smooth at 484-500) and
not the gait's phase (on throughout, w 1.00, phase advancing 0.19 rad/frame). It is gait.leg_yaw's forward/backward
decision: the fitted body heading in v106 swings from 121 to 75 deg while the velocity heading sits at 163-176
(the tackler turns his torso), so the yaw between them crosses 90 deg at 491 and again at 494 -- leg_yaw flips
to "moving backwards" (advance -0.106 m/frame, yaw -88) for three frames and the whole leg plane turns 180 deg:
the right ankle jumps 0.44 m up in one frame and back. v105's fit had him 30 deg off the velocity there. The
boundary is a cliff at exactly 90 deg; a torso twisted 90 deg off the line of running is a tackle, not a
backpedal. Fix: hysteresis on the backwards decision along a run (flip only past 90 + margin, un-flip only under
90 - margin); counting the play's flips first ($S/flip_count.py, v105 vs v106).
Flip count on the play (the gait on, live window, the cliff at 90 deg): v106 9 backwards flips inside on-runs on
5 ids (3 at 507/509/556/560, 4 at 533, 6 at 469, 9 at 491/494, 12 at 562; 94 backwards frames of 612 on, 50
frames within 15 deg of the boundary); v105 4 flips on 3 ids (3, 4, 12). Every flip is a leg plane turning 180
deg between two frames. Built: gait.BACK_MARGIN_DEG 30 (leg_yaw takes the previous frame's decision;
gait_sequence carries it along a run; tests: the twisted torso stays forward, a backpedal still flips, a 30 ->
100 -> 30 deg facing sweep keeps the hip rows smooth). Measuring: flips with the margin, the sprinter's ankles,
07l with margin 0 (v106b) vs 30 (v107p).
**Measured (08:40):** with the margin, backwards flips inside on-runs 9 -> 0 (backwards frames 94 -> 84 of 612);
the sprinter's ankles at 488-496 descend smoothly (no swap); 07l on the live play: joint jitter p90 0.0609 ->
0.0594, p99 0.2452 -> 0.2112 (v105 0.185), worst id 9 0.228 -> 0.217, id 3 0.112 -> 0.102; steps 2 / hops 0 /
census 0.16 unchanged; planted 11 -> 10 % of moving frames. Shipped as the module default; v107 chain = v106 +
this. The jitter p99 left (0.21 vs v105 0.185) is the sprinter's right wrist on a jumpy keypoint (446-483).
v107 09d (joints_v107, 395-607): hinge jerk 2 (= v106), trunk 0, sideways legs L 4.4 % / R 3.1 % (v106 4.6 / 3.0).
The chain (v106 + gait.BACK_MARGIN_DEG 30) is rendering; film next (the sprinter 488-494 legs, the usual strips).
**The sprinter's right wrist (08:55):** projected against the fine-tuned table, id 9's right wrist has a keypoint
on 22 of the 60 frames 440-500 (none at 450-454, 465-473, 478-493), confidence 0.09-0.33 on 457-464 (under the
fit's 0.3 floor: unobserved) and the observed ones jump 50-139 px frame to frame; the rendered wrist sits 15-66 px
off the keypoint where one exists. The arm away from the camera on a small blurred sprinter is mostly UNSEEN and
the fit swings it between sporadic pulls. Arm launched on the copy: 05p --unseen-temporal-mult 3 on the ft2
keypoints (an unseen limb keeps the previous frame's pose harder), live keys, rulers + the wrist trace
($S/arm_unseen.log).
**Unseen-limb hold, REJECTED (09:20):** 05p --unseen-temporal-mult 3 on the ft2 keypoints, live keys, rendered
with the new gait default: jitter p90/p99 0.0593/0.2113 against 0.0594/0.2112 without it, jerk 2 = 2, VPoser and
placement unchanged, the sprinter's wrist-worst frames 45 -> 47. The wrist swing is not an unseen limb thrown by
the prior; it is the fit's records at the sparse observed frames being pulled to keypoints that jump 50-139 px,
with the frames between interpolated. Open item (one id, jitter p99 0.21 vs v105 0.185): a per-keypoint temporal
veto at the fit's INPUT (a wrist keypoint far from its neighbours' at low confidence dropped, the temporal term
holding the arm) -- a data gate, not a prior; not built today.

**09:45 -- v107 = CURRENT BEST, film-checked.** v106 + gait.BACK_MARGIN_DEG 30. Strips against v106: the sprinter
488-494 now runs through the tackler's contact with a normal stride (v106 kicked the right leg high at 492 and
spread the legs at 494: the flipped leg plane); 410-422 identical (diff black); the whole scene at 450/500/562 on
the film. Rulers: steps 2 / hops 0 / census 0.16 / planted 10 %; 09d jerk 2, trunk 0, sideways legs 4.4 / 3.1 %;
07l joint jitter p90/p99 0.0594/0.211 (v106 0.0609/0.245, v105 0.0644/0.185); backwards flips inside on-runs 0
(v106 9). Renders: diag/play_001_v107_hifi_720.mp4, _sideline_blend.mp4, _sideline_sbs.mp4; endzone lock finishing.

**10:20 -- a systematic knee straightening since v105 (the fine-tuned fit).** Joints exports, play window, 22 ids
with 106 body-frames each: mean knee flexion 124.9 -> 131.6 deg, p25 110.6 -> 118.3, pelvis height 0.910 -> 0.932
m; 12 of 22 ids straighter by more than 5 deg, none more bent: Oweh 15 +15.6, the quarterback 80 +15.4, Noah Gray 74
+15.0, Taylor 12 +13.0, Hamilton 28 +12.1, Suamataia 37 +11.2, Trey Smith 76 +10.9, Humphrey 204 +9.0. The planted
share slid 12.4 -> 11.1 -> 10.5 % and the sideways-leg share fell with it. Suspect: self-training drift -- the
pseudo-labels are the fit's own reprojections (its L2 prior pulls toward straight legs where the keypoints are
weak), the fine-tuned detector learned them, the refit followed. The film decides: strips of 12, 80, 74, 15
(v105 vs v107). If v105's bent knees are the film's, the drift is a regression the sprinter's win hid; the fix
would be labels only where the joint is ANCHORED in both cameras (fit_cross and two-view fit_self), never a
one-view fit's leg.
Film on the knee drift (strips v105 vs v107): the quarterback 80 in the pocket at 480-500 stands with the legs
spread straight in v107 where the film has an athletic bent-knee base (v105 closer, if a touch over-bent); Oweh
15 rushing at 440-460 stands taller in v107 than the film's low drive (v105 closer); Taylor 12 in his pass set
and the receiver 74 read as a wash in stills. A mild, consistent regression across the engaged and pocket men,
hidden behind the sprinter's win. Hypothesis: AGREE_PX 12 lets the fit's projection REPLACE a confident detection
in its own camera (fit_self), so the label inherits the fit's prior (straighter legs) by up to 12 px, the detector
learns it, the refit follows -- a self-training loop. Measuring the fit-minus-detector offset at the knees in the
fit_self labels; if it points toward the hip-ankle line, the fix is: a confident detection in its own camera is
the label (det), the fit only labels what the other camera anchors (fit_cross).
**Measured (10:45):** in pose_ds2's labels, fit_self knees sit toward the hip-ankle line by +1.1 px mean (sideline,
73 % of them) and +1.7 (endzone, 66 %); hips +1.7/+3.2 px lower, knees and ankles 1-2 px higher on the sideline;
|fit - det| p50 2.5-4.4 px. Small per round, amplified by the refit's prior on the new keypoints. Jogging-band
ruler (jog_ab, v105 vs v107): the lock finds MORE stances on v107 (32 vs 27; band planted with the lock 0.20 vs
0.17), so the 07l planted slide is not the band's. FIX: pseudo_labels.SELF_LABEL "det" -- a joint anchored in its
own camera takes the detector's point (source tag fit_self kept); the fit labels only what the other camera
anchors. Dataset pose_ds3 rebuilding, pose_ft3 retraining after the v107 chain frees the GPU ($S/ds3_train.log),
then the copy chain and film ($S/after_train3.log: ft3_chain -> ft3_film against v107). The knee mean (124.9 v105
/ 131.6 v107) is the ruler for it, with the planted share, jerk, jitter, VPoser and the film of 80 / 15 / 9.
**Two mistakes on the way (11:05):** (1) the derived ds3 script broke at the training step (a wait loop pasted into
an echo string; `n: unbound variable`), the gate had passed. (2) Worse: 09g reads <play-dir>/poses_refit.json, which
is now the PORTED ft2 fit -- so pose_ds3's labels (fit_cross 11,811 vs 13,841, det 36,699 vs 33,621) came from the
already-drifted fit: a second generation of the same loop, not a fair test of the label rule. 09g gained --refit;
pose_ds3 rebuilt from poses_refit.json.v105 (the pretrained fit) so the ONLY change against pose_ds2 is
SELF_LABEL det; then pose_ft3 ($S/train3.sh -> ds3_train.log). Lesson for the next-play recipe: the label
builder must reproject the fit of the PRETRAINED detector; never re-label from a fine-tuned fit.
**pose_ft3 (12:00; labels: own-camera-anchored joints = the detector's point, from the v105 fit):** held-out
PCK@10 pretrained -> fine-tuned (ft2 in brackets): endzone fit_cross 0.7 -> 54.2 % (66.1), 20.4 -> 9.3 px; sideline
fit_cross 50.7 -> 83.3 (87.5); endzone det 99.3 -> 89.4 (90.8); fit_self 99.8 -> 90.4 (now a detector-point class).
Smaller fit_cross gains are expected (the model no longer learns the fit's own-camera projections, and fit_cross
labels are fit projections too). Confidence gate PASS: endzone 9,392 body-frames >= 0.3 (pretrained 9,306), body
joints 0.96-1.00. The copy chain runs; the knee ruler ($S/knee_ruler.py on joints_lkft3 vs v105/v107) and the
film of 80 / 15 / 9 / 5 decide.
**12:40 -- the label-rule hypothesis is FALSIFIED.** lkft3 (pose_ft3's fit on the live keys): steps 2 / hops 0 /
census 0.16; jerk 4; VPoser p99 18.3 (the sprinter at 416/442, 23); jitter p90/p99 0.0610/0.212; knee mean 132.2
deg -- the same straightening as v107 (131.6; v105 124.9): 15 of 22 ids straighter by > 5 deg against v105, and
against v107 only 139 moved (+8.7). The own-camera label rule was not the cause. Measuring the DETECTORS
themselves (ft2, ft3 vs pretrained, confident knees, per camera): is the fine-tuned knee displaced toward the
hip-ankle line? If yes on the endzone, the carrier is fit_cross (the fit's leg projected into the other camera:
a one-camera anchor leaves the knee free along the viewing ray and the fit's prior straightens it), and the fix is
fit_cross for the ARMS only (the original target: the sprinter's flung arms), never the legs.
**Detector-level measurement (12:50):** confident knees, fine-tuned vs pretrained, displacement toward the
hip-ankle line: ft2 sideline +1.3 px (72 % of knees), endzone +2.9; ft3 sideline +0.5 (57 %), endzone +2.6. The
own-camera rule fixed most of the sideline drift and none of the endzone's, where the labels are fit_cross (12,364
of 13,841 slots) -- the fit's leg projected into the camera that did not anchor it, straightened by the prior along
the anchoring camera's ray. FIX (commit): pseudo_labels.CROSS_JOINTS = the arms (COCO 5-10); the legs are the
detector's own point or nothing. pose_ds4 from the v105 cache, pose_ft4, the copy chain, the knee ruler and the
film ($S/ds4_train.log, $S/after_train4.log). Expected: knee mean back near 125 with the sprinter's arms kept.
pose_ds4 (13:10; arms-only fit_cross, own-camera det, from the v105 cache): slots 114,971; det 40,078 (34.9 %),
fit_self 41,196, fit_cross 6,791 (5.9 %; endzone 5,475, sideline 1,316; joints 5-10 only), none 26,906; gate PASS;
pose_ft4 training. The legs are now the pretrained detector's own points everywhere.
Elbows too, on the detectors (vs the pretrained, toward the shoulder-wrist line): ft2 sideline +1.9 px (74 %),
endzone +0.8; ft3 +0.9 / +1.0. The arm labels stay the fit's across cameras (the sprinter's win); the elbow mean
joins the knee ruler as the second check on the fourth detector.
**pose_ft4 (14:05):** held-out PCK@10 pretrained -> fine-tuned: endzone fit_cross (arms only now, n 1,073) 1.0 ->
48.2 %, 21.2 -> 10.3 px; sideline fit_cross 51.6 -> 85.4; endzone det 99.4 -> 93.7 (ft2 90.8, ft3 89.4: the legs
are det labels now, so the det class holds better); fit_self 99.8 -> 94.8. Confidence gate PASS. 05n: 29 players,
89 % of the observable joints, median reprojection 3.8 px (ft2 1.6: the legs no longer agree with the fit by
construction); 05f 29 players / 488 frames, rms 0.065 m. 05p, rulers, film and the knee/elbow ruler follow.
**14:25 -- the label hypotheses are falsified TWICE.** lkft4 (arms-only fit_cross, legs = the pretrained
detector's points): steps 2 / hops 0 / census 0.16; jerk 4; VPoser p99 17.5 (the sprinter); jitter 0.0623/0.227;
knee mean 131.6, elbow mean 126.8 -- identical to v107 (131.6 / 126.6) and lkft3 (132.2). Three detectors with three
label rules give the same straightening against v105 (124.9 / 118.8), so the labels are not the carrier. What all
three chains share and v105 does not: the FIT CODE. v105's cache is the v100 merge -- old two-view records from
earlier 05f runs plus a 09-23 one-view refit on the endzone-blind frames -- while every chain refits EVERYTHING with
today's 05f and 05p. Test running: the PRETRAINED keypoints through today's 05n/05f only, merged onto the live keys
(one-view frames keep v105's records), knee/elbow ruler ($S/live_05f_test.log). If the knees come out ~131, the
straightening is today's two-view fit against the old records, and the film question is which fit is right on the
quarterback and the rushers -- not the detector.
**14:50 -- CONFIRMED: the knee straightening is the FIT CHAIN's, not the detector's.** The PRETRAINED keypoints
through today's 05n/05f (two-view only, the copy chain's thresholds 6 / 0.5), merged onto the live keys: knee mean
132.1, elbow 125.8 -- v107's numbers (131.6 / 126.6), the same ids on top (80 +15.3, 15 +15.2, 74 +14.6, 12, 28,
76, 37, 204), 15 of 22 straighter by > 5 deg against v105. The three fine-tunes and their three label rules were
innocent; every chain refitted the two-view frames with today's 05n + 05f, while v105's two-view records date from
09-09/09-11 (poses_refit_fused 09-09, poses_tri 09-11). 05f's code has not changed since (git: only the VPoser
option), so the difference is 05n's input (the cameras, the triangulation) and/or the copy chain's looser
--min-valid-joints 6 --min-frame-frac 0.5 (defaults 10 / 0.7: frames with six triangulated joints get two-view
records whose LEGS the L2 prior straightens). The default-threshold variant is running ($S/live_05f_default.log).
The 09-11 two-view refit ALSO ran with --min-valid-joints 6 --min-frame-frac 0.5 (HANDOFF line 244), so the
thresholds are not it either. What changed since 09-11 in 05n's inputs: cameras.npz (09-18 03:13, the sideline
tail fix) and the keypoint table (09-22, the id folds). The two-view fit today triangulates with the 09-18 cameras;
the endzone camera is known to be ~8 px off (the 09i refinement was right but never ported). Next test: 05n/05f
on play_copy_b (the refined endzone camera), merged onto the live keys, knee ruler -- if the knees come back to
~125, the straightening is the endzone camera's bias in the triangulation, and the port of the refined camera FOR
THE FIT ONLY is the fix (as the fine-tuned keypoints are for the fit only).
Default thresholds (10 / 0.7): knee mean 131.7, elbow 125.6 -- the same; thresholds innocent (26 players fitted,
9 and 17 skipped). The refined endzone camera triangulates far tighter: 05n median reprojection 2.6 px against 5.4
with the live camera (28 players, 86 % of the observable joints); its knee ruler is running.
**15:20 -- the old two-view records were sideline-dominated fits.** Same 2,396 (frame, id) records, the fit's
legs/arms projected against the pretrained detector's confident keypoints (live cameras): v105's records read
legs 2.9 / 6.2 px (p50 / p90) on the SIDELINE and 14.1 / 29.8 on the ENDZONE, arms 2.3 / 12.8; today's 05f records
read legs 7.7 / 8.4, arms 6.7 / 7.4 -- balanced between the cameras. The old fit followed the sideline detector's
bent knees; the new one honours an endzone camera known to sit ~8 px off, and the compromise straightens the legs.
So the "regression" is two-view geometry, not a detector, and the candidate fix is the refined endzone camera
(09i) for the FIT: its triangulation already reads 2.6 px against 5.4. Measuring the residual table under the
refined camera and the knee ruler on its records.
Refined endzone camera in the two-view fit: knee mean 132.3 -- no change (legs 6.3 / 8.1 px against the two
detectors under it; the old records 2.9 / 10.2). The camera pose is not the lever. 05f fits the TRIANGULATED joints
(05n), not the cameras, so the straightening sits in the triangulation's inputs (the endzone knee/ankle keypoints,
foreshortened from behind) or in the fit's prior on those joints. Next: the triangulated knees themselves, old
poses_tri.json (09-11) against today's -- are the raw 3D knees straighter before any fit?
**15:45 -- the raw triangulation is UNCHANGED since 09-11.** Raw triangulated knee angles (SMPL-X tree, 395-607):
old poses_tri 124.4 mean, today's 123.6 (live camera) / 123.8 (refined) / 126.7 (ft2); on 1,101 shared knees today
vs old delta +0.0 deg. So 05n gives the same 3D knees and the straightening happens between the triangulation and
the record: today's 05f turns 124-deg triangulated knees into 132-deg records, while v105's records on those keys
sit at 125 -- and read 2.9 px on the sideline / 14 px on the endzone, the signature of a sideline ONE-VIEW fit.
Suspicion: v105's "two-view" keys are mostly earlier 05p one-view records that overwrote the 05f ones (v81-v100
passes), i.e. the play has been rendered from sideline-only fits for weeks, and today's chains are the first true
two-view fits on those frames. Checking the cache's mono record list; the endzone film judges the knees
(endzone_knees.png: the quarterback 480/500, Oweh 440/460, v105 vs v107).

**16:00 -- RESOLVED: the knee "drift" was the sideline's own bias; v107's straighter knees are RIGHT.** The
endzone film (endzone_knees.png) settles it: the quarterback at 480 and 500 stands in the pocket with a modest
knee bend and an upright torso -- v107 has exactly that, v105 crouches deep with the torso folded (a fit that put
the knee bend toward the sideline camera, where flexion is invisible, and matched the sideline at 2.9 px by
over-bending). Oweh at 440/460 reads as a wash from the endzone. The 3D picture: the old records on the two-view
keys were sideline-dominated fits (2.9 px sideline / 14 px endzone); today's chains are the first true two-view
fits on those frames (7.7 / 8.4), and a two-view fit is straighter because the endzone sees the flexion the
sideline cannot. My "v105 closer" verdicts from the sideline strips were the sideline's bias -- the other camera
is the pose ruler as it is the placement ruler. Thread closed with no fix owed; v107 stays CURRENT BEST.
Innocent along the way: the fine-tune, its three label rules, the copy chain's thresholds, the endzone camera
pose. Kept (measured on their own rulers): SELF_LABEL det (the sideline detector's knee drift against the
pretrained +1.3 -> +0.5 px) and CROSS_JOINTS arms-only (endzone det PCK@10 90.8 -> 93.7); the rendered rulers are
neutral to them. Next-play recipe note: label from the PRETRAINED fit (09g --refit), judge the pose on BOTH cameras.
The refined endzone camera in the triangulation (05n 5.4 -> 2.6 px; the two-view legs 7.7 / 8.4 -> 6.3 / 8.1) is
the next candidate: v108 = v107 + the refined camera for the FIT only (ft2 keypoints on play_copy_b's cameras).

## 2026-09-24 16:10 (machine clock; the stamps from ~11:00 to 16:00 above ran ahead of it) -- label rules reverted

The two label rules (SELF_LABEL det, CROSS_JOINTS arms) rested on the knee-drift premise the endzone film falsified,
and both lost on film and on every ruler against pose_ft2 (same tool, same code, live keys): VPoser p99 / over-8
v107 10.7 / 0.022 vs ft3 18.3 / 0.032 vs ft4 17.5 / 0.028; jerk 2 / 4 / 4; jitter p99 .211 / .212 / .227; held-out
endzone fit_cross PCK@10 66.1 / 54.2 / 48.2 (arms). Film: ft3 flings the sprinter's arm out again at 414-418; ft4
leans him ~45 deg at 410-418 and throws an arm wide at 422; v107 upright. Defaults back to fit / None (verified: the
rebuilt labels reproduce pose_ds2 exactly, 114,988 slots); the knobs stay as 09g --self-label / --cross-arms-only.
pose_ft2 stays the shipped detector. NOT pursued: the refined endzone camera in the fit (sideline leg residual 7.7 ->
6.3 px, knees unchanged) -- the 09-23 closure stands (the drawn bodies do not move under it; its placement ruler read
14 px worse in the endzone), and the gain is too small to re-open it.

## 2026-09-25 00:50 -- ML status: VPoser in the fit re-measured (mixed, not shipped); the facing prior from BDB works

**VPoser in the fit, on the fixed 05p** ($S/vp_chain.sh): the lkft2c recipe with ONE knob changed (05p --vposer-weight
0.01; 831 s), merged onto the same live keys, both arms' copy rulers re-run with today's loader. Control -> VPoser:
VPoser score p99 10.13 -> 8.56, over-8 share 0.029 -> 0.015 (its own ruler: circular); joint jitter p90/p99
0.0531/0.1833 -> 0.0512/0.1713; sideways L/R arm 6.7/13.3 -> 6.2/12.8 %, L/R leg 4.2/6.0 -> 4.5/5.9 %; jerk 5 = 5;
reprojection 8.3 -> 8.2 px; knees/elbows unchanged (no id moves 5 deg); steps 2 / hops 0 / census 0.169 both. 7.1 % of
live body-frames move a joint > 15 cm, all one-view ids (3, 0, 9, 5, 12, 84). Film at the largest change per id
($S/vp_film2.png): the motion receiver at 464 better (a raised arm the film does not show goes away), the safety #21 at
490 WORSE (an arm pushed out where the film holds it tight in his backpedal), the rest too small to judge. Not shipped;
the 09-24 "win" (p99 15.9 -> 7.7) was the refit bug. Next arm: weight 0.005, or the prior on the legs and trunk only.

**Action classifier, self-labelled: dead end (5adcc52).** Two-view fits as labels, facing-free features, held out by
player: 37-42 % vs a 37 % majority and a 54 % hand rule; the labels are not physical (19 % "backward" above 5 m/s).

**Facing prior from real tracking: works (ea480bd).** BDB 2026 input, 2023 week 1 (data/tracking/input_2023_w01.csv,
819 pass plays, measured o and dir): the same features, held out by PLAY 74.2 % (forward 85, backward 79, sideways 61)
vs 41.7 % majority and 57.0 % hand rule; on play 1's two-view labels 73.4 % (majority 40.0 %): it transfers. Confident
one-view disagreements with the drawn facing: the motion receiver 430-460 (18 of 28), the stretch the film shows wrong.
As a record rule (pose.action_class.drop_against_prior; offline on play 1): drops only id 9's 476/488/494/504, all
facing him off his sprint. Model: data/models/facing_prior_bdb2023w01.pt (09l rebuilds it). Wiring into the loader next.

## 2026-09-25 01:30 -- VPoser 0.005 (not shipped); a random film audit; the KC left line is still crossed in the endzone

**VPoser in the fit at 0.005** ($S/vp5_chain.sh): score p99 10.13 -> 8.89, jitter p99 0.183 -> 0.179, arms/legs within
0.1 pp. Film: keeps the 0.01 arm's defect (the safety #21 at 490, an arm pushed out) and loses its gain (the motion
receiver's raised arm at 464 is back). Not shipped at either weight; VPoser stays the ruler, not the fit.

**Random audit, 30 drawn bodies on both cameras' film** ($S/audit_sheet.py, seed 7; $S/audit_*.png): ~55-60 % right;
~17 % arm pose wrong (a long tail -- arms raised or flung out, one dive; a wrist 15 cm over the shoulder is only 2.1 %
of one-view body-frames and mostly real: the throw 518-532, the catch 562; the exception the motion receiver 432-482);
~17-20 % misplaced 0.5-2 m in the endzone view (some of it the endzone camera's own wander, removed by the next ruler);
1 wrong man.

**Depth ruler on the drawn bodies** ($S/depth_ruler.py): each two-view body against the ground point under its own
endzone box, the frame's common offset removed (the endzone camera: |cx| p50 0.33 m, the known bias). Across the field
(the sideline's blind axis, the endzone's sharp one): p50 0.10, p90 0.45, p99 2.33 m; 13 % over 0.75 m overall. The
tail is IDENTITY, not placement: the KC left line at 420-500. Endzone track t139 (labelled 139) is #76 the left tackle
(y ~ -4; the sideline's 37 is there); endzone t33 (labelled 204) is #62 Thuney (y ~ -2); endzone t17 (17) the centre
#52 (y ~ -1.4). The sideline side is tangled too: t39 (139) at the centre's y ~ -1 at 436-452 and at the guard's
y ~ -2.2 from 476, t25 (204) at the guard's 444-484, both ids on one spot at 476-484. So the two-view fits of 37/139/204
blend neighbouring linemen (Thuney's facing errors before the record rules were this). NEXT: untangle on a copy with
the endzone jerseys (09c + 08z per camera track), refit two-view for the three, measure on the depth ruler + census +
film. Also id 4 (BAL) 1.4 m across at 398-560: check its endzone rows the same way.

**The KC left line, read on the endzone film (2026-09-25 ~01:20; $S/ez_jerseys.png, $S/ez_switch.png).** Endzone
tracks by jersey: t139 = #76 Suamataia at sideline 424-472 (blurred engaged 484-490, off 496-504), #62 Thuney from 516
(labelled 139 there, correctly); t33 = #62 Thuney 400-504 (labelled 204 to 486, then 166), #52 Humphrey by 516; t17 =
#52 400-472; t37 = #76 at 400-412 and from 490 (a gap exactly while t139 covers him). The sideline side is itself
switching (its t39, id 139, stands on the centre's spot at 436-452 and on the guard's from 476; t25, id 204, on the
guard's 444-484; both on one spot at 476-484), so the #62/#52 part needs its own frame-by-frame pass. The unambiguous
part -- #76 is sideline 37 throughout -- is being measured on the copy: endzone t139 clip 402-480 -> 37
($S/untangle76_chain.sh; 08z + the same map on keypoints_2d_ft2 via $S/relabel_ft2_keypoints.py, then 05n/05f/05p).

**id 4 (BAL) 1.4 m across at 398-560 is not identity:** his sideline track ends at 443 and resumes at 528 while the
endzone (t45, then t136) boxes him rushing forward between #65 and #74; the timeline holds him near his last sideline
spot through the hole. The hole-hold rules (endzone_only_rule.hold_holes and the stand-still) decide it -- a candidate
for "follow the endzone's own track through a long hole when it is one id throughout", measured separately.

**#76's endzone rows relabelled on the copy: film-true, NOT ported (2026-09-25 01:57).** endzone t139 clip 402-480 ->
37 (08z; the same map on keypoints_2d_ft2), then 05n/05f/05p and the copy rulers. id 37 (#76) gains 57 two-view
records at 417-495 (4 before); id 139 had NONE there before either (the triangulation's reprojection gate had refused
the crossed pairing), so the crossing had not corrupted Thuney's fit, only denied #76 his second view. But census 0.169
-> 0.272 with 24 fewer body-frames drawn: sideline id 139 has holes at 417-435 and 453-475 and was drawn there on the
crossed endzone rows (on #76's spot); moved to 37, he vanishes. The "fold that exposes a hole" trap
(`fold-on-a-copy-first` (memory note, not in the repo)). Jitter p99 0.183 -> 0.176, arms/legs within 0.4 pp, steps 2 / hops 0. The copy's tables are
restored from live (md5 equal); its poses_refit_fused.json may carry the 08v remap (unused by the --refit 2v chains).
Next: the whole left-line untangle -- who is 139 on the sideline in his holes (the stand-still/hole rules), the sideline
t39/t25 switching between #52 and #62 -- one frame-by-frame pass with both films, then this relabel with it.

## 2026-09-25 12:40 -- VPoser shift rejected; 05r's merged-box rule fixed (v116 rendering); the pipeline fits on ft2; gait vs lock; placement SURGES

**VPoser shift (pose_prior.SHIFT) on the per-joint limb ruler: REJECTED.** Endzone film, live: every limb joint worse
or equal (ankle p90 29/23 -> 31/26, wrists 23/33 -> 24/33); limb joints over 25 px arms 359 -> 382, legs 323 -> 378.

**05r --merged-rule swallowed (1e487ae, default; v116).** 05r skipped every endzone box over 1.5x the id's median width
as merged. On the endzone film Madubuike at 444-474 is ONE man lunging between #65 and #74 (his ft2 keypoints on him,
#65 boxed beside him at IoU ~0.1); only 516-522 is a real merge (#65 bending over him, #65's own box gone, the
keypoints #65's). Neither the keypoints' span of the box nor "two ids, one skeleton" separates the cases (the merged
man has no skeleton of his own) -- swallowed(): wide AND a neighbour who overlapped (IoU >= 0.3, last 6 clip frames)
lost his box, or shares it (IoU >= 0.5). 84 more records. Madubuike's endzone limb joints over 25 px 113 -> 50; all ids
legs 326 -> 300, arms 364 -> 318; sideline, 07l, jerk unchanged; joint jitter p99 0.21 -> 0.17. The width rule over
395-615 reproduces the live v115 cache record for record (the fit is deterministic). Film: the limbs lean into the
lunge; the BODY is still drawn a torso width to his right (placement anchored on trailing ankles -- open).

**Pipeline keypoints (461428c).** tri / refit_mono / refit_ez ran 05n / 05p / 05r on keypoints_2d.parquet (the
pretrained detector) while every live cache since v106 was fitted on keypoints_2d_ft2.parquet by hand. Now KP = ft2
when present.

**Gait vs foot lock (ablation, v115 tables; 05k runs the lock only under --gait, so "no gait" = no lock too).**
Sprinters' planted share (07l, pelvis > 6 m/s, 685 frames) / leg joints over 25 px endzone, sideline:
v115 gait+lock 14 % / 323, 114; neither 1 % / 298, 76; lock on its jogging band only 1 % / 317, 78; lock on every speed,
gait never fires (gait.RUN_M 1e9, foot_lock.RUN_M_LOCK 1e9) 11 % / 315, 79 (id 9 sideline leg mean 17.5 -> 9.3 px).
Joint jitter p99 0.21 (v115) / 0.12 / 0.13 / 0.17. The gait's legs are out of the film's phase by design (PHASE_MATCH
off, measured before); the lock on the jogging band costs the quarterback (endzone legs 56 -> 67; backpedal = motion
against facing, which the reach-signal strikes assume away). The gait also fires on the centre and Madubuike, whose
drawn pelvis surges past 4.8 m/s (below). NOT decided: needs a render of the feet.

**Placement SURGES -- a new ruler ($S/surge_ruler.py).** Smoothed pelvis acceleration (centred differences over
+-4 frames) > 25 m/s^2: v115 live 396 of 2295 body-frames (17 %), 22 ids, nearly all ACROSS the field (the sideline's
line of sight); timeline dump 769 of 4588 (same share). Control: set players before the snap 22 of 1864, 12 of them
the left tackle wobbling ~6 m/s across in his stance. The centre slides 1.4 m across at 416-428 (7 m/s), 1.3 m along
at 510-526, and swings 1.2 m out and back at 558-584; Madubuike, with no detection in either camera at 590-606, moves
2.3 m in 16 frames. The step ruler (> 0.25 m/frame) never sees them: the smoother spreads each slide over frames.
Placement ablation running (own-id snap off, depth snap off, refit placement off, despike off).
