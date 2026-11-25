---
type: concept
kind: object
status: partly located
updated: 2026-11-24
---

# Hands

Where each player's hands are: needed for ball possession, blocks and tackles.

**Goal object** · status: **partly located**

## Today

- Wrists only. The keypoint detector (YOLOv8-pose, 17 COCO points) has no hand points.
- SMPL-X hand poses are set to zero in the render.
- The ball is placed in the carrier's hands from the body, not from detected hands.

## Where in the code

- `nfl_gsplat/pose/coco.py`: the 17 COCO keypoints and their SMPL-X mapping
- `nfl_gsplat/render/carry.py`: the ball held by the carrier
- `nfl_gsplat/render/play_timeline.py`: hand poses set to zero

## Notes

- **Findings:** [Pose](../findings/pose.md), [Ball and play events](../findings/ball-and-play-events.md), [Rulers](../findings/rulers.md)
- **Related:** [Pose](pose.md), [Ball](ball.md), [Player body](player-body.md)

## Next

Try a whole-body keypoint detector (hand points); define a hand-centre point with a confidence. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
