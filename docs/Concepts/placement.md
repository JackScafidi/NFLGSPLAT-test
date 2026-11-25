---
type: concept
kind: stage
status: working
updated: 2026-11-24
---

# Placement

Where each body stands on the field on every frame: ground points, depth along a camera's line of sight, who is drawn and how gaps are bridged.

**Pipeline stage** · status: **working**

## Today

- Two-camera bodies stand at their triangulated position; one-camera bodies at their box bottom.
- Rules decide who is drawn (edge-clipped, endzone-only, duplicates) and fill short gaps.
- These rules live in `nfl_gsplat/render/`, though they decide positions, not looks.

## Where in the code

- `nfl_gsplat/render/play_timeline.py`, `timeline.py`, `depth_snap.py`, `edge_rule.py`, `endzone_only_rule.py`, `pair_rule.py`
- `nfl_gsplat/pose/place_on_field.py`

## Notes

- **Findings:** [Placement](../Findings/placement.md), [Tracking and pairing](../Findings/tracking-and-pairing.md), [Rulers](../Findings/rulers.md)
- **Decisions:** [0007: Keep the box bottom as the one-view ground point](../Decisions/0007-box-bottom-is-the-one-view-ground-point.md)
- **Related:** [Player body](player-body.md), [Feet](feet.md), [Census](census.md), [Play data](play-data.md)

## Next

Move the placement rules into Layer 1 so their output is play data. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
