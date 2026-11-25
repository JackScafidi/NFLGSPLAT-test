---
type: journal
date: 2026-11-24
---

# Set up on the Windows PC

## What was done

- Cloned to `C:\Users\jacks\Documents\NFLGSPLAT\NFLGSPLAT-test`. Windows'
  Documents folder is redirected to OneDrive; this local folder is not synced.
- Installed ffmpeg 9.1 and Obsidian 1.15.1 with winget. Git 2.45.1 and
  Python 3.11 were already present.
- Created `.venv` (Python 3.11) with `pip install -e ".[test]" "pyarrow<21"`
  and torch 2.11.0+cu128. NumPy stayed at 1.26.4; CUDA sees the RTX 2060.

## What was measured

- CPU test suite (`pytest -m "not gpu and not slow and not real_video"`):
  1371 passed, 20 skipped. The skips are missing torchvision, smplx and the
  SMPL-X / VPoser files.
- Ruff: 2239 findings on `main`. 38 fixed by hand; E501 ignored, see
  [decision 0003](../decisions/0003-ignore-e501.md).

## What it means

- The suite has now passed on Windows; no Windows-specific failures.
- A fresh install still needs the `pyarrow<21` pin and a separate torch
  install. Both are tasks in the foundations plan.
