---
name: live-transcription
description: >
  Use when working on the shattered-audio live transcription system —
  multi-mic capture, real-time transcription, voice profiles, speaker
  identification, chunking, cold-pass diarization. Triggers: "live
  transcription", "shattered-audio live", "voice profiles", "enroll speaker",
  "retrain profiles", "audio devices", "recording session", "transcription
  pipeline", mic/capture/VAD issues, speaker ID problems, cold pass errors.
  Also use when maintaining, debugging, or extending any module under
  tools/audio/src/shattered_audio/.
---

# Live Transcription System

Multi-source live D&D session transcription. Captures from all attached
microphones, writes a rolling real-time transcript during play, and runs a
higher-accuracy second pass in the background. Speaker identification uses
voice profile embeddings with mic-channel priors.

## Architecture

```
Audio Capture (capture.py)
  → Per-mic ring buffers, device watchdog
  → Async frame generator

Voice Activity Detection (vad.py)
  → Silero VAD, utterance segmentation
  → Best-mic selection per utterance (RMS energy)

Hot Pass (hot_pass.py)              Cold Pass (cold_pass.py)
  whisper-medium, ~2s lag              whisper-large-v3 + pyannote
  + voice profile ID                   + voice profile ID
  → Inbox/current.md                   → Inbox/sNN-chunk-NNN.md
  (rolling, truncated as               (replaces hot output
   cold pass catches up)                per chunk)

Chunker (chunker.py)
  15 min target, snaps to silence gap >2s
  Saves WAV + triggers cold pass

Voice Profiles (profiles.py)
  resemblyzer d-vectors (256-dim)
  ~/.config/shattered-audio/profiles/
  Cosine similarity + channel prior boost
```

All wired together by `live_session.py` in a single asyncio process.

## CLI Commands

All commands are under the `shattered-audio` entry point.
Venv: `tools/audio/.venv`. Install: `pip install -e ".[all]"`.

### `shattered-audio live`

Start a recording session. Ctrl+C to stop.

```
shattered-audio live --session 12 [--speakers nick,alex] [--config path]
```

Writes `Inbox/current.md` (hot) and `Inbox/sNN-chunk-NNN.md` (cold).
WAV chunks saved as `Inbox/sNN-chunk-NNN.wav`.

### `shattered-audio enroll`

Create or update a voice profile.

```
shattered-audio enroll "Nick" recording.wav        # from file
shattered-audio enroll "Nick" --record 30           # record 30s from mic
```

Profiles: `~/.config/shattered-audio/profiles/{slug}.npy` + `{slug}_meta.yaml`.
Re-enrolling blends with existing (0.3 old + 0.7 new).

### `shattered-audio retrain`

Update profiles from a corrected transcript. After fixing speaker labels in a
chunk markdown file, retrain to improve future identification.

```
shattered-audio retrain Inbox/s12-chunk-001.md --audio-dir Inbox/ --blend 0.7
```

### `shattered-audio devices`

List available audio input devices with channel count and sample rate.

## Configuration

Config search order: `--config` flag → `./config.yaml` → `~/.config/shattered-audio/config.yaml`.

Key settings:

| Field | Default | Purpose |
|---|---|---|
| `whisper_model` | `mlx-community/whisper-large-v3-mlx` | Cold pass model |
| `whisper_model_fast` | `mlx-community/whisper-medium-mlx` | Hot pass model |
| `mic_names` | `[]` (all mics) | Restrict to named devices |
| `channel_priors` | `{}` | Map mic→speaker for confidence boost |
| `channel_boost` | `0.15` | Cosine similarity boost for channel prior |
| `speaker_threshold` | `0.7` | Minimum similarity for profile match |
| `chunk_target_minutes` | `15` | Target chunk duration |
| `chunk_silence_gap` | `2.0` | Silence gap to snap chunk boundary |
| `profiles_dir` | `~/.config/shattered-audio/profiles` | Voice profile storage |
| `inbox_path` | `Inbox` | Output directory |

Example `config.yaml`:

```yaml
mic_names:
  - "MacBook Air Microphone"
  - "USB-C Audio"
channel_priors:
  mic_0: "Nick"
speaker_threshold: 0.65
```

## Dependencies

```
pip install -e ".[all]"     # everything
pip install -e ".[live]"    # capture + profiles (no diarization)
pip install -e ".[diarize]" # pyannote only
```

Pyannote diarization requires:
1. `HF_TOKEN` env var with a valid HuggingFace token
2. Accepted license at https://huggingface.co/pyannote/speaker-diarization-3.1

If unavailable, cold pass still runs — just without diarization labels.

## Maintenance Workflows

### Adding a new player

1. `shattered-audio enroll "PlayerName" --record 30` — have them speak naturally
2. Optionally set `channel_priors` in config if they sit near a specific mic
3. Run a short test: `shattered-audio live --session 99`, verify their name appears

### Improving accuracy after a session

1. Review `Inbox/sNN-chunk-NNN.md` — fix any wrong speaker labels
2. `shattered-audio retrain Inbox/sNN-chunk-NNN.md --audio-dir Inbox/`
3. Profiles update in-place with weighted blending

### Adding a new microphone

1. Plug in the mic, run `shattered-audio devices` to find its name
2. Add to `mic_names` in config.yaml
3. Optionally add `channel_priors` entry mapping new mic to nearest speaker

### Debugging speaker ID issues

**Start with diagnostics:** Open the cold-pass chunk files (`Inbox/sNN-chunk-NNN.md`)
and check the `speaker_confidence` field in frontmatter — it shows average cosine
similarity per speaker (e.g. `{"Nick": 0.94, "Alex": 0.72}`). This tells you whether
the problem is low confidence (borderline profiles) or missing profiles entirely.

Then apply fixes based on what you see:

- Scores just below threshold → lower `speaker_threshold` (e.g. 0.65)
- Wrong names assigned → raise `speaker_threshold` (e.g. 0.8)
- A speaker consistently low → re-enroll with a longer sample (30s+)
- Many UNKNOWN on short lines → expected; utterances <2s lack enough audio for
  reliable embeddings
- One mic always worse → add `channel_priors` to boost that mic's expected speaker

## Module Map

| Module | Purpose |
|---|---|
| `capture.py` | Multi-mic sounddevice capture, ring buffers, device watchdog |
| `vad.py` | Silero VAD utterance segmentation, best-mic selection |
| `profiles.py` | Voice profile CRUD, d-vector embedding, cosine similarity |
| `hot_pass.py` | Real-time whisper-medium transcription → current.md |
| `cold_pass.py` | Background whisper-large-v3 + pyannote → chunk markdown |
| `chunker.py` | Time+silence hybrid chunking, WAV output |
| `live_session.py` | Asyncio orchestrator wiring all components |
| `config.py` | YAML config loading with defaults |
| `cli.py` | Typer CLI (live, enroll, retrain, devices, transcribe, assemble) |
| `diarize.py` | Pyannote speaker diarization wrapper |
| `transcribe.py` | MLX Whisper transcription wrapper |

## Known Limitations

- Whisper may detect wrong language on very short initial utterances (noise)
- Voice encoder loads on CPU (not MPS) — fast enough but not GPU-accelerated
- Single-process: capture + transcription share one Python process
- Cold pass blocks a thread via `asyncio.to_thread` — one chunk at a time
