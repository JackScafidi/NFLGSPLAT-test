---
type: concept
kind: stage
status: working
updated: 2026-11-24
---

# Identity

Who each track is: team from kit colour, jersey number, roster name and position role.

**Pipeline stage** · status: **working**

## Today

- Team from torso colour; jersey numbers by OCR votes over both views; names from the nflverse roster.
- Position roles from the pre-snap formation give unnamed players a height and weight.

## Where in the code

- `nfl_gsplat/identity/`: `team_color.py`, `jersey_vote.py`, `roster.py`, `roles.py`, `resolve.py`
- `scripts/08c_identity_all22.py`, `08f_team_by_colour.py`, `08n_role_builds.py`

## Notes

- **Findings:** [Identity and teams](../Findings/identity-and-teams.md), [Tracking and pairing](../Findings/tracking-and-pairing.md)
- **Decisions:** [0008: Don't find officials by shirt stripes alone](../Decisions/0008-officials-not-by-shirt-stripes.md)
- **Related:** [Tracking](tracking.md), [Referees](referees.md)

## Next

Take kit colours and the kicking-play flag from each play's settings, not environment variables. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
