---
type: findings
topic: cameras-and-sync
period: 2026-09-05 to 2026-09-09
entries: 5
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Cameras and clip sync

How the sideline and endzone cameras are solved on every frame, and how the two clips are lined up in time. Every 3D position is placed through these cameras.

5 entries from 2026-09-05 to 2026-09-09, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Cameras](../concepts/cameras.md), [Feet](../concepts/feet.md), [Reprojection error](../concepts/reprojection-error.md)

**Decisions:** [0009: Don't refine per-frame cameras to the yard lines alone](../decisions/0009-no-per-frame-camera-refine-to-yard-lines-alone.md), [0010: Don't refine the endzone camera to its own paint](../decisions/0010-endzone-camera-not-refined-to-its-paint.md), [0011: Don't set the endzone pitch from the ankle ruler alone](../decisions/0011-endzone-pitch-not-from-ankle-ruler.md), [0012: Don't seed the joint solve with another play's mount](../decisions/0012-no-seeding-joint-solve-from-another-play.md), [0013: Bound the paint reader's implied lens to the seed play's](../decisions/0013-bound-implied-lens-in-paint-labelling.md)

## The endzone camera track invents motion; the pairing is the wound (2026-09-05, later)

Directive from the user (relayed): play 1 only until it works properly; no
compute on other plays. Play 5 was delivered (`diag/play_005_hifi_720.mp4`)
and its chain stopped; play 2 served as the diagnostic bench (CPU only).

**Kit labels in the TIME linker are dead** at any label quality: helmet set,
five plays, ten views (`07j`, `data/helmet/tracking_accuracy_kits.json`):
six views refused the saturation split (both teams in white, separation
1.2-1.4, the refusal in `team_color.saturation_split` at 1.6 / gap 50), and
on the four that split the hard gate was worse (purity p10 0.45 -> 0.37) and
a soft 1 m cost neutral to slightly worse. `08b --kit-link` defaults to off.
The kit's place is the cross-camera pairing veto: 53 % -> 17 % cross-kit ids
on play 2 (`--kit-link block` reaches 0 of 71 at +15 fragments).

**Why the pairing is a coin flip.** For the same player the two cameras'
foot points sit 1.4 m apart per frame with no bias; per frame only 10-12 of
22 players pair; most ids are one-view and render twice. Per-camera tracks
paired by trajectory (`tracking/pair_tracks.py`, `08b --pairing track`,
commit 471c6cf) found only 5 pairs on play 2, because the offset between
the cameras for one player is not noise but a slow swing: pre-snap a
lineman who is pixel-static in the endzone view (1 px) has a ground point
wandering 1.7-2.6 m, and a fixed endzone pixel's ground point swings 4 m in
a second while the sideline's holds to 0.1 m. The picture
`diag/p2_endzone_353_420.jpg` shows frames 353 and 420 of the endzone with
the SAME camera pose to the pixel while the old track claims 5.4 deg of
rotation between them. The endzone track (14 sparse paint solves, focals
jumping 5-10 % between neighbours, interpolated by 08b) invents motion.
The sideline is trustworthy (refined every frame; its players are static
to 0.04 m pre-snap).

**The fix in progress: `scripts/08h_endzone_track.py`.** Every endzone
frame registers into one reference through `calibration/endzone_mosaic`
(players masked, 170-1200 inliers, H near identity where the camera is
still); the motion between frames is the footage's; the absolute pose is
the open part. Tried and refused by the players ruler (median distance from
each sideline player's ground point to the nearest kit-consistent endzone
one, `08h` refuses to write unless it improves): (a) a per-frame focal
scale (no effect); (b) the mean of the old track's frames transported to
the reference (2.35 -> 3.07 m on play 2: the anchors scatter 3.7 deg, their
mean is not a pose); (c) a 4-parameter fit of the reference focal and
rotation on the players with the centre held (2.35 -> 2.61 m play 2, 1.18
-> 2.50 m play 1). The old track's per-anchor paint fits compensate a wrong
centre frame by frame, which a single pose cannot, so the running
experiment (`scratchpad/endzone_static_pose.py`) fits 7 parameters (focal,
rotation, centre) on a static pre-snap window where camera and players
both hold still, with restarts, then propagates through the mosaic and
scores the whole play. `08b --cameras cameras.npz` (commit da798e5) links
with per-frame cameras once a track passes. Play 1 is re-rendering
meanwhile with rule D's kits (keypoints -> tri -> refit -> hifi).

## 08h works once the camera-from-homography step is a ray fit (2026-09-06/07)

Every "pose fit refused" verdict on 08h was scored on broken motion.
Bisected on play 2 frames 353-360: a 0.4 px homography step came out of the
matrix route (K_t R_t = H^-1 K_ref R_ref, rows normalised, SVD polish) as
0.18 deg of rotation, 0.9 m on the ground at 300 m; the polish, not the
translation, set the rotation near the identity. `rot_focal_from_homography`
fits (rotation, log focal) to a pixel grid's rays instead: a pixel-static
player holds to 1 cm (commit a2fc4ee, tests in
`tests/test_endzone_track_rayfit.py`). Motion by consecutive-frame steps
composed outward (394-482 inliers per step); direct links to the reference
alias on the periodic yard lines at long gaps (play 1, 475-535: 7-21 px).
Composed steps drift over a play's second half (play 1: 7-90 px by frame
655, with the anchors right there), so the chain is anchored every 10
frames where a direct link's ray fit is under 2 px and blended between
anchors. First passing players rulers: play 1 1.19 -> 0.90 m (share within
1 m 0.43 -> 0.55) on the plain chain over 353 frames; play 2 2.35 -> 1.68 m.
Also measured: on play 2's reference frame the old endzone camera has the
field rolled 6 deg and the hash columns 200 px inside the painted ones
(`diag/p2_ref353_overlay.jpg`); paint alone cannot fix the focal at a 4 deg
lens (six points over 6 x 9 m at 300 m ran the solver to its bound), so
depth stays with the sideline's players.

