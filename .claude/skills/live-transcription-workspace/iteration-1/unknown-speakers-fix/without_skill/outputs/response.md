# Fixing UNKNOWN Speakers in an Existing Transcript and Improving Future Accuracy

## How Speaker Identification Works

The `shattered-audio` tool has two layers of speaker identification:

1. **Voice profiles** (resemblyzer d-vector embeddings) — stored at `~/.config/shattered-audio/profiles/`. Each profile is an `.npy` embedding + a `_meta.yaml` file. The system compares each utterance's audio against all enrolled profiles using cosine similarity. If the best match exceeds the `speaker_threshold` (default 0.70), the speaker is assigned. If nothing clears the threshold, the utterance is labeled `UNKNOWN_N`.

2. **Channel priors** — optional config that maps a mic name to an expected speaker, giving that speaker a score boost (`channel_boost`, default 0.15). This helps when players have dedicated mics.

During a live session, the **hot pass** (fast model, real-time) and **cold pass** (accurate model, per-chunk) both run `identify_speaker()` from `profiles.py`. If no profiles are loaded or none match above threshold, you get UNKNOWNs.

---

## Part 1: Fixing the Existing Transcript

You have two options depending on the transcript format.

### Option A: CSV-based transcript (NotebookLM / assemble pipeline)

This is what you used for Session 04. The CSVs have a `Speaker` column. The fix workflow:

1. **Run the assemble command** to get a single continuous transcript:
   ```
   cd tools/audio && .venv/bin/shattered-audio assemble <SESSION_NUMBER> --audio-dir ../../audio/sessions
   ```
   This produces `assembled.csv` and prints a speaker distribution showing how many lines are unresolved.

2. **Identify who the unknown speakers are.** Look at the distribution output. For each `Speaker N` or `Unknown` label:
   - Read lines around each unknown cluster in context — what are the adjacent known speakers saying? Who is being addressed?
   - Check if the line count for a known speaker seems suspiciously low (suggesting their voice drifted to an unknown label). Session 04's `Speaker 1` was Crissdalyn because Crissdalyn's count was 275 and Speaker 1 was 262 — together they matched the expected volume for one player.
   - Look for self-identifying content ("I cast...", references to their own character).

3. **Create a resolved CSV.** Once you know the mappings, produce a `resolved.csv` with the Speaker column corrected. You can do this with a script or a find-and-replace. The Session 04 pattern (`audio/sessions/session04/speaker-map.md` + `resolved.csv`) is the established convention.

4. **Document your evidence** in a `speaker-map.md` alongside the resolved CSV (as was done for Session 04). This is important for audit trail.

### Option B: Markdown transcript (live session / shattered-audio transcribe)

If the transcript is in the `[HH:MM:SS] **Speaker:** text` format:

1. Open the markdown file (e.g., `Inbox/current.md` or `Inbox/s<NN>-chunk-<NNN>.md`).
2. Find-and-replace `**UNKNOWN_1:**` (etc.) with the correct speaker name.
3. Use the same contextual analysis — who's talking, who's being addressed, what's the content.

### After fixing either format: retrain profiles

Once you have a corrected transcript, feed it back to improve future sessions:

```
cd tools/audio
.venv/bin/shattered-audio retrain <path-to-corrected-transcript.md> \
  --audio-dir <dir-with-chunk-wavs> \
  --blend 0.7
```

The `retrain` command:
- Parses `[HH:MM:SS] **Speaker:** text` lines from the corrected markdown
- Extracts the corresponding audio segments from the WAV files
- Skips any lines still labeled `UNKNOWN`
- Blends new embeddings with existing profiles (default: 70% new, 30% old)
- Saves updated `.npy` profiles to `~/.config/shattered-audio/profiles/`

**Important:** The retrain command expects markdown format (`[HH:MM:SS] **Speaker:** text`), not CSV. If your corrected transcript is in CSV format, you'll need to convert it first, or manually enroll speakers from audio clips (see below).

---

## Part 2: Improving Future Accuracy

There are several independent levers, ordered from highest to lowest impact.

### 1. Enroll all players' voice profiles

Right now you only have a profile for `nick` (2 samples). Every other player has no profile, which means the system has nothing to match against — hence the UNKNOWNs.

Enroll each player either from a file or by recording:

```
# From an audio file where the speaker talks for 10+ seconds:
.venv/bin/shattered-audio enroll "DM" path/to/dm-speaking.wav
.venv/bin/shattered-audio enroll "Delmar" path/to/delmar-speaking.wav
.venv/bin/shattered-audio enroll "Jean Claude" path/to/jc-speaking.wav
.venv/bin/shattered-audio enroll "Crissdalyn" path/to/crissdalyn-speaking.wav
.venv/bin/shattered-audio enroll "Perrin" path/to/perrin-speaking.wav

# Or record live (N seconds from default mic):
.venv/bin/shattered-audio enroll "DM" --record 30
```

