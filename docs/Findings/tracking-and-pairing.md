---
type: findings
topic: tracking-and-pairing
period: 2026-09-07 to 2026-09-26
entries: 18
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Tracking and pairing

Detections, tracks, and which sideline track and endzone track are the same person: pairing, folding two IDs into one, and splitting one ID that holds two people.

18 entries from 2026-09-07 to 2026-09-26, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Tracking](../Concepts/tracking.md), [Identity](../Concepts/identity.md), [Placement](../Concepts/placement.md), [Census](../Concepts/census.md), [Footage review](../Concepts/footage-review.md)

**Decisions:** [0005: Don't merge twin tracks by box geometry](../Decisions/0005-dont-merge-twin-tracks-by-box-geometry.md), [0006: Don't pair cameras by the regressor's body pose](../Decisions/0006-regressor-pose-is-not-a-pairing-cue.md)

## One avatar per sideline track; the pairing stays ambiguous (2026-09-07)

Play 1 with the footage-driven endzone track written (`cameras.npz`, old
track in `cameras_endzone_interp.npz`) and re-linked three ways on the same
cameras (`diag/p1_frame`, `p1_track`, `p1_track25`):

| link | ids | in both cams | cross-kit | paired / frame | one-view / frame |
|---|---|---|---|---|---|
| old cameras, per frame | 106 | 62 | 24 % | 15 | 14 |
| new cameras, per frame + kit gate | 176 | 84 | 23 (27 %) | 13 | 17 |
| new cameras, track pairing 2.5 m | 147 | 29 | 8 (28 %) | 9 | 23 |
| new cameras, track pairing 1.0 m | 166 | 17 | 6 (35 %) | 5 | 31 |

The better endzone track did not make pairing decisive: box bottoms give
about 1 m of depth error per camera and players stand 1-2 m apart, so a
third to a half of the players stay unpaired in each camera and the
cross-kit share of the pairs made is unchanged. The kit gate only bites
where both boxes carry a label (63 %), and the position-only linker joins
across kits over time. What the numbers do say: the timeline was drawing
both copies of every unpaired player -- 37 ids a frame, 18 endzone-only,
each a ghost at the endzone's poor x. `render/endzone_only_rule.py`: an id
the endzone alone sees, never two-view, is left out (same shape as the
edge rule); one avatar per sideline track, the endzone kept for
triangulation where it pairs. Play 1 v9 runs on the per-frame kit-gated
link with the new cameras: rulers are triangulated joints passing (v8:
42 %) and avatars per frame (v8: about 29 for 29 people plus ghosts).

Next for pairing: appearance at track level -- the jersey number read in
both cameras must agree and the kit must match -- before position decides;
the OCR runs after the link today (08c), so the order changes.

## v21: a wrong pair sawtoothed by a metre a frame (2026-09-08)

Ruler: second differences of the timeline's state xy per frame.
Box-placed ids p90 18 mm (smooth_xy does its job); record-placed ids p90
27 mm but p99 1365 mm -- 250 of the 253 triples over 0.5 m belong to id 9.
Id 9 is a WRONG PAIR: the sideline track runs 28 m along y (a receiver),
the endzone track stands still; the two cameras' ground points sit 14 m
apart at the median. The pairing accepted it as a number match because
its offset statistic is the mean difference vector over the overlap,
which averages out when tracks cross (mean 2 m, per-frame up to 15 m);
the fused refit then triangulated two different people, the timeline
averaged the two cameras' points (7 m from either), refused the refit's
placement against that average, and interpolated between refused
records at the odd frames: a 1 m sawtooth every frame, and the avatar
named Noah Gray (#83 read on the endzone track). 27 two-camera ids: median
distance p50 1.04 m; 4 over 2 m, 2 over 3 m (ids 9 at 14.2, 37 at 4.2).
Now: `pair_by_appearance` gates on the median per-frame distance
(MAX_MEDIAN_DIST_M 4.0; the test has crossing tracks with a shared
number); `render.pair_rule.mispaired_ids` guards a play-dir paired before
the gate (the timeline drops the id's endzone rows and says so);
`place_from_refit` interpolates only between records it accepted. Play 1:
ids 9 and 37 dropped from the fused cache and refit one-view (05p; the
fused cache rebuilt by 05f under numpy 1 first -- a copy written from the
numpy-2 venv does not load in the smplx venv). Result: the timeline's xy
second differences for record-placed ids p99 1365 -> 115 mm, one triple
over 0.5 m instead of 253; the merged cache's jitter p99 260 -> 213 mm,
hands/feet p90 103 -> 94 (the wrong pair's triangulated poses were among
the worst). v21 = v20 + this (10:58, `diag/play_001_v21_hifi_720.mp4`,
sent to the user; stills against v20 in `diag/p1_v20_v21_strip.jpg`: id 9,
the receiver, now stands where the sideline sees it; the rest identical).
**v21 is the deliverable and the pipeline's reproducible baseline** --
every rule above is in the script. PROVEN by v22 (11:00-18:04 with a
power-off in between; `scripts/pipeline_play.sh` resumed at the render):
the script from the link stage with all of today's rules -- per-camera
link, OCR 33 of 151 ids, 27 pairs with the median gate (25 two-camera ids,
0 cross-kit, 9 paired a frame), identity 21 named with the same three
demotions and the kicker vetoed, 22 players triangulated at 66 % / 8.4 px,
damped refit 0.096 m, 3609 one-view records at 3.5 px, 23 bodies a frame,
4 default-posed. `diag/play_001_v22_hifi_720.mp4`; stills against v21 in
`diag/p1_v21_v22_strip.jpg` are the same formation. **v22 is the
baseline** (v21 was assembled on v14's caches; v22 is the script).

## The cameras' ankle RAYS, not their ground points, say whether a pair is right (2026-09-10)

Chasing the motion man's arms at 262-270 produced a false lead worth keeping.
The two cameras' ankle ground points (each camera's ankle ray taken to z = 0.08)
disagree by 1.11 m in x for him where every other player's agree to 0.20 m, which
looks like a mis-pair. They are not: the two rays miss each other by 0.15 m. The
sideline camera is nearly horizontal, so a ray that passes within a hand's width
of the truth lands a metre away on the turf, and the ground-point difference is
mostly the z assumption. The ray miss is the honest test: 3189 of play 1's frames
have confident ankles in both cameras, they miss by 0.15 m at the median, and 1 %
by more than 0.6 m. `05p --two-view-max-miss` (default 0.6 m) leaves those frames
to the one-view pass.

What the arms actually are: at 262-272 the temporal keypoint filter throws out
his left elbow and wrist (the crowd), so no camera constrains that limb and only
the L2 pose prior holds it. `Mono2DConfig.unseen_temporal_mult` holds an unseen
limb at the pose it had instead. MEASURED at 6 (ids 9 and 12): the runner's arm
speed p90 in his own frame went 10.8 -> 11.7 m/s and the footage strip is
unchanged. It does not help: the limb is unseen for two or three frames at a
time, so holding it only delays the snap back, and the pose it is held at came
from the frame the detector had already lost. OFF by default. If this is picked
up again, the thing to hold an occluded limb with is a real pose prior (a
learned one, or the player's own pose distribution over the play), not the
previous frame.

## Two ids on one body: the feet tell, the boxes do not (2026-09-10)

The render stood two avatars on one man in play 1's trenches. The sideline
tracker held the left tackle as ids 18 and 19 for 139 frames and the quarterback
as 16 and 22 for 58, which shows structurally too: six interior linemen on a
five-man line, two quarterbacks under centre.

Box geometry cannot find them. From the sideline the line of scrimmage is seen
end-on, so two men standing a metre apart in depth overlap in the image exactly
as a duplicate does: ids 14 and 27 (two Baltimore players, one behind the other
in the footage) sit 0.19 box heights apart with IoU 0.66 and any box rule flags
them. The ankle keypoints' rays taken to the turf resolve depth and separate the
two cases cleanly -- over play 1's same-team sideline pairs the duplicates sit
0.03 and 0.11 m apart and the next pair 0.80 m. Each id's ankle track is filled
across gaps of up to 4 frames first: the pose detector suppresses one of two
overlapping boxes, so a twin pair carries ankles on the same frame only 3 times
in 58, and the raw test (both ankles, same frame) read 18 & 19 as 1.30 m apart
off those three frames alone.

`tracking.twins` + `scripts/08o_merge_twins.py`: same team, no disagreeing
jersey numbers, feet within 0.20 m, boxes overlapping 0.3 IoU, 20+ frames
judged. 0.35 m was the first threshold and it folded the endzone's quarterback
into the lineman beside him (0.29 m at the feet, two men in the footage) --
that is the calibration of this rule. The merge is per BODY, not per camera:
ids are global, so a merge found in one camera moves the other camera's rows too
(the first cut folded endzone 113 into 22 while the sideline folded 22 into 16,
splitting one person's two views). Where the merge leaves two boxes of one
camera on a frame, the less confident is dropped, so the merged id holds one box
per frame. The stage runs between the repair and the roles, under numpy 1, and
08c --from-cache follows it.

## v34: the gap fill lands, and the count turns out to be fragmentation (2026-09-11)

08q recovered 607 sideline boxes inside gaps in existing tracks, from detections
the 0.35 threshold had rejected, and the keypoints were re-read for them. At the
snap Kansas City goes from 8 drawn bodies to 9 of 11, and 27 players triangulate
from both cameras instead of 25. The overall count error did not move: 2.93 ->
2.95 bodies a frame from the snap.

What that says is where the error really lives. Play 1's eleven Kansas City
players are carried by 32 separate sideline track ids, and Baltimore's by 51. A
player is tracked, lost, and picked up again as a NEW id -- which produces both
halves of the error at once: a hole while nobody holds him, and a surplus where
the old id and the new one overlap. Filling the small holes inside a track cannot
reach either.

By phase of play (bodies drawn, truth 11 and 11):

    at the snap (280-340)   KC 8.8   BAL 11.7
    the run     (340-460)   KC 12.2  BAL 11.8

The next piece is joining fragments into one identity per player. Position-only
stitching is a measured dead end (2026-09-07: it welded a wrong pair for every
right one). What is new since: the kit read from the pose torso, the role and
build per player, depth-corrected positions, and the one-place-at-a-time veto in
the pairing. A stitch gated on those is worth measuring against the census.

## v38: every join trimmed to the frames its rays agree, and it wins on all three rulers (2026-09-12)

08r now emits `frame_from`/`frame_to` -- the longest unbroken run whose ray miss is within
`--max-ray-miss` -- and 08s converts that by the clip offset and relabels only inside it, refusing a
proposal that carries no interval. v38 replays every join from the pre-pair backups rather than trimming
in place: six applied (0<-102, 7<-89, 11<-19, 25<-33, 28<-21, 80<-22), one eviction confined to its
interval (endzone 25 over 385-471 only, 51 track rows). Two-view coverage 25 -> **27 players**.

    05u, 2155 identical body-frames, 27 players    v37        v38
    id 25                                        0.23 m     0.04 m
    id 22                                        0.20       0.01
    every other player                           identical to the centimetre
    pooled |along-ray| p90 / p99              0.06 / 0.83   0.04 / 0.39
    players worse by more than 0.10 m                       0 of 27

    05t, 2299 paired body-frames                   v37        v38
    endzone p50 / p90 / p99               8.5/16.5/135.5   8.4/15.3/60.1
    endzone frames over  20 px              134 ( 5.8 %)    71 ( 3.1 %)
    endzone frames over  30 px               98 ( 4.3 %)    33 ( 1.4 %)
    endzone frames over 100 px               36 ( 1.6 %)    13 ( 0.6 %)
    sideline p50 / p90                        4.2 / 12.1    4.3 / 12.4

    census                                        2.94        2.84   (exactly 11 and 11: 9 -> 10)

The trim hits exactly what it was aimed at -- the tail. id 25's endzone p90 of 483 px is gone, and the
pooled p99 halves on both rulers while the sideline stays flat and no player regresses.

**And one result nobody proposed: id 22 improved from 0.20 m to 0.01 m without being a candidate.**
Endzone track 22 was relabelled onto sideline 80 only over frames 363-511; outside that window it keeps
its own id, and sideline 22 holds it there at 0.01 m. That single endzone track was covering **two
different men at different times**, and splitting it by interval gave each his own -- a failure whole-track
joining cannot even express, let alone repair.

**Scanned for more of them, and there are none.** Asking which sideline id wins each 60-frame block of
every endzone track flagged **19 of 25** -- which is not a finding, it is the same mistake as the
per-frame ray test, made again: no margin requirement, on a measurement where a neighbour at ~100 m
misses almost as little as the right man (10 confident joins out of 137 per-frame tests). Requiring the
block winner to beat its runner-up by 0.15 m and each claimant to hold two or more blocks leaves **1 of
19**, and that one does not survive inspection either: endzone 74 is claimed by sideline 74 over frames
440-559 at 0.08 m rays / 0.67 m turf, which is simply its own correct pairing, and by sideline 3 over
140-379 at 0.17 m rays but **1.42 m turf**, failing the 1.0 m cap outright. So the id 22 case was the
only real one, the interval trim already repaired it, and no further machinery is warranted.

**id 17, the worst remaining player (0.24 m along, 0.13 m across), is not a pairing problem either.**
Searched against every endzone track: the one in use is the best on both rulers (0.18 m rays, 0.71 m
turf), and every alternative is worse (0.25/0.70, 0.30/1.27, 0.80/1.93, 0.83/2.80, 1.19/6.11). A clean
negative -- stop looking for a partner there.

**So placement is done to diminishing returns and the census is the binding problem.** At pooled
|along-ray| p90 0.04 m and endzone p99 60 px, the remaining error is the body count at 2.84 a frame. The
measured cause at the snap is 21 ids for 22 players, KC 9 and BAL 12, because the sideline views the line
end-on and merges the offensive line into one mass -- while the endzone sees those men individually and
`endzone_only_ids` discards them as ghosts. The targeted fix looked like keeping an endzone-only id when NO
sideline body stands within ~1.5 m of it (2-4 such ids a frame, measured), which is the same "is the
sideline drawing that man" test `beyond_sideline_span` already carries.

**Measured before building it, and it is dead.** Counting endzone bodies with no sideline body within
1.5 m, by phase:

    snap (300-340)       3.5 a frame     KC 0.2     BAL 3.4
    run  (340-460)       3.0             KC 0.3     BAL 2.8
    after the whistle    5.0             KC 2.1     BAL 3.0
    late (560-660)      16.3             KC 9.9     BAL 6.4

At the snap they are almost entirely Baltimore and essentially **zero Kansas City** -- and KC is the team
short by two, while BAL is already over at twelve. The rule would add bodies to the wrong team. The ids
most often "alone" are 85 and 87 at 510 frames each, which are the officials the behind-the-offence rule
already excludes, plus 88 and 106 from the same list.

The reason is structural: **in a pile every occluded man has a sideline body within 1.5 m by
construction -- his neighbour.** So "no sideline body nearby" cannot tell a man the sideline merged into
his neighbour from a man it already draws, which was the entire point. Recovering the line needs the
endzone bodies admitted with a correct identity, and that is the pairing problem again -- which needs
both cameras to see the ankles, exactly what a pile denies. Do not re-propose a proximity test here.

**But the deficit IS recoverable, and I nearly concluded otherwise on a bad number.** In the line box
(|x - LOS| <= 3 m, |y| <= 8 m) the endzone resolves **9-11 Kansas City ground points** on every sampled
frame from 290 to 360, against the sideline's 7-8 and the 6-7 the render actually draws. Pooling the two
cameras' points at 0.6 m then gave KC **12-13 places**, which is more men than can be in that box, and I
read that as the endzone over-segmenting the pile -- which would have killed the whole line of attack.
It is a clustering artifact: a man whose sideline and endzone points sit more than 0.6 m apart is
counted twice by the pooling, so the pooled figure inflates and means nothing here.

The film settles it. Marking the endzone's line-box ground points on frame 285 (= sideline 300) gives
**10 markers and exactly 10 distinct red-jerseyed men** -- 87, 76, 62, 15, 65, 7, 83, 12, 10 and one
half-hidden behind 87 -- each marker at a different man's feet, none stacked on one body. The endzone
genuinely resolves the men the sideline merges into a mass.

So the route is admission by **region and count, not identity**: inside the line box, where the endzone
resolves more distinct places than the sideline, the surplus are real men. That needs no pairing, which
is what the pile denies. The risk is drawing a body at the wrong depth, so it must be scored on 05t and
05u as well as the census. That was the next build, and it is dead too -- measured before writing it.

The candidates do not separate from the duplicates by distance. Splitting every Kansas City endzone body
in the line box by whether the sideline tracks that id **anywhere** (so the sideline can see him: a
re-count) or **never** (so it cannot: plausibly a man it merged), and measuring how far each sits from
the nearest sideline KC body:

    the sideline DOES track this id elsewhere (a re-count)   1150 body-frames   p50 1.16 m
    the sideline NEVER tracks this id (plausibly unseen)      579 body-frames   p50 1.17 m

    threshold   admits unseen   admits re-counts   purity
      0.6 m          436              873           33 %
      1.0            301              654           32 %
      1.2            287              531           35 %
      1.5            216              149           59 %
      2.0             82              101           45 %

Identical medians, and no threshold reaches even 60 % purity; the 1.5 m bump sits between 35 % and 45 %,
so it is a wiggle in a noisy curve, not a boundary. Tuning to it would be fitting noise.

The film had already shown why, on the snap frame: of the four candidates there, id 37 sits at lineman
76's feet with the sideline's own point 0.68 m away and id 22 sits on the back 10 with sideline points
beneath it -- both re-counts -- while id 38 and id 74 stand on men carrying no sideline point at all. Two
real and two duplicates, at 1.38/1.49 m and 0.68/1.06 m, ranges that overlap the moment cross-camera
disagreement is included. **A man the sideline merged into his neighbour and a man it already draws sit
the same distance from that neighbour.** Proximity cannot tell them apart, in the line box or anywhere
else.

So the census route through geometry is closed: admitting the line needs identity for those bodies, and
the pile is exactly what denies identity (both cameras must see the ankles). The remaining honest
options are a detector that separates overlapping bodies in the sideline view, or accepting that the
snap deficit is not recoverable from this footage.

**Jersey identity cannot admit them either.** The obvious next door: the endzone plainly shows the
linemen's numbers, the OCR reads them confidently (id 86 reads 62 on 250 frames, id 97 reads 82 on 215,
id 38 reads 55 on 326), so a body with a number is a man whether or not the ankle rays can pair him.
Dead, because `player_uid` is **not unique per man**: seven uids are claimed by two or three different ids
(`2024_T1_7` by ids 22, 76 and 80; `2024_T1_62` by 33, 139 and 140; `2024_T1_52` by 17 and 104), three
ids carry more than one uid (id 25 reads 76 on 112 frames, 62 on 87, 5 on 9), and the totals are 16 and
16 against a truth of 11 and 11. Admitting a body because it carries a number would draw the same man two
or three times -- the ghost problem in a new costume.

**Two corrections to myself, both from reading rather than assuming.** I reported the line-box candidates
as having "no identity" because `PlayerIdentity.name` was None: that attribute does not exist on the
object at all (`cameras, corroborated, height_m, jersey, player, team, total_votes, tracks, votes,
weight_lb`), and the identities are populated -- the sample resolves to jersey 21, BAL, "Brandon
Stephens". And I reported that `pipeline_play.sh` would reproduce roughly v34 because it runs 05p without
`--two-view`: it does not, line 59 sets `--two-view --endzone-weight $EZW` unless `ONE_VIEW=1`, and
`TWO_VIEW_PX_MAX = 40` is already the committed default inside 05p. The real gap was narrower -- 08r/08s
were not pipeline stages, so a fresh play got v38's fitting but not its pairing. Now wired in as `pair`,
between `twins` and `roles`, because 08s rewrites the tables that roles/tri/refit all read.

**The single worst body-frame in the play is id 17 at frames 458-460**, 4.49 m along the ray -- and the
two cameras' ankle rays there miss by **2.34 m**, so the triangulated "truth" is itself wrong. It is a
mis-paired window, not a misplaced body, and it accounts for id 17's 0.13 m across-ray component, the
last named placement defect. A candidate for the same interval trim.

**So 05u was scoring bodies against a truth it had never checked, and the fix moves the headline.** The
ruler now drops any frame whose two cameras' ankle rays miss by more than 0.6 m -- the same bound the
two-view fit uses to call a frame mis-paired -- because a crossing point the cameras disagree about is
not a truth to score against. On play 1 that is **15 body-frames of 2161**, and the effect is entirely
in the tail:

    pooled |along-ray|        v37 before -> after     v38 before -> after
    p99                        0.83 -> 0.70 m          0.39 -> 0.36 m
    max                        4.49 -> 1.50            4.49 -> 0.62

Every player's median is unchanged and it is still 0 of 27 worse, which is the signature of removing
noise rather than data. **The worst body-frame in play 1 is 0.62 m, not 4.49 m** -- the figure quoted in
the v36, v37 and v38 entries above was the mis-paired id 17 window being scored as placement error.

The general lesson, which cost three entries' worth of inflated maxima: a ruler that scores against a
triangulated point must validate the triangulation first. The same discipline as the cross-view ruler
itself -- measure with an instrument whose own error you have bounded.

## v37: two re-pairings, and the census finally moves (2026-09-12)

`08s --give-up-incumbent` applied the two the gate passed, evicting each sitting endzone track to a
**fresh unused id rather than deleting it** (endzone 7 -> id 145, endzone 25 -> id 146; 648 track rows and
10676 keypoint rows moved). sideline 7 went from 95 to 467 endzone frames, sideline 25 from 172 to 181.

    05u, 2093 identical body-frames, 25 players    v36        v37
    id 25                                        0.69 m     0.02 m
    id  7                                        0.23       0.00
    every other player                           identical to the centimetre
    pooled |along-ray| p90                       0.22       0.05
    players worse by more than 0.10 m                       0 of 25

    05t per player (the same keypoints)      sideline p50/p90     endzone p50/p90
    id 7  v36                                    1.8 /  2.3        27.1 /  38.6
    id 7  v37                                    5.0 /  7.3         6.3 /   7.9
    id 25 v36                                   17.0 / 32.3        98.4 / 386.2
    id 25 v37                                    8.9 / 13.2        15.5 / 483.4

id 7 is the textbook case: near-perfect in the camera it was fitted to and 27 px in the other -- the
blind-camera signature -- replaced by 5-6 px in **both**, which is what a correct pairing looks like.

**The census moved for the first time this session: 3.02 -> 2.94 bodies a frame, and frames exactly
eleven-and-eleven 3 -> 9 of 361.** The mechanism is in the log rather than inferred: "frames beyond an
id's sideline span left out" fell **2110 -> 1412**, because a relabelled endzone track now sits under an
id with a long sideline span instead of being cut as out-of-span. Correct pairing buys population, not
just placement.

**The residual, named.** id 25 keeps the tail: its endzone p50 improves six-fold but p90 goes 386 -> 483
px, and it owns the pooled p99 rise (313.7 -> 388.5) while the metres stay flat (p99 1.01 -> 1.03, max
4.49 unchanged). That is time-localisation inside the new pairing -- right for most frames, badly wrong
on a minority -- and endzone 33 spans 378-562 against sideline 25's 381-634. The join should be per
interval, exactly as the earlier finding said.

**And time-localisation turns out NOT to be general, which makes that job small.** Scanning every
pairing's ray miss per 60-frame block (16 ids with 40+ paired ankle frames):

    id  frames  overall p50   best block   worst block   spread   over 0.6 m
    25      46        0.17         0.11          1.90     1.79       37 %     <- re-paired in v37
     7     184        0.08         0.03          1.54     1.51        7 %     <- re-paired in v37
    the other 14      0.04-0.19       --            --    0.02-0.10   0-2 %

Only **2 of 16** vary by more than 0.25 m between blocks, and they are precisely the two tracks v37
re-paired by eviction. Every long-standing pairing is flat. So the fix is not general interval support
in 08r/08s: it is trimming a newly applied relabel to the span where its rays actually agree, which is
a much smaller change than the earlier finding implied. The mechanism is plain enough -- an evicted
incumbent's replacement is chosen on the frames where both ids have confident ankles, and applied to the
whole span, so the edges of that span are where it goes wrong.

## v36: the four pairings applied, and they pay in metres (2026-09-12)

08s relabels an endzone track onto its real sideline owner -- it never unions the ids, because an id
spans both cameras and unioning 11 with 19 would sweep in sideline 19, a different man present on 370 of
the same frames. Applied to play 1's four accepted proposals: **1453 track rows and 22457 keypoint rows**
moved, three ids that had no second view now have one, and 05p refitted (two-view coverage 24 -> 25
players, 1793 -> 2047 frames, 1851 anchored on the triangulated ankles).

    05u, the same 1900 body-frames on 24 players     v35        v36
    id 80                                          0.26 m     0.02 m
    id  0                                          0.23       0.02
    id 11                                          0.12       0.01
    id 28                                          0.07       0.01
    every other player                             identical to the centimetre
    pooled |along-ray| p90 / p99                0.21 / 0.65   0.05 / 0.41
    players worse by more than 0.10 m                         0 of 24

    05t, the same 2061 paired body-frames            v35        v36
    endzone p50 / p90 / p99                    9.7/45.8/163.5  8.7/15.5/80.5
    endzone frames over 20 px                   478 (23.2 %)   78 ( 3.8 %)
    endzone frames over 30 px                   371 (18.0 %)   41 ( 2.0 %)
    sideline p50 / p90                            3.4 / 12.7   4.0 / 12.5

**Read the v35 column carefully.** It is v35's BODIES scored against the CORRECTED pairing, which is why
its endzone numbers are worse here than when v35 was scored against its own wrong pairing (p90 16.7
then, 45.8 now). Both columns share one truth, which is the only fair comparison, but it means the
headline 45.8 -> 15.5 partly measures the pairing fix rather than the fit. The metres are the cleaner
statement: four players improve by 0.06-0.24 m and nobody moves the wrong way.

**The census did not move: 3.02 bodies a frame, 3 frames of 361 exactly eleven and eleven.** Placement
and population are independent axes and this was a placement change. Also worth noting what the ruler
cannot show: id 19, v35's worst body, had a wrong endzone partner (the two cameras' own ground points
for "him" 1.31 m apart); relabelling that track onto its real owner leaves him one-view and therefore
absent from 05u's table rather than visibly better. Removing a wrong pairing is right, but count the
players in each column before reading the percentiles.

Still held back: **`7 <- 89` at 0.08 m over 184 frames**, the strongest pairing evidence in the play,
because taking it means giving up endzone 7 -- whose pairing with sideline 7 has *zero* frames with
confident ankles in both cameras. It needs `--allow-repairing` and a deliberate decision.

## 2026-09-20 (00:30): the KC 12th man on the right of the line -- three ids on two men, folded on the film (v86)

**The ruler, made honest first.** timeline.vanishings counted every frame after a track's end with no same-team body
within 0.6 m of the last spot; most were re-identifications (6 -> 78, 15 -> 168, 9 -> 77 overlapping 4 frames,
198 -> 206 placed 1.5-2 m apart by the two cameras). A same-team id born within 5 frames of the end whose first body
stands within 2.0 m of the last spot is now a succession (VANISH_SUCCESSOR_REACH / _M): end frames on v85 667 -> 301.
The worst list now leads with BAL 1 (walks off, nobody takes over), 40 (goes on as the OLD id 198 -- no birth test sees
it) and the centre's 166 after 568 (real). Commit bcb5f43.

**KC over 11 on 75 of the 213 play frames (v85).** On those frames the closest same-team pairs are 49/76 (0.1-0.5 m),
38/76, 38/49, 12/49, 205/211, 157/211. The film (`diag/pocket/sl_right_cluster.png`, `sl_38_early.png`): jersey 65
(Trey Smith, RG) is drawn as 38 (375-479 on the sideline, 125-471 on the endzone), then 76 (480-647) AND 49 (551-563);
jersey 74 (the right tackle) is 12 (505-577) and then 49 (569-620, box IoU 0.69 with 12's). So 49 is a third id
hopping between two men, and 38 is 76's earlier name.
- The sideline box-twin gate (BOX_TWIN_IOU 0.6 -> 0.45 / 0.35, probe_boxtwin_ab2.py): never touches 49 (its overlap
  with 76 hovers at 0.34-0.40 while 76 is absent 563-575, so no run of 8), and at 0.35 it starts eating engaged
  neighbours (139 at 475-485, 84 at 577-587): census 1.009 -> 0.986, 49 untouched. Rejected.
- Folds on the film's say-so (08z; backups .pre_fold.14/15/16): 38 and 49 into 76 on 480-563, 49 into 12 on 564-620,
  then all of 38 into 76 (its 375-479 sideline rows are jersey 65 too -- the first partial fold left 38 ending at 486
  and the ruler read a 121-frame false vanishing). Result on the play window: census 1.009 -> 0.887, steps 5, hops 0,
  vanish holes 5/87 -> 4/82, end frames 301 unchanged; 76 drawn 395-637, 12 395-620, 49 only after the play.
  08v carried 50 fused and 17 sideline posed frames to 76. v86 chain launched; film check of the right side next.

**The Raven on the right side of the line: one man under three ids (01:15).** Jersey crops (`diag/pocket/jersey_1_40_198_206.png`)
and the box strip after BAL 1's last box (`sl_1_after.png`): the Raven engaged with jerseys 74/65 from ~445 is id 40, then
198 from 483 (two boxes on him 483-484, 40 going on by endzone rows alone to 526) and 206 from 555/571 -- one man. A
RETRACTION of my first reading: he is NOT BAL 1 re-identified; 1 is another Raven (blocked by Noah Gray at the line at
412-420) who is genuinely unboxed after 434 -- a real vanishing still open. Folds on the film's say-so (backups .pre_fold.17/18):
198 into 40 on 483-660, 206 into 40 on 555-660. 40 drawn 414-592 as one id; steps 5, hops 0; vanish end frames 301 -> 256
(the false ends of 40/198/206 gone); census 0.887 -> 0.948 -- the 483-526 ghost (40 by the endzone plus 198 by the sideline,
two bodies on one man) leaves, and with BAL 1 still missing the count drops to 10 there: the census cannot judge a ghost's
removal while a real man is missing, the film can. v86 chain relaunched on these tables (the first launch was stopped at
its first stage to fold first, so the render and the blends share one state).

**v86 rendered and film-checked (01:50 machine clock): `diag/play_001_v86_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` /
`_endzone_blend`. CURRENT BEST.** 07l on 395-607: steps 5, hops 0, census 0.95 (KC 11.25 / BAL 10.85; v85 1.01 with KC 11.37).
Film vs render on the right of the line (`diag/pocket/right_v86_check.png`, 440-590): jerseys 65 and 74 and the Raven on them
drawn as one body each at every checked frame, no double on 65 (the 49/76 twin) and one Raven (40) through 592. Tables
snapshotted as `*.v86` (tracks, keypoints, identity, poses_refit, poses_sideline). Lead for BAL 1 (unboxed after 434): the
wide strip `diag/pocket/sl_1_wide.png` shows a fragment id 153 near him at 434 and 460 -- one of the short fragments the rider
rule drops as riding another body (Noah Gray's, who blocks him); if 153's boxes are his, a fold 153 -> 1 draws him on.

**BAL 1's lead is dead (02:05).** Fragment 153 is six sideline boxes (433-434, 457-460) on team T1 with an unreadable kit, not
the Raven; BAL 1 has no box in either camera after 434 (endzone 376-384 only). A detection hole -- the sideline detector
losing a man Noah Gray blocks, then nothing on him for 173 frames -- open item (1). Pose rulers v81 -> v86 (07l, live):
root jitter p90 0.0261 -> 0.0261, joints jitter p90 0.1095 -> 0.1126, p99 0.364 -> 0.380 (37 ids from 41 after the
folds); the catch strip (review_v86/strips/render_ball_f556.png) reads as v81: the ball to the receiver at 560-562, the
tacklers on him from 564.

## 2026-09-20 (03:00): a white ghost on the centre -- the nose tackle's second id -- and the lock's gate made honest (v87)

**The ghost.** BAL after 434 read 10 on 75 frames, 11 on 78 and 12 on 20; the closest same-team pair on the over-full frames
was 13/84 at 0.2-1.6 m. The film (`diag/pocket/sl_13_early.png`, `sl_13_84.png`): 13 is the nose tackle on the centre from
the snap to 436; at 437 the detector re-detects that Raven as 84 and 13's box drifts onto the CENTRE (a KC man) and rides
him to 492. The v86 blend (`ghost13_v86_check.png`, 450-492) shows it plainly: two white bodies at the centre's spot, the
film has one Raven there. Folds (backups .pre_fold.19/20): 13 into 84 on 1-436 (one Raven, 84 now 395-587), 13 into 204
on 437-660 (39 of its boxes dropped where the centre had his own, the rest on his gap frames). 08v carried 198 fused and
70 sideline posed frames to 84.

**What it broke, and why that was right.** The centre's lock fell from 500-540 to 500-524 (the static hold): the lock's
"engagement history" (an other-team box on his at IoU >= 0.4 on 8 of his last 15 boxed frames) had been satisfied by
13's BAL-labelled box on the centre himself. With honest boxes the centre and 84 overlap only on their last four frames
(0.67-0.96 at 494-499, 0.05-0.11 before) -- the same as BAL 1 and Noah Gray (0.14-0.25 on 405-408): before the detector
merges them, a block and a walk-over look alike in the boxes, and both pairs CONVERGE to contact at the end (204-84
1.22 -> 0.36 m over 485-499; 1-74 1.84 -> 0.74 over 406-420). What tells them apart is the opponent's pace after: the
Raven on the centre moves 0.26-0.48 m per 10 frames through 527 and 0.62+ from 530; Gray 0.53-0.79 from the first
frame. STAND_LOCK_SLOW_M 1.0 -> 0.5 (an opponent faster than that at the first frame refuses the lock and the static
hold applies; later it ends the lock); STAND_LOCK_HISTORY 0 (the box gate off, code kept). Measured on the folded
tables: the centre locked 500-528, BAL 1 static 14, steps 5, hops 0, vanish end frames 256 -> 262; census 0.948 ->
1.146 -- the honest number: the ghost had stood in for BAL 1, whose 173-frame absence now shows in the count.
The seventeenth lesson of the corrections file, in a new form: a gate tuned on the data can be tuned on an artefact of
the data; when a film-true fix breaks a rule, suspect the rule's evidence, not the fix.

**v87 rendered (03:40 machine clock): `diag/play_001_v87_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` / `_endzone_blend`.
CURRENT BEST.** 07l on 395-607: steps 5, hops 0, census 1.15 (KC 11.19 / BAL 10.58 -- the honest count with the 13 ghost
gone and BAL 1 still unboxed after 434). Tables and pose caches snapshotted as `*.v87`. Commits 29b5427 (the lock's pace
gate), e2599a4 (HANDOFF). Open, in value order: (1) the sideline detector's holes -- BAL 1 after 434 (173 frames, no box
in either camera), the centre after 528 (his box merged into Thuney's; 164's endzone rows are him but sit 1.0-1.3 m off
and beyond his sideline span); (2) the endzone pairing's several ids for one man (174/166/164 on the centre) -- a runtime
handover with a blended seam; (3) the pile's synthesised lying poses; (4) the 12th KC man on 75 frames is down to the
37/211 and 205/211 twins.

## 2026-09-21 (01:30): the Ravens' count -- every candidate for the eleventh man, checked and named

BAL draws 10 on 117 play frames of v88 (448-560), 11 on 64, 12 on 32. Per frame the sideline boxes those same ten
Ravens on the field (probe_bal_count.py projects every box bottom through the camera). The candidates for the eleventh:
- 36 (BAL, boxed 435-607, never drawn): stands at (-23.6, +24.8) for the whole clip -- the far sideline at the line of
  scrimmage, not moving: an official (the dweller rule is right). 44/46/52/53: 1.5-2 m beyond the far sideline, still: bench.
- 146 (endzone-only 468-624): jersey 0, Roquan Smith -- 171's endzone second id (171 is drawn 395-529, then 55 from 529,
  born the frame 171 ends). 202/210, OCR-named Roquan Smith: his third and fourth endzone ids.
- 112 (endzone-only 524-634): jersey 90, the Raven on the right tackle -- 40's endzone second id (40's own endzone rows end
  at 538; the sideline film shows one Raven on the 65/74 pair).
- 89 (endzone-only 480-539): jersey 40 at the endzone frame's right edge; his ground point projects onto id 7's sideline box.
- 85: the referee. 87, 110, 116: the crowd at the endzone's top edge.
- The 12-frames (416-440): BAL 1's static hold beside 40 (1.1-1.5 m), and 60/55 (0.6-0.7 m, 568+: 60 goes on as 55, IoU
  0.80 -- the twin rule's stretch drop leaves a few frames).
So the tenth-to-eleventh gap is BAL 1's man, an edge rusher blocked by Noah Gray at 412-420, with NO box in either camera
from 435 to the end and nothing at 2560 px either: hidden in the pile from both angles. No rule can draw a man no camera
saw; the census stays at BAL 10.6 on this play and that is the honest number.

**The Film Room, version 3 (01:50):** the joints file now carries both broadcast cameras' solved poses per frame and the
page has "Sideline cam" / "Endzone cam" presets that put the viewer's eye where the film's camera was (frame by frame; the
vertical field of view from fy -- the sideline lens is ~11.7 degrees). Use them next to the blends: what the blend
shows on one frame, the viewer shows from the same eye with orbit available a drag away. Commit: see git log
("viewer: the broadcast cameras as presets").

## 2026-09-21 (02:40): the left of the KC line -- two men, four crossed ids, and a fold per camera (v89)

KC read 12 on 54 play frames of v88; the closest pairs were 205/211, 37/211, 211/157, 139/204 (the lock's projection
beside Thuney) and 80/204. The film (`diag/pocket/sl_37_early.png`, `sl_37_hole.png`, `sl_211_205.png`): two linemen on
the left of the line carry four ids that CROSS at 523 -- man A is 37 to 523, then 211, then 205 from 574; man B is 211
to 522, then 157 from 529, then 37 from 574. First attempt, four whole-id folds (157 <- 37 from 574, 157 <- 211 to 522,
37 <- 211 from 523, 37 <- 205 from 574): steps 5 -> 2, census 1.02 -> 0.94, A one id -- but man B vanished 501-547: a
global id is one sideline track joined to one endzone track, and 211's endzone track (25) had stayed on B from 500 to
610 while its sideline track walked onto A at 523, so "211 from 523 into 37" dragged B's endzone rows onto A, and B's
own sideline boxes there are six. Restored to before the second fold (backups .pre_fold.25 / .pre08v.14 / .18) and
08z got --cam / --track-id (fold_ids: one camera's rows, or one camera track's rows, of the dropped ids; keypoints and
poses follow through the (cam, frame, track_id) join): 157 <- 37 --cam endzone --track-id 25 (B's endzone track back
to B), 157 <- 211 (B's early sideline rows). Commit 8d46c64.

**Result on the play window:** A (37) drawn 395-637 as one id; live steps 5 -> 2 (157's three steps at 553-556 were the
crossed ids), hops 0, census 1.023 -> 0.944. Man B is drawn 500 and 547-637 and NOT 501-546: the sideline has six boxes
on him there, his endzone track starts at 532 and the loader's hole rule drops the middle of a 46-frame hole. Before
today he read as drawn on those frames only because 211's sideline track had walked onto A -- a ghost twin of A, not
B. The honest count shows the gap; the fix is the same as the centre's (a re-detection at 2560 px on those frames
with 03e, then a fold) and is the next step for this man. v89 chain launched.

**Man B's gap re-detected, nothing found (03:05).** 03e on the sideline 496-550 at 2560 px, conf 0.25: 0 candidates with
the duplicate test at IoU 0.15, 6 single-frame candidates at IoU 0.45, no run of 8. YOLO does not separate him from the
pile there either (his six existing boxes on those frames are what it sees). A detection hole in both cameras, like
BAL 1's; the honest count stands.

**v89 rendered (03:40 machine clock): `diag/play_001_v89_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` / `_endzone_blend`.
CURRENT BEST by the rulers.** 07l on 395-607: live steps 2 (from 5), hops 0, census 0.94 (KC 11.12 / BAL 10.60). Tables and
pose caches snapshotted as `*.v89`; the Film Room republished on v89 (Version 4). Film check of the left of the line in
`diag/pocket/left_v89_check.png` (500-600).
Read: the left of the line matches the film at every strip frame 500-600 (man A engaged with his rusher through 600, man B
drawn from 547, BAL 14 / 21 and the right-edge pair in place). Remaining honest gaps: man B 501-546, BAL id 1 after 434.

## 2026-09-21 evening -- the two missing Ravens after 434 were in the tables (v90 in progress)

**Read off the film with 09b (both cameras, 400-600):**
- **id 15 = id 168** (the rusher on KC id 37): 168 is born at 470 as the taller of two boxes on one body, the twin rule
  dropped it 470-481, and 15's own track ended at 485 (so the census read 10 there). Folded 15 <- 168: one body 395-637.
- **id 4 (the rusher on KC 65, jersey 92 Madubuike by the endzone film)** is hidden behind 65 from the sideline camera
  from 448 (65 is between the camera and him; at 24 deg elevation a man 1 m behind another is three-quarters hidden), and
  the endzone camera -- BEHIND the offence, the OL's backs to it -- boxes him under three endzone-only ids in turn:
  198 (to 478; ground points agree with 4's sideline to 0.5 m on 400-442, id 40 stands 3 m away), 136 (479-507, going
  down beside 65), 112 (524-607, up again, between 65 and the right tackle). Folded all three into 4 --cam endzone.
- **id 1 (chip-blocked by the tight end 400-424)** is boxed by NO camera after 428: hidden behind id 40's man / the right
  tackle from the sideline, unboxed in the endzone (03e at 2560 px on the endzone 420-520: 36 candidates, no run of 12).
  Honest gap, like man B (157, 501-546).
- **id 194** was a second box on id 40's man 467-504 and four frames on 4's man 505-509; removed (08za). Folding its
  505-509 into 4 extended 4's sideline span to 509 and turned his REAL endzone stretch 444-503 into a hole the hole
  rule extrapolated to a 5 m hump (steps 2 -> 14): a fold that adds frames at the END of a span changes what the span
  rules see in between.
- **id 4's one stray sideline box at 465** (the tracker re-associated another man's detection 22 frames after the loss)
  was the join the beyond-span rule measured (2.73 m) and dropped his 38 real endzone frames with; `08za_drop_rows`
  (new) removes a row, keypoints follow. Corrections must beat what they correct: the 198 fold measured WORSE (steps
  2 -> 7) until this box was found.
- **id 212 = id 40's track pair continuing (sideline 45, endzone 45)** but its boxes are merged with 65 in the sideline
  and overlap 4's in the endzone: folding it in made the same-body test drop 4 again (census 0.728 -> 0.779). Reverted;
  40 still vanishes 593-607.

**Rules changed (all A/B'd through the real loader, knobs passed at call time; commits fd6a5a1, 9f57a98):**
- `beyond_sideline_span`: the same-body test asks the endzone's boxes -- a sideline man within 1.2 m is the same man
  unless he has his own endzone box apart from this body's (SAME_BODY_APART_IOU 0.3). Census 0.770 -> 0.728.
- `stand_still`: STAND_BRIDGE_MAX_FRAMES 50 -> 60 (4's hole is 51 frames; 0.728 -> 0.61); a hold inside a hole runs to
  the hole's far end (STAND_HOLE_HOLD_TO_END; 0.61 -> 0.498); the seam's length follows the distance and eases in/out
  (STAND_SEAM_STEP_M 0.15; steps 8 -> 2, hops 1 -> 0). A latent KeyError in the hole-lock's fallback fixed (test).
- **Rejected:** a fragment-box rule (drop sideline boxes far shorter than the track's height; 40's 571-592 boxes are
  35-49 px of a 100 px man with bottoms 2-3 m off): whole-track median 0.5 -> steps 0 but census 0.54 + a hop;
  recent median + rising bottom 0.6 -> steps 5, census 0.549. The fragments are the anchors the holds and same-body
  tests use. 40's 2.5 m swing at 568-592 stays (not a step, not a vanish).

**Rulers 395-607: v89 steps 2 / hops 0 / census 0.944 -> now 2 / 0 / 0.498** (KC and BAL each ~0.25 off eleven).
Remaining vanishings: 1 (435-607) and 157 (501-546), both unboxed by both cameras; 40 (593-607); 139 (596-603).
Tables snapshotted `*.v90`; the v90 render chain launched ~19:40.

**Correction (same evening, before v91):** the endzone-only id 112 (524-607) is NOT id 4's man. Its own identity votes
read jersey 90 (David Ojabo) and the endzone frame at 600 shows the 90 on the man right of the right tackle; the man
on KC 65 from 528 wears 92 (Madubuike = id 4's man; the votes on track 45 read 92, which is why v86 named 198 and 212
"Madubuike"). So from 528 id 40's tracks (sideline 45, endzone 45, and 212 after the cut) are id 4's man, and 112 is
id 40's (Ojabo) -- 40's own tracks (to 526/538) were Ojabo all along, not "Kyle Hamilton": the 14 is id 28. Read the
jerseys in the ENDZONE camera (they face it) before pairing two men 1 m apart. Also on the film: 171 -> 55 (Roquan's
tackle on the tight end; 60 a second box; 55's box on Hamilton from 600), 6 -> 78 (the far-side corner), 84 -> 83 (the
nose tackle), 30 -> 180 (the same track pair). Fold script `$S/folds_v91.sh`, names `fix_names_v91.py`; applied after
the v90 chain ends (the blends re-read the tables).

**v91 (render launched ~19:55):** the film-true untangling of Madubuike (4) and Ojabo (40) from 528 measured WORSE
(steps 12, hops 6, census 0.911): giving id 4 the sideline track-45 rows 528-660 extended his sideline span past his real
endzone stretch 444-527, which the hole rule then treated as a long hole and deleted beyond HOLE_REACH of either end
(452-519 gone) -- the same trap as 194's four frames an hour earlier. Reverted; v91 = v90 + the span-safe folds only:
171 <- 55, 60 (Roquan's tackle; 171's pile fragments 550-570 and 55's rows on Hamilton 600+ dropped first), 6 <- 78,
84 <- 83, 30 <- 180, and the names (4 Madubuike 92, 40 Ojabo 90, 28 Hamilton 14, 15 Oweh 99, 171 Roquan 0, 2 Marcus
Williams 32). Rulers: steps 2 / hops 0 / census 0.465. CAVEAT: after 528 the body drawn as 4 is Ojabo and the body
drawn as 40 is Madubuike (the census and the render are unaffected; the click-to-id names are swapped for those two).

**Candidate for tomorrow, measured on a scratch copy with the film-true folds applied (`$S/probe_holes.py`):** a hold_holes
variant that keeps an endzone track inside a LONG hole where it forms a continuous chain from the hole's near end
(first point within HOLD_M of the sideline's, then <= 0.6 m x gap per step, gaps <= 5): census 0.911 -> 0.714 at steps 2 /
hops 0 (0.3 m / gap 3 kept only 6 frames: the endzone's depth jitter breaks a tight chain). Two more things stand in the
way of the film-true ids: the beyond-span TAIL join is measured against a fragment box (40's 522-526, 70 px of a 100 px
man) and reports lead-in and tail as one entry, so Ojabo's 112 rows die with the pre-snap lead-in; and a hold whose
last box is an ended endzone track dies on the cover test at once (4's 494-519).

**v91 rendered (20:40 machine clock): `diag/play_001_v91_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` / `_endzone_blend`.
CURRENT BEST, film-checked.** 07l on 395-607: live steps 2, hops 0, census 0.46 (KC 11.12 / BAL 11.18). The pile checked
against the film at 440-607 (`diag/pocket/pile_v91_check.png`): the Ravens hidden behind KC 65 drawn where the film has
them, the left pile (98, 99, the nose tackle) three white bodies for three white men, Roquan on the tackle. Tables
`*.v91`; the Film Room republished on v91 (Version 5). Next: the three rule refinements in `$S/patch_three_rules.py`
(same-team same-body test, the hold at the start of an over-cap hole, the hole chain) -- A/B via `probe_ab_three.py`
on the live tables and on the film-true scratch copy (`$S/play_copy`, 2.6 GB).

**Three refinements measured alone, live tables (v91) and the film-true scratch copy, 21:10:**
- same-team same-body test (a Raven next to a KC man is not his copy): live census 0.465 -> 0.789, copy 0.826 -> 0.972.
  REJECTED on both: it re-admits endzone-only bodies beside the other team (KC 17's rows 441-471 drawn, id 4's 508-545
  lost to the box-apart test against 40's Ojabo box). The old any-team distance test was doing real work; a principled
  refinement lost twice (23rd case).
- a hold at the start of a hole longer than the bridge cap: live unchanged (no such hole), copy 0.826 -> 0.836 (id 1's
  14 frames at 421 back, nothing else): neutral, kept OFF (STAND_LONG_HOLE_HOLD False, test sets it).
- the endzone chain inside a long hole (HOLE_CHAIN_STEP_M 0.6, gap 5): live unchanged, copy 0.826 -> 0.629 (id 4 drawn
  to 493 instead of 451). ADOPTED (default on); a fold that lengthens a span across a real endzone stretch no longer
  deletes it. The film-true Madubuike/Ojabo assignment still measures 0.629 against v91's 0.465: the beyond-span
  tail join on 40's fragment boxes (522-526) and id 4's dead hold after 493 (an ended endzone track has no cover) remain.

## 2026-09-21 21:40 -- v92: the film-true ids, measured first on a scratch copy, then ported (render launched)

With the hole chain in place (879e8fe) the film-true assignment that lost at 20:00 wins. Measured on the scratch copy
first (`$S/play_copy`, 2.6 GB): 0.826 -> 0.629 (chain) -> 0.545 (Ojabo one id) -> 0.451 (id 40 emptied); then the same
eleven operations on the live tables: **steps 2 / hops 0 / census 0.441** (v91: 0.465), Ojabo's 173-frame vanish gone.
- **id 1 = David Ojabo (90)**: his own sideline track to 413 (the fragment boxes 414-420 dropped), id 40's sideline
  track 40 (405-526) and sideline track-45 rows 485-527, the endzone track 40 to 416 (it wore 90), and the endzone-only
  112 (524-634, the 90 vote) -- drawn 395-565, 572-575, 595-605.
- **id 4 = Nnamdi Madubuike (92)**: as before plus the sideline track-45 rows 528-660 and endzone track 45 (539-577) that
  were id 40's, and 212 -- drawn 395-493, 520-609; his 494-519 (down beside 65, no box in either camera) remains.
- **id 7 = Malik Harrison (40)**: his own tracks all along; id 40's endzone rows 417-538 (they wore 40) were his second
  copy and are dropped. **id 40 no longer exists.** The twelfth Raven at 414-434 was Ojabo drawn twice (id 1 held at his
  fragment spot while the sideline already boxed him as 40).
- Recipe that worked: play the fold sequence on a copy of the play dir (08z/08za take --play-dir), read the loader's
  rulers there, then port. Remaining: 157 (KC man B) 501-546, 4 494-519, 171 600-607 (Roquan under the pile), 139.

**v92 rendered (2026-09-22 00:35, after a GPU pause for the user's own tests): `diag/play_001_v92_hifi_720.mp4` +
`_sideline_blend` / `_sideline_sbs` / `_endzone_blend`. CURRENT BEST, film-checked.** 07l on 395-607: live steps 2, hops
0, census 0.44 (KC 11.12 / BAL 10.89). The pile checked at 420-570 (`diag/pocket/pile_v92_check.png`): two bodies drawn
beside KC 65 and the right tackle where the film shows one man visible and one hidden behind him, the left pile
(98, 99, the nose tackle) matches, Ojabo one body from the snap. Tables `*.v92`; the Film Room republished on v92
(Version 6). Next patch, drafted in `$S/patch_uncovered.py`: the static hold ends only after STAND_UNCOVERED_FRAMES
(3) consecutive uncovered frames (id 4 dies at 494 on a detector dropout of the covering box).

**2026-09-22 00:55 -- the hold's cover-dropout tolerance (STAND_UNCOVERED_FRAMES), v93 launched.** The static hold ended on
the first frame the last box stood uncovered; id 4's covering boxes come and go at 494-499 (a detector dropout, he is on
the turf beside 65 on the film) and the hold died there. Ending only after N consecutive uncovered frames, A/B through the
loader on 395-607: N=1 census 0.441, N=3 0.413, N=6 0.305 (id 4 drawn 395-609 continuous; steps 2 / hops 0 in every arm).
6 adopted; a man who really left costs at most six held frames at his last spot. v93 = the v92 tables + this constant;
render launched 00:55, tables snapshotted `*.v93`. Remaining vanishings on the play window: 157 (KC man B, 501-546),
171 (Roquan under the tackle pile 600-607), 139 (601-604).

**v93 rendered (2026-09-22 ~06:00): `diag/play_001_v93_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` / `_endzone_blend`.
CURRENT BEST, film-checked.** 07l on 395-607: live steps 2, hops 0, census 0.31 (KC 11.15 / BAL 11.02). Film check at
490-540 (`diag/pocket/pile_v93_check.png`): id 4 held beside KC 65 through his turf frames where the film has him hidden
behind 65, nothing else moved from v92. Tables `*.v93` (= v92's), the Film Room on v93 (Version 7). Remaining
vanishings on the play window: 157 (KC man B 501-546: his row at 500 sits on Thuney's spot, so a hold there would be a
twin), 171 (Roquan under the tackle pile 600-607), 139 (601-604). A "successor must be newborn" rule for the hold was
tried and left OFF: it disarms the box-twin protection (unit test: id 40 held 20 frames on 198's spot). The film-true
scratch copy (`$S/play_copy`) deleted after porting.

**KC's +0.15 on v93 (33 frames at 12-13 in six short runs, 06:40):** read on the film, not twins: the centre (204) and the
quarterback 0.2-0.5 m apart at 547-556 are two men standing together after the throw; the centre and Thuney (139) 0.2 m
apart at 436-440 are two men side by side on the nose tackle whose boxes overlap (the ground points coincide, the men are
0.7 m apart along the camera's line of sight). The twelfth KC body at 547-556 is one of {3, 5, 11, 12, 37, 74, 76, 77, 80,
139, 157, 204}: eleven roles (5 OL, 2 TE, 2 WR, RB, QB) and man B (157) -- so either 157 doubles one of the linemen or a
WR id is a second box; needs the KC jerseys read in the endzone film at 547-556 the way the Ravens' were. Not done.
A "successor must be newborn" hold rule tried and left off (it disarms the box-twin protection); "a teammate inside the
twin radius is not an exempt neighbour" measured neutral on play 1 and kept on (principled, no cost).
**Lead on the twelfth KC body at 547-556 (07:00):** the endzone frame at 550 boxes the LEFT TACKLE (76 Suamataia) as id
157, and the centre (52 Humphrey) is hidden behind Mahomes there; the sideline frame draws 204 on the red man beside
Thuney (the centre) and 157 on the man engaged with Oweh (99); the timeline puts 37 at y -3.6 (the tackle's spot), 157
at -1.0 and 204 at -0.5. So 37 and 157 may be one man (the tackle) under a sideline id and an endzone id, and 204's
stored name "Suamataia 76" is a wrong jersey vote (it is the centre). Same recipe as the Ravens: per-camera tracks,
jerseys in the endzone film, fold per camera, measure on a copy first. Not done.

**07:45 -- man B was man A.** Per-camera tracks at 538-562: id 37 = sideline track 25 (y -4.5) + endzone track 37 (y -4.1);
id 157 = endzone track 25 on the SAME spot (y -3.6) + sideline track 37 whose boxes are fragments (72-111 px of a 150 px
man) with bottoms that put him at y -1.0. One man, the left tackle (76 Suamataia, boxed 157 in the endzone frame at 550);
the second body between the guard and the centre from 547 was a phantom, and his 501-546 "hole" a phantom too. Folded
37 <- 157: vanishings on the window drop to 171 (8) and 139 (1), but the census goes 0.305 -> 0.498 because the centre
(204) then loses 557-607: hidden behind Mahomes for the endzone camera, his nearest sideline body becomes the QB 0.5 m
away and the gap-branch same-body test (same_body_gap_m) drops his endzone tail. 157 was, by accident, the body that
kept him. A span-length gate on the same-body test measured worse (0.671). LIVE TABLES RESTORED TO v93 (the phantom
stays, the centre stays); the folded state is on `$S/play_copy2` for the next step: the gap-branch test needs the id's
OWN last sideline point against the neighbour's -- the sideline had the centre and the QB 0.5-1.1 m apart at 556, two
men -- before it calls the endzone tail a copy. Also 204's stored name is a wrong vote (he is the centre, not Suamataia).

**08:30 -- the centre's tail is a MERGED BOX, and it moves the quarterback.** On v93 the centre (204) has no box in either
camera after 556 (hidden behind Mahomes for the endzone camera) and his hold dies at once on the twin veto: from 557 the
sideline detector boxes the quarterback and the centre as ONE box (IoU 0.95 with the centre's last box), the
quarterback is placed at that box (his sideline point jumps from (-18.2,-1.0) at 555 to (-20.0, 0.0) at 560 while the
endzone camera keeps him at (-17.5,-0.5) -> (-16.9,-0.4)), so the drawn QB stands 0.34 m from the centre's last spot and
the centre reads as his twin. Two errors from one box: the centre vanishes 557-607 and the QB is drawn ~2-3 m forward
of where the endzone camera has him. Also measured and reverted: a successor-history rule for the hold (a same-team box
that was not on the man's box before his loss is a neighbour, not his new id) -- no effect on any arm (the veto, not the
successor test, is what stops the hold) and it broke the box-twin unit test. Next: read the QB against the film at
556-600 (`diag/pocket/qb_v93_check.png`); if the endzone is right, the sideline override needs a merged-box guard (a
box whose width/height jumps and that another sideline id's last box sits inside at IoU > 0.9 is two men).
Read (`qb_v93_check.png`, 552-596): the drawn quarterback at x -20 is RIGHT -- the film has him standing a metre behind
the line after the throw; the endzone camera's (-17, -0.4) is its depth error, not his position. So the merged box
places the QB about right and the only loss is the centre, blocked by the twin veto (STAND_CLEAR_M 0.45) on a real
0.34 m gap. A/B of 0.30 / 0.35 running.
STAND_CLEAR_M 0.30 / 0.35: no change (204 still ends 556) -- the stopper is the successor test: the merged box is the
QB's box on the centre's last box at IoU 0.95, same team, so the hold reads "the centre under a new id". Two men, one
box, the other camera blind to the centre: unless a successor test can tell a merge from a re-identification, this is an
honest gap. Trying the successor-history rule at IoU 0.9 (a true box twin overlapped his box at 0.9 before the loss; a
quarterback stepping up did not).
The 0.9-history successor rule: no effect either (204 still ends 556) and three unit tests fail; reverted. So the branch
that stops the centre's hold at 556 is STILL UNIDENTIFIED -- not the twin radius (0.30 tested), not the successor test
(history 0.3 and 0.9 tested). NEXT STEP, before any more rules: instrument `stand_still.hold_or_lock` with a per-id
stop reason (moved / no last box / twin veto: who / successor: who / uncovered / cap) printed by the loader for the
ids in a STAND_DEBUG_IDS set, and read it for 204 at 556. Then design. v93 stays CURRENT BEST.
**09:40 -- the stopper found by instrumenting, not guessing:** `STAND_DEBUG_IDS` (timeline.stand_still) logs every hold
decision; for 204 at 556: "hold_or_lock start, last box sideline (1382,602,1456,697); neighbours []; 557: hold stops,
twin veto by [(80, 0.34)]". The QB, placed at the merged box, stands 0.34 m from the centre's spot. And the radius A/B
was VOID: the loader never passed clear_m (nor slow_m, window) at call time -- bound as defaults -- so both arms ran at
0.45; identical arms were the tell (probe-monkeypatch-default-args, second time). The call now passes them; a real
0.30 / 0.35 A/B is running. For 171 at 599: "no hold, moved 1.45 m over the window" -- Roquan was making the tackle;
by design, honest.
Real A/B (clear_m passed at call time): 0.30 census 0.305, 0.35 0.291, 0.45 0.305 -- steps 2 / hops 0 in all; 0.35
adopted (three body-frames; not worth a render, v93 stays the rendered best, tables unchanged). The centre still stops at
557 at every radius: past the veto, the successor test fires on the QB's merged box (IoU 0.95 on his last box). A
"successor must have overlapped his box before the loss" rule cannot tell a merge from a re-identification: the unit
fixture's id 198 jumps 10 m onto 40's spot with no prior overlap and IS his new id, and the QB's placement also jumps
(1.8 m over 555-560) when his box merges. So the centre 557-607 is honest at the rules level. Candidate for a data step:
a DE-MERGE -- a sideline box that grows by a third while another id's last box lies inside it at IoU > 0.9 is two men;
split it with the two ids' last box sizes (03e-style, --apply with backups), then the centre keeps a box and the QB
keeps his place. Roquan 600-607: "moved 1.45 m over the window", the tackle -- by design.
**Merge census (10:15, read-only probe):** on 395-607 the sideline has 41 events where a box grows by a third or more
while another id's last box (seen within 6 frames, absent now) lies inside it: the QB absorbing the centre at 557
(1.66x), the RB absorbing the QB at 450 (4.7x, the h 184 box), Gray absorbing Roquan at 516/519/556 (the tackle), the
RG absorbing Madubuike at 557/599/603, Roquan absorbing Hamilton at 591, the centre absorbing the nose tackle at 414
(2.7x) -- engagements and tackles, both teams. A de-merge data step has plenty of targets. Design notes: the grown box
spans both men; the absorbed man's box is the part not covered by the grower's LAST box (his own size, at the far
side); the grower's box bottom moved to the nearer man's feet, so the grower's placement jumps too (the QB's 1.8 m at
555-560 -- yet the film puts him at x -20, so check each case on the film before trusting either bottom).

**10:50 -- not a merge: an id SWAP at 557 between the quarterback and the centre.** Sideline boxes: 80's track 79 sits
on the QB at 550-556 (x 1505-1513); at 558 80's OTHER sideline track (54) lands on the centre (x 1424, where 204's track
900 ended at 556) and from 570 track 79 continues on the centre (1465 -> 1563 by 607); the real QB runs on under 157's
track 37 (x 1503 -> 1609, 548-607, a second box on him at 548-556). The endzone's 80 (track 54) stays on the QB. So in
v93 the body drawn as 80 from 558 IS the centre (that is why "the QB at x -20" matched the film -- I matched the
centre), the QB is the body drawn as 157, and the centre "vanishes" only by id. Recipe (testing on a fresh copy,
`$S/play_copy3`): 204 <- 80 sideline track 54 (558-566) and track 79 (570-660); 80 <- 157 sideline track 37 (548-660);
37 <- 157 endzone track 25. The ball (08y --qb 80) then follows the right man after the throw. The 41-event "merge"
census still stands for the other cases (the RB's box over the QB at 450, Gray over Roquan at 516).
Measured on the copy: census 0.291 -> 0.235, steps 2 / hops 0, the QB (80) drawn 395-637 on the right man, the centre
(204) 395-634, id 157 gone; vanishings on the window down to 166 (407-420, pre-existing under the successor rule) and
Roquan's tackle (600-607). Ported to the live tables as v94 (render launched ~11:00). Lesson: the "phantom" 157 was two
different men's boxes (the tackle's in the endzone, the quarterback's in the sideline), and the sideline id 80 carried
two tracks that both slid onto the centre after the throw -- a same-camera SWITCH the 08t pass did not cut because the
switch happens where two men stand 0.4 m apart. Read per-camera tracks with x over time (a table, six lines) before
believing any body's id after an engagement.

**v94 rendered (machine clock ~07:30, 2026-09-22): `diag/play_001_v94_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` /
`_endzone_blend`. CURRENT BEST, film-checked.** 07l on 395-607: live steps 2, hops 0, census 0.23 (KC 11.10 / BAL 11.06).
Pocket check 550-600 (`diag/pocket/pocket_v94_check.png`): the quarterback's body stands behind the line where the
film's 15 is, the centre is back beside Thuney against 98, no red body missing. Tables `*.v94`; the Film Room on v94
(Version 8). KC names set from the endzone jerseys (204 Humphrey 52, 37 Suamataia 76, 76 Trey Smith 65, 12 Taylor 74,
11 Kelce 87) -- they feed the rendered numbers from the next render on. Remaining on the window: 166 (407-420, the
centre's other id at the snap, 14 frames), Roquan's tackle 600-607 (moving, by design). The 41 grown-box events are the
next data-step candidate; every id in a pile deserves the per-camera x-over-time table before it is trusted.

**v95 rendered (2026-09-22, machine clock ~09:00): `diag/play_001_v95_hifi_720.mp4` + `_sideline_blend` / `_sideline_sbs` /
`_endzone_blend`. CURRENT BEST, film-checked.** v94 + two row drops read off the 09c audit: id 166's sideline rows 395-435
(a second box on the centre at the snap -- KC read 12 at 396-406) and Roquan's fragment boxes 520-528 (61-68 px of a
100 px man, 2 m across; his hole now bridges to his tackle rows). 07l on 395-607: live steps 2, hops 0, census 0.18
(KC 11.05 / BAL 11.06). Film checks: the snap pocket 398-428 (`diag/pocket/snap_v95_check.png`) and the tackle 510-560
(`tackle_v95_check.png`) both match. The vanish list on the window is empty but for Roquan's tackle 600-607 (moving,
by design). Tables `*.v95`; the Film Room on v95 (Version 9).

**Pre-snap stretch (215-394) and the tail, measured on v95 (the user's clip starts at 215; the rulers only score 395-607):**
exactly 11/11 on 107 of 180 pre-snap frames; KC 10 on 39 (holes of 204 at 220-223/256-257, 76 at 225-230, and 234-250
where id 31's man is gone), KC 12-13 on 28 (291-298 and 377-394: 204 within 0.2-0.4 m of the QB and of 17). The
09c audit says: id 82 (264-307) is a WIDE SHORT box (88 x 66 px) -- the centre crouched over the ball -- while 204's
pre-snap sideline track 25 is a standing 160 px man 60 px to its right, i.e. the quarterback under centre; so pre-snap
204 is the QB's second body and the real centre is 82 (whose "vanish 308-393" is the centre disappearing before the
snap). id 31 (222-228, 71 px) is the right guard's early fragment; 76 has no sideline box at 216-262. The tail 608-619
runs KC 9 / BAL 10 (tracks end after the down). Trying STAND_FROM_CLIP_START (stand_still from the clip start, not the
snap) for the pre-snap holes; the QB/centre pre-snap twin and 82 need the film (a crouched centre's box is half a man).
STAND_FROM_CLIP_START measured: the play window unchanged (steps 2 / hops 0 / census 0.183); pre-snap exactly-eleven
frames 107 -> 112 but KC-12 frames 24 -> 62 -- the holds re-draw the pre-snap twins (31 held 25 frames beside the
guard, 204's standing box 73 frames beside the QB). OFF by default; fold the pre-snap twins first (82 = the crouched
centre; 204's pre-snap track 25 = the QB's second body; 31 = the guard's fragment), then re-measure.
Strip `diag/pocket/presnap_centre_qb.png` (sideline 240-370): the man in id 82's crouched box wears 62 -- Thuney, not
the centre -- so 82 is Thuney's PRE-SNAP id (139 takes him from 435); 166 and 191 are further boxes on the same crouched
men (twins), 19 a box on the man below, and 204's pre-snap track 25 is the standing man behind the line. The set
formation is drawn 11/11 on 107 of 180 frames by the formation hold; the rest is this twin soup. Worth one film session
with 09c + 08z --cam --track-id before the snap (fold 139 <- 82, drop 166/191/19 where they double), then re-measure
STAND_FROM_CLIP_START. Low priority against the play itself.

**Pre-snap KC line, read from one table (every KC sideline id near the line 215-394: span, median ground, box h/w):**
by across-position y: 11 Kelce at -5.4 (33 a 5-frame twin), 19 = the left tackle at -3.6 (127 x 108 crouched; 37 takes
him from 370; 166 a second box on him 291-394), 82 = Thuney at -0.8 (69 x 87 crouched; 139 takes him only from 435, so
he VANISHES 308-434 before the snap), 17 = the centre at +0.5 on the ball (82 x 88 crouched), 204's pre-snap track 25 =
the QUARTERBACK standing behind him (160 tall, x -22.5; 80's own box starts at 377), 31 = the right guard's fragment
218-233 (76's own box from 375, his pre-snap body from the endzone), 12 = the right tackle (137 x 121, the guard merged
in), 3 = the right receiver/tight end at +5.0, 5 Pacheco 7 m deep. Fold set under test on `$S/play_copy4`: 80 <- 204's
pre-snap track 25; 204 <- 17; 37 <- 19; 139 <- 82; drop 166's sideline rows to 435, 33, 31. Ships only if the play
window stays 2 / 0 / 0.18 and the pre-snap exactly-eleven count rises.
**Pre-snap fold set REJECTED (measured on the copy):** whole-id folds: play census 0.183 -> 0.286; restricted to 215-394:
0.211 with post-snap stubs of 17/19 drawn as a twelfth Chief 395-440; stubs dropped: 0.286 again, and the pre-snap
stretch collapsed (exactly eleven on 43 of 180 frames, KC 10 on 122; Thuney's 139 now vanishing 223-263 and 308-354).
Cause: the loader's quarterback-under-centre rule holds 80 at the spot he steps back from and names the CENTRE by id
(17); moving 17's rows to 204 and 204's pre-snap track to 80 pulled that rule's anchors out from under it, and the
"centre" it then removed from the QB's spot was the real centre. The pre-snap ids are load-bearing for that rule.
Leave the pre-snap as v95 (107 of 180 frames exactly eleven); if it is ever revisited, read the film per id AND the
qb-under-centre rule's inputs first. Copy discarded. v95 stands.
**STAND_TO_CLIP_END (on):** stand_still runs to the clip's end (down + tail, 615) instead of the down. Play window unchanged
(2 / 0 / 0.183); the tail 608-615 goes from (KC 9, BAL 10) x6, (9, 11) x2 to (9, 11) x6, (10, 12) x2 -- one more Raven on
six frames, a held twin on the last two. Not worth a render on its own; the next render carries it.

## 2026-09-25 03:05 -- the KC left line untangled on the copy (chain 2 measured; chain 3 = the port candidate, running)

**Who is who, settled on both films.** Endzone by jersey (above). Sideline by depth ORDER ($S/line_order.py): the
three men stand one behind another along the sideline's line of sight, so each sideline box's foot row ranks it and the
rank is matched to the endzone's jersey-labelled order across the field: 37 = #76 nearest on every frame; sideline t25
(labelled 204, 210-499) = #62 Thuney (second); t17 (17) = #52 at 400-420; t39 (139) = #52 at 438-474 then Thuney from
~476 (its early rows 384-408 are Gray on the right side, left alone). Identities in identity_resolved.pkl agree with the
target: 37 = Suamataia #76, 139 = Thuney #62, 204 = Humphrey #52 (17 = "P17", his unnamed early track).

**Two traps met.** (1) The same-keys merge onto the live cache uses the OLD ids: after a relabel it left the relabelled
men's new records out (2,824) and kept their stale ones -- fixed by remapping the base first (08v on a scratch dir
holding the live cache + the before/after tables; $S/untangle_line2_chain.sh). (2) 08z will not keep a fresh id
(SetupError: no rows) -- a temporary holder must be an existing id (17 held the centre's t39 rows before folding into
204); a failed step silently let the next fold dedupe two men (40 boxes) -- the run was killed and redone.

**Chain 2 (all relabels, the centre as 17, correct merge) vs control (lkft2c on today's loader):** census 0.169 ->
0.164, steps 2 / hops 0, the centre no longer vanishes; the depth ruler's across-field p99 2.33 -> 1.18 m, over 1.5 m
4.9 -> 2.8 %; endzone film: Thuney and #76 drawn ON their men at 436-476 with their arms on their rushers
($S/line2_ez.png). But hinge jerk 5 -> 14, all nine new on the centre at 482-484 and 512-514: at 475-492 his only
sideline rows are a 5-box fragment (39 px wide) and at 510-530 endzone-only boxes. Chain 3 ($S/untangle_line3_chain.sh)
drops the fragment and keeps 204 (Humphrey's name and build).

## 2026-09-25 06:10 -- the pre-snap line answered on the film; a dead pre-snap fill found; the hole chain's outlier

**Pre-snap KC left line + quarterback (read on both films; $S/zoom_side_line.png, zoom_side_t19.png,
line_presnap_a.png).** The pre-snap census had been |KC-11| 0.511 on v110-v112 (215-394): Thuney drawn 30 of 180
frames, the left tackle 25, sideline ghosts 19/166/82/31 in their place. The tracks: sideline t25 (g139) is the
QUARTERBACK under centre until 383 (t80 takes him at 377; 379 a blip onto #62), #62 Thuney from 384 -- so the v111
port's fold of t25 210-499 into 139 was wrong before 384 (and v110 had it under 204); sideline t19 (g19, "jersey 67")
is #76 the left tackle, some frames a box merged with #62's upper body; t33 (g166) is #76 from 291; t37 sits on #62
(its box bottom on #76's body) 372-390 and on #76 from 395; t82 is a twin on the quarterback 217-248 and Thuney's
upper body 264-307; endzone t86 (g86, jersey 62, KC OL) is Thuney 140-392 and was never drawn (the span rule and the
dedupe took him against the sideline ghosts). The quarterback's endzone t22 (g22/g164) doubles the centre's box at
216-248 and sits past the line at 272-280: NOT folded. On the copy (scratchpad presnap_fold.sh: drops t19 291-400,
t37 370-394, t25 377-383, t82 217-248; folds t25 210-376 -> 80, t19 14-290 -> 37, t33 291-394 -> 37, endzone t86 ->
139, t82 264-307 -> 139): pre-snap |KC-11| 0.511 -> 0.183, the quarterback, both tackles-side men and Thuney drawn on
all 180 frames in film order (-3.3 / -1.5 / 0 / QB behind); the QB hold now finds no candidate (his track starts at
210) and is not needed. Left: Trey Smith (76) absent on 31 frames. Refit on the folded tables pending (GPU).

**The pre-snap hole fill has been dead code since 5779113 (09-20).** fill_presnap_holes (adopted 3ebc0ea, 09-18,
0.52 -> 0.43) sat at the end of the line-vouch branch; 5779113 inserted the pocket and short-team vouch blocks above
it and the fill became the body of `if SHORT_TEAM_VOUCH_CLEAR_M is not None` (OFF). Trey Smith's 31 missing pre-snap
frames are exactly the fill's case: absent from ground at the vouch (the span rule's same-body test takes his
endzone-only frames against the quarterback's sideline point 1.3 m across -- the quarterback has no endzone box to
prove them apart), vouched on both sides. Fix (move the block back; AST structure test) waits for the render chain.

**Madubuike's hole (id 4, sideline 443-528).** The endzone chain rule broke on one box: at 491 endzone t45's box is
on KC #74 beside him (1.3 m across, inside the isotropic 1.8 m three-frame bound, so TAKEN), the true point at 493 then
failed and ENDED the chain; the rule deleted 493-516 while endzone t136 boxed him crawling on the turf (film), and the
timeline held him at the 491 point, a metre off, 492-504. Variant (runtime patch, scratchpad patch_chain_variant.py):
a point off the chain is skipped, not the chain's end; a step is bounded along the endzone camera's ray by step_m and
across it by 0.2 + 0.17 m per frame of gap (also refuses the box merged with #65 over him at 518-522). On the whole
play only two long holes carry endzone points: id 4 (+17 frames, -491) and the centre 204 474-533 (+19; endzone t33
on Humphrey there, film). Live 07l unchanged (steps 2 / hops 0 / census 0.16); the endzone strips A/B are running.

## 2026-09-25 07:30 -- the pre-snap KC line + quarterback fold PORTED (v113 tables); endzone regressor poses (flag)

**Copy A/B (presnap_refit.sh; one tail, chain + fill on):** A0 live tables: play census 0.16, pre-snap |KC-11|
0.400, pre-snap trunk past 70 deg 140 body-frames, pre-snap R arm sideways 28.3 %. A1 folded (live cache remapped):
0.131 / 0.056 / 118 (#76 inherited the merged-box ghost 19's records: R arm sideways on 82 frames, 54 frames past
70 deg). A2 folded + refit (05n/05f/05p on the folded tables; merge_relabelled.py: same keys + 127 new records for
37/80/139 on 14-400): 0.131 / 0.056 / 65, R arm 23.8 % (the quarterback's hands under centre 56), live window
unchanged (steps 2 / hops 0 / jerk 4). NOTE: the copy's sideline regressor cache must be the remapped one before the
tails -- drop_unboxed_poses keeps a record whenever the id has a box in EITHER camera, so the quarterback's old
records under 139 would have drawn Thuney pre-snap (checked per id: remap moves t25's 29 records to 80, 63 to 37).
**Ported** (port_presnap.sh; tables snapshotted *.v112; the four tables hash-equal to the copy's; poses_refit.json <-
the copy's lkps, poses_sideline.json <- the one-shot remap).

**Endzone regressor poses (bb3fa9d, flags off):** Gray's pre-snap arms flung up -> hands on knees (endzone film);
moving men contort (records 6 frames apart) -> ENDZONE_POSES_PRESNAP_ONLY. A/B on the ported play running.

**Found, not fixed:** at the end of the play (586-601) Thuney (endzone-only after his sideline track ends at 565) and
#76 (sideline-backed) are both drawn 36-115 px left of their own endzone ankle keypoints (the endzone film): #76's
depth along the sideline's line of sight is a metre off where the depth snap did not take the endzone's point, and
Thuney's endzone box merges with #76's. Next placement unit after v113.

## 2026-09-26 00:45 -- the late pile read on the film (v119 tables): #98 one id, Thuney on the ground, a ghost Raven gone

**What the film shows (both cameras, 540-600; $S/boxes_region.py + kp_zoom.py crops in diag/pile_*.png, id84_*.png):**
- Two Ravens at Taylor (#74, RT): **#90 Ojabo outside him** (endzone track 112, id 1 -- right) and **a second Raven
  engaged with #65 (RG) between the two** -- sideline track 45 = id 4 (Madubuike, #92) is that man (right). His feet
  are hidden behind #65 in the sideline view; the endzone has no box for him (he is inside #74's and #65's boxes).
- **id 84 = #98 Travis Jones** (endzone film pre-snap: the Raven in a three-point stance over #62), the same man as
  the named id 81 (#98) from 568. Sideline track 84 is him to 541; at 551-565 its boxes sit inside Thuney's own box
  (track 39); at **566-580 it is Thuney ON THE GROUND** under #98 (his track 39 ends at 565); at 581-587 it is on #99.
  So "a Raven drawn twice" at 556-587 was partly Thuney, lying on the turf, drawn as a white Raven -- and the real
  Thuney vanished at 601 because his sideline presence ended at 565.

**Fix (port_v119.sh, measured on play_copy4 first; the live tables are byte-identical to the copy):** 08za drops
track 84's rows at 551-565 and 581-587; 08z relabels track 84 at 566-580 to 139 (Thuney) and folds 84's sideline
track 13, endzone track 13 and track 84 (437-541) into 81. 07l: steps 20 / 0 and hops 0 unchanged; census live
0.04 -> **0.08** (KC 10.97 -> **11.00**, BAL 11.01 -> 10.92). The census is worse for an honest reason: the ghost
masked a real missing body -- at 570-586 Madubuike's body is drawn on Ojabo's endzone point (the positional depth
snap) and Ojabo's own body is deduped under it, so one body stands for two men; the ghost made it read 11.

**Measured and not shipped: depth_snap.SPARE_MISSED** (patch_snap_notaken as a knob, default OFF, tested): the
positional snap may not take an endzone point of a man the sideline tracks at other times but misses on this frame.
With it (v117n): KC 11.00, census 0.05, the 12-Raven frames at 610-613 gone and the pre-snap KC RG back at 218-234 --
but Madubuike's sideline-only point lands 0.6 m BEYOND Ojabo (y 3.4 vs 2.8; the film has him between #65 at y 1.1 and
#74 at 1.5): with his feet hidden behind #65, the box bottom is high in the image and the ground point is too deep.
One wrong placement for another, plus Ojabo flickering out at 568-574 and 592. Needs a ground point for hidden feet
(box height from the man's own unoccluded frames) before it can ship.

**Lighting (render.shade, 05k --shade, 94e4796):** the bodies were flat kit colour with no light (cutouts; a pile of
Chiefs one red mass). Each splat is re-lit through its own normal (the z axis of its rotation, which mesh_to_gaussians
and uniform.decal_gaussians lay along the outward surface normal -- checked on the SMPL-X rest mesh: chest +z, crown
+y). Two lights on the broadcast-camera stills 556-604 (render_view_shade_ab / _ab2 vs render_view_v118): the first
took the camera-facing kit to ~0.76 of the film's colour (maroon reds); the chosen one leans toward the near sideline,
ambient 0.66 / diffuse 0.48, camera side ~0.92, far side 0.66. The light knobs were default ARGUMENTS in the first
draft -- a with_flag arm would have measured nothing (the known trap); they are read at call time now (3847d39).

**v119 = v117b tables + the pile fix + --shade + --sky** ($S/launch_v119.sh: hero follow 1080p, skycam behind the
offense 1080p, the sideline broadcast camera's own pose 720p + its local blend). The 05q overlay on both films at
572-612 (diag/overlay_v119_pile.png): Thuney drawn on the turf under #98, #98 one body, no white body on Thuney.
Still wrong: at 570-586 Madubuike's body stands on Ojabo's spot and nobody between #65 and #74; at 606-615 (after the
down) id 69 -- a late sideline fragment of the Raven behind #65 -- is drawn right of Ojabo in the endzone view.
