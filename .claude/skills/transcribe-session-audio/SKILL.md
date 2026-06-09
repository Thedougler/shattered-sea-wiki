---
name: transcribe-session-audio
description: >
  Turn a recorded Shattered Sea session into a speaker-labeled transcript (Whisper
  large-v3 + pyannote over the per-mic tracks in .raw/sessions/session-NN/audio/raw/,
  writing per-part CSV chat logs). Auto-loads saved voice profiles; runs BEFORE
  session-ingest. Triggers: "/transcribe-session-audio", "transcribe the session",
  "who said what". The voice-profile model lives in manage-voice-profiles. Full
  trigger list in the skill body.
---

# Transcribe Session Audio

## When to use

Full trigger set: "/transcribe-session-audio", "transcribe the session",
"transcribe the audio", "make the transcript", "who said what", "turn the recording
into text", "process the session recording", "save a voice profile".

Turn a recorded session into per-part CSV chat logs with timestamps and speaker
labels. Reads the isolated per-mic m4a tracks captured by
[[record-session-audio]] and writes the format the [[session-ingest]] skill
consumes next.

**Pipeline:** [[record-session-audio]] → **this skill** → `shattered-audio assemble` → [[session-ingest]]

## How Speakers Are Labeled

Three layers, each falling back to the next:

1. **Voice profiles** (Whisper text + resemblyzer d-vectors + prosody) →
   identifies actors and their character voices (personas). Loaded automatically.
2. **Mic prior** — whichever mic a voice came from. Because each person has
   their own mic, the mic *is* a strong speaker signal (the DM's mic → "DM").
   Set these in `tools/audio/config.yaml` under `channel_priors`.
3. **Stable label** — `Speaker mic01`, so [[session-ingest]] can resolve it later.

pyannote diarization (splitting two voices on one mic) runs only when `HF_TOKEN`
is set; without it, each mic is treated as a single speaker stream — correct for
the usual one-person-per-mic table.

## Usage

Run the bundled script (resolves the venv, runs from the repo root):

```
.claude/skills/transcribe-session-audio/scripts/transcribe.sh --session NN
```

| Flag | Purpose |
|---|---|
| `--session NN` | **Required.** Reads `.raw/sessions/session-NN/audio/raw/`; writes parts to `.raw/sessions/session-NN/audio/parts/` and transcripts to `.raw/sessions/session-NN/transcripts/raw/`. |
| `--no-profiles` | Label purely by mic prior; skip voice-profile identification. |
| `--save-profile "Name"` | Enroll/refresh a voice profile from this session's audio. |
| `--from-mic mic01` | Which mic to harvest the `--save-profile` voice from. |
| `--actor "Nick"` | Save the profile as a character voice (persona) under this actor. |
| `--model REPO` | Override the Whisper model (default large-v3). |

First run downloads Whisper large-v3 (~1.5 GB) to the HF cache.

## After Transcribing

1. Stitch the parts into one continuous transcript:
   `tools/audio/.venv/bin/shattered-audio assemble NN`
2. Hand off to [[session-ingest]] for speaker resolution, cleanup, and promotion
   into canon. Its `--speaker-map` corrections feed back into the voice profiles,
   so accuracy improves every session.

## Saving Voice Profiles

A profile makes future sessions label that person (and their character voices)
automatically. Harvest one from a session where you know who's on which mic:

```
# the player's natural voice, from their mic
transcribe.sh --session 7 --save-profile "Nick" --from-mic mic01

# a character voice that player performs (actor must exist first)
transcribe.sh --session 7 --save-profile "Grigori" --from-mic mic01 --actor Nick
```

Inspect what's enrolled: `tools/audio/.venv/bin/shattered-audio profiles`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running before recording finished | Stop [[record-session-audio]] first — needs finalized m4a chunks. |
| Expecting `assembled.csv` to be the deliverable | The per-part `.raw/sessions/session-NN/transcripts/raw/session-NN-part-PP.csv` files are what session-ingest reads. |
| Worrying that pyannote is "missing" | It's optional. Without `HF_TOKEN` the mic-isolated labels are already strong. |
| Speakers all show `Speaker micNN` | No profiles enrolled and no `channel_priors` set — add priors or `--save-profile`. |

## Troubleshooting

- **`No recording found`** → wrong session number, or recording wrote elsewhere
  (`--audio-dir`).
- **`No mic tracks`** → `.raw/sessions/session-NN/audio/raw/` has no `mic-XX/*.m4a`
  files. Confirm [[record-session-audio]] actually captured audio.
- **Wrong character labels** → see the speaker-ID tuning table in the
  [[live-transcription]] reference (`actor_threshold`, `persona_margin`, etc.).
