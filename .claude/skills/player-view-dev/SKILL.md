---
name: player-view-dev
description: >
  Launch and manage the player-view NiceGUI app for development. Invoke for:
  "start the app", "run player-view", "dev server", "run the overlay",
  "test player-view", "set up the app". Handles venv setup, dependency install,
  dev server launch, and test execution for the player-view/ subproject.
disable-model-invocation: true
---

## What this does

Standardizes the player-view development workflow: venv creation, dependency installation, dev server launch, and test execution. The app is a NiceGUI web app serving live voice transcription and OBS overlays on `localhost:8080`.

## Prerequisites

- Python 3.11+ (required for MLX/parakeet)
- Apple Silicon Mac (MLX requirement)
- `HF_TOKEN` in repo-root `.env` (for pyannote.audio model downloads)

## Commands

### Setup (first time or after dependency changes)

```bash
cd player-view
python3.11 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

### Run dev server

```bash
cd player-view
.venv/bin/python -m player_view.main
```

Serves on `localhost:8080`. Key routes:
- `/dm` — DM control panel
- `/save-speaker` — voice profile management
- `/session` — live session view

### Run tests

```bash
cd player-view
.venv/bin/pytest tests/ -x -q
```

Tests don't require the ML stack (no GPU/MLX needed).

## Workflow

1. Check if `.venv` exists in `player-view/`. If not, create it and install deps.
2. Check if deps are current: `pip install -e ".[dev]"` is idempotent.
3. Start the dev server or run tests depending on what was asked.
4. For code changes: edit files in `player-view/src/player_view/`, then run tests to verify.

## Architecture reference

See the **player-view Architecture** section in the repo-root `CLAUDE.md` for the layer breakdown (pages, services, models, components).
