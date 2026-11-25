---
type: index
updated: 2026-11-25
---

# Decisions

One note per decision, numbered in order. A decision is never edited to say
something else: a later decision supersedes it, and both say so in `status`.
New note: copy [the template](../templates/decision.md).

| # | Decision | Status | Date |
| --- | --- | --- | --- |
| [0001](0001-local-only-no-pace.md) | Run everything locally; no PACE, no SLURM | accepted | 2026-11-24 |
| [0002](0002-layers-1-and-4-first.md) | Build Layer 1 (extraction) and Layer 4 (viewing) first | accepted | 2026-11-24 |
| [0003](0003-ignore-e501.md) | Ignore ruff's line-length rule (E501) | accepted | 2026-11-24 |
| [0004](0004-docs-vault-structure.md) | `docs/` is an Obsidian vault that extends the existing folders | accepted | 2026-11-24 |
| [0005](0005-dont-merge-twin-tracks-by-box-geometry.md) | Don't merge twin tracks by box geometry | accepted | 2026-09-10 |
| [0006](0006-regressor-pose-is-not-a-pairing-cue.md) | Don't pair cameras by the regressor's body pose | accepted | 2026-09-08 |
| [0007](0007-box-bottom-is-the-one-view-ground-point.md) | Keep the box bottom as the one-view ground point | accepted | 2026-09-08 |
| [0008](0008-officials-not-by-shirt-stripes.md) | Don't find officials by shirt stripes alone | accepted | 2026-09 |
| [0009](0009-no-per-frame-camera-refine-to-yard-lines-alone.md) | Don't refine per-frame cameras to the yard lines alone | accepted | 2026-09 |
| [0010](0010-endzone-camera-not-refined-to-its-paint.md) | Don't refine the endzone camera to its own paint | accepted | 2026-09-05 |
| [0011](0011-endzone-pitch-not-from-ankle-ruler.md) | Don't set the endzone pitch from the ankle ruler alone | accepted | 2026-09-05 |
| [0012](0012-no-seeding-joint-solve-from-another-play.md) | Don't seed the joint solve with another play's mount | accepted | 2026-09-05 |
| [0013](0013-bound-implied-lens-in-paint-labelling.md) | Bound the paint reader's implied lens to the seed play's | accepted | 2026-09-05 |
| [0014](0014-machine-settings-layer.md) | One settings layer for this machine's paths and interpreters | proposed | 2026-11-25 |
| [0015](0015-camera-above-the-field.md) | The joint solve keeps the camera above the field | accepted | 2026-11-24 |
| [0016](0016-one-numpy-2-environment.md) | One NumPy 2 environment for the whole pipeline | proposed | 2026-11-25 |

Decisions 0005 to 0013 come from HANDOFF.md's "What has been measured and
rejected" list (recorded 2026-11-24, evidence word for word). Many more
rejections are recorded inside the [findings](../findings/Findings.md) entries;
search them for "rejected" or "not shipped".

## Older dead ends (memory note not in the repo)

HANDOFF.md ended its rejected list with this summary of a memory note,
`measured-dead-ends.md`, that was never committed:

> Memory `measured-dead-ends.md` has the numbers. Headlines: endzone from paint
> (dead); per-detection team labels and looser gates in the linker (worse);
> generic and football-trained re-ID embeddings (neutral / worse than ImageNet
> at the linker's question); a whole-field coverage gate (rejected the right
> camera); numerals as the only ruler (constant was wrong — the hashes caught it).

"Endzone from paint (dead)" was later overturned: `scripts/08l` now solves the
endzone camera on its paint (see [the pipeline](../reference/pipeline.md)).
