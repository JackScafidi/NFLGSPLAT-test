---
type: concept
kind: object
status: partly located
updated: 2026-11-24
---

# Ball

Where the ball is on every frame, and who holds it.

**Goal object** · status: **partly located**

## Today

- Not detected. `scripts/08y_ball_path.py` places it from the bodies: at the centre's hands before the snap, with the quarterback, a ballistic arc from release to catch, then with the carrier.
- The release and catch frames are typed in by hand.

## Where in the code

- `scripts/08y_ball_path.py`: the ball's path from bodies and events
- `scripts/09a_ball_in_film.py`, `nfl_gsplat/tracking/ball_film.py`: the ball read in the footage
- `nfl_gsplat/ball/`: detector and 3D Kalman code
- `nfl_gsplat/render/ball.py`: drawing it

## Notes

- **Findings:** [Ball and play events](../Findings/ball-and-play-events.md), [Render and viewer](../Findings/render-and-viewer.md)
- **Related:** [Play events](play-events.md), [Hands](hands.md), [Render and viewer](render-and-viewer.md)

## Next

Write events to the play data; measure the detector where the ball is visible. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
