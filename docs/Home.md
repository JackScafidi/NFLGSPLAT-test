---
type: index
updated: 2026-11-24
---

# NFLGSPLAT

Two synced broadcast clips of a play (sideline + endzone) in; a clean 3D
recreation and the location of every player's body, head, hands and feet, the
ball and the referees out, on every frame.

- **Where things stand:** [STATE.md](STATE.md)
- **What changes next:** the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz) (Claude doc)
- **How Claude works here:** [CLAUDE.md](../CLAUDE.md)

## Where things go

| Folder | What lives there | Index |
| --- | --- | --- |
| `concepts/` | The hubs: goal objects, pipeline stages and measures. Every other note links to the concepts it touches | [Concepts](concepts/Concepts.md) |
| `findings/` | What was tried and measured, by subject (cameras, tracking, identity, placement, pose, ball, render, rulers, versions) | [Findings](findings/Findings.md) |
| `decisions/` | One note per decision: what was chosen, why, what it rules out | [Decisions](decisions/Decisions.md) |
| `journal/` | One dated note per working session from 2026-11-24 on | [Journal](journal/Journal.md) |
| `plays/` | One note per play: clips, situation, status | [Plays](plays/Plays.md) |
| `reference/` | How the pipeline works, the working method, the old environment, play 1's inputs | [Pipeline](reference/pipeline.md), [Play 1's inputs](reference/play-1-inputs.md) |
| `superpowers/` | Design specs and their implementation plans (June to August) | [Specs and plans](superpowers/Specs-and-plans.md) |
| `agent-context/` | Claude's memory notes, one fact each | [Memory index](agent-context/MEMORY.md) |
| `archive/` | Out-of-date notes, kept for search | [Archive](archive/Archive.md) |
| `templates/` | Templates for new notes (Obsidian: *Insert template*) | folder |
| `_attachments/` | Images pasted in Obsidian. **Gitignored**, so no NFL frame is committed by accident | n/a |

## The graph

Open it with **Ctrl+G**; on any note, *Open local graph* (Ctrl+P) shows just
its neighbours. Colours: gold = concepts, red = STATE and Home, blue =
findings, green = decisions, orange = plays, purple = journal, grey =
reference, specs and memory. Archive and templates are hidden. A concept with
few links is where work is missing.

## Other reference notes

- [Plausibility rulers](PLAUSIBILITY.md) and the
  [endzone acceptance runbook](ENDZONE_ACCEPTANCE_RUNBOOK.md).
- [First end-to-end results](RESULTS_first_end_to_end.md) and the
  [photometric appearance design](DESIGN_photometric_appearance.md).
- [HANDOFF.md](HANDOFF.md): now a map of where the old 7660-line journal went.

## Rules for notes

- **Links:** markdown links (`[text](path.md)`), so they work on GitHub too.
- **Front matter:** every note starts with `type`, `date` and, where it has one,
  `status`. Obsidian shows these as properties.
- **Names:** decisions `NNNN-short-title.md`; journal `YYYY-MM-DD-short-title.md`;
  plays `<away>-at-<home>-<season>-wk<N>-play-NNN.md`.
- **Never** paste NFL footage, frames or secrets into a note that is committed.
