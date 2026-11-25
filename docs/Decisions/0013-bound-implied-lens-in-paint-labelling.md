---
type: decision
status: accepted
date: 2026-09-05
source: docs/HANDOFF.md, "What has been measured and rejected" (recorded 2026-11-24)
---

# 0013: Bound the paint reader's implied lens to the seed play's

## Decision

The paint reader's row labelling may not imply a lens outside 1/1.6 to 1.6 times the seed play's (fixed in dd1b95c). A labelling's fit to its own lines never outranks a plausible lens.

## Evidence

Word for word from HANDOFF.md. Re-propose only with new evidence.

- The paint reader's row labelling with two rows only (2026-09-05, diagnosed
  by drawing the correspondences, `diag/play3_corr_394.png`): the far
  sideline's yard ticks and the far hash row get labelled as the two sidelines
  (+24.38 / −24.38), a 2.3× cross-field stretch and a 41° lens, while grid
  consistency, an x-instrument, still scores 0.95 and the ladder is right
  (consecutive 5-yd lines). Four-row frames label correctly and give the 12°
  the boxes ask for; the pooled candidate was the compromise (25°, players
  2.78 m), and play 4's rulers disagreement (hashes 1.82 vs numerals 0.99) was
  the same stretch. Fixed in dd1b95c by bounding the implied lens to the seed
  play's (×1/1.6..1.6) inside `assignment_is_possible`; a labelling's fit to
  its own lines never ranks above a plausible lens again.

## Related

- **Concepts:** [Cameras](../Concepts/cameras.md)
- **Findings:** [Cameras and clip sync](../Findings/cameras-and-sync.md)
