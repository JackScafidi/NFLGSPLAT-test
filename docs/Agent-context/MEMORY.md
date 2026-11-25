# Memory Index

One durable fact per note. Status reviewed 2026-11-24; "historical" means the
note is accurate for its date but the pipeline has moved on.

- [Endzone camera bring-up](endzone-camera-bringup.md) — **historical (2026-07-24).** Field-markings EXHAUSTED + geometric cross-camera FAILED on real data (87px mispairs, Y-reflection outscores truth). Jersey-IDENTITY approach BUILT on branch jersey-identity-endzone. Since then the endzone camera is solved on its paint by `scripts/08l` (see [the pipeline](../Reference/pipeline.md)).
- [Fixed-center joint solve: RESOLVED](next-cycle-focal-pose-from-homography.md) — **historical (2026-07-07).** Camera calibration solved (first full-play cameras.npz, 816/986 frames, camera (−3.6, 80.5, 35.9)m); load-bearing lessons (camera-side label mirror, graphics poisoning, solve order) + follow-ups inside.
- [Landmark detector bring-up risks](landmark-detector-bringup-risks.md) — **historical.** Watch absent-channel false positives + yard-window consistency when training the learned field-landmark detector on real footage. The working pipeline calibrates from the paint (`scripts/08`), not this detector.
- [NFL Pro All-22 download pipeline](nfl-pro-all22-download-pipeline.md) — **current.** Reverse-engineered sideline+endzone video download: plays→coaches→asset→signed lura m3u8; bearer rotates/cookie-bound (don't reimplement auth), piggyback browser + yt-dlp. Scripts in scripts/06_*.

Archived: [PACE GPU → embers partition](../Archive/pace-gpu-embers-partition.md) (PACE is not used, [decision 0001](../Decisions/0001-local-only-no-pace.md)).
