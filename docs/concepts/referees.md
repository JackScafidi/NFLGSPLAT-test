---
type: concept
kind: object
status: not located
updated: 2026-11-24
---

# Referees

Where each official is: they are on the field and occlude players.

**Goal object** · status: **not located**

## Today

- Officials on the field are not tracked as separate bodies; the detector and linker fold them in.
- Boundary staff and the sideline official are excluded by position and shirt stripes.
- They render as one generic striped-shirt avatar.

## Where in the code

- `nfl_gsplat/identity/officials.py`: telling officials apart
- `nfl_gsplat/avatars/generic_assets.py`: the generic avatar
- `nfl_gsplat/render/offfield_rule.py`: who is left off the field

## Notes

- **Findings:** [Rulers](../findings/rulers.md), [Identity and teams](../findings/identity-and-teams.md)
- **Decisions:** [0008: Don't find officials by shirt stripes alone](../decisions/0008-officials-not-by-shirt-stripes.md)
- **Related:** [Identity](identity.md), [Tracking](tracking.md)

## Next

Track officials as their own objects with a pose, like players. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
