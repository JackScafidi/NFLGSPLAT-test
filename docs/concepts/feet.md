---
type: concept
kind: object
status: partly located
updated: 2026-11-24
---

# Feet

Where each player's feet are: they anchor the body to the turf and decide where a player stands.

**Goal object** · status: **partly located**

## Today

- Ankles only; no heel or toe points.
- A foot-lock rule keeps planted feet still; a gait model drives the legs.
- Ankle rays from the two cameras are the test for whether a pair of tracks is one player.

## Where in the code

- `nfl_gsplat/render/foot_lock.py`, `nfl_gsplat/render/gait.py`, `nfl_gsplat/render/stance.py`
- `nfl_gsplat/pose/keypoint_filter.py`: keypoint clean-up, including left/right flips

## Notes

- **Findings:** [Rulers](../findings/rulers.md), [Render and viewer](../findings/render-and-viewer.md), [Ball and play events](../findings/ball-and-play-events.md), [Tracking and pairing](../findings/tracking-and-pairing.md), [Pose](../findings/pose.md), [Cameras and clip sync](../findings/cameras-and-sync.md)
- **Decisions:** [0007: Keep the box bottom as the one-view ground point](../decisions/0007-box-bottom-is-the-one-view-ground-point.md), [0010: Don't refine the endzone camera to its own paint](../decisions/0010-endzone-camera-not-refined-to-its-paint.md), [0011: Don't set the endzone pitch from the ankle ruler alone](../decisions/0011-endzone-pitch-not-from-ankle-ruler.md)
- **Related:** [Pose](pose.md), [Placement](placement.md), [Player body](player-body.md)

## Next

Add heel and toe points from a whole-body detector and check them against the foot lock. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
