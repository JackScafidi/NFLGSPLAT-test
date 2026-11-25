---
type: decision
status: accepted
date: 2026-11-24
---

# 0004: `docs/` is an Obsidian vault that extends the existing folders

## Context

`docs/` already held Claude's memory notes (`Agent-context/` with a
`MEMORY.md` index), dated specs and plans (`Superpowers/`), and the 7660-line
`HANDOFF.md`. The project will grow to many plays and many decisions.

## Decision

- The vault root is `docs/`, so notes travel with git and the vault never
  indexes code, `.venv` or `data/`.
- Existing folders stay where they are. New folders follow the same pattern,
  front matter plus an index note: `Decisions/`, `Journal/`, `Plays/` and
  `Templates/`. `Home.md` is the front door.
- Links are markdown links, so they work on GitHub.
- Pasted images go to `_attachments/`, which is gitignored.
- Shared Obsidian settings are committed; per-device workspace files are not.

## Consequences

- Paths in code comments and old commits keep working.
- `HANDOFF.md` stays whole until it is split into `Decisions/` and `Journal/`,
  a task in the foundations plan.
- An image meant for the repo (a diagram, never an NFL frame) must be saved
  outside `_attachments/` on purpose.
