---
type: decision
status: accepted
date: 2026-09-08
source: docs/HANDOFF.md, "What has been measured and rejected" (recorded 2026-11-24)
---

# 0006: Don't pair cameras by the regressor's body pose

## Decision

The pose regressor's body pose is not used on its own to pair sideline and endzone tracks. It picks the true partner 18 % of the time. The helmet dataset is the test bed if it is ever revisited.

## Evidence

Word for word from HANDOFF.md. Re-propose only with new evidence.

- **The regressor's body pose as a cross-camera pairing cue (2026-09-08,
  play 1, 85 common posed frames, 885 same-id pairs vs 47k other-id):**
  pelvis-relative joint distance same p50 0.109 m, other p50 0.130, 30 % of
  others below the same-median; the nearest endzone pose is the true
  partner 18 % of the time (chance 4 %). A weak cue on its own; untested
  in combination with the position gate, and there is no pair truth on
  play 1 to test it with (the helmet set has both views labelled -- the
  instrument if this is ever pursued).

## Related

- **Concepts:** [Tracking](../Concepts/tracking.md), [Pose](../Concepts/pose.md)
- **Findings:** [Tracking and pairing](../Findings/tracking-and-pairing.md), [Pose](../Findings/pose.md)
