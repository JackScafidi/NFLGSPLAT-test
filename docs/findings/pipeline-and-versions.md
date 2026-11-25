---
type: findings
topic: pipeline-and-versions
period: 2026-09-04 to 2026-09-26
entries: 22
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Pipeline runs and versions

Pipeline runs and stage order, and play 1's version history with each version's measured state.

22 entries from 2026-09-04 to 2026-09-26, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Render and viewer](../concepts/render-and-viewer.md), [Play data](../concepts/play-data.md), [Census](../concepts/census.md), [Plausibility rulers](../concepts/plausibility-rulers.md), [Footage review](../concepts/footage-review.md)

**Decisions:** [0002: Build Layer 1 and Layer 4 first](../decisions/0002-layers-1-and-4-first.md)

## Current state (2026-09-04)

Two plays of BAL@KC 2024 wk1 run end to end unattended through
`scripts/pipeline_play.sh`: `data/all22/bal_at_kc_2024_wk1/play_001` =
`001_Sideline_KC_2-20_BLT_24` + `002_Endzone_KC_2-20_BLT_24` (KC 2nd-and-20
at the BAL 24); `play_002` = `004_Sideline_KC_3-9_BLT_13` +
`003_Endzone_KC_3-9_BLT_13`. The clip numbers pair by PLAY DESCRIPTION, not
by number. Play 3 (`010_Sideline_BLT_1-10_BLT_30`) fails the sideline paint
gates (players 2.8 m) and is parked.

Calibration, measured per play: sideline from paint with the rulebook
constants (hash tick centre 3.1242 m, numeral centre 12.50 m) reads both
rulers at 1.00; three judges pick the sideline candidate (rulers agree,
players 1.55–2.15 m, grid-on-paint ≤ 25 px); per-frame refinement to paint
(08e) takes play 1's grid from 9.5 to 5.4 px and play 2's from 12.7 to 9.0;
5-yard shift lands the formation at 23.3 / 14.1 yd from the goal line
against the descriptions' 24 / 13 (LOS check from the filename, with a LATE
guard when tracks start after frame 120). Endzone side of play 1 had been
mirrored; fixed.

Fidelity rework (user: "players falling over, not every player visible,
not smooth"): `render/timeline.py` draws every detected player every
frame (26–27 bodies/frame; 22 play, two deep officials, ~2 cross-camera
ghosts), ground from both views' feet, poses fused → single-view → median
stance facing velocity, per-joint SLERP, tilt clamp 35° (median tilt had
been 39°), view-aware dedupe. `05k_render_hifi.py` renders 1920×1080 on the
GPU at the source rate over the stride, ~6 s/frame, resumable.

Appearance: `05i` fits per-vertex colours to the footage (sparse torch
splatter, coverage-weighted loss, colour prior). v2 textures (60/106 and
53/85 ids) still rendered khaki: at 140 px a limb is 3–5 px wide and its
vertices sample turf-mixed pixels. v3 (commit ebd0355) drops samples within
0.12 of the frame's turf colour before the median (turf-likeness 0.72–0.84
→ 0.01 on the two bodies measured; held-out crop L1 gets slightly WORSE,
the instrument rewarded the bleed). The v3 re-fit of both plays and the
`render_hifi_v3` renders take ~5–6 h locally (2.5 min/body) and resume.

`--helmets` (render.helmet) dresses the head vertices in the team's shell;
on in the pipeline's hifi stage (a red or black shell reads as a football
player where a bare head reads as a mannequin).

**Field frame (2026-09-04).** Play 2's cameras were 80 YARDS off along
the field and every gate passed: paint is periodic and end-symmetric, a
"10" numeral backs both ends, the LOS check measures to the nearest goal
line. The footage warped onto the ground plane (`05l_field_from_footage.py`,
pipeline stage `field`, PNG in diag) is the check that caught it: the
footage's goal line, numerals and end zone must sit on the drawn ones.
Play 1 did; play 2 did not until a −73.15 m shift was applied (cameras,
poses_refit, poses_fused; `*_before_80yd.*` kept). The shift solver had
three faults (commit 8877612): strips only inside the goal lines, a
margin on shared support, and readings vetoing candidates. Play 2 now
solves −80 yd at net 11.6 vs −1.3; LOS 13.1 yd vs 13.

**Joints decision (2026-09-04 night, a17c5af..459bc45).** The 3-D joints
now come from GEOMETRY: 2-D keypoints per view (05m, YOLOv8-pose,
matched to the tracked boxes) triangulated with both calibrated cameras
(05n, through pose.triangulate) and refit to SMPL-X unchanged (05f on
`poses_tri.json`). The monocular regressor per view fused across views
(05e) is opt-in (FUSE=1). The camera ruler (05o: both refits projected
into both views against the detector keypoints) on play 1: monocular
22.7 / 40.7 px (sideline / endzone), triangulated 8.8 / 12.1 px, every
joint group, posed every frame instead of every sixth; play 2: 28 / 55
→ 9 / 11 px. Ground ruler: planted feet reach the turf under play 1's
cameras (raw triangulated lower ankle p10 +0.02 m), so no endzone pitch
correction there; play 2's fitted bodies float (p10 +0.22 m): its
endzone pitch is off by a few tenths of a degree and only the ankle
ruler sees it (the box-bottom gap is minimal at the current pitch by
construction). The second ruler now exists (efaed88: grid_fit scores the
endzone view's across-the-image yard lines, any orientation gated
against the projected lines) and settles it differently: on play 2 the
planted feet sit UNDER the turf at the current pitch (raw triangulated
lower ankle p10 −0.22 m) while the median floats (+0.20), and no pitch
moves both to the turf -- the float is dispersion in a sparse
triangulation, not a camera bias; the endzone paint reads 60–77 px there,
flat. On play 1 the feet are right at 0° (p10 −0.01) while the paint
prefers +0.3..0.5° (41 → 27 px): a 27 px residual is an error in another
parameter (roll, yaw, focal) a pitch cannot absorb. No pitch correction
on either play. The full endzone refinement against its paint was then
built (623eab0: `08e --cam endzone --orient-tol 25 --out`) and REFUSED
by the ankle ruler on play 1: paint 39.3 → 22.6 px, but the triangulated
lower ankle p10 −0.01 → −0.45 m, ray agreement 7.3 → 10.2 px, joints
passing the gate 47699 → 9291. The paint pulls the endzone away from
where the sideline's rays cross; the endzone's residual is not in
rotation+focal and its paint at 23–27 px is not a ruler the geometry
trusts. cameras.npz untouched (`cameras_endzone_refined.npz` kept for
the record). Do not pursue the endzone paint further.

