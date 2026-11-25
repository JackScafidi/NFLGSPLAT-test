---
type: index
updated: 2026-11-25
---

# Specs and plans

Design specs (`specs/`) and their implementation plans (`plans/`), written with
the superpowers workflow. The 15 from June to August 2026 are about the data
layout and camera calibration, before the working pipeline of September. The
November drafts are newer and say so in their status.

Each of the 15 still says "Approved (design); implementation plan pending", though
each has a plan. Those lines were never updated, so check a spec against the
code before relying on it. Today's cameras come from the paint solve
(`scripts/08`, `08e`, `08l`; see [the pipeline](../reference/pipeline.md)).

| Date | Spec | Plan |
| --- | --- | --- |
| 2026-11-25 | [Pipeline runner](specs/2026-11-25-pipeline-runner-design.md) (accepted; stage list open) | none yet |
| 2026-08-17 | [Endzone calibration via static mosaic](specs/2026-08-17-endzone-static-mosaic-calibration-design.md) | [plan](plans/2026-08-17-endzone-static-mosaic-calibration.md) |
| 2026-07-22 | [Jersey-identity endzone calibration](specs/2026-07-22-jersey-identity-endzone-calibration-design.md) | [plan](plans/2026-07-22-jersey-identity-endzone-calibration.md) |
| 2026-07-17 | [Cross-camera bootstrap roll fix](specs/2026-07-17-cross-camera-bootstrap-roll-fix-design.md) | [plan](plans/2026-07-17-cross-camera-bootstrap-roll-fix.md) |
| 2026-07-15 | [Cross-camera endzone calibration](specs/2026-07-15-cross-camera-endzone-calibration-design.md) | [plan](plans/2026-07-15-cross-camera-endzone-calibration.md) |
| 2026-07-12 | [Player masks for calibration](specs/2026-07-12-player-masks-for-calibration-design.md) | [plan](plans/2026-07-12-player-masks-for-calibration.md) |
| 2026-07-08 | [Endzone calibration via rotate-90](specs/2026-07-08-endzone-rotate90-calibration-design.md) | [plan](plans/2026-07-08-endzone-rotate90-calibration.md) |
| 2026-07-06 | [Fixed-center joint solve](specs/2026-07-06-fixed-center-joint-solve-design.md) | [plan](plans/2026-07-06-fixed-center-joint-solve.md) |
| 2026-07-04 | [Pretrained-hybrid field registration](specs/2026-07-04-pretrained-hybrid-field-registration-design.md) | [plan](plans/2026-07-04-pretrained-hybrid-field-registration.md) |
| 2026-06-26 | [Learned field-landmark detector](specs/2026-06-26-field-landmark-detector-design.md) | [plan](plans/2026-06-26-field-landmark-detector.md) |
| 2026-06-23 | [Line labelling via homography consensus](specs/2026-06-23-homography-consensus-labeling-design.md) | [plan](plans/2026-06-23-homography-consensus-labeling.md) |
| 2026-06-23 | [Hash-row-intersection correspondences](specs/2026-06-23-hash-row-intersection-correspondences-design.md) | [plan](plans/2026-06-23-hash-row-intersection-correspondences.md) |
| 2026-06-22 | [Hinted per-frame field registration](specs/2026-06-22-hinted-field-registration-design.md) | [plan](plans/2026-06-22-hinted-field-registration.md) |
| 2026-06-21 | [Per-frame camera calibration](specs/2026-06-21-per-frame-calibration-design.md) | [plan](plans/2026-06-21-per-frame-calibration.md) |
| 2026-06-21 | [Automatic per-frame field registration](specs/2026-06-21-auto-field-registration-design.md) | [plan](plans/2026-06-21-auto-field-registration.md) |
| 2026-06-12 | [Per-play season tree (data layout)](specs/2026-06-12-per-play-season-tree-design.md) | [plan](plans/2026-06-12-per-play-season-tree.md) |
