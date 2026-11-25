---
type: findings
topic: identity-and-teams
period: 2026-09-05 to 2026-09-25
entries: 5
source: docs/HANDOFF.md (moved verbatim 2026-11-24)
---

# Identity and teams

Who each track is: team from kit colour, jersey number, roster name and position role.

5 entries from 2026-09-05 to 2026-09-25, oldest first, moved word for word from [HANDOFF.md](../HANDOFF.md). Each heading keeps its original date. All entries concern play 1 (BAL at KC 2024 week 1) unless they say otherwise. See the [findings index](Findings.md) for every entry in date order.

**Concepts:** [Identity](../concepts/identity.md), [Tracking](../concepts/tracking.md), [Referees](../concepts/referees.md)

**Decisions:** [0008: Don't find officials by shirt stripes alone](../decisions/0008-officials-not-by-shirt-stripes.md)

## Play 1 v8 (2026-09-05 19:32): kits from the saturation vote

`diag/play_001_hifi_720.mp4`, 255 frames. Identity from cache with the kit
deciding (31 of 106 named, the OCR overruled on 4), keypoints and
triangulation again (47 players of 83 with keypoints, 42 % valid joints at
8.3 px), refit 47 players over 443 frames at 0.091 m rms, 08f refused
(gap 10), so identity's teams stand. Frame `diag/play_001_v8_a.jpg`: the
red cluster sits on the ball, white spread; numbers on the sure ids;
officials still white; one-view duplicates remain (the endzone track).

## Kits: the team from saturation votes, and what it exposed (2026-09-05)

The team label every play carried came from ONE crop per track and a global
two-means on mean HSV (`calibration/identity_precompute`). Against
crop-verified kits (`diag/sure_id_corrections.json`, sideline crops) it was
near random: a crosstab against the new rule is 25/31 vs 24/26 on play 1.
The "sure" identities (roster name from a number unique to one roster)
inherited it, so 10 of 18, 4 of 12 and 2 of 15 on plays 1, 2, 4 wore the
other team's kit and had that team's number painted on them.

**Rule D** (`identity/team_color.split_by_saturation_votes`, side agent's
measured winner): per CAMERA a 1-D two-means on every detection's torso
SATURATION; each detection votes; a track's label is the majority. The
higher-saturation cluster is the coloured kit in both cameras (centres
44/141 sideline, 55/150 endzone on every play so far), so one label means
one kit in both views without a global fit. Per detection, the label is
2.3 % wrong at margin 0.4 (`|S - mid| / (hi - lo)`) over 83 % of the boxes
(sideline 2.1 %, endzone 4.6 %).

**The kit decides the roster** (`08c --saturated KC`, pipeline `RED`): the
number is looked up on the kit's roster; a number unique to the OTHER roster
no longer names the player (the OCR is 75 % per track and a wrong name
paints a wrong number). From cache on plays 1, 2, 4: 31 / 27 / 38 named
of 106 / 85 / 82, the kit overruling the number on 4 / 2 / 7 ids, mostly
one-digit reads (#0, #1, #3). The roster vote (numbers unique to a roster)
"disagrees" on the white cluster on every play -- it rests on 0-2 reads, and
is printed as a check only.

**What it exposed.** Of the ids seen by both cameras, 24 %, 53 % and 30 %
(plays 1, 2, 4) wear DIFFERENT kits in the two views: the per-frame pairing
in `08b` joined different players (play 2 id 7: BAL #44 white on the
sideline, a KC red jersey in the endzone, `diag/kit_play_002_id7.png`), and
some sideline tracks switch players mid-track (play 1 id 5,
`diag/kit_play_001_id5.png`). Every later stage inherited it: triangulation
across two people (why only 23-28 % of joints pass the gates on plays 2 and
4), names on the wrong body, 5-7 pieces per player.

**The fix in 08b** (`tracking/kits.py`, commit d74f3b7): each box carries a
signed saturation margin; `fuse_frame` refuses a cross-kit pair; the fused
points carry the kit into `link3d` as labels (which it already gates on: a
track votes its label, a detection never joins a known mismatch);
`tracks.parquet` gains `kit_margin` and `kit`, and identity's `team_votes`
reads them. `--no-kit-link` keeps the pairing gate only. NOT yet run end to
end (the GPU was on play 5): the first run is play 2 against its current
`tracks.parquet` -- ids disagreeing across cameras, track count,
triangulated joints passing, names. The earlier "labels in the linker are
worse" dead end used the balanced HSV split that carried no information;
`07j` has a fourth variant (`kits`, margin 0.4) re-measuring it on the
helmet set.

**Play 5** (047/048, BAL 30): the paint judge's grid limit was missed by 2
px (27 vs 25) with both rulers agreeing at 0.95 and players 1.72 m, so
`08 --max-grid-px` (pipeline `GRID_PX`) widens it for one play, printed
with the verdict; the check stage then passed on two of three (numerals
0.983, LOS ok, hashes 1.043) and the footage field landed on the drawn one
(logo on the 50, faint yard lines on the drawn lines).

## One roster player, one avatar at a time (2026-09-08)

The identity cache on v16 carried four names on two overlapping ids each:
"Harrison Butker" (#7 -- the kicker, on a 2nd-and-20) on ids 16 and 17
for 616 frames, Isiah Pacheco (#10) on 5 and 37 for 278, Marquise Brown
(#5) on 53 and 89, Nelson Agholor on 79 and 82. 08c names every id on its
own from its jersey vote, so two tracks that both read "7" are both the
kicker, and the render draws him twice. The vote counts behind a winner
were only logged (`vote_jersey_numbers`), so nothing could rank the two
claims. Now: `jersey_votes_win` / `jersey_votes_total` per row (future
runs), `scripts/08j_jersey_votes.py` for a play whose cache predates them
(the OCR re-voted on the current global ids -- no re-pairing, the pose
caches keyed by id stay valid -- into `jersey_votes.json`), and
`identity.exclusive.exclusive_names` in 08c after `merged` is built: among
ids claiming the same (team, jersey) with overlapping spans the strongest
vote keeps the name, the others lose it (jersey 0, `P<id>`, kit kept); a
tie within 1.5x names neither, since a wrong name is the worse defect.
Play 1 (08j on the CPU, 5 min: 32 (cam, id) keys read a number, the
re-vote agrees with the cached winner on 30): four ids lost a shared
name -- 37 (Pacheco, kept 5), 17 (Butker, kept 16), 89 (Brown, kept 53),
79 (Agholor, kept 82); 22 named. The kept "Butker" is still the kicker on
a 2nd-and-20: `specialist_veto` (K, P, LS unnamed unless `--kicking-play`)
takes that one too.

## Builds by role, and one id that held two men (2026-09-10)

The user asked two things of v28: fix "joint overlap / player confusion" by giving
each player a fixed set of joints traced frame to frame (occluded ones inferred from
SMPL-X's priors), and explain why a defensive lineman and a cornerback come out the
same body. Both were measured before anything was built.

**Builds.** The roster build (height -> beta 0, weight -> beta 1 via mesh volume)
reached only the ids the jersey OCR named; unnamed "P<id>" bodies were 1.85 m with
no weight. `identity/roles.py` + `scripts/08n_role_builds.py` read the role off the
pre-snap formation: the snap is the first frame after which fewer than 40 % of the
bodies stand still for 12 frames (play 1: 300); the formation is set where 70 % stand
still (62); the line of scrimmage is the midpoint of the two teams' crouched lines
(x = -24.0 m; the play's BAL 24 is -23.8). Offence on the line: the five distinct
bodies nearest the formation's centre (two ids within 0.7 m are one body) are the OL,
a stance beyond them a TE, else WR; an upright body on or just behind the line within
2.5 m of centre is the passer; the backfield within 7 m is RB (QB if on the centre's
line and standing). Defence: a stance on the line = DL, standing on the line within
9 m = LB (edge / walked-up), second level within 4 m of centre = LB, else DB; a
defender more than 0.8 m past the ball is mis-teamed (no role). Named ids take their
roster position; a track that starts within 90 frames of a same-team roled track's
end, within 2.5 m + 0.06 m/frame of where it ended, inherits its role if it beats the
runner-up by 1 m. Builds are the KC/BAL 2024 medians (OL 1.96/143 kg, DL 1.91/134,
LB 1.88/107, DB 1.83/91, WR 1.83/89, TE 1.96/111, RB 1.78/98, QB 1.87/96), written
into identity_resolved.pkl (frozen dataclass: `dataclasses.replace`), which both 05p
and the timeline read. Play 1 v30: 26 roles from the formation, 28 from the roster,
9 inherited, 31 unnamed ids built. Known limits: with a lineman hidden behind the
centre the tight end is the fifth body (OL build, 32 kg over); adjacent linemen are
0.3 m apart laterally in the sideline ground points, so duplicate tracks on one
lineman look like two bodies.

**Confusion, measured.** A ruler (`scratchpad/kp_conflict.py`): project every
fitted body's joints into the camera and count detected keypoints that sit within
12 px of ANOTHER body's same or mirrored joint while more than 8 px from their own.
Sideline: 0.1 % of 57k keypoints (0.5 % near another body at all); endzone 0.5 %.
The runner's occluded 262-268 has no stolen keypoints: it is occlusion. The user's
per-player joint set is what the per-box detector + temporal term already give; the
prediction-gated assignment was NOT built because there is nothing for it to fix at
the keypoint level. One outlier: id 17 had 28 % (sideline) / 34 % (endzone) of its
keypoints more than 40 px from its own fit.

**The outlier was an identity merge.** The v28 strip for 17 at 190-211 shows the drawn
body on the quarterback's keypoints at the centre's place: sideline id 17 held the
centre AND the quarterback standing 0.7 m behind him for 165 frames (old sideline 16
merged into 17 by the lag -15 re-pairing), plus two short fragments; sideline 21 and
15 and endzone 3, 17, 42 likewise (1883 duplicate rows, keypoint sets of 22-25 rows
that 05p skips). The greedy loop's continuation waiver ("the same person within 1 m")
let both sideline tracks hold the endzone centre track and the union-find merged
them; the fit then sat 46-59 px between the two bodies through 142-374, and the edge
cross-fade dragged even the one-view frames onto the centre's placement.
`global_ids_checked` (tracking/pair_by_appearance.py) refuses a union that would put
two same-camera tracks overlapping in time beyond a short continuation (45 frames,
half the shorter span) into one id; 08i prints the drops (play 1: 4). Re-running the
repair needs the `*_oldids` caches (they carry tracks_oldpair.parquet's ids; the live
caches' merged ids cannot map back by boxes): `08i --keypoints keypoints_2d_oldids.parquet
--keypoints-ids tracks_oldpair.parquet`, copy the oldids caches into place, `08m --old
tracks_oldpair.parquet` (scratchpad `p1_v30_repair.sh`). After it: 0 oversized keypoint
sets, 50 duplicate rows (continuations), the centre a crouched body at the line, the
quarterback his own chain (16 -> 22 -> 33 -> 49). The veto also keeps genuine duplicate
tracks (two tracker ids on one lineman) apart; that is the linker's problem, to be
fixed by box overlap, not ground distance, and measured by bodies drawn vs boxes.

**Versions.** v29 = v28b + role builds (poses only; runner strip unchanged). v30 =
v29 + the vetoed re-pairing (fits running at the time of writing).

## 2026-09-25 05:40 -- a v111 regression found and fixed: the centre's role (v112 renders)

The ball path (08y) and the loader's quarterback-under-centre hold both take the centre as the role-OL id nearest the
mean across of the role-OL ids at the snap. Folding 17 (role OL) into 204 dropped 17's role and 204 (Humphrey) had
none, so both picked 139 (Thuney): the v111 render has the pre-snap ball in Thuney's hands and ball.json lost 150 frames
(251 of 401). The role list was polluted besides: Kelce (11) was OL, the left tackle (37) and Trey Smith (76) had no
role. Fixed in identity_resolved.pkl (play_001 and play_copy; backup *.pre_role204): 11 = TE, 37 / 76 / 204 = OL.
08y now: centre 204, 401 frames. NOTE for any fold: carry the dropped id's ROLE to the kept id -- 08z pops the dropped
id's roles entry. The QB hold still takes out 146 pre-snap frames of 139 (Thuney's pre-snap sideline track): the
same frames it took out of 204 in v110, so not new; whether t25's early pre-snap rows are Thuney or the quarterback is
open. The id-19 "P19" (jersey 67, role OL) stands 0.5 m from #76 at the snap: a probable twin, open.
v111's viewer (Version 27) used the earlier ball file (401 frames) and is unaffected. v112 = v111 + the roles: export
and render running.
