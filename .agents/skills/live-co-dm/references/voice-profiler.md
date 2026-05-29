# Voice Profiler — how to run it

Captures a clean voice sample for **one character voice** and saves a reusable
profile the transcriber uses to separate speakers. Complete `setup.md` first.

## Run

```bash
source .claude/skills/live-co-dm/.venv/bin/activate
export HF_TOKEN=hf_...            # for the pyannote embedding model
python3 .claude/skills/live-co-dm/scripts/voice_profiler.py \
    --name "Grigori" --player "Dave"
```

Then open the printed URL (default http://localhost:8080) in a browser.

- `--name` — the **character voice** (e.g. `Grigori`, `Captain Nona`). One profile per
  voice, so a player who does three voices gets three profiles.
- `--player` — the **physical person** performing it (e.g. `Dave`). This groups a
  person's multiple character voices so the identifier can tell them apart.
- `--script-file PATH` — optional. Override the bundled teleprompter passage with your
  own text. The agent can generate a custom, character-flavored script and pass it here;
  the tool just displays whatever text it's given.
- `--port N` — optional, change the web port.

## At the keyboard

1. Click **Start** and read the auto-scrolling teleprompter aloud — *in character* — at
   a natural pace. The default passage is deliberately funny and phonetically rich
   (plosives, sibilants, rolled Rs, dynamic range) to get a strong embedding. Aim for
   the full read (~60–90s).
2. Click **Stop & Save**. The tool embeds the audio and writes
   `.claude/skills/live-co-dm/profiles/<character-slug>.json`.
3. If it warns the new voice resembles an existing profile, that's expected for two
   voices by the same player — but if two *different* people collide, re-record one in a
   quieter room or with more vocal contrast.

## Where profiles go

`profiles/<slug>.json` — small JSON (embedding as a float array + metadata). These are
**committed** to the repo so the whole table's voices travel with the wiki. Re-running
with the same `--name` overwrites that character's profile.

## Tips for separable profiles

- Quiet room, consistent mic distance.
- Perform the *character* voice you'll actually use at the table, not your neutral voice.
- Longer and more varied beats short and flat — the teleprompter is built for this.
