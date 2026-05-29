# Setup — voice tools (one-time)

The bundled scripts run on **Apple Silicon** (Parakeet v3 via MLX; pyannote/diart on
MPS or CPU). The agent's unit-test suite needs none of this — only the live
capture/finalization adapters do.

## 1. Virtualenv + dependencies

```bash
python3 -m venv .claude/skills/live-co-dm/.venv
source .claude/skills/live-co-dm/.venv/bin/activate
pip install -r .claude/skills/live-co-dm/requirements.txt
```

The venv directory is gitignored. Keep it out of the wiki's base environment so
`.claude/scripts/` stays pure-stdlib.

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
(System Settings → Privacy & Security → Microphone). For the cleanest profiles and
transcripts, use a decent mic in a quiet room — input quality is the single biggest
lever on speaker-separation accuracy.

## 4. Verify

```bash
# Pure logic — must pass with no ML stack:
cd .claude/skills/live-co-dm/scripts && python3 -m unittest discover -s . -p 'test_*.py'

# Real adapters (with venv active + HF_TOKEN set), optional:
RUN_ML_TESTS=1 python3 -m unittest test_ml_integration -v
```

## Accuracy levers (why this is set up the way it is)

The campaign's audio is hard: ~5 players, heavy crosstalk, each voicing 2+ characters.
The design leans on every available lever:

- **Tell pyannote the speaker count.** Pass `--speakers N` (physical people at the
  table, not characters). This is the biggest single accuracy gain on overlapped speech.
- **Enroll long, varied samples.** The teleprompter targets ~60–90s of phonetically
  rich, dynamic-range reading per character voice → stronger, more separable embeddings.
- **Profile per character, group by player.** Each profile's `player` field lets the
  identifier disambiguate the several voices one person performs.
- **Two passes.** The live pass is provisional (latency-bound). The finalize pass
  re-diarizes the whole recording at once for global clustering — that's the canon.
- **Overlap is preserved, not guessed.** Crosstalk regions emit stacked `[overlap]`
  lines so no speaker is silently dropped; low-confidence IDs are marked `(?)`.
