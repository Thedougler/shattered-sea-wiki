# Session Transcription — how to run it

Continuous, 4h+ live capture with accurate, overlap-aware speaker separation, then a
high-accuracy offline finalize pass. Complete `setup.md` and enroll voice profiles
(`voice-profiler.md`) first.

## Pass 1 — live capture (run at session start, leave running)

```bash
source .claude/skills/live-co-dm/.venv/bin/activate
export HF_TOKEN=hf_...
python3 .claude/skills/live-co-dm/scripts/transcribe_session.py \
    --session 4 --speakers 5
```

- `--session N` — session number. Omit to auto-pick the next one.
- `--speakers N` — **physical people at the table** (not character count). Supplying
  this is the single biggest accuracy win on crosstalk — always set it.
- `--threshold` — cosine match cutoff for voice ID (default 0.5). Raise it if voices are
  being confused; lower it if known voices fall through to `Unknown-N`.

It captures the mic, splits audio on silence, and continuously writes:

- `wiki/sessions/.live/session-04/live_transcript.md` — a growing, speaker-attributed
  transcript (this is what the live co-DM agent reads).
- `wiki/sessions/.live/session-04/audio/NNNN_HHhMMmSSs.wav` — silence-chunked audio.

Everything under `.live/` is **gitignored** scratch. Each transcript line is flushed to
disk immediately, so a crash at hour three keeps everything written so far. Leave it
running the whole session; `Ctrl-C` to stop.

Lines look like:
```
**Delmar** (Ben) [01:12:04]: hold fast, she's coming about
**Nona (?)** (Sam) [01:12:05] [overlap]: belay that
```
`(?)` = low-confidence attribution. `[overlap]` = the line came from a crosstalk region;
both speakers get their own stacked line so no one is dropped.

## Pass 2 — finalize (after the session)

The live pass is provisional. Finalization re-diarizes the **entire** recording at once
with the known speaker count (global clustering — far more accurate on overlap), re-runs
ASR, and writes the canonical transcript:

```bash
python3 .claude/skills/live-co-dm/scripts/finalize_session.py \
    --session 4 --speakers 5
```

Output: `wiki/sessions/session-04-transcript.md` — a **committed** markdown transcript
(the audio stays gitignored). From there, promote it into canon with `ttrpg-wiki-ingest`
(transcript-ingest path) when you're ready to fold the session into the wiki.

## If separation is poor

- Confirm `--speakers` matches the people actually talking.
- Re-enroll thin/echoey profiles in a quieter room (see `voice-profiler.md`).
- Nudge `--threshold` (up to split confused voices, down to rescue known ones).
- Remember the design preserves overlaps rather than guessing — heavy crosstalk will
  show `[overlap]`/`(?)` markers; that's honest uncertainty, not a bug. The finalize
  pass resolves much of it.
