# Setup — shattered-audio engine (one-time)

The `shattered-audio` engine lives at `tools/audio/` in the repo root. The wrapper scripts
(record.sh / transcribe.sh / voices.sh) auto-resolve the venv — you only need to build it
once.

## 1. Virtualenv + dependencies

Python 3.11+ required. No Python 3.11?

```bash
brew install python@3.11
```

Then from `tools/audio/`:

```bash
cd tools/audio
python3.11 -m venv .venv
.venv/bin/pip install -e '.[all]'
```

The venv directory is gitignored. After this, all three wrapper scripts find it automatically.

## 2. Hugging Face token + model license (optional — for diarization)

pyannote speaker diarization is gated behind a free HF account. Without `HF_TOKEN`, each
microphone track is treated as a single speaker — perfectly fine for the usual
one-mic-per-person table setup.

To enable diarization:

1. Create a free [Hugging Face](https://huggingface.co) account and generate a read token.
2. Accept the user conditions for **`pyannote/speaker-diarization-3.1`** on its HF model page.
3. Export the token before running any audio skill:
   ```bash
   export HF_TOKEN=hf_xxxxxxxxxxxxxxxxx
   ```

Model weights download on first use and cache locally.

## 3. Microphone permission (macOS)

Grant microphone access to your terminal app: System Settings → Privacy & Security →
Microphone. Do this before the first recording session.

## Operations

The three operator-facing skills handle all actual work:

- **record-session-audio** — captures multi-mic table audio.
  ```bash
  .claude/skills/record-session-audio/scripts/record.sh --session N
  ```
- **transcribe-session-audio** — Whisper large-v3 + pyannote (when `HF_TOKEN` is set),
  speaker-labeled by voice profile and mic prior.
  ```bash
  .claude/skills/transcribe-session-audio/scripts/transcribe.sh --session N
  ```
- **manage-voice-profiles** — all voice-profile CRUD and the actor→persona model.
  ```bash
  .claude/skills/manage-voice-profiles/scripts/voices.sh <subcommand>
  ```

## Accuracy levers

- **Enroll long, varied samples.** Aim for 30+ seconds of natural speech with varied cadence
  per voice. Longer and more varied beats short and flat.
- **One persona per character voice, grouped under the actor.** Each real person is an actor;
  each character voice they perform is a persona under that actor. This lets the identifier
  disambiguate multiple voices from one person.
- **Corrections fold back via the retrain loop.** After each session, the session-ingest
  `speaker-map.md` + `shattered-audio retrain --speaker-map` loop sharpens profiles
  automatically — accuracy improves session over session.

See the **live-transcription** skill for engine internals and speaker-ID tuning parameters.
