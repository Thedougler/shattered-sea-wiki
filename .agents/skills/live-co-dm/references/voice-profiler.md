# Voice Profiler — how to run it

Captures a clean voice sample for **one character voice** and saves a reusable
profile the transcriber uses to separate speakers. Complete setup first (see
the README at `voice-transcription/` or `references/setup.md`).

## Run

The easiest way — the wrapper handles venv + HF token:

```bash
./save_voice.sh --name "Grigori" --player "Dave"
```

Or manually with the venv active:

```bash
source voice-transcription/.venv/bin/activate
export HF_TOKEN=hf_...
python3 -m voice_transcription.cli.save_voice --name "Grigori" --player "Dave"
```

Then open the printed URL (default http://localhost:8080) in a browser.

- `--name` — the **character voice** (e.g. `Grigori`, `Captain Nona`). One profile per
  voice, so a player who does three voices gets three profiles.
- `--player` — the **physical person** performing it (e.g. `Dave`). This groups a
  person's multiple character voices so the identifier can tell them apart.
- `--script-file PATH` — optional. Override the bundled teleprompter passage with your
  own text.
- `--port N` — optional, change the web port.

## At the keyboard

1. Click **Start**. The ASR model loads (a few seconds on first run), then recording
   begins. Read the teleprompter aloud — *in character* — at a natural pace. Words
   grey out as they are recognized, so you can see your progress. The default passage
   is deliberately funny and phonetically rich (~60–90s).
2. Click **Stop & Save**. The tool embeds the audio, shows status in the browser and
   terminal, and exits cleanly.
3. If it warns the new voice resembles an existing profile, that's expected for two
   voices by the same player — but if two *different* people collide, re-record one in a
   quieter room or with more vocal contrast.

## Where profiles go

`voice-transcription/profiles/<slug>.json` — small JSON (embedding as a float array +
metadata). These are **committed** to the repo so the whole table's voices travel with
the wiki. Re-running with the same `--name` overwrites that character's profile.

## Self-correcting profiles (correction loop)

Every time you save a profile, the tool doesn't just use the teleprompter read — it also
**harvests that character's lines from corrected past sessions** and folds them in:

1. The deliberate teleprompter read is the **anchor** (weighted heavily — it's clean,
   single-speaker, and long).
2. For each committed `wiki/sessions/session-NN-transcript.md` that still has its `.live`
   audio, the tool finds the spans attributed to **this character**, slices that audio,
   and embeds it. Lines marked `[overlap]` or low-confidence `(?)` are **skipped**.
3. Each harvested embedding is accepted only if it's similar enough to the anchor; stray
   mis-attributions are **rejected**, so correction can only sharpen a profile.

**The payoff:** after you correct and finalize a session transcript, just **re-save that
character's profile** — it automatically absorbs the corrected audio and gets more
accurate for next session.

## Tips for separable profiles

- Quiet room, consistent mic distance.
- Perform the *character* voice you'll actually use at the table, not your neutral voice.
- Longer and more varied beats short and flat — the teleprompter is built for this.
