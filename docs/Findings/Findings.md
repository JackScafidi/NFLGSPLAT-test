---
type: index
updated: 2026-11-24
---

# Findings

What was tried and measured, grouped by subject. Each note keeps its entries word for word, dated, oldest first. New findings go in a dated [journal](../Journal/Journal.md) note; a finding that settles a question also gets a [decision](../Decisions/Decisions.md).

| Subject | Covers | Entries |
| --- | --- | --- |
| [Cameras and clip sync](cameras-and-sync.md) | How the sideline and endzone cameras are solved on every frame, and how the two clips are lined up in time | 5 |
| [Tracking and pairing](tracking-and-pairing.md) | Detections, tracks, and which sideline track and endzone track are the same person: pairing, folding two IDs into one, and splitting one ID that holds two people | 18 |
| [Identity and teams](identity-and-teams.md) | Who each track is: team from kit colour, jersey number, roster name and position role | 5 |
| [Placement on the field](placement.md) | Where each body stands on every frame: ground points, depth along a camera's line of sight, who is drawn, and how gaps are bridged | 9 |
| [Pose](pose.md) | Each body's joints: 2D keypoints, triangulation, SMPL-X refits, priors and fine-tuned detectors | 9 |
| [Ball and play events](ball-and-play-events.md) | The snap, the release and the catch, the ball's path, and when the play is dead | 4 |
| [Render and viewer](render-and-viewer.md) | The 3D render and the browser viewer: first-person view, gear and the stadium backdrop | 5 |
| [Rulers (how results are measured)](rulers.md) | The measurements used to judge a change: plausibility rulers, the count of bodies per team (census), overlays, and the footage as the final judge | 5 |
| [Pipeline runs and versions](pipeline-and-versions.md) | Pipeline runs and stage order, and play 1's version history with each version's measured state | 22 |

## Every entry, in date order

