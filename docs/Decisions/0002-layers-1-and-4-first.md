---
type: decision
status: accepted
date: 2026-11-24
---

# 0002: Build Layer 1 and Layer 4 first

## Context

The project has four layers: 1 extraction (video to play data), 2 a store
across many plays, 3 an analysis library, 4 viewing (3D render and viewer).
Today the output is a rendered video, and no single data file describes a play.

## Decision

Work on Layer 1 and Layer 4 first. Layers 2 and 3 are added as the project
grows. Layer 1's output is one versioned set of play data, and Layer 4 reads
only that.

## Consequences

- The play data format is designed now, so Layers 2 and 3 need no rework.
- Rules that decide where bodies are move out of `nfl_gsplat/render/` and into
  Layer 1.
- See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).

## Related

- **Concepts:** [Play data](../Concepts/play-data.md), [Render and viewer](../Concepts/render-and-viewer.md)
- **Findings:** [Pipeline runs and versions](../Findings/pipeline-and-versions.md)