## v11, v12, v13: the endzone track decided by triangulation (2026-09-08)

Three runs of play 1 through the same chain (per-camera link, OCR,
appearance pairing, identity, pose, keypoints, tri, refit, hifi), differing
only in the endzone track:

| | v11 | v12 | v13 |
|---|---|---|---|
| endzone track | interpolated, mount y=4 | footage (08h), from y=0 | interpolated, y=0 |
| players ruler (m) | 1.68 | 1.38 | 1.41 (v12's re-solve) |
| pairs / paired per frame | 23 / 9 | 23 / 6 | 24 / 10 |
| players triangulated | 18 | 15 | 21 |
| observable joints passing / reproj | 60 % / 6.7 px | 58 % / 10.4 px | 62 % / 7.9 px |
| refit rms | 0.087 | 0.091 | 0.085 |
| named | 29 | 25 | 26 |
| bodies per frame | 16 | 16 | 16 |

The footage-driven track loses on the geometry that matters although it
passes the players ruler and holds pixel-static players to 1 cm: the
feet-fitted anchors are locally right for the paired players, and a
single pose fitted from a capped nearest-neighbour objective is not. It is
opt-in now (`ENDZONE_TRACK=1`). The mount's across-field refinement stays
off (y = 0 pairs more, triangulates more). **v14 is the current deliverable
and the pipeline's reproducible baseline** (v13 plus the pairing overlap
floor at 6 frames, 67dab0d): 29 pairs, 27 two-camera ids, 0 cross-kit, 22
players triangulated at 63 % of observable joints and 8.4 px, 26 named, 16
bodies a frame. `diag/play_001_v14_hifi_720.mp4` (v13 kept beside it; strip
`diag/play_001_v10_v11_v13_strip.jpg`).

Open, in value order: two-view coverage (10 of 22 paired per frame; the
sideline OCR reads no numbers at 130 px bodies, so pairing rests on kit
and position), fragments (74 sideline tracks for ~29 people), the pose
of one-view bodies (monocular). Officials inside the field are NOT among
the unnamed white sideline ids on play 1 (all eight darkest are Baltimore
players, `diag/p1_v13_white_unnamed.jpg`): the sideline does not track
them as separate bodies, so the kit fault reduces to the boundary staff
and the sideline official, both excluded.

## The sideline camera through the rendered span (2026-09-08)

