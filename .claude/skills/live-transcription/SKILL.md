---
name: live-transcription
description: >
  Use when working on the shattered-audio live transcription system —
  multi-mic capture, real-time transcription, voice profiles, speaker
  identification, character voice separation, persona enrollment, chunking,
  cold-pass diarization. Triggers: "live transcription", "shattered-audio
  live", "voice profiles", "enroll speaker", "enroll character voice",
  "retrain profiles", "audio devices", "recording session", "transcription
  pipeline", "persona", "character voice", mic/capture/VAD issues, speaker
  ID problems, cold pass errors. Also use when maintaining, debugging, or
  extending any module under tools/audio/src/shattered_audio/.
---

# Live Transcription System

Multi-source live D&D session transcription with character voice separation.
Captures from all attached microphones, writes a rolling real-time transcript
during play, and runs a higher-accuracy second pass in the background.

Speaker identification uses a **two-stage hierarchical model**: Stage 1
identifies the physical speaker (actor) via d-vector embeddings + mic channel
priors. Stage 2 distinguishes character voices (personas) using embeddings +
prosodic features (pitch, energy, speaking rate). Falls back to actor name
when persona can't be distinguished.

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
  + v2 speaker ID (actor→persona)      + v2 speaker ID (actor→persona)
  → Inbox/current.md                   + full prosody analysis
  (rolling, truncated as               → Inbox/sNN-chunk-NNN.md
   cold pass catches up)                (replaces hot output per chunk)

Chunker (chunker.py)
  15 min target, snaps to silence gap >2s
  Saves WAV + triggers cold pass

Voice Profiles (profiles.py)
  ActorProfile → PersonaProfile hierarchy
  resemblyzer d-vectors (256-dim) + prosodic features
  Exemplar embeddings (up to 8 per persona)
  ~/.config/shattered-audio/profiles/
```

All wired together by `live_session.py` in a single asyncio process.

## Voice Profile System (v2)

### Actor vs. Persona

An **actor** is a physical person at the table. A **persona** is a character
voice performed by that actor. The DM typically has many personas (NPCs); each
player usually has one (their PC).

```
profiles/
  nick/           # actor directory
    base.npy      # actor's natural voice embedding
    meta.yaml     # name, sample_count, is_dm, personas list
    thunk.npy     # persona embedding
    thunk_prosody.yaml
    grigori.npy
    grigori_prosody.yaml
  alex/
    base.npy
    meta.yaml
    delmar.npy
    delmar_prosody.yaml
  chad.npy        # legacy flat profile (still loads fine)
```

### Two-Stage Identification

**Stage 1 — Actor identification:**
Cosine similarity of d-vector against actor base embeddings + channel prior
boost. If no personas registered, returns actor name immediately.

**Stage 2 — Persona disambiguation:**
For actors with personas, compares utterance embedding + prosody against each
persona's exemplar embeddings + prosody stats. Combined score:

```
combined = (1 - prosody_weight) * embedding_sim + prosody_weight * (1 - prosody_dist)
```

Returns persona name if it beats the "self" (actor base) score by
`persona_margin`. Otherwise returns actor name (graceful degradation).

### Confidence Tiers

| Tier | Actor Score | Persona Score | Output |
|------|-------------|---------------|--------|
| high | >= 0.80 | >= 0.70 | Character name |
| medium | >= 0.70 | < 0.70 | Actor name |
| low | < 0.70 | n/a | UNKNOWN_N |

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

Create or update a voice profile — actor (default) or persona (with --actor).

```
# Enroll actor (player's natural voice)
shattered-audio enroll "Nick" recording.wav
shattered-audio enroll "Nick" --record 30
shattered-audio enroll "Nick" --dm --record 30   # mark as DM

# Enroll persona (character voice) under an actor
shattered-audio enroll "Thunk" --actor Nick --record 10
shattered-audio enroll "Grigori" --actor Nick recording.wav
```

Actor must exist before enrolling personas. Re-enrolling blends with
existing (0.3 old + 0.7 new). Personas store up to 8 exemplar embeddings.

### `shattered-audio profiles`

List all actors and their character voices.

```
shattered-audio profiles              # list all
shattered-audio profiles Nick         # detail for one actor
```

### `shattered-audio retrain`

Update profiles from a corrected transcript. Handles both actor names and
persona names (resolved via the actor registry).

```
shattered-audio retrain Inbox/s12-chunk-001.md --audio-dir Inbox/ --blend 0.7
shattered-audio retrain transcript.md --legacy    # v1 flat profiles only
```

Transcript labels supported: `**Thunk:**` (resolved to Nick's persona),
`**Nick (as Thunk):**` (explicit), `**Nick:**` (actor base voice).

#### `--speaker-map` (session-ingest integration)

Accepts a `speaker-map.md` from the session-ingest skill and remaps UNKNOWN
labels during parsing — no manual find-replace needed:

```
shattered-audio retrain Inbox/s12-chunk-001.md \
  --speaker-map audio/sessions/session12/speaker-map.md \
  --audio-dir Inbox/ --blend 0.7
