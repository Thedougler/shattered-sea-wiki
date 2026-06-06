# Setting Up a Voice Profile for Jordan

Three steps: enroll their voice, optionally configure a mic prior, and verify it works.

---

## 1. Enroll Jordan's Voice

Make sure the `shattered-audio` venv is active (`tools/audio/.venv`), then run:

```
shattered-audio enroll "Jordan" --record 30
```

This records 30 seconds from the default mic and generates a 256-dimensional d-vector embedding. Jordan should speak naturally during the recording -- full sentences at a conversational pace, not single words. The more representative the sample, the better the speaker ID will perform during play.

The command creates two files:

- `~/.config/shattered-audio/profiles/jordan.npy` -- the embedding vector
- `~/.config/shattered-audio/profiles/jordan_meta.yaml` -- metadata

If you already have a recording of Jordan (e.g., from a session zero or a voice memo), you can enroll from file instead:

```
shattered-audio enroll "Jordan" recording.wav
```

30 seconds is the practical minimum. Shorter samples degrade cosine similarity matching, especially for short utterances during play.

---

## 2. (Optional) Set a Channel Prior

If Jordan will consistently sit near a specific microphone, you can give the system a hint. Open your config file (`./config.yaml` or `~/.config/shattered-audio/config.yaml`) and add a `channel_priors` entry mapping that mic to Jordan:

```yaml
channel_priors:
  mic_0: "Nick"
  mic_2: "Jordan"
```

The mic index corresponds to the order listed by `shattered-audio devices`. This adds a cosine similarity boost (default `+0.15`) when audio comes from that mic, which helps with short or ambiguous utterances. It is not required -- the voice embedding alone handles identification -- but it noticeably improves accuracy when everyone has a consistent seat.

---

## 3. Verify with a Test Session

Run a throwaway live session to confirm Jordan's name appears correctly in the transcript:

```
shattered-audio live --session 99
```

Have Jordan say a few sentences, then Ctrl+C to stop. Check `Inbox/current.md` -- Jordan's name should appear as the speaker label on their lines. If their utterances show up as `UNKNOWN` or misattributed to another player:

- **Too many UNKNOWNs:** Lower `speaker_threshold` in config (e.g., from `0.7` to `0.65`). Short utterances under ~2 seconds often fall to UNKNOWN regardless -- that is a known limitation of resemblyzer.
- **Wrong speaker assigned:** The embedding may not be distinct enough. Re-enroll with a longer sample (45-60s), or raise `speaker_threshold` to `0.75` to tighten matching.
- **Inconsistent results:** Check `speaker_confidence` values in chunk frontmatter to see per-speaker similarity scores. If Jordan's scores hover near the threshold, a channel prior will help push them over.

---

## 4. After the First Real Session

Once you have actual session audio with corrected speaker labels, you can refine Jordan's profile:

1. Review the chunk files in `Inbox/` (e.g., `Inbox/s13-chunk-001.md`) and fix any lines where Jordan was misidentified.
2. Retrain from the corrected transcript:

```
shattered-audio retrain Inbox/s13-chunk-001.md --audio-dir Inbox/ --blend 0.7
```

This blends the new embedding with the existing one (70% new, 30% old), so the profile improves over time without losing the original enrollment data.

---

## Quick Reference

| What | Command |
|---|---|
| Enroll from mic | `shattered-audio enroll "Jordan" --record 30` |
| Enroll from file | `shattered-audio enroll "Jordan" recording.wav` |
| List mics | `shattered-audio devices` |
| Test session | `shattered-audio live --session 99` |
| Retrain after corrections | `shattered-audio retrain <chunk.md> --audio-dir Inbox/` |
| Profile location | `~/.config/shattered-audio/profiles/jordan.npy` |
