# Voice Profiler — moved

Voice-profile capture and management now live in the **manage-voice-profiles** skill,
backed by the `tools/audio` (`shattered-audio`) engine. The old `save_voice.sh` /
`voice-transcription/` teleprompter flow described here is retired.

Profiles can also be saved directly from real session audio via the **transcribe-session-audio**
skill's `--save-profile` flag.

## Actor → persona model

Each real person at the table is an **actor** (their natural, out-of-character voice). Each
character voice they perform is a **persona** enrolled under that actor. A player who does
three voices = 1 actor + up to 3 personas. Enroll only the voices you actually need; you can
add personas later.

Profiles live at `~/.config/shattered-audio/profiles/` on each machine.

## Key commands

`voices.sh` is shorthand for `.claude/skills/manage-voice-profiles/scripts/voices.sh`, run
from repo root.

```bash
# Enroll an actor (real person, natural OOC voice)
voices.sh enroll "Nick" --record 30

# Enroll a persona (character voice, grouped under an actor)
voices.sh enroll "Grigori" --actor "Nick" --record 30

# List all enrolled actors and personas
voices.sh profiles

# Live speaker-ID test — TUI that shows who the mic hears in real time
voices.sh watch
```

## Correction loop

After each session the **session-ingest** `speaker-map.md` + `shattered-audio retrain
--speaker-map` loop folds transcript corrections back into the profiles. Accuracy improves
session over session without re-recording.

See the **live-transcription** skill for engine internals and speaker-ID tuning parameters.

## Tips for separable profiles

- Quiet room, consistent mic distance.
- Perform the *character* voice you'll actually use at the table, not your neutral voice.
- Longer and more varied samples beat short and flat ones — aim for at least 30 seconds of
  natural speech with varied cadence.
- If two voices collide (similarity warning), re-record one with more vocal contrast or in a
  quieter environment.
