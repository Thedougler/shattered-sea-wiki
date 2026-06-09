# Session Transcription — moved

Recording and transcription now live in two dedicated skills, both backed by the
`tools/audio` (`shattered-audio`) engine. The old `transcribe_session.sh` /
`finalize_session.sh` / `voice-transcription/` flow described here is retired.

## Record (at session start)

Use the **record-session-audio** skill. One ffmpeg process per mic captures each
person to an isolated, chunked m4a track — built to run 4+ hours and stop cleanly.

```bash
.claude/skills/record-session-audio/scripts/record.sh --session N
```

Output: `.raw/sessions/session-NN/audio/raw/mic-KK/part-000.m4a` (one file per mic per 15-min part) + `.raw/sessions/session-NN/audio/manifest.json`.

## Transcribe (after the session)

Use the **transcribe-session-audio** skill. Whisper large-v3 (+ pyannote when
`HF_TOKEN` is set) over the per-mic tracks, speaker-labeled by voice profile and
mic prior.

```bash
.claude/skills/transcribe-session-audio/scripts/transcribe.sh --session N
tools/audio/.venv/bin/shattered-audio assemble N      # stitch parts → one transcript
```

Output: `.raw/sessions/session-NN/transcripts/raw/session-NN-part-PP.csv` (`ID,Start,End,Speaker,Text`),
consumed by the **session-ingest** skill.

## Voice profiles

Saved/refreshed through transcribe-session-audio (`--save-profile`), auto-loaded on
every transcribe. The session-ingest `speaker-map.md` + `shattered-audio retrain
--speaker-map` loop folds corrections back in, so accuracy improves each session.
See the **live-transcription** skill for engine internals and speaker-ID tuning.