Grid distance of play 1's refined sideline track at 16 sampled frames:
2.7-6.6 px from frame 20 to 620, then 69 / 99 / 93 px at 670 / 720 / 770.
The tracks (and the render) end at 660: the late drift the memory warns
of is the post-whistle pan-out, outside the rendered span. No action.

## The endzone camera was never on its paint; the clips are 15 frames apart (2026-09-09, evening)

Three days of pose-side probes (priors, endzone weights, joint limits,
bounds tables) could not put the runner's legs under him. The footage
overlay's second look (`diag/overlay_ez2_0.3`) showed the two-view records
40-60 px off the player although their own sideline reprojection was 3 px:
the fit had floated 0.2-0.5 m off the turf to satisfy both cameras and the
box-point pin at once. Chasing that:

- **Ray-miss ruler** (`scratchpad/miss_ruler2.py`, now
  `calibration.endzone_paint.player_rulers`): per frame, the two cameras'
  rays through every confident keypoint of every paired player -- their
  miss distance, and the heights the closest points give hips and ankles.
  Play 1 as exported: miss 0.21 m at the median, 0.45 m while the endzone
  pans (frames 255-290), triangulated hips 1.7 m, ankles 0.3-0.8 m.
- **The endzone camera's paint** (`scratchpad/ez_paint_overlay.py`,
  `diag/ez_paint/`): the projected yard lines 40-85 px off the painted
  ones on EVERY frame, rolled, the hash rows 150 px off their columns. The
  camera came from the players' feet against the sideline's placement
  (from_players) with the mount centre a grid PRIOR at (60, 0, 20).
- **Rejected on the way**, each measured: refine_paint on the endzone
  (rotation + focal, centre held): grid 56 -> 28 px and the rays miss 5x
  WORSE (0.21 -> 1.06 m; a pencil of parallel lines does not see the
  lateral axis). The ray miss alone as an objective: degenerate, the fit
  rotates the camera up so the rays meet 5-30 m in the air. Yard lines +
  rays + an ankles-on-turf prior with the centre free: the lines
  registered one line off at the far end (nearest-line assignment, 60 px
  start on 60 px spacing), fits rolled the grid. A field crown: the two
  cameras' box-bottom ground points differ by a constant, not by distance
  from the centre line -- no crown.
- **What works** -- `scripts/08l_endzone_paint.py`
  (`calibration.endzone_paint`): yard lines clustered by their row at the
  image centre and registered by consecutive counting from the red end
  zone's edge (the goal line is the first line BELOW the red, which stops
  25 px short of it; its own white edge and the letters make lines above),
  the hash-mark dashes (grey > 150 -- they are thin and blurred -- RANSAC
  per column) for yaw and lateral position, the mount centre solved once
  over 12 frames, rotation and focal per frame from the neighbour's camera
  with two registrations tried and the paint picking, deltas smoothed over
  9 frames. Play 1: centre (60, 0, 20) -> (88.3, 0.6, 20.8), focal 9.9k ->
  15.2k, paint 2.3 px, dashes 1.3 px on 501/510 frames. The players, which
  the fit never saw: ray miss 0.213 -> 0.135 m, ankles +0.33 -> +0.05 m,
  hips 1.06 -> 0.83 m; the pan frames 0.10-0.19 m. Applied to play 1;
  original kept as `cameras_endzone_players.npz`. 08l refuses to write
  when the players do not confirm the paint.
- **The clip offset.** With the camera right, 05n's offset search sat at
  the edge of its range (-3, then -10 when widened, monotone): its ruler
  scores every player's reprojection and standing players meet at any
  offset. `scripts/05o_clip_offset.py` (`pose.clip_offset`) uses only
  (frame, player) pairs with sideline ground speed >= 3 m/s: a clear
  minimum at -14/-15 frames (0.110 m; 0.29 at +14, 0.53 at -70). The
  endzone clip runs 15 frames (0.25 s) AHEAD of the sideline where +3
  behind had been assumed. A runner at 8 m/s is 2 m from himself in 15
  frames -- that WAS the runner (id 9 paired 2.4 m off; 0.74 m re-paired
  at lag -15). The pairing, the triangulation's 42 % ceiling, the "two-view
  wobble" and the 1 m pairing ambiguity all carried this.
