---
type: concept
kind: stage
status: working
updated: 2026-11-24
---

# Render and viewer

Layer 4: the 1080p render and the browser viewer that show the play from any angle.

**Pipeline stage** · status: **working**

## Today

- `scripts/05k_render_hifi.py` renders every body as Gaussians on the GPU, with a procedural field and stadium backdrop.
- `viewer/play_room.html` reads a joints file and offers any angle and a first-person view; it is hardcoded to play 1.

## Where in the code

- `scripts/05k_render_hifi.py`
- `nfl_gsplat/compositing/splat_torch.py`: the GPU rasteriser
- `nfl_gsplat/render/`: `shade.py`, `sky.py`, `uniform.py`, `helmet.py`
- `viewer/play_room.html`

## Notes

- **Findings:** [Render and viewer](../findings/render-and-viewer.md), [Pipeline runs and versions](../findings/pipeline-and-versions.md)
- **Decisions:** [0002: Layers 1 and 4 first](../decisions/0002-layers-1-and-4-first.md)
- **Related:** [Play data](play-data.md), [Head](head.md), [Ball](ball.md)

## Next

Make the render and viewer read only the play data; make the viewer load any play. See the [Foundations plan](https://claude.ai/artifact/K7SoiabWPzAFs2HgP2Ekpz).
