---
type: concept
kind: measure
status: in use
updated: 2026-11-24
---

# Footage review

Checking the drawn bodies against the real footage, frame sequence by frame sequence. The final judge: a ruler that disagrees with the film is replaced.

**Measure** · status: **in use**

## Today

- Overlays of the drawn body on the real player in both cameras, and strips of consecutive rendered frames.
- Described as the standing loop in the [working method](../Reference/working-method.md).

## Where in the code

- `scripts/05q_overlay_footage.py`: the body over the footage
- `scripts/09b_film_strip.py`, `09c_track_audit.py`

## Notes

- **Findings:** [Rulers](../Findings/rulers.md), [Tracking and pairing](../Findings/tracking-and-pairing.md), [Render and viewer](../Findings/render-and-viewer.md), [Ball and play events](../Findings/ball-and-play-events.md), [Pipeline runs and versions](../Findings/pipeline-and-versions.md)
- **Related:** [Plausibility rulers](plausibility-rulers.md), [Tracking](tracking.md)

## Next

Keep it, beside a ground-truth benchmark (the helmet dataset). See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