- **Re-pairing without re-running the GPU stages**: `scripts/08m_relabel_caches.py`
  (`tracking.relabel`) carries keypoints and pose caches to the new ids by
  their boxes (raises when the boxes differ; refuses under numpy 2 -- the
  caches are numpy-1 pickles).
- **The box-point anchor is biased** (2399 paired frames whose ankles
  agree to 0.3 m): the sideline's box-bottom ground point sits 0.31 m from
  the triangulated ankle midpoint (0.54 m pre-snap, the stances), the
  endzone's 0.44 m along its depth; the sideline's ankle ray at z = 0.08
  sits 0.06 m off (pre-snap 0.32). 05p's two-view pass now anchors on the
  triangulated ankles where both cameras see them (pin weight 10 -> 2);
  the one-view pass keeps the box (a separate change, measured next).

Pipeline: stages `endzone_paint` (after check), `offset` (after keypoints),
`repair` (08i --lag, 08m, 08c --from-cache; before tri); 05n reads
clip_offset.json. v26 = all of the above + 05p --two-view --endzone-weight
1.0 on the re-paired play (`scratchpad/p1_v26.sh`, `p1_v26b.sh`); strips in
`diag/overlay_v26/`, clip `diag/play_001_v26_hifi_720.mp4`.

**v26 sent (2026-09-09 20:20)** with the runner strip: the first version with
the runner's legs under him (frames 260-269); 272-281 and 245-257 still
flail. Two-view: 20 players, 1314 records, sideline 7.1 px / endzone 4.8 px;
1221/1546 frames anchored on the triangulated ankles. Probes on the runner
after v26, each judged on the strips against v26's (`diag/overlay_probe_*`):

- Keypoint filter judging by the nearest pair (kept the runner's ankles):
  WORSE -- the detector's left/right labels flip for 2-4 frames on 11 % of
  his frames (arms; legs 8 %) and the window-3 median had been catching
  those. Reverted.
- A refit from the rigid start when the warm-started frame is worse than
  10 px: WORSE -- lower rms with wider legs on one-view frames; the warm
  start is the regulariser the depth ambiguity needs. Off (RESTART_PX inf).
- Anatomical joint-range prior at weight 10 in the two-view fit: WORSE --
  83/222 two-view frames accepted, sideline 24.6 px.
- A flip-aware left/right rule (`keypoint_filter.fix_lr_flips`, 05p
  --fix-lr): swaps a limb group's labels where the swapped ones continue
  the last two frames' prediction and the given ones contradict it; finds
  826 flips on play 1 (the runner 111/441 frames). Probe running.

Also measured: only ~9 of 22 players carry an endzone partner per frame.
15 endzone tracks sit 14-15 m from every sideline track (the bench); 21
endzone tracks clash on kit with every candidate within 2.5 m (BAL #0's
270-frame endzone track has no white sideline track within 2.5 m: the
sideline does not track him there); the rest are fragments. Pairing v27:
numbers outrank a kit clash, a same-person continuation shares the span,
median 2 m / lateral 1.2 m gates on ankle ground points -> 37 pairs, the
worst at 1.33 m but one.

**Later the same evening (v27 running, GPU paused at the user's request at
21:28 with the v27 render at 154/324 frames -- resumable):**

- The side-agnostic left/right residual (Mono2DConfig.lr_symmetric, 05p
  --lr-symmetric): no help on the runner (probe v27sym). His bad frames
  258-270 have bad sideline keypoints (another player covers him; the fit
  cannot reach them, 10-35 px), not flips. Off.
- The 9-frame pose smoothing was a moving MEAN of axis-angle vectors: it
  smeared the runner's legs (limb reprojection 19 -> 25 px p50, 44 p90; a
  leg swung out where the stride turned) while halving a lineman's jitter
  (limb speed in the body frame 1.24 -> 0.50 m/s). Now a moving MEDIAN,
  window 7: the runner as the fit put him (19 px), the lineman 0.66 m/s.
  Ruler: `scratchpad/smooth_ruler.py`.
