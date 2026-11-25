---
type: decision
status: accepted
date: 2026-09
source: docs/HANDOFF.md, "What has been measured and rejected" (recorded 2026-11-24)
---

# 0009: Don't refine per-frame cameras to the yard lines alone

## Decision

Per-frame camera refinement does not use the yard lines alone. Near-parallel lines trade rotation against focal length, so it needs priors, a reject threshold and smoothing.

## Evidence

Word for word from HANDOFF.md. Re-propose only with new evidence.

- Per-frame camera refinement to the yard lines alone: the pencil of near-parallel
  lines trades rotation about their direction against focal length; it needs
  priors, a 3 deg / 20% reject and along-track smoothing, or it wanders 2 deg.

## Related

- **Concepts:** [Cameras](../concepts/cameras.md)
- **Findings:** [Cameras and clip sync](../findings/cameras-and-sync.md)
