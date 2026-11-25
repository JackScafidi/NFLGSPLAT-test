---
type: concept
kind: stage
status: partly working
updated: 2026-11-24
---

# Play events

The moments that structure a play: snap, handoff or release, catch, tackle, whistle.

**Pipeline stage** · status: **partly working**

## Today

- The snap and the end of the play are found from the bodies (`scripts/08x_play_end.py`).
- The release and catch frames are typed in by hand for the ball path.

## Where in the code

- `scripts/08x_play_end.py`: when the play is dead
- `scripts/08y_ball_path.py`: release, catch and carry

## Notes

- **Findings:** [Ball and play events](../findings/ball-and-play-events.md), [Pipeline runs and versions](../findings/pipeline-and-versions.md)
- **Related:** [Ball](ball.md), [Play data](play-data.md)

## Next

Write events to `events.json` in the play data, each marked detected or manual. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