```

The speaker-map is a markdown table with `| Label | Resolved To | Confidence |`
columns. Only high and medium confidence resolutions are applied. This turns
UNKNOWN lines into usable training data, so every session's speaker corrections
improve future accuracy.

See `session-ingest` skill, Pass 1b for the full workflow.

### `shattered-audio devices`

List available audio input devices with channel count and sample rate.

## Configuration

Config search order: `--config` flag → `./config.yaml` → `~/.config/shattered-audio/config.yaml`.

| Field | Default | Purpose |
|---|---|---|
| `whisper_model` | `mlx-community/whisper-large-v3-mlx` | Cold pass model |
| `whisper_model_fast` | `mlx-community/whisper-medium-mlx` | Hot pass model |
| `mic_names` | `[]` (all mics) | Restrict to named devices |
| `channel_priors` | `{}` | Map mic→speaker for confidence boost |
| `channel_boost` | `0.15` | Cosine similarity boost for channel prior |
| `actor_threshold` | `0.7` | Min similarity for actor identification |
| `persona_threshold` | `0.6` | Min combined score for persona identification |
| `persona_margin` | `0.05` | Persona must beat "self" score by this |
| `prosody_weight` | `0.3` | Weight of prosody features in persona scoring |
| `max_exemplars` | `8` | Max exemplar embeddings per persona |
| `speaker_threshold` | `0.7` | v1 compat — maps to actor_threshold |
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
actor_threshold: 0.7
persona_threshold: 0.6
prosody_weight: 0.3
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

### Adding a character voice

1. Ensure the actor is already enrolled
2. `shattered-audio enroll "CharacterName" --actor ActorName --record 10`
   — have them do the character voice for 10+ seconds
3. Repeat enrollment 2-3 times with different samples for more exemplars
4. `shattered-audio profiles ActorName` — verify persona appears with exemplars
5. Test with a short live session

### Improving accuracy after a session

**Manual correction (quick):**

1. Review `Inbox/sNN-chunk-NNN.md` — fix any wrong speaker/character labels
2. `shattered-audio retrain Inbox/sNN-chunk-NNN.md --audio-dir Inbox/`
3. Profiles update in-place with weighted blending

**Via session-ingest (automatic, preferred):**

When session-ingest runs Pass 1 (speaker resolution), it produces a
`speaker-map.md` with high-confidence corrections. Pass 1b feeds those
corrections directly into retrain via `--speaker-map` — no manual editing
of chunk files needed. This is the recommended path because session-ingest
uses conversational context and process of elimination, which catches
errors that manual review might miss.

See `session-ingest` skill, Pass 1b for details.

### Adding a new microphone

1. Plug in the mic, run `shattered-audio devices` to find its name
2. Add to `mic_names` in config.yaml
3. Optionally add `channel_priors` entry mapping new mic to nearest speaker

### Debugging speaker ID issues

**Start with diagnostics:** Open the cold-pass chunk files (`Inbox/sNN-chunk-NNN.md`)
and check the `speaker_confidence` field in frontmatter — it shows average cosine
similarity per speaker. The `speaker_actors` field shows which personas map to which
actors.

Then apply fixes based on what you see:

- Actor scores just below threshold → lower `actor_threshold` (e.g. 0.65)
- Wrong actor names assigned → raise `actor_threshold` (e.g. 0.8)
- Persona never detected → check `persona_threshold` and `prosody_weight`; ensure
  the character voice was enrolled with distinctive enough samples
- A speaker consistently low → re-enroll with a longer sample (30s+)
- Many UNKNOWN on short lines → expected; utterances <2s lack enough audio for
  reliable embeddings
- One mic always worse → add `channel_priors` to boost that mic's expected speaker
- Persona confused between two characters → enroll more exemplars with
  `shattered-audio enroll "Name" --actor Actor --record 10`

### Debugging persona accuracy

The prosody features help distinguish character voices with different pitch/energy/rate
profiles. If two personas have very similar prosody (e.g. two NPCs both speaking in
a normal register), d-vectors alone may not separate them. Solutions:

- Exaggerate vocal differences when enrolling character voices
- Lower `persona_margin` to make persona detection more aggressive
- Increase `prosody_weight` if the characters differ mainly in pitch/rate
- Accept that some subtle character voices will fall back to actor name — this is
  correct behavior, not a bug

## Transcript Output Format

### Hot output (current.md)

Uses character names when persona is detected, actor names otherwise.

### Cold output (chunk markdown)

```yaml
speakers_detected: [Nick, Thunk, Grigori, Alex, Delmar]
speaker_actors:
  Thunk: Nick
  Grigori: Nick
  Delmar: Alex
speaker_confidence:
  Nick: 0.89
  Thunk: 0.72
  Grigori: 0.68
```

## Module Map

| Module | Purpose |
|---|---|
| `capture.py` | Multi-mic sounddevice capture, ring buffers, device watchdog |
| `vad.py` | Silero VAD utterance segmentation, best-mic selection |
| `profiles.py` | Actor/persona profiles, d-vector + prosody, enrollment, identification |
| `hot_pass.py` | Real-time whisper-medium transcription → current.md |
| `cold_pass.py` | Background whisper-large-v3 + pyannote → chunk markdown |
| `chunker.py` | Time+silence hybrid chunking, WAV output |
| `live_session.py` | Asyncio orchestrator wiring all components |
| `config.py` | YAML config loading with defaults |
| `cli.py` | Typer CLI (live, enroll, profiles, retrain, devices, transcribe, assemble) |
| `diarize.py` | Pyannote speaker diarization wrapper |
| `transcribe.py` | MLX Whisper transcription wrapper |

## Known Limitations

- Whisper may detect wrong language on very short initial utterances (noise)
- Voice encoder loads on CPU (not MPS) — fast enough but not GPU-accelerated
- Single-process: capture + transcription share one Python process
- Cold pass blocks a thread via `asyncio.to_thread` — one chunk at a time
- Resemblyzer d-vectors encode vocal tract identity, not performance — personas
  with very similar pitch/rate to the actor's natural voice may not separate