- The remaining 19 px on the runner: the fit used the regressor's betas
  (~1.72 m) and the timeline rendered the roster build (1.85 m default for
  an unnamed id) -- every rendered body sat ~20 px above its own
  keypoints (`diag/runner_f242_labelled.jpg`). 05p fits with the roster
  build now (render.roster_shape.roster_builds; --no-roster-betas to
  compare). Probe v27roster measures it.
- The pipeline's refit_mono runs the two-view fit by default
  (ENDZONE_WEIGHT=1.0; ONE_VIEW=1 for the v25 mode).

- **The fit put the ankle joint on the turf; the render puts the sole on it.**
  SMPL-X's ankle joint sits 0.08 m above the sole (a pointed toe 0.19 m),
  so every fitted body stood through the turf and the render lifted it
  6-15 px above its own keypoints (`diag/runner_f242_labelled.jpg`: the
  whole skeleton shifted up, the pose identical to the record). The roster
  build was not it (probe v27roster: 20.6 px). `fit_mono2d.sole_height`
  (ankles - 0.08, feet - 0.02) is the ground term and the rigid start's
  placement now: the runner's skeleton sits on him (probe v27sole), the
  lineman's limbs 4.7 -> 2.3 px. The ankle-ray ground anchor (ankle at
  0.08) and the ground term agree at last.
- The pose median holds only where a component turns less than 0.5 rad in
  the window; a fast limb stays raw (runner limbs 17.1 -> 14.7 px).
- A tighter one-view gate (8 px rms, --one-view-px-max): no help -- the
  runner's occluded frames (258-270) pass an all-joint rms gate while their
  arms alone sit 10-35 px off. Gate stays 20.
- **v28 poses (CPU, 22:59-23:24):** two-view 21 players, 1813/1859 frames,
  sideline 5.9 px / endzone 3.9 px (v27: 6.5 / 4.6); one-view 3097 frames at
  2.7 px (3.2). Strips `diag/overlay_v28/`: the lineman (12) and a walking
  BAL player (2) sit on their keypoints to the pixel; the runner (9) is on
  his body except 258-270 (occluded, arms follow bad keypoints). The render
  waits for the GPU (`p1_v28_render.sh`).
- **The runner's 258-270 were the two-view EDGE, not the occlusion.** The
  one-view pass cross-faded its fit toward the bordering two-view record over
  12 frames -- body pose included (w = 1 - d/13) -- and pulled the pose
  toward that record at ten times the usual init weight. A sprinter got a
  stride phase from 0.2 s later: f260 wrists 73 / 59 px off while the fit
  itself sat at 3 px; every probe of the evening (filter, restart, joint
  limits, flip rules, gates, per-joint rejection) looked at those frames and
  could not move them. The edge now carries its HEADING and placement only
  (blend_params(pose=False), EDGE_BLEND_POSE): f260 arms 40 -> 8.5 px, 264
  38 -> 14, 266 36 -> 19 (probe v28edge; the rest is the occlusion, arms
  filtered out and held by the temporal term). Per-joint rejection
  (--joint-reject-px) stays off: no effect there.
- **v28b poses done (01:46):** two-view 21 players, 1813/1859 frames,
  sideline 5.9 px / endzone 3.9 px; one-view 3097 frames at 2.6 px. Strips
  in `diag/overlay_v28/`. `poses_refit.json` is v28b (v28a kept as
  `poses_refit_v28a.json`, v27 as `poses_refit_v27.json`). The hi-fi render
  is the only thing left and needs the GPU: `bash scratchpad/p1_v28_render.sh`
  (~50 min), then send `diag/play_001_v28_hifi_720.mp4` and the runner strip.

- Prepared, CPU only: `scratchpad/p1_v28_poses.sh` (the full 05p with the
  roster build and the sole on the turf, teams, strips) and
  `p1_v28_render.sh` (the GPU render, on request).

Open after this: the one-view anchor from the ankle ray (ruler above);
the pairing's ground points from ankles (its 2 m gate feels the 0.8 m
box bias; ids 14, 25, 73, 78 still 2.5-3 m mis-paired at lag -15); 08c
named 28 ids after the re-pair (check against the previous run); frames
past 510 (the play over, 8-45 pairs) stay poor on every ruler.
