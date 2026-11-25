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
| `Concepts/` | The hubs: goal objects, pipeline stages and measures. Every other note links to the concepts it touches | [Concepts](Concepts/Concepts.md) |
| `Findings/` | What was tried and measured, by subject (cameras, tracking, identity, placement, pose, ball, render, rulers, versions) | [Findings](Findings/Findings.md) |
| `Decisions/` | One note per decision: what was chosen, why, what it rules out | [Decisions](Decisions/Decisions.md) |
| `Journal/` | One dated note per working session from 2026-11-24 on | [Journal](Journal/Journal.md) |
| `Plays/` | One note per play: clips, situation, status | [Plays](Plays/Plays.md) |
| `Reference/` | How the pipeline works, the working method, the old environment, play 1's inputs | [Pipeline](Reference/pipeline.md), [Play 1's inputs](Reference/play-1-inputs.md) |
| `Superpowers/` | Design specs and their implementation plans (June to August) | [Specs and plans](Superpowers/Specs-and-plans.md) |
| `Agent-context/` | Claude's memory notes, one fact each | [Memory index](Agent-context/MEMORY.md) |
| `Archive/` | Out-of-date notes, kept for search | [Archive](Archive/Archive.md) |
| `Templates/` | Templates for new notes (Obsidian: *Insert template*) | folder |
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
