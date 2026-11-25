---
type: decision
status: accepted
date: 2026-09-10
source: docs/HANDOFF.md, "What has been measured and rejected" (recorded 2026-11-24)
---

# 0005: Don't merge twin tracks by box geometry

## Decision

Two track IDs are not merged because their boxes overlap. From the sideline, players in a line stack in the image, so box geometry cannot tell a duplicate from two men.

## Evidence

Word for word from HANDOFF.md. Re-propose only with new evidence.

- **Merging "twin" tracks by box geometry (2026-09-10, play 1, sideline):**
  three ids look like one body under two ids (16 & 22 the quarterback,
  18 & 19, 21 & 28), so two avatars stand on one man. A rule of "box centres
  within 0.25 box heights and IoU >= 0.4 over 20+ common frames" catches them
  -- and also catches 14 & 27, which the footage shows to be TWO Baltimore
  players one behind the other (gap 0.19 heights, IoU 0.66). From the sideline
  the line of scrimmage is seen end-on, so bodies stack in the image at every
  depth: box geometry cannot tell a duplicate from two men in a line, and the
  ankle ground points do not separate them either (16 & 22 sit 0.96 m apart,
  the genuine pair 14 & 27 1.28 m). The one test that did separate them is
  the KEYPOINTS: 16 & 22 agree to 8 px (0.05 box heights), 18 & 19 to 50 px
  (0.40) -- but the pose detector's own suppression emits keypoints for only
  one of a twin pair on all but 3-4 frames, so the test almost never fires.
  Not adopted. Anything built here must be judged on bodies drawn vs bodies
  in the footage, per `corrections-must-beat-what-they-correct` (memory note, not in the repo), and the
  v16 duplicate rule (ground distance) is the cautionary case.

## Related

- **Concepts:** [Tracking](../Concepts/tracking.md)
- **Findings:** [Tracking and pairing](../Findings/tracking-and-pairing.md)
