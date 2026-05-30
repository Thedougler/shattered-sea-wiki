# Setup — voice tools (one-time)

The voice-transcription tools run on **Apple Silicon** (Parakeet v3 via MLX;
pyannote/diart on MPS or CPU). The code lives at `voice-transcription/` in the
repo root.

## 1. Virtualenv + dependencies

The wrapper scripts (`save_voice.sh` / `transcribe_session.sh` /
`finalize_session.sh`) build and populate the venv automatically — they pick a
Python >= 3.11 and install deps from `pyproject.toml`, so you normally don't run
these by hand. To do it manually:

```bash
python3.11 -m venv voice-transcription/.venv   # or any python3.11+
source voice-transcription/.venv/bin/activate
pip install -e voice-transcription/
```

No `python3.11`? Install one with `brew install python@3.11`.

The venv directory is gitignored.

## 2. Hugging Face token + model licenses

pyannote's diarization and embedding models are gated. Once:

1. Create a (free) Hugging Face account and a read token.
2. Accept the user conditions for **`pyannote/speaker-diarization-3.1`** and the
   embedding model on their HF model pages.
3. Export the token before running:
   ```bash
   export HF_TOKEN=hf_xxxxxxxxxxxxxxxxx
   ```

First run downloads the Parakeet and pyannote weights (a few minutes); they cache
locally after that.

## 3. Microphone permission

On macOS, grant microphone access to the terminal/app you launch the scripts from
(System Settings -> Privacy & Security -> Microphone). For the cleanest profiles and
transcripts, use a decent mic in a quiet room.

## 4. Verify

```bash
# Pure logic — must pass with no ML stack:
cd voice-transcription && pip install -e ".[dev]" && pytest tests/

# Real adapters (with venv active + HF_TOKEN set), optional:
RUN_ML_TESTS=1 pytest tests/test_ml_integration.py -v
```

## Accuracy levers

- **Tell pyannote the speaker count.** Pass `--speakers N` (physical people at the
  table, not characters).
- **Enroll long, varied samples.** The teleprompter targets ~60–90s per character
  voice.
- **Profile per character, group by player.** Each profile's `player` field lets the
  identifier disambiguate the several voices one person performs.
- **Two passes.** The live pass is provisional. The finalize pass re-diarizes the
  whole recording at once for global clustering — that's the canon.
- **Overlap is preserved, not guessed.** Crosstalk regions emit stacked `[overlap]`
  lines; low-confidence IDs are marked `(?)`.