| Date | Entry | Subject |
| --- | --- | --- |
| 2026-09-04 | Current state (2026-09-04) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-05 | The endzone camera track invents motion; the pairing is the wound (2026-09-05, later) | [Cameras and clip sync](cameras-and-sync.md) |
| 2026-09-05 | Play 1 v8 (2026-09-05 19:32): kits from the saturation vote | [Identity and teams](identity-and-teams.md) |
| 2026-09-05 | Kits: the team from saturation votes, and what it exposed (2026-09-05) | [Identity and teams](identity-and-teams.md) |
| 2026-09-06 | 08h works once the camera-from-homography step is a ray fit (2026-09-06/07) | [Cameras and clip sync](cameras-and-sync.md) |
| 2026-09-07 | One avatar per sideline track; the pairing stays ambiguous (2026-09-07) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-07 | The 42 % triangulation figure has a structural ceiling (2026-09-07) | [Pose](pose.md) |
| 2026-09-07 | Who is drawn: four exclusion rules, and v10's order (2026-09-07) | [Placement on the field](placement.md) |
| 2026-09-07 | Play 1 v9 and v10 delivered (2026-09-07) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-07 | The pipeline's stage order since feabdfc (2026-09-07) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-07 | v11: the script end to end, and what the fresh run taught (2026-09-07 evening) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-08 | v11, v12, v13: the endzone track decided by triangulation (2026-09-08) | [Cameras and clip sync](cameras-and-sync.md) |
| 2026-09-08 | v15: the one-view bodies refit to the keypoints (2026-09-08) | [Pose](pose.md) |
| 2026-09-08 | v16: the duplicate rule was eating six players a frame (2026-09-08) | [Placement on the field](placement.md) |
| 2026-09-08 | v18: the two-view bodies shook; the fused refit damped (2026-09-08) | [Pose](pose.md) |
| 2026-09-08 | v19: the one-view fill-in popped at every triangulation gap (2026-09-08) | [Pose](pose.md) |
| 2026-09-08 | v20: the timeline anchored the model's origin, 0.35 m from the pelvis (2026-09-08) | [Placement on the field](placement.md) |
| 2026-09-08 | The sideline camera through the rendered span (2026-09-08) | [Cameras and clip sync](cameras-and-sync.md) |
| 2026-09-08 | v21: a wrong pair sawtoothed by a metre a frame (2026-09-08) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-08 | v23: the user's four notes on v22 (2026-09-08 evening) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-08 | One roster player, one avatar at a time (2026-09-08) | [Identity and teams](identity-and-teams.md) |
| 2026-09-09 | The footage as the ruler (2026-09-09) | [Rulers (how results are measured)](rulers.md) |
| 2026-09-09 | The endzone camera was never on its paint; the clips are 15 frames apart (2026-09-09, evening) | [Cameras and clip sync](cameras-and-sync.md) |
| 2026-09-10 | Builds by role, and one id that held two men (2026-09-10) | [Identity and teams](identity-and-teams.md) |
| 2026-09-10 | The cameras' ankle RAYS, not their ground points, say whether a pair is right (2026-09-10) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-10 | Two ids on one body: the feet tell, the boxes do not (2026-09-10) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-10 | Where play 1 stands at v31 (2026-09-10, late) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-11 | The endzone overlay, and what it showed (2026-09-11) | [Rulers (how results are measured)](rulers.md) |
| 2026-09-11 | Counting bodies per team: the ruler, and what it says (2026-09-11) | [Rulers (how results are measured)](rulers.md) |
| 2026-09-11 | v34: the gap fill lands, and the count turns out to be fragmentation (2026-09-11) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-12 | The census metric was scoring the aftermath (2026-09-12) | [Rulers (how results are measured)](rulers.md) |
| 2026-09-12 | v38: every join trimmed to the frames its rays agree, and it wins on all three rulers (2026-09-12) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-12 | v37: two re-pairings, and the census finally moves (2026-09-12) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-12 | ground_positions keyed by the TRACKER's id, not the player's (2026-09-12) | [Placement on the field](placement.md) |
| 2026-09-12 | v36: the four pairings applied, and they pay in metres (2026-09-12) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-12 | The ruler was blind, and the gate preferred it (2026-09-12) | [Rulers (how results are measured)](rulers.md) |
| 2026-09-17 | 2026-09-17 (overnight): the clip ends when the play is dead; a gait for the legs | [Ball and play events](ball-and-play-events.md) |
| 2026-09-17 | 2026-09-17 (evening): the snap was never at 300 -- RETRACTION of the live window and the clip end | [Ball and play events](ball-and-play-events.md) |
| 2026-09-18 | 2026-09-18 (morning): the ball, and the quarterback under centre | [Ball and play events](ball-and-play-events.md) |
| 2026-09-18 | 2026-09-18 (afternoon): the ball went to the WRONG MAN -- RETRACTION of "receiver 77", "out of bounds", "touchdown" | [Ball and play events](ball-and-play-events.md) |
| 2026-09-19 | 2026-09-19 (evening): players vanishing in the pocket -- a man who vanishes stands still | [Placement on the field](placement.md) |
| 2026-09-19 | 2026-09-19 (night): the endzone camera's depth is a BIAS, not a wander -- taken out of endzone-only placements (v85) | [Placement on the field](placement.md) |
| 2026-09-20 | 2026-09-20 (00:30): the KC 12th man on the right of the line -- three ids on two men, folded on the film (v86) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-20 | 2026-09-20 (03:00): a white ghost on the centre -- the nose tackle's second id -- and the lock's gate made honest (v87) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-20 | 2026-09-20 (morning): the viewer, and the detector holes measured -- one new track, no missing Raven | [Render and viewer](render-and-viewer.md) |
| 2026-09-21 | 2026-09-21 (01:30): the Ravens' count -- every candidate for the eleventh man, checked and named | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-21 | 2026-09-21 (02:40): the left of the KC line -- two men, four crossed ids, and a fold per camera (v89) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-21 | 2026-09-21 evening -- the two missing Ravens after 434 were in the tables (v90 in progress) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-21 | 2026-09-21 21:40 -- v92: the film-true ids, measured first on a scratch copy, then ported (render launched) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-22 | 2026-09-22 -- the user's next three asks: natural motion, gear/textures, first-person view | [Render and viewer](render-and-viewer.md) |
| 2026-09-22 | 2026-09-22 (machine clock ~13:00-15:00) -- first-person gaze, the receiver's id, the motion rulers' first two mechanisms, gear | [Render and viewer](render-and-viewer.md) |
| 2026-09-24 | 2026-09-24 05:30 -- the copy's census loss explained: the fine-tune's confidence head collapsed on the endzone | [Pose](pose.md) |
| 2026-09-24 | 2026-09-24 16:10 (machine clock; the stamps from ~11:00 to 16:00 above ran ahead of it) -- label rules reverted | [Pose](pose.md) |
| 2026-09-24 | 2026-09-24 16:45 -- first-person POV (the user: "can we figure out how we can do POVs better?") + a 05p bug | [Render and viewer](render-and-viewer.md) |
| 2026-09-24 | 2026-09-24 17:50 -- v108 = CURRENT BEST (film-checked on both cameras) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-24 | 2026-09-24 18:40 -- v109: the first-person spins were the bodies' (two pose-record rules), the eye, own arms | [Render and viewer](render-and-viewer.md) |
| 2026-09-24 | 2026-09-24 19:45 -- v109 = CURRENT BEST (rendered, film-checked on both cameras) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-24 | 2026-09-24 20:45 -- PAUSED (user powering off): v110 render stopped mid endzone view | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 00:15 -- v110 = CURRENT BEST (render finished after the power-off; film-checked on both cameras) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 00:50 -- ML status: VPoser in the fit re-measured (mixed, not shipped); the facing prior from BDB works | [Pose](pose.md) |
| 2026-09-25 | 2026-09-25 01:30 -- VPoser 0.005 (not shipped); a random film audit; the KC left line is still crossed in the endzone | [Pose](pose.md) |
| 2026-09-25 | 2026-09-25 03:05 -- the KC left line untangled on the copy (chain 2 measured; chain 3 = the port candidate, running) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-25 | 2026-09-25 04:10 -- v111 = v110 + the KC left line untangled + the bridge pose blend (ported; render running) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 05:15 -- v111 = CURRENT BEST (rendered, film-checked on both cameras) | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 05:40 -- a v111 regression found and fixed: the centre's role (v112 renders) | [Identity and teams](identity-and-teams.md) |
| 2026-09-25 | 2026-09-25 06:10 -- the pre-snap line answered on the film; a dead pre-snap fill found; the hole chain's outlier | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-25 | 2026-09-25 06:40 -- v112 reviewed; the hole chain and the pre-snap fill adopted; the endzone pose gap measured | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 07:30 -- the pre-snap KC line + quarterback fold PORTED (v113 tables); endzone regressor poses (flag) | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-25 | 2026-09-25 08:40 -- v113 = CURRENT BEST (rendered; film-checked); v114 rendering | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 09:35 -- v114 rendered (strips checked; camera views running); 05r measured for v115 | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 10:45 -- v115 (05r poses, pose only) rendering; a drawn cross-view ruler; two placement probes | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 11:15 -- v115 = CURRENT BEST (rendered; film-checked); viewer Version 30, write-up Version 18 | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 12:40 -- VPoser shift rejected; 05r's merged-box rule fixed (v116 rendering); the pipeline fits on ft2; gait vs lock; placemen... | [Pose](pose.md) |
| 2026-09-25 | 2026-09-25 13:45 -- v116 = CURRENT BEST (viewer Version 31); surges: two placement fixes measured; the gait stays; v117 identity fixes on... | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 14:50 -- PAUSED (power-off). Placement change committed (5ba0160, default ON); live tables = v116; v117 identity fixes on the... | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 22:35 -- deadline push (user: a good product in ~9 h): v117b rendering; kits from the film; sky staged | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-25 | 2026-09-25 23:35 -- v117b = CURRENT BEST (film-checked); stadium backdrop in (05k --sky, viewer); v118 = v117b + sky rendering | [Pipeline runs and versions](pipeline-and-versions.md) |
| 2026-09-26 | 2026-09-26 00:45 -- the late pile read on the film (v119 tables): #98 one id, Thuney on the ground, a ghost Raven gone | [Tracking and pairing](tracking-and-pairing.md) |
| 2026-09-26 | 2026-09-26 01:10 -- hidden feet: the short-box rule measured and rejected; v120 = v119 + stands that rise | [Placement on the field](placement.md) |
| 2026-09-26 | 2026-09-26 01:35 -- v121: Madubuike's depth read off the film; 11 v 11 on every frame from snap to whistle | [Placement on the field](placement.md) |
| 2026-09-26 | 2026-09-26 01:55 -- v122 = v121 + depth_snap.SPARE_MISSED on (f2d58ee): Ojabo on #90, the KC RG drawn pre-snap | [Placement on the field](placement.md) |
| 2026-09-26 | 2026-09-26 03:30 -- deadline deliverables: v122 published (showcase V5, write-up V20, Film Room V37) | [Pipeline runs and versions](pipeline-and-versions.md) |

Older results: [first end-to-end results](../RESULTS_first_end_to_end.md).
