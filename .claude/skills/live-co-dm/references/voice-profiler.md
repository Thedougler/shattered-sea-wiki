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

## Self-correcting profiles (correction loop)

Every time you save a profile, the tool doesn't just use the teleprompter read — it also
**harvests that character's lines from corrected past sessions** and folds them in:

1. The deliberate teleprompter read is the **anchor** (weighted heavily — it's clean,
   single-speaker, and long).
2. For each committed `wiki/sessions/session-NN-transcript.md` that still has its `.live`
   audio, the tool finds the spans attributed to **this character**, slices that audio,
   and embeds it. Lines marked `[overlap]` or low-confidence `(?)` are **skipped** — they
   are exactly the audio most likely to be the wrong voice.
3. Each harvested embedding is accepted only if it's similar enough to the anchor; stray
   mis-attributions that survived your edits are **rejected**, so correction can only
   sharpen a profile, never poison it.

**The payoff:** after you correct and finalize a session transcript (fixing any
mislabeled lines), just **re-save that character's profile** — it automatically absorbs
the corrected, real in-character audio and gets more accurate for next session. The saved
profile records how many spans were folded in (`enhanced_spans`) and from which sessions
(`enhanced_sessions`).

This only kicks in for sessions whose `.live` audio still exists (it's gitignored scratch;
don't delete it if you want to keep improving profiles). No corrected sessions yet, or no
audio left? Saving still works — you just get the plain teleprompter profile.

## Tips for separable profiles

- Quiet room, consistent mic distance.
- Perform the *character* voice you'll actually use at the table, not your neutral voice.
- Longer and more varied beats short and flat — the teleprompter is built for this.
