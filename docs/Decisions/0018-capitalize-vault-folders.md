---
type: decision
status: accepted
date: 2026-11-25
---

# 0018: Capitalize the vault's top-level folders

## Context

The owner installed the Fathom Starmap Obsidian plugin, which draws the vault
as a 3D galaxy. It names its constellations after the top-level folders, and
it pulls notes into its "black hole" only if their path starts with exactly
`Archive/` (a case-sensitive test in its code). The vault's folders were all
lowercase, so the archive showed as an ordinary constellation.

## Decision

Chosen by the owner on 2026-11-25: capitalize all ten top-level folders in
`docs/`. They are now `Agent-context`, `Archive`, `Concepts`, `Decisions`,
`Findings`, `Journal`, `Plays`, `Reference`, `Superpowers` and `Templates`.
Subfolders (`Superpowers/specs`, `Superpowers/plans`) and file names are
unchanged.

## Consequences

- 273 links were recomputed for the new layout. Each was resolved against the
  old one first, so links to the repo-root `archive/` (archived code, outside
  the vault) were left alone.
- 32 path mentions changed: CLAUDE.md, README.md, SETUP.md, Home.md,
  [0004](0004-docs-vault-structure.md), [0017](0017-archive-the-slurm-path.md),
  and one docstring.
- Notes moved word for word from HANDOFF.md keep their prose, so they may
  still name the old lowercase paths. Their links were updated.
- Obsidian's settings follow the new names: the README ignore list, the
  templates folder and the graph colour queries. So does
  `tests/test_docs_vault.py`.
- [0004](0004-docs-vault-structure.md)'s choice of folders stands; only
  their names changed.

## Related

- **Concepts:** none directly (vault layout).
- **Decisions:** [0004: `docs/` is an Obsidian vault that extends the existing folders](0004-docs-vault-structure.md)
