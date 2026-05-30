# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

NiceGUI web app serving two roles: player-facing display pages (added to OBS as browser sources) and a DM control panel for managing everything from a browser tab. Uses parakeet-mlx for streaming ASR and pyannote for speaker embeddings on Apple Silicon.

## Commands

```bash
# Setup (first time)
python3.11 -m venv .venv
.venv/bin/pip install -e ".[dev]"

# Run (serves on localhost:8080)
.venv/bin/python -m player_view.main

# Tests (no ML stack needed)
.venv/bin/pytest tests/
.venv/bin/pytest tests/test_speaker_scorer.py -v   # single file
.venv/bin/pytest tests/test_session_transcriber.py::test_name -v  # single test
```

Requires Python 3.11+, Apple Silicon (MLX), and `HF_TOKEN` in the repo-root `.env` (for pyannote gated models).

## Architecture

Source lives in `src/player_view/`. Entry point is `main.py` which wires up services at startup via `services.init()`.

### Layers

- **`pages/`** — NiceGUI `@ui.page` route handlers, one file per URL. Each player-facing page has a 100px operator header (crop in OBS to hide from players).
- **`services/`** — ML and audio backends. The `services/__init__.py` module holds singleton instances (`services.asr`, `services.audio`, etc.) initialized at startup and torn down on shutdown.
- **`models/`** — `state.py` (shared session state) and `voice_profile.py` (`ProfileStore` for JSON profiles in `profiles/`).
- **`components/`** — reusable UI pieces (header, teleprompter).

### Pages

| Route | File | Role |
|---|---|---|
| `/dm` | `dm.py` | DM control panel |
| `/save-speaker` | `save_speaker.py` | Voice profile enrollment teleprompter |
| `/test-speaker` | `test_speaker.py` | Raw ASR + profile matching |
| `/session` | `session.py` | Live transcription chat log |
| `/slideshow` | `slideshow.py` | Image rotation from a folder |
| `/map/{name}` | `map_view.py` | Full-screen named map image |

### Services

| Service | Backend | Purpose |
|---|---|---|
| `ASRService` | parakeet-mlx | Streaming speech-to-text |
| `AudioService` | sounddevice | Microphone capture |
| `DiarizationService` | pyannote.audio | Speaker separation/embedding |
| `SpatialAnalyzer` | — | Spatial audio analysis |
| `SessionTranscriber` | orchestrates ASR+diarization+profiles | Assembles live transcript with speaker labels |
| `LLMService` | — | LLM integration |
| `ProfileStore` | — | Load/save voice profiles as JSON |

## Testing Notes

Tests mock all ML services — no GPU or model downloads needed. The `conftest.py` provides `tmp_profile_dir` and `profile_store` fixtures. Test files cover: voice profiles, speaker scoring, session transcription, spatial analysis, audio multichannel, and service wiring.
