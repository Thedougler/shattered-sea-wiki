# Fixing UNKNOWN Speaker Labels

Two separate problems here: fixing the transcript you already have, and reducing UNKNOWNs in future sessions. Both are straightforward.

---

## Part 1: Fix the Existing Transcript

### Step 1 -- Manually relabel UNKNOWN lines

Open each chunk file in `Inbox/` (files named `sNN-chunk-NNN.md`). The transcript format is:

```
[00:14:23] **UNKNOWN:** I cast Eldritch Blast at the cultist.
```

Replace `UNKNOWN` with the correct speaker name:

```
[00:14:23] **Nick:** I cast Eldritch Blast at the cultist.
```

You can usually figure out who's talking from context -- what character they're playing, what they said, the conversation flow. If you have multiple UNKNOWNs in a row, the audio chunks are saved as WAV files alongside the markdown (`Inbox/sNN-chunk-NNN.wav`), so you can listen back to confirm.

### Step 2 -- Retrain profiles from the corrected transcript

Once your labels are fixed, feed the corrected transcript back into the voice profiles:

```bash
shattered-audio retrain Inbox/s12-chunk-001.md --audio-dir Inbox/ --blend 0.7
```

Do this for each chunk you corrected. The `--blend 0.7` flag means 70% weight on the new data and 30% on the existing profile, so each retrain meaningfully updates the speaker embedding.

The retrain command:
- Parses the timestamps and speaker labels from the markdown
- Extracts the corresponding audio segments from the WAV file
- Skips any lines still labeled UNKNOWN (so leave those if you genuinely can't tell)
- Skips segments shorter than 0.5 seconds
- Updates the `.npy` profile files in `~/.config/shattered-audio/profiles/`

Repeat for every chunk file you corrected. More corrected data means better profiles.

---

## Part 2: Reduce UNKNOWNs in Future Sessions

UNKNOWN labels happen when the cosine similarity between an utterance's voice embedding and every enrolled profile falls below the `speaker_threshold` (default: 0.7). There are several causes and fixes, roughly in order of impact.

### Lower the speaker threshold

The default of 0.7 is conservative. If you're getting a lot of UNKNOWNs but rarely getting *wrong* speaker labels, drop it:

In your `config.yaml` (at `./config.yaml` or `~/.config/shattered-audio/config.yaml`):

```yaml
speaker_threshold: 0.60
```

Start at 0.65 and go lower if needed. If you start seeing wrong names assigned, bump it back up. The threshold is a tradeoff: lower catches more speakers but risks misidentification.

### Set channel priors

If each player sits near a specific mic, channel priors give that speaker a confidence boost (+0.15 by default) on utterances from their mic. This can push borderline UNKNOWN matches over the threshold.

```yaml
channel_priors:
  mic_0: "Nick"
  mic_1: "Alex"
  mic_2: "Chad"
channel_boost: 0.15
```

The mic names (`mic_0`, `mic_1`, etc.) correspond to the order mics appear in `mic_names`. Run `shattered-audio devices` to see available devices and set `mic_names` to control ordering.

### Re-enroll with longer samples

The resemblyzer voice encoder needs sufficient audio to build a reliable d-vector. If profiles were enrolled with short clips, they'll be noisy. Re-enroll with 30+ seconds of natural speech:

```bash
shattered-audio enroll "Nick" --record 30
```

Have each player talk naturally -- don't read a script, just chat. Re-enrolling blends with the existing profile (30% old, 70% new) so it won't throw away prior data.

If you already did the retrain step above, your profiles are already improved. But a clean 30-second enrollment in a quiet room can still help, especially for players whose voices were underrepresented in the session audio.

### Short utterances are inherently hard

Utterances under about 2 seconds produce unreliable embeddings -- the voice encoder just doesn't have enough signal. These will often come back as UNKNOWN regardless of settings. This is a known limitation of the resemblyzer approach and there isn't a config fix for it. The retrain loop is the best mitigation: the more session data you feed back, the better the profiles get at matching even shorter segments.

### Check profile health

Verify your profiles exist and look reasonable:

```bash
ls ~/.config/shattered-audio/profiles/
```

You should see one `.npy` and one `_meta.yaml` per speaker. If a player is missing entirely, that explains their UNKNOWNs -- enroll them. The `_meta.yaml` files show `sample_count`; higher is generally better. After a few retrain cycles, profiles with 10+ samples should be quite reliable.

---

## Summary of the Workflow

```
Session produces UNKNOWNs
  --> Manually fix speaker labels in Inbox/sNN-chunk-NNN.md
  --> shattered-audio retrain <chunk.md> --audio-dir Inbox/
  --> (repeat for each chunk)
  --> Adjust config: lower threshold, add channel_priors
  --> Next session should be better
```

The retrain loop is the core mechanism. Each session you correct and retrain makes the next session more accurate. After 2-3 sessions of corrections, UNKNOWN rates should drop significantly.