For the audio file approach, you can extract clean segments from your existing Session 04 `.m4a` parts. Pick stretches where you're confident a single speaker is talking for 10-30 seconds (longer is better). Use `ffmpeg` to extract:

```
ffmpeg -i session04-part00.m4a -ss 00:00:29 -to 00:01:00 -ac 1 -ar 16000 dm-sample.wav
```

Each `enroll` call blends with any existing profile (30% old + 70% new), so calling it multiple times with different samples improves accuracy.

### 2. Configure channel priors

If players have dedicated microphones (or consistent seating positions relative to mics), add `channel_priors` to your config. Create `~/.config/shattered-audio/config.yaml` (or a project-local `config.yaml` in `tools/audio/`):

```yaml
vault_path: /Users/nick/ai-os/shattered-sea/wiki
mic_names:
  - "MacBook Pro Microphone"    # or whatever your devices are called
  - "USB Audio Device"          # a second mic if you have one

channel_priors:
  mic_0: DM                    # DM sits nearest mic_0
  mic_1: Delmar                # Delmar sits nearest mic_1

channel_boost: 0.15            # cosine similarity bonus for expected speaker on that mic
```

Run `shattered-audio devices` to see your available input devices and their names. The `mic_names` list controls which devices are opened during a live session. Channel priors give a +0.15 cosine similarity bonus to the expected speaker on that mic, which helps break ties.

### 3. Lower the speaker threshold (carefully)

The default threshold is 0.70 cosine similarity. If you have good profiles enrolled and are still getting UNKNOWNs, you can lower it:

```yaml
speaker_threshold: 0.60
```

Don't go below ~0.55 or you'll start getting false positives (wrong speaker assigned with high confidence). Monitor the `speaker_confidence` values in the cold pass chunk frontmatter to calibrate.

### 4. Use multiple microphones

The system supports multi-mic capture (`MultiMicCapture` in `capture.py`). Each utterance is attributed to the mic with the highest RMS energy. Combined with channel priors, this dramatically improves identification because you're comparing a cleaner signal (from the closest mic) against the voice profile.

Even a second USB mic positioned on the opposite side of the table helps.

### 5. Retrain after every session

Make it a habit: after each session, correct the transcript's speaker labels (at least the high-confidence ones) and run `retrain`. The profiles get better with more samples. The current `nick` profile only has 2 samples — ideally you want 5-10+ per speaker.

### 6. Use the speakers flag during batch transcription

When running the non-live `transcribe` command, pass `--speakers` to hint the expected speakers:

```
.venv/bin/shattered-audio transcribe audio.m4a -s 5 --speakers "DM,Delmar,Jean Claude,Crissdalyn,Perrin"
```

This tells pyannote diarization how many speakers to expect (`num_speakers`), which improves its clustering. Without this hint, it guesses the speaker count and often gets it wrong.

---

## Quick-Start Checklist for Next Session

1. Enroll all 5 speakers (DM + 4 PCs) using clean audio from Session 04
2. Create `~/.config/shattered-audio/config.yaml` with `mic_names`, `channel_priors`, and `vault_path`
3. Run a test: `shattered-audio live -s 0 --speakers "DM,Delmar,Jean Claude,Crissdalyn,Perrin"` and talk for 30 seconds — verify speakers are identified in `Inbox/current.md`
4. After the session, correct any remaining UNKNOWNs and run `retrain`

---

## Reference: Key File Paths

| File | Purpose |
|---|---|
| `tools/audio/src/shattered_audio/profiles.py` | Voice profile enrollment, identification, and retraining logic |
| `tools/audio/src/shattered_audio/config.py` | Config schema — all tunable parameters |
| `tools/audio/src/shattered_audio/hot_pass.py` | Real-time transcription pass (where UNKNOWN labels originate) |
| `tools/audio/src/shattered_audio/cold_pass.py` | Accurate per-chunk pass (also does speaker ID) |
| `tools/audio/src/shattered_audio/cli.py` | CLI commands: `transcribe`, `live`, `enroll`, `retrain`, `assemble`, `devices` |
| `~/.config/shattered-audio/profiles/` | Voice profile storage (`.npy` + `_meta.yaml` per speaker) |
| `~/.config/shattered-audio/config.yaml` | User config (does not exist yet — create it) |
| `audio/sessions/shattered-sea-dictionary.csv` | Whisper spelling corrections (name normalization, not speaker ID) |
| `audio/sessions/session04/speaker-map.md` | Example of how Session 04's speaker resolution was documented |
