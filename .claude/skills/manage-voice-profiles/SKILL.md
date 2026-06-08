---
name: manage-voice-profiles
description: >
  Use when adding, viewing, updating, deleting, or testing voice profiles for
  session speaker identification. Triggers: "/manage-voice-profiles", "enroll voice",
  "save my voice", "add voice profile", "voice profile", "list profiles", "delete
  profile", "test voice recognition", "who is speaking", "watch voices", "speaker ID",
  "save character voice", "new player setup", "voice profiles", "player voices".
  Authoritative reference for all voice profile CRUD — use instead of
  transcribe-session-audio when the task is managing profiles, not processing audio.
---

# Manage Voice Profiles

CRUD and live-testing for the voice profiles that drive automatic speaker
identification in [[transcribe-session-audio]] and [[record-session-audio]].

Profiles live at `~/.config/shattered-audio/profiles/` and are **auto-loaded**
by every transcription run.

**Wrapper:** `.claude/skills/manage-voice-profiles/scripts/voices.sh <subcommand>`
proxies all args to `shattered-audio` via the repo venv.

## The Actor → Persona Model

Each real person at the table is an **actor**. Each character voice they perform
is a **persona** under that actor.

| Level | What it captures | Example |
|---|---|---|
| Actor | Natural speaking voice (OOC, rules questions) | `Nick` |
| Persona | An in-character voice they perform | `Crissdalyn` under `Nick` |

**Always enroll two profiles per player:** actor first, then their character(s).

**DM has multiple personas** — one per voiced NPC. Example setup:

```
DM (actor)
├── Thunk     (persona)
├── Grigori   (persona)
└── … any other voiced NPCs
```

## Quick Reference

**Output the terminal command, then let the DM run it themselves.**

### List

```bash
.claude/skills/manage-voice-profiles/scripts/voices.sh profiles
.claude/skills/manage-voice-profiles/scripts/voices.sh profiles "Nick"  # detail view
```

### Create / Update (Enroll)

```bash
# Actor — natural speaking voice. Record 30+ seconds of natural OOC speech.
.claude/skills/manage-voice-profiles/scripts/voices.sh enroll "Nick" --record 30

# DM actor (sets the is_dm flag)
.claude/skills/manage-voice-profiles/scripts/voices.sh enroll "DM" --record 30 --dm

# Persona — actor must exist first. Speak in character for 30+ seconds.
.claude/skills/manage-voice-profiles/scripts/voices.sh enroll "Crissdalyn" --actor "Nick" --record 30

# Enroll from an audio file instead of recording live
.claude/skills/manage-voice-profiles/scripts/voices.sh enroll "Nick" path/to/nick.m4a

# Best quality: harvest minutes of speech from a real session
.claude/skills/transcribe-session-audio/scripts/transcribe.sh --session 7 --save-profile "Nick" --from-mic mic01
.claude/skills/transcribe-session-audio/scripts/transcribe.sh --session 7 --save-profile "Crissdalyn" --from-mic mic01 --actor Nick
```

Re-enrolling an existing name **merges** (blends 70% new / 30% old embedding),
silently — there is no confirmation prompt.

**One mic, multiple voices — important.** `--save-profile --from-mic` harvests
*all* of that mic's audio indiscriminately. It is correct for a one-voice
person, but for a player who voices several characters on the same mic (the DM,
or Sarah doing Vex + Lyra), harvesting "Vex" from her mic blends her OOC speech
*and* her Lyra lines into the Vex profile. For multi-voice people, enroll each
persona deliberately with live `--record` (they speak in-character), or refine
from a **corrected transcript** where lines are labelled `Name (as Persona)` —
[[transcribe-session-audio]]'s retrain path segments audio by that label and is
the accurate way to refresh multi-voice profiles from session audio.

### Delete

```bash
# Delete one persona only
.claude/skills/manage-voice-profiles/scripts/voices.sh delete "Crissdalyn" --actor "Nick"

# Delete actor + all their personas
.claude/skills/manage-voice-profiles/scripts/voices.sh delete "Nick"

# Skip confirmation
.claude/skills/manage-voice-profiles/scripts/voices.sh delete "Nick" --yes
```

### Live Test TUI

```bash
.claude/skills/manage-voice-profiles/scripts/voices.sh watch
```

Listens on the default mic (energy-gated VAD), identifies each utterance, and
prints a rolling table — no audio is recorded or saved. Ctrl+C to stop.

```
Time      Speaker                Confidence
09:14:22  DM → Thunk             0.81
09:14:31  Nick                   0.76
09:14:55  DM                     0.71
```

Optional flags: `--mic N` (device index from `voices.sh devices`),
`--threshold 0.02` (louder rooms), `--history 20`.

## New-Player Setup Workflow

1. `voices.sh profiles` — confirm not already enrolled
2. Player speaks naturally (OOC) for 30s: `voices.sh enroll "PlayerName" --record 30`
3. Player speaks as character for 30s: `voices.sh enroll "CharName" --actor "PlayerName" --record 30`
4. `voices.sh watch` — both speak; confirm their names appear

## DM Multi-Persona Setup

```bash
voices.sh enroll "DM" --record 30 --dm
voices.sh enroll "Thunk" --actor "DM" --record 30    # speak as Thunk
voices.sh enroll "Grigori" --actor "DM" --record 30  # speak as Grigori
```

Add more NPCs the same way as they are given recurring voiced roles.

## How Profiles Are Used Automatically

During `transcribe-session-audio`:
1. Stage 1 — actor identified via d-vector embedding (resemblyzer)
2. Stage 2 — persona distinguished via embeddings + prosody (pitch, speaking rate)
3. Fallback — mic prior from `channel_priors` in `tools/audio/config.yaml`

Confidence tiers in output: **high** ≥ 0.8, **medium** 0.7–0.8, **low** < 0.7.

## Troubleshooting

| Problem | Fix |
|---|---|
| All labels show `Speaker micNN` | No profiles enrolled or channel_priors not set |
| Character misidentified as actor's OOC voice | Need more enrollment samples — use `--record 60` or harvest from session |
| `sounddevice not installed` (watch fails) | `cd tools/audio && .venv/bin/pip install -e '.[all]'` |
| Wrong profiles dir | Check `profiles_dir` in `tools/audio/config.yaml`; default is `~/.config/shattered-audio/profiles/` |
| Persona confidence too low | Lower `persona_margin` in config (default 0.05) |