**Play 2's right-edge column (2026-09-05).** Not one lineage at several
depths: 2–3 endzone-ONLY bodies per frame, each its own endzone track,
all placed at x ≈ −24 m because their endzone boxes are clipped by the
TOP of the frame (y1 = 0, 55–80 px tall, foot at the frame's top edge,
which maps to one ground line); 45 % of endzone boxes in frames 250–450
touch the top or bottom edge. x = −24 is 8–9 m behind the offence: the
officials, seen at the far top of the endzone view, drawn as default-
posed KC players. Candidate rules, not applied: a box touching the
BOTTOM edge has no foot point (drop from placement); a box touching the
TOP edge keeps its foot but has no height (no height gate; the geometric
signature for the officials question). Measured as an exclusion (one-view
id, never two-view, every box within 8 px of an edge): play 1 drops 23
ids (4.4 % of states, median 0/frame; 3 on the sideline at y ≈ +25 m, 20
late in the BAL end zone), play 2 drops 19 (10 % of states, median
3/frame, all 2–10 m behind the offence); no sure identity hit on either
play; every dropped id is TOP-clipped. Play 1's late end-zone group is
people beyond the end line (a seated row of photographers and an official
with a flag in the endzone frame's top 160 px), not players the sideline
lost: the sideline keeps 19–22 boxes through its zoom-out, 13 of the 19
project outside its frame and the 6 inside project onto empty end zone;
the one real end-zone player (BAL 32, a sure two-view id) is not dropped.
No time guard needed. The coordinator is adding the exclusion and fixing
build_timeline's views default (a pid with no views record was treated
as two-view at interpolated frames).
Two-view bodies now stand at their refit's translation (median shift
0.58 m from the box-bottom point); the tilt clamp is 60° for two-view
poses (measured p90 38°, none past 60), 35° for single-view. Play 2's
triangulation covers fewer players (23 % of joints pass); with `05f
--min-valid-joints 6 --min-frame-frac 0.5` all 30 refit, reprojection
13.4 / 12.2 px against 28 / 55 monocular, the head weakest (27 px
sideline: sparse joints), feet mixed (p10 −0.20, median +0.24 m) -- the
renderer drops bodies to the turf regardless. Renders `render_hifi_v5`:
play 1 from `poses_refit_tri.json`, play 2 from `poses_refit_tri6.json`
with `--team-by-colour`.

**Appearance decision (2026-09-04 evening, e37176c).** The hi-fi render
wears SYNTHETIC UNIFORMS by body region from identity's team
(render.uniform: helmet, jersey with sleeves to the elbow, forearm skin,
gloves, pants, socks, shoes; kits for KC red over white and BAL white
over black). Textures fitted from the footage cannot give a jersey at
140 px (one to three clean samples per vertex, turf bleed, speckle; after
de-mixing and smoothing the fit's gain over the plain median is ~0) and
flat team colours with a helmet read cleaner than any of them. The fit
stage (05i) is opt-in in the pipeline (FIT=1); the fitted textures stay
on disk for side-by-sides. Jersey numbers (c586cc2) go on ids whose
identity is sure -- a roster name and a (team, number) no other id of the
play claims (18/106 in play 1, 12/85 in play 2) -- as a surface decal:
ink texels of a 64-px raster pinned to jersey faces by barycentric
weights, 4 mm Gaussians lifted 8 mm off the posed surface (vertex
colours smeared: the torso lattice is 2.5 cm). The footage keeps the
field. Pipeline hifi flags: `--uniforms --numbers --helmets --follow
--eye-offset 2 -26 10 --fov 50 --field-texture`.

**Joints from geometry (2026-09-04 evening, 0036731).** `05m_triangulate_compare.py`
triangulates the regressor's 2-D joints (per-view caches; SMPLest-X's own
137 layout, 17 SMPL-X body joints mapped by NAME, and mirrored about the
box centre because the caches predate the runner's Y-up flip) through the
per-frame cameras and scores against the fused monocular lift on rulers
neither optimises. Play 1, 50 two-view players: the fused lift is 20–25 %
SHORT of anatomy on every bone (thigh 0.39 m, shank 0.41, ear-to-ankle
1.20 for a 1.85 roster median); triangulation has the metric scale (0.45,
0.50, 1.48) and is noisier per frame (bone variation 0.14 vs 0.10, ankles
0.32 vs 0.16 m off the turf). Next source for the refit: triangulated
joints with bone lengths held constant. `render.roster_shape` (dbcf29e)
already sets every avatar's stature to the roster height (the regressor
betas gave 1.71 m; roster 1.85). `08f_team_by_colour.py` (team from torso
saturation where bimodal: play 2 47/35 against identity's 62/23; play 1
refuses) feeds `05k --team-by-colour`.

**Timeline exclusions and seeds (2026-09-05).** `render.edge_rule`
(c47e073): a one-view id whose every box touches its frame's top or bottom
edge is left out (officials at the top of the endzone view, sideline
personnel, people beyond the end line; measured on both plays, no sure
identity lost). Interpolated frames now inherit an id's nearest recorded
views (a one-view id had passed as two-view there). Play 3's sideline
paint solve refuses: its candidates fit the paint (17 px) with a
25-degree lens 74 m out and players 2.78 m; a focal sweep along the paint
was built and FALSIFIED (player height is invariant along it, and the
paint costs 24 px per 25 % of focal). Remedy: `08 --seed-from <play-dir>`
(`SEED_FROM=` in the pipeline) seeds the joint solve with the sideline
mount of a solved play of the same game (plays 1 and 2 agree on (-4,
-100, 42) m, 12-15 degrees).

**Play 3 diagnosis (2026-09-05).** Holding the centre at the mount
(5e2a833) did not rescue it: the paint asks for a 21–53° lens from that
mount while the players' boxes (107 px, against 116 and 122 on plays 1
and 2) say 12°. The paint READER mislabels this clip; the gates refuse
correctly and nothing is exported. The correspondence diagnostic (drawn on
frames 394 and 622, `diag/play3_corr_*.png`) found the row-labelling trap
listed under "measured and rejected"; fixed in dd1b95c. Play 4 (`025_Sideline_KC_1-10_KC_49` +
`026_Endzone`, midfield) runs the whole chain with the mount held.

**Gates that lied by omission (2026-09-05).** `08` judged candidates only
when there were more than one, so a single held-mount candidate skipped
the three judges (play 3 went through at 2.81 m); fixed 55764d0. The
paint reader's row labelling in two-row frames called the far sideline
plus the far hash row the two sidelines (2.3x stretch, 41° lens) and grid
consistency cannot see a cross-field stretch; `assignment_is_possible`
now takes a lens band from the seed play (dd1b95c, `08 --seed-from` /
`--band-from`). The hash ruler is fooled by the midfield logo's white
paint (play 4 at the KC 49: hashes 1.82, numerals 0.99, LOS 48 vs 49,
field texture exact), so the pipeline's check passes a disagreement on
two of three witnesses, loudly (09757f0). Play 4 is the third play
through the chain, delivered 2026-09-05 06:30 (`diag/play_004_hifi_720.mp4`):
identity 44 of 82 named, 43 players triangulated at 7.7 px, refit 19 of
43 at the old 70 % frame threshold (the pipeline now uses 6 joints and
50 %), teams by colour refused (not bimodal), so identity's split stands
and leans KC. Any further play runs with `scratchpad/run_play.sh <dir>
<sideline.mp4> <endzone.mp4> <los-yards> --fresh --from-paint`, which
sets RED/WHITE and SEED_FROM=play_001. Play 3 under the band with the centre free gives the
right lenses (16–18°) and still fails every judge (rulers 0.78 vs 2.11 on
one candidate, players 2.55 m on the other, grids 61–95 px): its row
labelling is wrong beyond the two-row trap. Parked, refused honestly;
the next instrument there is the reader's per-frame labelling drawn on
the frames (`scratchpad/play3_correspondences.py`).

**Renderer (2026-09-04, 7688363).** Every body and the field rendered as
per-pixel salt-and-pepper (a flat red body: std 34/255, 1 % near-black
pixels), unchanged by splat size or opacity. The sparse splatter's
running sum of log(1 − α) spans every pair of the frame and reached
tens of millions, where float32 resolves to ~4; the per-pixel exclusive
difference was noise. Summed in float64 now; a dense uniform plane must
render flat (test). Every hi-fi render before this carried it. The
textures are also mesh-Laplacian smoothed (aca87c2: speckle from one to
three valid samples per vertex; roughness halves) and the fit's held-out
measure skips turf pixels like the loss (59d31e3).

