---
type: decision
status: accepted
date: 2026-09-05
source: docs/HANDOFF.md, "What has been measured and rejected" (recorded 2026-11-24)
---

# 0010: Don't refine the endzone camera to its own paint

## Decision

The endzone camera is not refined to its own painted lines. The paint fit improved but the feet refused it, so nothing was applied.

## Evidence

Word for word from HANDOFF.md. Re-propose only with new evidence.

- The endzone camera refined to its own paint (2026-09-05, 623eab0, kept as
  `08e --cam endzone --orient-tol 25 --out`): the paint improves (play 1
  median grid 39 → 23 px) and the feet refuse it -- triangulated lower ankle
  p10 −0.01 → −0.45 m, ray agreement 7.3 → 10.2 px, joints passing the gate
  47699 → 9291. The endzone's paint at 23–27 px is not a ruler the geometry
  trusts, and its residual is not in rotation and focal. Two rulers, one
  disagreed, nothing applied. `cameras_endzone_refined.npz` is the record.

## Related

- **Concepts:** [Cameras](../Concepts/cameras.md), [Feet](../Concepts/feet.md), [Reprojection error](../Concepts/reprojection-error.md)
- **Findings:** [Cameras and clip sync](../Findings/cameras-and-sync.md)
