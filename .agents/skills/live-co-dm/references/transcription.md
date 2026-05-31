# Session Transcription — how to run it

Continuous, 4h+ live capture with accurate, overlap-aware speaker separation, then a
high-accuracy offline finalize pass. Complete setup and enroll voice profiles first.

## Pass 1 — live capture (run at session start, leave running)

```bash
./transcribe_session.sh --session 4 --speakers 5
```

Or manually with the venv active:

```bash
source voice-transcription/.venv/bin/activate
export HF_TOKEN=hf_...
python3 -m voice_transcription.cli.transcribe --session 4 --speakers 5
```

- `--session N` — session number. Omit to auto-pick the next one.
- `--speakers N` — **physical people at the table** (not character count). Always set it.
- `--threshold` — cosine match cutoff for voice ID (default 0.5).

It captures the mic, splits audio on silence, and continuously writes:

- `wiki/sessions/.live/session-04/live_transcript.md` — a growing, speaker-attributed
  transcript (this is what the live co-DM agent reads).
- `wiki/sessions/.live/session-04/audio/NNNN_HHhMMmSSs.wav` — silence-chunked audio.

Everything under `.live/` is **gitignored** scratch. Each transcript line is flushed to
disk immediately. Leave it running the whole session; `Ctrl-C` to stop.

## Pass 2 — finalize (after the session)

```bash
./finalize_session.sh --session 4 --speakers 5
```

Output: `wiki/sessions/session-04-transcript.md` — a **committed** markdown transcript.
From there, promote it into canon with `ttrpg-wiki-ingest` (transcript-ingest path).

## Closing the loop — correcting voice profiles

After you correct a finalized transcript, **re-save the affected characters' voice
profiles** (`voice-profiler.md`). The profiler harvests corrected lines and folds real
in-character audio into the profile.

Keep the session's `.live/session-NN/audio/` directory until you're done improving
profiles from it.

## If separation is poor

- Confirm `--speakers` matches the people actually talking.
- Re-enroll thin/echoey profiles in a quieter room.
- Nudge `--threshold` (up to split confused voices, down to rescue known ones).
