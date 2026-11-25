---
type: decision
status: accepted
date: 2026-09-05
source: docs/HANDOFF.md, "What has been measured and rejected" (recorded 2026-11-24)
---

# 0012: Don't seed the joint solve with another play's mount

## Decision

The camera joint solve is not seeded with another play's camera mount and left to run. On play 3 the fault was upstream of the solver (decision 0013).

## Evidence

Word for word from HANDOFF.md. Re-propose only with new evidence.

- Seeding the joint solve with another play's mount and letting it run
  (2026-09-05, 5e2a833): on play 3 the paint asks for a 21–53° lens from the
  seeded mount while the boxes say 12°; holding the centre there did not
  rescue it. The fault was upstream of the solver (next entry).

## Related

- **Concepts:** [Cameras](../concepts/cameras.md)
- **Findings:** [Cameras and clip sync](../findings/cameras-and-sync.md)
