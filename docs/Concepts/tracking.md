---
type: concept
kind: stage
status: working
updated: 2026-11-24
---

# Tracking

Detecting people in each view, following them through time, and pairing a sideline track with the endzone track of the same person.

**Pipeline stage** · status: **working**

## Today

- YOLO detections in both views, linked on the field into tracks.
- Pairing across cameras is at its ceiling for what both cameras see; 9 to 10 of 22 players are paired per frame.
- Many fixes are folds of two IDs into one, made by hand on the footage.

## Where in the code

- `nfl_gsplat/tracking/`: `detect_track.py`, `link3d.py`, `pair_by_appearance.py`, `twins.py`, `fold.py`, `gap_fill.py`
- `scripts/08b`, `08i`, `08k`, `08o`, `08q`, `08r`, `08s`, `08z`: export, pairing, splits, twins, gap fill, folds

## Notes

- **Findings:** [Tracking and pairing](../Findings/tracking-and-pairing.md), [Identity and teams](../Findings/identity-and-teams.md), [Placement](../Findings/placement.md)
- **Decisions:** [0005: Don't merge twin tracks by box geometry](../Decisions/0005-dont-merge-twin-tracks-by-box-geometry.md), [0006: Don't pair cameras by the regressor's body pose](../Decisions/0006-regressor-pose-is-not-a-pairing-cue.md)
- **Related:** [Identity](identity.md), [Placement](placement.md), [Footage review](footage-review.md)

## Next

Record manual folds in a per-play corrections file and replay them on every run. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
