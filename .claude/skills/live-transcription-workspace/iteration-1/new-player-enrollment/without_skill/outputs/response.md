# Setting Up Jordan's Voice Profile

The transcription system (`shattered-audio`) uses voice embeddings to identify who is speaking during live sessions. Here is the full walkthrough for getting Jordan enrolled.

---

## Prerequisites

The `shattered-audio` tool lives at `tools/audio/` and needs its venv with the `live` extras installed (which pulls in `resemblyzer` for voice embeddings and `sounddevice` for mic recording). The venv already exists at `tools/audio/.venv/`. Activate it with:

```
source tools/audio/.venv/bin/activate
```

Or invoke the CLI directly:

```
tools/audio/.venv/bin/shattered-audio
```

---

## Step 1: Enroll Jordan's Voice

The CLI has a dedicated `enroll` command. There are two ways to capture the voice sample.

### Option A: Record live from a microphone (recommended)

Have Jordan sit at the mic and speak naturally for 15-30 seconds -- reading aloud, introducing themselves, or just chatting. Longer samples produce better embeddings.

```
shattered-audio enroll "Jordan" --record 30
```

This records 30 seconds from the default mic at 16kHz mono, extracts a d-vector embedding via resemblyzer, and saves it to the profiles directory.

### Option B: Enroll from an existing audio file

If you already have a recording of Jordan (voice memo, Discord clip, etc.):

```
shattered-audio enroll "Jordan" /path/to/jordan-sample.wav
```

Any format pydub can read works (wav, mp3, m4a, etc.). The tool converts it to 16kHz mono internally.

### What gets created

Two files land in `~/.config/shattered-audio/profiles/`:

| File | Contents |
|---|---|
| `jordan.npy` | 256-dimensional voice embedding (numpy array) |
| `jordan_meta.yaml` | Display name, sample count, optional mic associations |

You can verify enrollment by checking:

```
ls ~/.config/shattered-audio/profiles/jordan*
cat ~/.config/shattered-audio/profiles/jordan_meta.yaml
```

The meta file will look like:

```yaml
name: Jordan
sample_count: 1
```

---

## Step 2: (Optional) Associate Jordan with a specific microphone

If your table setup assigns each player a dedicated mic (e.g., Jordan always uses USB mic #3), you can set up a **channel prior** so the system gives a confidence boost when Jordan's voice comes from that mic. This is configured in your `config.yaml`.

First, check what mics are available:

```
shattered-audio devices
```

This lists all input devices with IDs and names. Then create or edit the config file at `~/.config/shattered-audio/config.yaml`:

```yaml
mic_names:
  - "MacBook Pro Microphone"
  - "USB Audio Device"       # Jordan's mic, for example

channel_priors:
  mic_0: "Nick"
  mic_1: "Jordan"

channel_boost: 0.15
speaker_threshold: 0.7
```

The `channel_priors` map mic IDs (assigned in order from `mic_names`) to expected speaker names. When audio arrives from `mic_1` and somewhat matches Jordan, the system adds a +0.15 cosine-similarity boost, making correct identification more likely in noisy conditions.

This step is optional -- the voice embedding alone works without mic priors -- but it meaningfully improves accuracy when you have per-player mics.

---

## Step 3: (Optional) Strengthen the profile with multiple samples

A single enrollment works, but accuracy improves with more samples. You can re-run the enroll command:

```
shattered-audio enroll "Jordan" --record 30
```

The system detects the existing profile and blends the new embedding with the old one (70% new, 30% old). The `sample_count` in the meta file increments. Two or three enrollment passes with different speech samples (different energy levels, topics, vocal registers) produce a more robust profile.

---

## Step 4: Verify during the live session

When you start the live session:

```
shattered-audio live --session <N> --speakers "Nick,Jordan,..."
```

The CLI loads all profiles from `~/.config/shattered-audio/profiles/` and prints which ones it found:

```
Voice profiles: nick, Jordan
```

If it prints `No voice profiles loaded`, the profiles directory is wrong or empty -- check the `profiles_dir` setting in your config.

During the session, the hot pass (real-time transcription) identifies each utterance's speaker by comparing its voice embedding against all loaded profiles. If confidence falls below the threshold (default 0.7), the speaker is labeled `UNKNOWN_N` in the live transcript.

---

## Step 5: Retrain after the first session (recommended)

After the session, you will have a transcript with speaker labels. Review it, correct any misattributions (change `UNKNOWN_1` to `Jordan` where appropriate), then retrain:

```
shattered-audio retrain /path/to/corrected-transcript.md --audio-dir /path/to/chunks/ --blend 0.7
```

This parses the `[HH:MM:SS] **Speaker:** text` lines from the transcript, extracts the corresponding audio segments, and updates each speaker's embedding. The `--blend` flag controls how much weight goes to the new data (0.7 = 70% new, 30% old). After one real session of retraining, Jordan's profile will be significantly more accurate.

---

## Quick Reference

| Task | Command |
|---|---|
| List audio devices | `shattered-audio devices` |
| Enroll from mic (30s) | `shattered-audio enroll "Jordan" --record 30` |
| Enroll from file | `shattered-audio enroll "Jordan" /path/to/file.wav` |
| Check profiles | `ls ~/.config/shattered-audio/profiles/` |
| Start live session | `shattered-audio live -s <N>` |
| Retrain after session | `shattered-audio retrain <transcript.md> --blend 0.7` |

---

## Troubleshooting

**"No voice profiles loaded"** -- The CLI looks for profiles in `~/.config/shattered-audio/profiles/` by default. If you moved the directory, set `profiles_dir` in `~/.config/shattered-audio/config.yaml`.

**Jordan keeps showing as UNKNOWN** -- The threshold is too high for the current embedding quality. Either lower `speaker_threshold` in config (try 0.6), enroll with a longer/cleaner sample, or retrain after manually correcting a transcript.

**"resemblyzer not installed"** -- The `live` optional dependency group is required. Install it: `pip install -e ".[live]"` from `tools/audio/`.
