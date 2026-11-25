---
type: concept
kind: stage
status: not built
updated: 2026-11-24
---

# Play data

Layer 1's single output: one versioned folder per play locating every object on every frame, with how each value was obtained. The render and viewer read nothing else.

**Pipeline stage** · status: **not built**

## Today

- Not built. Today a play's results are spread over stage files: `cameras.npz`, `tracks.parquet`, `poses_*.json` (Python pickles), `identity_resolved.pkl`, `ball.json`.
- The format is proposed in the Foundations plan (the Layer 1 output section).

## Where in the code

- Not built yet. Its inputs are written by `scripts/08b_export_play_dir.py`, `05f`, `05p`, `08c` and `08y`.

## Notes

- **Findings:** [Pipeline runs and versions](../findings/pipeline-and-versions.md)
- **Decisions:** [0002: Layers 1 and 4 first](../decisions/0002-layers-1-and-4-first.md)
- **Related:** [Player body](player-body.md), [Ball](ball.md), [Play events](play-events.md), [Render and viewer](render-and-viewer.md)

## Next

Write the format down, export play 1 into it, and make Layer 4 read only it. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