The same texture is the hi-fi render's field (`05k --field-texture`,
pipeline stage `hifi`): real paint, end zones and night lighting, the
procedural field colour-matched where the cameras never looked. Against
real turf the v2 khaki bodies vanish; the v3 textures are required.

Still open, in value order: identity/texture continuity across track
breaks (stitching measured no better than none, see below); the two deep
officials render as team players (stripe score and torso colour both
measured non-discriminative; position at the snap is the remaining
instrument, ~10 m behind the offence, and play 2's clip starts mid-play
so it only helps play 1); cross-camera ghosts (measured 2026-09-04: a
sideline-only and an endzone-only id that project into each other's
boxes average 0.8/frame on play 1, 0.6 on play 2, before the timeline's
dedupe -- scratchpad `ghost_crosscam.py`; a reprojection merge was built
(de1e2c8) and measured: every pair it finds already falls to the
depth/across rule, bodies per frame and duplicates dropped unchanged on
both plays, so it was reverted); 25–34 default-posed states per play; identity's TEAM labels: 08c splits each
track's torso colour two ways (team_color.split_two_teams_balanced) and
votes the clusters onto the real teams by roster overlap, and on play 2
that disagreed with the per-id saturation gap on 22 of 52 ids (47/35 by
colour against identity's 62/23); the render takes teams from 08f where
the saturation is bimodal, but identity itself should adopt the gap split
where it passes -- a re-run of 08c re-keys the fused/refit caches, so it
waits for a pose-chain rebuild. `05k --follow` dollies the virtual camera with the play's smoothed
centroid (render.camera_path); judge on a clip before it goes in the
pipeline.

## Play 1 v9 and v10 delivered (2026-09-07)

| | v8 | v9 | v10 |
|---|---|---|---|
| endzone track | interpolated anchors | footage (08h) | footage (08h) |
| link | per frame, old cams | per frame + kit gate | per-camera tracks, appearance pairing |
| two-camera ids / cross-kit | 62 / 24 % | 84 / 23 | 21 / 0 |
| players triangulated | 47 | 36 | 15 |
| observable joints passing | 65 % | 66 % | 57 % |
| named | 31 | 49 | 33 |
| timeline bodies / frame | ~29 | 21 | 17 |
| excluded ids (edge / ghosts / dwellers / striped) | 23 / - / - / - | 30 / 32 / 26 / 0 | same rules |

Files: `diag/play_001_v9_hifi_720.mp4`, `diag/play_001_v10_hifi_720.mp4`,
strips `diag/play_001_v8_v9_strip.jpg`, `play_001_v9_v10_strip.jpg`. v10 is
the cleaner baseline (right kits, no ghosts, no staff, one body per
sideline track); its cost is two-view coverage, so most poses are
monocular. The 17 bodies per frame are the sideline's 22 tracked ids minus
excluded non-players -- what the sideline frames.

Measured and not adopted today: same-camera stitching with kit and number
vetoes (welds one wrong pair per right one on named fragments); depth
whitening before linking (fewer tracks by welding on the helmet set:
purity p10 0.49 -> 0.44, switches 191 -> 245); a wider kit gap for the
appearance pairing (22 -> 40 pairs, 8 -> 9 players paired per frame).
Sideline OCR reads 3 numbers to the endzone's 34 at 130 px bodies; an
upscale/band sweep was measured (`diag/sideline_ocr_exp.log`).

## The pipeline's stage order since feabdfc (2026-09-07)

`scripts/pipeline_play.sh <play-dir> <side.mp4> <end.mp4> <los> [--fresh]
[--from-paint]`, markers `.done_<stage>`; env RED/WHITE, SEED_FROM,
GRID_PX, FUSE, FIT, DIAG:

paint (08, --from-paint) -> export (08b from recon) -> refine (08e) ->
shift (08d --apply) -> endzone (08 --sideline-from, then 08b again) ->
check (08d rulers + LOS; two-of-three) -> **endzone_track (08h: the
endzone camera from the footage's motion; refuses to write unless the
players get closer)** -> **link (08b --cameras cameras.npz --pairing track
--pair-gap 0: camera tracks keep their ids; the export's tracks kept as
tracks_export.parquet)** -> field (05l; LOOK at the PNG) -> **identity
(08c OCR per camera track -> 08i pairing by number then kit -> 08c
--from-cache names on the paired ids; BEFORE the pose stages because
pairing changes the ids and every pose cache is keyed by id)** -> pose_s
-> pose_e -> keypoints (05m) -> tri (05n) -> [fuse, FUSE=1] -> refit (05f,
6 joints / 50 % frames) -> [fit, FIT=1] -> teams (08f) -> hifi (05k, 720p
encode into diag) -> render (05d). The script's header comment still lists
the old order; it is edited only when no instance runs. v11 is the first
fresh run through this order (2026-09-07 20:14).

## v11: the script end to end, and what the fresh run taught (2026-09-07 evening)

The first fresh `--fresh --from-paint` run of play 1 through the new stage
order failed twice before it ran: the launcher seeded play 1 from itself
(`SEED_FROM=play_001`; circular, a 52 px grid where the free solve gives
9 px) and the numeral ruler crashed on an empty strip from a wild
candidate (`yard_numbers.read_line_strips`, guarded, 9800092). Then it ran:
paint (candidate 1: (42, -102, 42.5), 11.8 deg, rulers 0.97/0.96, players
1.86 m, grid 9.2 px), refine, shift, endzone, check, endzone_track
(REFUSED, chain continued: 23c83f8), link (153 camera tracks), identity
(OCR 34 of 153 read, 23 pairs of which one on a number, 21 two-camera ids,
0 cross-kit, 29 named), pose, keypoints, tri (18 players, 60 % of
observable joints at 6.7 px), refit, hifi.

The sideline reproduced to the pixel against v10's cameras. The endzone
did not: the re-solve's refinement moved the mount to y = 4 on a height
tiebreak, and on the whole play that is worse (players 1.68 m at y = 4,
1.56 m at y = 0, 1.35 m with the footage-driven track from y = 0), so
`08h` could not beat the interpolated track from that start (1.77 m one
start, 1.82 m nine starts, 1.73 m seeded from v10's pose). The across-field
refinement is off (`REFINE_DY_M = (0.0,)`, bc09480): the feet do not see y
on 14 anchor frames; the synthetic justification was noiseless. v12 re-runs
the chain from the endzone stage with y held at the seed.

## v23: the user's four notes on v22 (2026-09-08 evening)

The user, on v22: (1) jitter and shakiness, players glitching in and out;
(2) the QB the wrong colour, players near each other switched around;
(3) every build the same, linemen no bigger than corners; (4) which play
is this. Measured and answered:

**Glitching in and out** (ruler: a drawn id's runs between rendered
frames): 223 disappear/reappear events over 54 drawn ids, gaps of 4-16
frames, 781 vanished frames -- 293 with a ground point and dropped by the
dedupe, the rest interpolated through a short detection gap and then
dropped by the dedupe as the neighbour's copy (linemen 0.8 m apart). Fix
(`timeline._anchored_by_frame`): a state whose id the sideline detected
within MAX_GAP_FRAMES (30) of the frame is anchored, never a duplicate;
only ids unseen for longer dedupe.

**The QB** is sideline id 5 for the whole play (frames 14-628), kit votes
42 red / 2 white, team KC, drawn red throughout; what is wrong on him is
the NUMBER: the endzone track paired to him read 10 on 7 of 7 crops, and
#10 is Pacheco, who stands beside Mahomes in the shotgun -- the pairing
cannot tell two backfield players 1-2 m apart along the endzone's depth,
and the name follows the endzone's number. Open.

**Switched around**: the kit margin per detection flips for good inside
10 of 74 sideline tracks (sustained runs of the other kit, 20-135
confident detections): the linker handed the track to another player.
`tracking.split_by_kit` cuts a per-camera track where the smoothed kit
sign holds for >= 15 confident detections (a blip of 6 is a shadow); 30
cuts on play 1 (13 sideline, 17 endzone), stage `split` (08k) between
link and identity, so numbers, partners and avatars are per player.

**Builds**: every avatar had the regressor's near-neutral girth, only the
height from the roster. SMPL-X beta1 sets girth (+-27 % of mesh volume
per +-2) almost without touching stature; the neutral body is 77 kg at
1010 kg/m^3 (BMI 26), so a roster weight is a target mesh volume.
`roster_shape.betas_for_height_weight` meets both (Travis Jones 1.93 m /
152 kg -> beta1 +2.7, 150 kg; Marquise Brown 1.75 / 77 -> -0.3). All 21
named ids carry a weight; unnamed ids keep the default build.

**The play**: BAL @ KC, 2024 week 1 (the Thursday opener, 5 Sep 2024), KC
on offence, 2nd-and-20 from the Baltimore 24; the next clips in the
folder are KC 3rd-and-9 and 4th-and-9 from the 13, so the snap gained
11 yards. Named on it: Mahomes' track carries #10 (see above), Pacheco,
Noah Gray, JuJu Smith-Schuster, Humphrey, Taylor, Suamataia; BAL Stephens,
Cooper Jr., Ojabo, Travis Jones, Agholor.

v23 = the script from the link stage with the split stage, the anchored
dedupe and the weighted builds. Its chain: 30 cuts (151 -> 181 per-camera
tracks), OCR 41 of 181, 36 pairs (30 two-camera ids, 0 cross-kit, 10
paired a frame), 28 named (5 shared names demoted, the kicker vetoed), 24
players triangulated at 65 % / 7.8 px, refit 0.096 m, 3603 one-view
records at 3.6 px, 25 states a frame.

The anchoring alone over-corrects: a ruler of VISIBLE defects per pair of
rendered frames (a body vanishing with no body within 0.6 m of where it
was; two bodies within 0.4 m) on v23's caches -- v22's rule 155 vanishes /
108 doubles; anchoring alone 39 / 360 (a second fragment id interpolated
on top of its player's detected body is now kept); anchoring with the
rule that an interpolated state within INTERP_DUP_M of a detected one is
still a duplicate: 46 / 123 at 0.4 m, 55 / 121 at 0.5. Adopted 0.4. v23's
render carries the anchoring alone (360 doubles); v24 = v23 + the radius.

**Shakiness as rendered** (ruler: the timeline's interpolated poses at
the render stride through the FK, second differences per rendered step,
hands and feet): p50 38 mm, p90 267 mm on v23 -- fused and one-view
records alike, i.e. limbs jumping a quarter metre between rendered
frames at the p90, where a sprinting limb's true second difference is
a few cm; first differences (real motion) p50 36, p90 147. A zero-phase
moving average over the interpolated axis-angles (`timeline.
smooth_axis_angles`, POSE_SMOOTH_FRAMES source frames):

| window | jitter p50 / p90 (mm) | motion p50 / p90 (mm) | 2nd/1st |
|---|---|---|---|
| off | 38 / 267 | 36 / 147 | 1.08 |
| 5 | 21 / 150 | 33 / 140 | 0.65 |
| 9 | 15 / 95 | 29 / 119 | 0.50 |
| 15 | 10 / 65 | 24 / 94 | 0.41 |
| 21 | 7 / 50 | 20 / 81 | 0.35 |

Adopted 9 (0.15 s): the jitter halves at the p90 and 81 % of the p90
motion stays; past that the smoothing eats strides. v24 carries it.

v23 rendered 20:17 (`diag/play_001_v23_hifi_720.mp4`; stills against v22
in `diag/p1_v22_v23_strip.jpg`): the linemen are visibly bulkier and the
backs slimmer (the roster builds), 25 states a frame with the anchoring
alone (some doubles at fragment overlaps, as the ruler said). v24 = v23's
caches + the 0.4 m radius + the 9-frame pose filter, render only (21:04,
`diag/play_001_v24_hifi_720.mp4`, sent; stills against v22 in
`diag/p1_v22_v24_strip.jpg`): 24 bodies a frame, 28 named, 34 ids with a
roster weight, 366 tilt-clamped states (78 before the pose filter: the
average of neighbouring axis-angles leans a few bodies past the limit for
a frame; harmless, the clamp catches it). **v24 is the deliverable.** The
QB (sideline track 5, the lone back 5.5 m behind the line) is drawn red
throughout and carries #10 from the endzone's 7-of-7 reads; whether that
body is Mahomes with a misread 15 or Pacheco could not be settled from
the crops -- the user is asked.

## Where play 1 stands at v31 (2026-09-10, late)

Sent: v30 (role builds, the pairing veto) and v31 (twins folded). Fits on the
v31 ids: two-view 1577 frames on 22 players at 6.1 px sideline / 4.1 px endzone,
one-view 3487 frames at 2.6 px, population median against a body's own keypoints
3.1 px (v28b 3.8, v30 3.2). The render draws 67 players over 647 frames.

The bodies that still sit worst against their own keypoints, all one-view:
id 13 at 12.9 px over 193 frames -- a defensive lineman in a three-point stance
whose LEFT arm reads 33-49 px off with keypoint confidence 0.26-0.46 while his
right arm sits at 10-15 px (the down hand is under his own body and the detector
barely sees it); then 76 (14.5 px, 34 frames), 40 (12.4, 20), 55 (9.7, 11).
Nothing there looks like an identity fault any more -- the fits are on the right
men, in the right poses, with an arm that cannot be seen.

Everything tried against the remaining arm jitter has now been measured and
rejected: the left/right flip filter, holding an unseen limb at its previous
pose, per-joint outlier rejection, the restart, anatomical bounds, and the
side-agnostic residual. The arms move when the detector loses them, and no
prior built out of the previous frame fixes that.

## 2026-09-24 17:50 -- v108 = CURRENT BEST (film-checked on both cameras)

v108 = the v107 tables + lkft2c (the ft2 two-view fit through 05p, merged onto the live keys; play_001/poses_refit.json
= lkft2c, backups .v107 (the buggy lkft2) and .v105). Live rulers (07l, 395-607): steps 2 / hops 0 / census 0.17.
Film: the endzone camera beside the endzone-view renders of v107 and v108 for the receiver 74 at 546-566
($S/ez_strip.py): the film has Gray square to the camera and the ball; v107 draws his back at 550-558 (torso -165 /
-171 / -154), v108 his front (-11 / -21 / -24; the endzone camera looks down -x, so a heading near 0 faces it). The
sprinter stays upright with his arms pumping, the back keeps his crouch, the whole-scene strips show nothing new.
Viewer Version 24 (v108 joints with look/eye), write-up Version 14 (the refit-input bug as an open-defect lesson).
Not shipped: lkft2p (05p --two-view --endzone-weight 0.3, the pipeline default arm): knees 122.4, the sideline
dominates, VPoser worse.

## 2026-09-24 19:45 -- v109 = CURRENT BEST (rendered, film-checked on both cameras)

diag/play_001_v109_hifi_720.mp4 + _sideline_blend / _endzone_blend; 07l steps 2 / hops 0 / census 0.17 (= v108).
Sideline-view renders v108 | v109 against the film ($S/lock_diff_strip2.py; $S/v109diff_*.png): id 6 at 576-590
(v108 his back to the camera with an arm flung out, v109 facing it as the film has him, number and face); id 9 at
494-502 (v108 turned toward the defender, v109 sprinting left with his lean); id 28 = Kyle Hamilton at 542-552 (v108
hunched then diving sideways at 552, v109 running away from the camera with his nameplate showing, as the film).
Endzone view ($S/v109_thuney_ez.png): Thuney's arms reach LEFT toward his rusher at 548-596 like the film; v108 reached
right. The whole-scene run sheet is unchanged elsewhere. Viewer Version 25 carries these joints.

Open after v109 (measured, not built): (1) two wrong records IN A ROW between two groups (id 12 = KC #71 at 590/596:
each agrees with one side, the vote keeps both; drawn a 314-degree spin, the film has him on his man) -- the detour
pass (drop a run of 1-2 records whose removal shortens the turn by > 170 deg within 24 frames) is the next unit;
(2) id 9 at 460-490: the fits there face him 90 deg off his sprint; no rule without the motion can fix a majority of
wrong records; (3) one-view bodies slide sideways to their chest faster than 3 m/s on 36 % of live steps (two-view
12 %) -- for id 3 the box says he really recedes from the camera while his fit faces 70 deg off that run; which is
wrong is open, and it makes his first-person camera strafe.

## 2026-09-24 20:45 -- PAUSED (user powering off): v110 render stopped mid endzone view

v110 = v109 + timeline.drop_detour_keyframes (24495c1), viewer Version 26. Rendered before the stop: the hifi clip
(diag/play_001_v110_hifi_720.mp4), the sideline blend and the sideline view (render_view_v110). The endzone view
(play_001/render_ezview_v110) stopped at 172 of 200 frames; the newest frame (560) was deleted in case it was half
written. RESUME: re-run the endzone view (05k --view-camera endzone ... --out-dir play_001/render_ezview_v110, the same
flags as v109's; it resumes from the frames on disk), then the v109-vs-v110 film strips for id 12 (588-600) and Oweh 15
(596-608) on both views; if they hold, v110 = CURRENT BEST. Scratch scripts: $S/chain_v110.sh (re-runnable end to end),
$S/film_v110.sh.

## 2026-09-25 00:15 -- v110 = CURRENT BEST (render finished after the power-off; film-checked on both cameras)

The endzone view resumed from its 172 frames. v109 vs v110 renders against the film ($S/v110diff_id12.png,
$S/v110_id12_ez.png, $S/v110_id15_ez.png): id 12 (a KC guard, on his man) keeps his back to the endzone camera through
588-606 as the film has him (v109 turned his face to it at 594) and no longer spins on the sideline view; on the
sideline his facing is left toward the defender but on the far side of it (the records after 596 sit 50-80 deg off the
film's slightly-toward-the-camera facing) -- steadier and closer, not exact. Oweh at 596-608 barely changes. Viewer
Version 26 = v110. Next: VPoser in the fit re-measured on the fixed 05p ($S/vp_chain.sh, running).

## 2026-09-25 04:10 -- v111 = v110 + the KC left line untangled + the bridge pose blend (ported; render running)

**Chain 3 (the port candidate) on the copy, with the bridge blend (4837025), vs the v110-equivalent control:** census
0.169 -> 0.160; steps 2 / hops 0; hinge jerk 5 -> 4 (without the blend 12: the centre's midpoint snap); joint jitter
p99 0.183 -> 0.163; the depth ruler's across-field p99 2.33 -> 1.18 m (over 1.5 m 4.9 -> 2.8 %); the vanishings list
unchanged. Ported to play_001 ($S/port_line.sh; tables snapshotted *.v110 plus the 08z/08za backups): the live tables'
md5 now equal the copy's; play_001/poses_refit.json <- lkft2l3c (05n/05f/05p on the relabelled tables, merged onto the
live keys remapped by 08v). The ids: 37 = Suamataia #76, 139 = Thuney #62, 204 = Humphrey #52 (17 folded into him);
the centre's 5-box sideline fragment at 475-492 dropped. The bridge blend alone on v110: jerk 5 -> 3 (id 84 at 594),
torso worst step 70 -> 40.

Still open on the line: id 4 (BAL) 1.4 m across in his 443-528 sideline hole (hole-hold, not identity); the centre's
endzone rows at 531-577 sit on a box shared with the Raven he blocks.

## 2026-09-25 05:15 -- v111 = CURRENT BEST (rendered, film-checked on both cameras)

Live 07l: steps 2 / hops 0 / census 0.16 (KC 10.96, BAL 11.03). 09d on v111 vs v110: jerk 5 -> 4, R leg sideways
6.0 -> 5.1 % (Thuney off the worst list), L arm 6.7 -> 6.3, R arm 13.3 -> 13.5; the look over 20 deg per step 1.08 ->
0.87 %, eye accel p99 0.230 -> 0.209; depth ruler across p99 1.18 m (v110 2.33). Film (endzone view v110 | v111,
$S/v111_thuney_ez.png, _76_ez, _centre_ez): Thuney projects on #62; the left tackle at 440 in a pass-set stance where
v110 lunged; at 500 the centre and Thuney drawn side by side like the film (v110: one lineman with a Raven in front).
Whole-scene sheet unchanged. Viewer Version 27, write-up Version 16. Next accuracy units: id 4's hole (the hole hold
pins him to the sideline's line while the endzone boxes him rushing on); the remaining arm-pose tail.

## 2026-09-25 06:40 -- v112 reviewed; the hole chain and the pre-snap fill adopted; the endzone pose gap measured

**v112 = CURRENT BEST (small).** v111 + the corrected roles: the hifi render's pre-snap ball sits at the centre's hands
on the turf (review_v112 ball strip 388-402), in the quarterback's from 398. Its joints export equals v111's body for
body (compare_exports: 4400/4400, no difference), so the viewer (Version 27) stands. The two camera-view renders were
stopped to free the GPU (kill_views_v112.ps1; NOTE: a venv python.exe is a launcher with a child interpreter carrying
the same command line -- a "stop two processes" watcher stops one render's pair).

**Hole chain adopted (e792787 flag, 52202cd on).** Flags off reproduce v112 and flags on the runtime-patch what-if,
exactly, on 13,424 drawn body-frames. Endzone film (05q strips diag/ov_chain_A|B): Madubuike over #92 on the turf
instead of on #74's block; the centre on #52 512-528 (the old bridge drifted 0.5 m onto Thuney), 500-508 a bridge
0.25 m right of him (no box on him there). Live 07l unchanged; depth ruler across p99 1.18 -> 0.86 m.

**Pre-snap fill ON again (321850f).** Live tables: pre-snap |KC-11| 0.511 -> 0.400; the one drawn change is Trey Smith
on 22 more pre-snap frames; live 07l unchanged; full census 1.49 -> 1.46. tests/test_play_timeline_structure.py pins
the block under the line vouch.

**The pose gap (next unit after v113).** With every pose cache counted (fused refit + the sideline regressor),
262 of 4,684 live drawn body-frames (5.6 %) have no pose record of their id within 6 frames: Madubuike 122 (his
hole), Thuney 52, the centre 35, ... -- 169 of them endzone-only. Pre-snap 462 of 7,855: Gray 165, the quarterback
157 (fixed by the pre-snap fold: t25's records move to 80), Trey Smith 125. The timeline SLERPs across such a gap,
which is why Madubuike is drawn upright while he crawls. The endzone camera's own regressor cache
(poses_endzone.json, 05c) sees him lying -- trunk 56-70 deg off upright at clip 482-494, 28-42 deg while he lunges --
but the loader never reads it: it is keyed by ENDZONE TRACK ids (45, 136 for id 4) and clip frames. A runtime patch
(scratchpad patch_endzone_poses.py: records mapped to global ids and sideline frames, used only where no fused or
sideline record lies within 3 frames; the endzone's wide boxes as "on the ground" only where the sideline has no box
of the id) is being measured. An earlier count that used the refit cache alone read 30 % "stale" -- an instrument
artifact (the sideline regressor fills those frames; the drawn joints articulate 0.06-0.2 m a step).

**Pre-snap fold refit (copy) running:** presnap_refit.sh (05n/05f/05p on the folded tables, merge_relabelled onto the
remapped live keys plus the relabelled men's new records on 14-400; arms A1/A2/A0 through one tail, chain + fill on).

## 2026-09-25 08:40 -- v113 = CURRENT BEST (rendered; film-checked); v114 rendering

**v113** = v112 + the hole chain (skip + across-ray bound) + the pre-snap fill back on + the pre-snap KC line and
quarterback fold (+ refit) + the endzone camera's regressor poses before the snap. Live 07l: steps full 37 (v112 42)
/ live 2, hops 0, census live 0.13 (0.16), full 1.40 (1.49); pre-snap |KC-11| 0.51 -> 0.06; depth ruler across p99
1.18 -> 0.86 m; 09d live unchanged (jerk 4), pre-snap trunk past 70 deg 140 -> 65. Film: endzone 05q strips per change
(diag/ov_chain_*, ov_ezpre_*, ov_snap_*), the hifi render strips (review_v113: the set line crouched, the quarterback
under centre, Madubuike placed at #65's block -- his crawl still drawn as a lunge). The camera-view renders were
stopped (kill_views_v113.ps1, kills every match until the chain reports done) to go straight to v114. Viewer Version
28 (joints_v113), write-up Version 17.

**v114 (rendering since 08:32)** = v113 + id 186 untangled (sideline t80 524-567 = Thuney's twin, dropped; endzone
t22 512-526 = the quarterback, folded into 80; live tables snapshotted *.v113) + depth_snap.SNAP_OWN_ID on (fb10956;
the quarterback 585-606 and #76 580-601 on their own keypoints in the endzone film, a metre off before). Next after
v114: Madubuike's crawl (an endzone keypoint fit for moving endzone-only men; the regressor's records six frames apart
contort), Thuney 586-601 on a box merged with #76's.

## 2026-09-25 09:35 -- v114 rendered (strips checked; camera views running); 05r measured for v115

**v114** = v113 + id 186 untangled + the own-id depth snap (fb10956). 07l: steps 36 / 2, hops 0, census live 0.13,
full 1.39. Render strips (review_v114): the quarterback standing in the pocket 586-608 (legs in a stride where he
stands -- old), #76 pass-blocking #99 580-602 like the film. Camera views rendering (not stopped this time).

**05r (3528e3b): the endzone-only one-view fit.** On v114's cache, live window, --lying-aspect 1.3, merged boxes
(> 1.5x the id's median width) skipped: 45 ids, 794 frames, 3-10 px. 09d live: jerk 4 unchanged; sideways bends up
(L arm 6.2 -> 8.9 %, R arm 13.7 -> 15.4, L leg 4.1 -> 8.6, R leg 5.1 -> 6.5; Madubuike 56 L-leg frames). The FILM
disagrees with that ruler (endzone strips diag/ov_05r_base|r): #32 (id 2) 510-546 and Thuney 560-595 drawn on their
keypoints (base: beside them), Gray's hands out for the ball at 536 (base: an arm over his head), Madubuike lying
along his body 494-502 (base: upright), zig-zag limbs 506-522. The sideways-bend ruler counts a backpedalling safety
and a crawling man as faults. -> v115 = v114 + 05r on 395-615 (859 records; $S/poses_refit_v115.json, installed after
v114's views finish). Then the pipeline stage (refit_ez after refit_mono).

**Logged, not chased:** Thuney's pose blips at pre-snap frame ~270 (one endzone regressor record at 269, not a
heading flip, so the flip veto keeps it); the quarterback's legs in a stride while he stands 586-608.

## 2026-09-25 10:45 -- v115 (05r poses, pose only) rendering; a drawn cross-view ruler; two placement probes

**v115 = v114 + 05r's endzone-only fits, POSE ONLY.** The first v115 run (10:00) moved bodies onto 05r's pelvis via
place_from_refit (the endzone's raw ground point: a 0.63 m step, hops 0 -> 1, census 0.13 -> 0.15) and was stopped;
73d44ba marks 05r's records no_place and place_from_refit skips them. Re-run: 0 of 13,386 drawn body-frames moved, 07l
identical to v114, heading changed on 1,703 (median 9 deg). v115 relaunched 10:11 (views running).

**A drawn cross-view ruler ($S/drawn_xview.py JOINTS [CAM] [LO HI]).** The exported (drawn) world joints projected
into the endzone film against its keypoints (shoulders..ankles), per body-frame the median px; then each frame's shared
offset (the endzone camera's bias) removed and split into the body's own offset (placement) and the shape (pose).
Live window, 1,156 body-frames: v112 p50/p90/p99 19.2/57.0/158.7 px; v113 19.1/55.6/143.3; v114 18.5/41.2/110.2 (the
own-id snap); v115 15.8/36.3/112.8. v114 -> v115: shape p90 24.0 -> 14.4 (05r; partly circular on its own frames),
placement p90 36.7 -> 31.5, p99 ~109 unchanged: the placement tail is sideline-seen men (the quarterback 426-526,
Raven 15 398-470, the centre 398-442, #32 458-540, #76) -- next unit.

**Probes.** MAX_REFIT_ACROSS_M 0.5 (the across-ray gate on the refit placement, 09-18 "no change"): steps full 36 ->
35, nothing else; #32 and Trey Smith unchanged on film -- not adopted. The loader without placement from the refit's
pelvis (place_from_refit_transl False): A/B running (the refit's two-view pelvis overrides the own-id snapped point).
Thuney's pre-snap blip at 270: drawn position and heading steady, the endzone camera smooth, his endzone regressor poses
steady -- the likely source is a sideline regressor record from t82's upper-body box (folded into 139); 1-2 frames,
logged. The quarterback's stride at 586-602 while he stands (0.2-0.8 m/s, under the gait): a one-view leg ambiguity.

## 2026-09-25 11:15 -- v115 = CURRENT BEST (rendered; film-checked); viewer Version 30, write-up Version 18

v115 = v114 + 05r's endzone-only fits as POSES ONLY (no_place). 07l identical to v114 (steps 36 / 2, hops 0, census
live 0.13, full 1.39). Drawn cross-view ruler (endzone film, live): p50/p90 15.8/36.3 px (v114 18.5/41.2); per joint
(shape) ankles p90 43 -> 29/23, wrists 35/43 -> 23/33; limb joints over 25 px: arms 644 -> 359, legs 795 -> 323.
Hifi render strips (review_v115): Madubuike on the turf beside and under #65 at 494-522 (v114: lunging upright);
Thuney pass-blocking #98/#99 560-596. Camera views rendering; they do not change the viewer.
Probes this hour, not adopted: the loader without refit placement (census 0.13 -> 0.10 but steps live 2 -> 6, jerk
4 -> 11, placement p90 31.5 -> 42.4 px); the foot lock off (the quarterback's leg joints over 25 px 67 -> 56 only --
his records at 420-468 ARE the two-view fits, and the endzone keypoints of a quarterback inside his pocket are the
ruler's own noise). NEXT candidates: the placement tail (vertical offsets of 20-26 px in the endzone film for the
quarterback, Raven 15, #32, #76 -- height/leg bend more than depth), Madubuike's zig-zag limbs, the late pile.

## 2026-09-25 13:45 -- v116 = CURRENT BEST (viewer Version 31); surges: two placement fixes measured; the gait stays; v117 identity fixes on the copy

**v116 rendered and film-checked** (swallowed 05r): Madubuike drawn lunging low into #65 through 444-486 on the hi-fi
render (review_v116/strips/render_4_f444.png), as on the endzone film. 07l = v115's. Viewer Version 31.

**Surges (the new ruler, $S/surge_ruler.py) -- mechanisms and two fixes, runtime patches, measured on v116's tables:**
- rate by placing source: two-view 7 %, sideline-only 24 %, endzone-only 33 %. The depth snap is not the cause (off /
  own-id off / carrying its correction: 779 / 850 / 728 vs 769 on the timeline dump).
- along-ray smoothing ($S/patch_xy_aniso.py; XY_ALONG 9 reproduces the shipped smoother to 6e-14 m): 31 frames
  along the sideline ray, 9 across -> surges 396 -> 116, steps full 36 -> 20 / live 2 -> 0, census live 0.13 -> 0.04,
  planted 14 -> 37 %, joint jitter p99 0.169 -> 0.160; endzone film joint p99 113 -> 81 px, over 40 px 8.0 -> 7.3 %;
  sideline film flat; pre-snap flat.
- FEET anchoring ($S/patch_feet_anchor2.py): placed_body puts the pelvis over a feet-measured point; states placed
  from feet points (not the refit's pelvis, 25 % of states) move by the posed pelvis - ankle offset (+-7-frame mean,
  weighted by the feet share): endzone offset p50/p90/p99 9.6/31.4/108 -> 8.8/26.1/90, Madubuike 49 -> 23 px mean;
  sideline tail slightly worse (Thuney). Moving every state (variant 1) hurt the QB / LT: refit points are pelvis-exact.
- COMBINED (31 box + feet v2): surges 396 -> 127, steps 36 -> 20 / 2 -> 0, census 0.13 -> 0.04, endzone joints over
  40 px 8.0 -> 5.0 %, p99 113 -> 87; sideline over 20 px 9.3 -> 10.3 %. Savitzky-Golay along the ray (31, 45) running.
  Repo change staged as $S/patch_repo_v117.py (timeline.smooth_xy along_window/centre, play_timeline.anchor_feet);
  applied only when no render/refit process imports those modules.

**The gait vs the lock on the fitted legs (gait never fires, lock at every speed): the gait STAYS.** The keypoint
ruler preferred the fitted legs (id 9 sideline legs 17.5 -> 9.3 px) but the sideline-view renders beside the footage
($S/fvr_id9_big.png) show the fitted sprinter crouched with his legs under him where the film has long strides; the
gait draws the strides. Id 3 mixed. A keypoint ruler on a small blurred sprinter is not the film.

**Identity: short excursions ($S/foreign_rows.py) -- v117 on the copy.** The quarterback's sideline id on the
centre's track 54 at 548-549 / 557 / 568-569: the refit fitted the centre's box, AGREED with the wrong box (passes the
1 m shift gate) and place_from_refit interpolated 537-547 toward it -- the QB walked 1.3 m along the field (sideline
film -54 px at 542). The centre on 84's track at 474 (a duplicate box). The left tackle's endzone id alternating
between his own box (track 25) and track 37, which drifted onto the Raven he blocks (a twin of Raven 15's own box,
IoU 0.96 at 540) -- the scan's suggestion (drop track 25) was WRONG, the film said drop track 37. Tools fixed
(79204b6, 41a1852): 08z / 08za relabel keypoints_2d_ft2.parquet too (every port had patched it by hand), 08za
--track-id and runs 08v, 08v drops records whose row was dropped or whose row moved to an id posed there already
(the QB kept the centre's record otherwise), swaps trade. Copy: fold + two drops applied, refit running.

## 2026-09-25 14:50 -- PAUSED (power-off). Placement change committed (5ba0160, default ON); live tables = v116; v117 identity fixes on the copy NOT ported

**State.** Live play_001 = v116 tables + cache (poses_refit.json = the swallowed 05r cache; .v115 backup). The repo
now smooths placement along the sideline ray (timeline.XY_ALONG_WINDOW 31) and anchors feet-point bodies by their feet
(play_timeline.FEET_ANCHOR) -- ON by default, so the next render of the live tables IS "v117a" (= the measured combined
arm: surges 396 -> 127, census 0.13 -> 0.04, steps 36/2 -> 20/0, endzone joints over 40 px 8.0 -> 5.0 %; sideline over
20 px 9.3 -> 10.3 %). Not yet rendered or film-checked as a version: NEXT = render v117a (chain scripts: sed v116 -> v117a
in $S/export_v116.sh / chain_v116.sh / launch_v116.sh), review strips, viewer + write-up.
Repo code and live data agree otherwise; full suite 1377 passed, 8 skipped.

**The copy (play_copy) = v117 identity fixes + refit** ($S/v117_copy.sh; 08v cleanup applied by hand before the merge):
QB sideline rows on the centre's track 54 folded into the centre; the centre's duplicate row at 474 dropped; the LT's
endzone track-37 rows at clip 526-558 (the Raven twin) dropped. With the new code on both sides (live+code vs copy+code):
QB surges 15 -> 2, joint jitter p99 0.162 -> 0.155; BUT census live 0.04 -> 0.12, the LT's endzone offset 12.4 -> 14.4
px, and the centre vanishes at 475-477: with the true last sideline point (473) his hole chain (474-546, a 72-frame
sideline hole) starts elsewhere and his endzone-placed points sit 0.3 m from Thuney's (also endzone-placed) -> dedupe
drops him. NOT ported. NEXT for the copy: a per-man bias correction in sideline holes -- shift the man's endzone points
by his own endzone-minus-sideline offset measured at the hole's two ends (interpolated), instead of the frame-wide
common mode (the plain x-hold was rejected twice because it freezes sprinters). The centre's endzone offset is 34 px mean
in BOTH versions: his whole hole is misplaced.

**Late pile (logged, not fixed).** Sideline track 45 carries id 1 at 485-527 and id 4 (Madubuike) at 528-631 -- one
tracker track, two ids; at 572-596 two white bodies (1 and 4) are drawn beside KC #74 where the endzone film shows ONE
Raven (#90), and a Raven getting up between #65 and #74 (likely #92) has no body. Settle who track 45 is on the ENDZONE
film (jerseys) before folding; per-camera folds only.

**Also measured and closed this session:** VPoser shift (rejected, every limb joint worse); the gait vs a lock on fitted
legs (the gait stays: film shows the fitted sprinter crouched); a backpedal gate on the lock (21 of 38 stances dropped,
QB unchanged, marginal: not adopted); Savitzky-Golay along the ray (worse: steps at run edges).

## 2026-09-25 22:35 -- deadline push (user: a good product in ~9 h): v117b rendering; kits from the film; sky staged

**v117a** (live v116 tables + 5ba0160's placement code) rendered and strip-checked (review_v117a): Madubuike's lunge as
v116, the ball flight and catch right. Rulers = the measured combined arm.
**v117b** = v117a + the quarterback fold (port_v117b.sh: sideline track 54 under 80 at 548-569 -> 204; tables and caches
byte-identical to play_copy2 where it was measured: QB drift 1.2 m gone, sideline offset 6.0 -> 4.5 px, surges 15 -> 2,
07l identical) + the film's kits (fd99517: BAL white pants/socks, KC white cleats). 07l: steps 20 / 0, hops 0, census
live 0.04, planted 36 %; 09d jerk 2 (R arm), trunk 12 (Madubuike's real lunge). Viewer Version 32 (kits by region,
3f5f43a). Hi-fi render running (setup is slower now: anchor_feet's SMPL-X pass over every state).

**Measured and rejected tonight:** a per-man hole bias along the endzone ray ($S/patch_hole_bias.py: +-0.1 px, the
centre slightly worse); the depth snap refusing endzone points of sideline-tracked men missed on that frame
($S/patch_snap_notaken.py: census 0.04 -> 0.10 -- with Madubuike no longer snapped onto Ojabo's point, 12 Ravens at
575-586, so sideline track 45 late in the play may BE Ojabo); span_gap 45/60 (identical arms: Thuney's 595 cut is not the
beyond-span rule; his track ends by another rule, 0 frames of his 190 dropped there).
The centre's 35 px endzone offset is mostly the ruler: his endzone box is merged with the Raven he blocks and then
with Mahomes passing in front; on the film the drawn body is on #52.

**Staged:** render/sky.py (+ tests) -- a night-stadium backdrop split at the camera's own horizon; 05k --sky
($S/patch_repo_sky.py) to apply once no 05k process starts; then the v118 hi-fi = v117b + --sky.
**Write-up:** Version 19 drafted ($S/patch_doc_v19.py applied to the scratch page), publishes after v117b's film check.

## 2026-09-25 23:35 -- v117b = CURRENT BEST (film-checked); stadium backdrop in (05k --sky, viewer); v118 = v117b + sky rendering

**v117b film check:** sideline blend 536-552 -- in v116 the quarterback's body trails ~1 m to the left of Mahomes on the
footage, in v117b it sits on him. Kits on the run sheet match the film (Ravens all white). Write-up Version 19, viewer
Version 33 (kits by region + a stadium bowl under a night sky; checked once in Chrome).

**The stadium (render.sky, e8a1c82 / c66ea3c):** the black band over the far sideline was GROUND beyond the field
texture (the follow camera looks down; its horizon is above the frame), so a sky gradient did nothing. backdrop(K, R, t)
intersects each pixel's ray with the ground: turf within 7 m of the lines, a wall, then stands with a crowd hashed
per 0.55 m ground cell (fixed on the ground, no flicker) in red/white, fading; sky only for rays that point up.

**The late pile, measured again (not fixed):**
- Thuney's vanish at 601: timeline.MAX_GAP_FRAMES (30) is also the window in which a body is "anchored" against the
  duplicate rule; his sideline track ends at 565, so from 595 his endzone-placed body in the pile is deduped (a teammate
  within 0.9 m) and the hold ends at 601. MAX_GAP_FRAMES 45 keeps him (601-613) and #65 (342-344) but draws Raven 1
  beside Madubuike's body at 570-579 and drops him at 587-590: census 0.04 -> 0.08 (KC exactly 11.0, BAL 11.01 ->
  11.04). 60 adds a pre-snap KC ghost (164 at 265-276). Not adopted.
- Folding sideline track 45 (528-631, id 4) into id 1 (Ojabo) -- census 0.04 -> 0.43 (BAL 10.6): track 45 from 528 is
  NOT Ojabo; merging deletes a man. v117b's labels stand; id 4 is drawn on Ojabo's spot because the positional depth
  snap slides Madubuike's sideline ray onto Ojabo's endzone point, and refusing that snap (patch_snap_notaken) drew 12
  Ravens at 575-586 -- one more duplicate somewhere in that pile. Needs a frame-by-frame endzone-jersey pass.

## 2026-09-26 03:30 -- deadline deliverables: v122 published (showcase V5, write-up V20, Film Room V37)

**The product (all private claude.ai artifacts):** Showcase https://claude.ai/artifact/4ZvVyiVwGC99u35gs9P7j3 (Version 5:
the v122 follow camera 1080p, the skycam behind the offense 1080p, the render from the sideline broadcast camera's own
solved pose 720p -- render only, never footage); the Film Room viewer https://claude.ai/artifact/9mq5mktV21UEkAKd9Dq61m
(Version 37: v122 joints + the render's seated crowd in its stands); the write-up https://claude.ai/artifact/8Dz8YFmWYkvvHidyfJL9KM (Version 20). Local videos:
C:/Users/sumedh/diag/play_001_v122_hifi_1080.mp4, play_001_v122_skycam_1080.mp4, play_001_v122_sideline_view_720.mp4
(+ the local-only blend against the footage, play_001_v122_sideline_blend.mp4).

**Tonight, in order (all measured, the film the judge):** the late pile's identities (#98 one id, Thuney on the turf,
a ghost Raven gone; v119); lit bodies (render.shade, --shade); stands that rise with a seated crowd (render.sky bowl);
Madubuike's depth read off the film (film_reads.json + depth_snap.apply_depth_reads; v121); the spare-missed snap on
(Ojabo on #90, the RG drawn pre-snap; v122). Rulers v117b -> v122: census live 0.04 -> 0.00 (every frame snap to whistle
11 v 11), clip frames 11 v 11 373 -> 390 of 401, steps 20/0 and hops 0 unchanged, surges 4.8 % -> 4.3 %.
Rejected tonight: the short-box hidden-feet rule (census 0.16), folding track 69 into Ojabo (606-609 lose a Raven).

**Open, in order of what a viewer would notice:** after the whistle (602-615) the pile's depths are off again --
Madubuike steps round #74 (the endzone film reads "92" beside Ojabo at 612) while the read window ends at 596, #74's own
depth is off, and track 69 (Ojabo back in the sideline view, 606-642) draws a twelfth Raven at 610-615; the RG
flickers out at 342-344 pre-snap; two KC-12 frames at 215-216; poses in piles. The independent review of tonight's
code (render.shade, sky bowl, depth_snap, the loader hook) found no defects; its two notes are fixed in the docstring.

**Artifact video lesson:** videos published as plain files next to the page (the files map) sat on a loading spinner in
the viewer; the documented route is the artifact ASSET store -- declare capabilities {assets: {}}, upload with
asset: true (file_paths), and reference the returned "/_blob/<id>" URLs verbatim (Showcase Version 4-5; the poster
loads that way, the video's playback was not confirmed before the browser extension disconnected). The MP4s are also
remuxed +faststart now (moov first). Showcase V1 (00:06) probably never played its video either.

**Also tonight, outside this thread:** a separate agent built a one-play report from the tracks
(https://claude.ai/artifact/U3ddAQTQgcZzHUUvZGENGo; scripts in $S/play_report/, not in the repo).
