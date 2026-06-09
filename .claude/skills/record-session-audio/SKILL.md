---
name: record-session-audio
description: >
  Use at the START of a Shattered Sea play session to capture the table audio.
  Triggers: "/record-session-audio", "record the session", "start recording",
  "start the session audio", "we're starting", "capture tonight's session",
  "begin recording the game". Records every microphone to its own isolated,
  chunked track for later transcription. This is a fire-and-wait recorder — it
  runs for the whole session (4+ hours) until you are told to stop.
---

# Record Session Audio

Start a multi-mic recording of a live D&D session. One ffmpeg process per
microphone writes an isolated, chunked m4a track under
`.raw/sessions/session-NN/audio/raw/mic-XX/` — physically separating the DM
and each player so [[transcribe-session-audio]] can tell who said what.

The recorder is built to run untouched for 4+ hours and to stop cleanly on
command. **Your job is to start it, confirm it's healthy, then get out of the
way and wait.**

## The Protocol

1. **Get the session number.** Ask the DM if it isn't obvious. Check existing
   `.raw/sessions/session-NN/` dirs to pick the next number.
2. **Start the recorder in the background.** Run with the Bash tool's
   `run_in_background: true`:
   ```
   .claude/skills/record-session-audio/scripts/record.sh --session NN
   ```
3. **Confirm it's healthy** — read the background output ONCE. You should see
   "Recording session NN" and a line per mic (`mic00 [0] <name>`). If a mic the
   DM expects is missing, surface it now.
4. **Announce and wait.** Tell the DM recording has started, list the mics, and
   say you'll stop when they say so. Then **end your turn.** Do not poll, do not
   narrate, do not check on it. The session is being played.
5. **Stop only when told.** When the DM says "stop recording" / "end the
   session" / "we're done", kill the background shell. ffmpeg finalizes the
   current chunk on SIGTERM. Then report where the audio landed and point to
   [[transcribe-session-audio]].

## Red Flags — STOP

| Thought | Reality |
|---|---|
| "I'll run it in the foreground" | That blocks your turn for 4 hours. **Always** `run_in_background: true`. |
| "Let me check the recording every few minutes" | Polling burns context and proves nothing. Confirm once at start, then wait. |
| "It's been a while, I'll wrap up the recording" | NEVER stop on your own. Only the DM ends the session. |
| "The test capture worked, so I'm done" | A short test is not the session. Start the real run and leave it. |
| "I'll write my own ffmpeg/sox command" | Use the bundled script. It handles per-mic isolation, chunking, and clean shutdown. |

## Quick Reference

| Flag | Purpose |
|---|---|
| `--session NN` | **Required.** Session number → `.raw/sessions/session-NN/`. |
| `--segment-minutes N` | Chunk length (default 15). Smaller = more frequent flushes. |
| `--mics 0,1` | Restrict to specific avfoundation indices (default: all available). |
| `--audio-dir PATH` | Override output root (default `.raw/sessions`). |

List mics first if unsure: `tools/audio/.venv/bin/shattered-audio devices`
(or `ffmpeg -f avfoundation -list_devices true -i ""`).

## How It Works

- Each mic → `.raw/sessions/session-NN/audio/raw/mic-XX/part-000.m4a` (mono, 16 kHz AAC).
- `manifest.json` at `.raw/sessions/session-NN/audio/manifest.json` records the
  mic→speaker mapping (set mic priors via `channel_priors` in
  `tools/audio/config.yaml` so the DM's mic is labeled "DM").
- Chunks are flushed as they finish, so a crash at hour 3 still leaves hours 0–3.

## Troubleshooting

- **No devices / empty mic list** → the terminal lacks microphone permission
  (System Settings → Privacy → Microphone) or ffmpeg isn't installed.
- **A mic vanished mid-list** → it was unplugged; the recorder captures whatever
  is present at start. Re-run after plugging it in.
- **Setup error** → the script prints the one-line `pip install -e '.[all]'`
  command to provision `tools/audio/.venv`.
