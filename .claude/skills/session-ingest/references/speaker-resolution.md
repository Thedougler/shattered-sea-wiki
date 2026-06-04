# Speaker Resolution

How to resolve "Speaker 1", "Speaker N", and "Unknown" labels in raw
transcript part CSVs. This is Pass 1 of the session-ingest skill.

---

## The Problem

The transcription tool assigns speaker labels based on voice profiles. When a
speaker's mic signal drifts (volume change, position shift, background noise),
the tool may assign a generic "Speaker N" label instead of the correct profile.

In Shattered Sea transcripts:
- "Speaker 1" is most often Crissdalyn's player with mic drift
- "Speaker 6/7" are typically short cross-talk artifacts
- All Speaker N labels must be resolved before canon extraction

---

## Resolution Method

For each unresolved speaker label, analyze in order:

### 1. Conversational Context (highest signal)

Look at the 5 lines before and after. Who is the unresolved speaker talking to?
Who responds to them?

```
DM: "Is it just the one you have?"
Speaker 1: "I may have more."        ← Speaker 1 is answering the DM
Jean Claude: "It depends on the price" ← JC continues the same negotiation
```

If Speaker 1 is in a conversation with the DM about whip shark eggs and Jean
Claude is also in that conversation, Speaker 1 is likely Jean Claude (same
topic, same scene) or a different PC in the same scene.

### 2. Process of Elimination

Count known speakers in the transcript. If 4 PCs + DM should be present but
only 3 PCs are identified, the unresolved speaker is likely the missing PC.

Check line counts: if Crissdalyn and Speaker 1 together account for roughly
one player's share of the conversation (~13–15% of total lines), that's
suspiciously complementary — the tool is splitting one speaker into two profiles.

### 3. Speech Pattern Matching

Each player has verbal habits:
- Short affirmative responses ("Yeah", "Okay", "Yes") — common for all, low signal
- Specific vocabulary or phrases — high signal
- Response length patterns — moderate signal
- Topic engagement — a speaker who only talks during combat vs. shopping

### 4. Temporal Clustering

If Speaker 1 appears in bursts (50 lines, then absent for 200, then 30 lines),
check whether the identified speaker disappears during those same windows. Mic
drift tends to be persistent within a segment, not random.

**Same-second interleaving** is the strongest mic-drift signal: when the identified
speaker and the unknown speaker alternate within seconds (e.g., Crissdalyn at 53:18,
Speaker 1 at 53:22, Crissdalyn at 53:25), this is voice-profile oscillation from
the same physical mic — near-certain evidence they're the same person.

### 5. Mechanical Context

During combat:
- "DC 19? DC 19 strength." → a player asking about a save
- "Bardic, yeah." → a player with bardic inspiration (Perrin has a bodhran)
- "I'm at 12 HP." → specific PC context

During roleplay:
- Responding to NPC dialogue directed at a specific PC
- Using character-specific knowledge

---

## DM as NPC Voice

The DM label covers both narrator voice and NPC dialogue. You do NOT need to
split these — the DM label is correct for both. However, during extraction
(Pass 2), note when the DM is voicing a specific NPC so the canon extract
attributes the statement properly.

Signals that the DM is voicing an NPC:
- Dialogue within a conversation with PCs
- First/third person shift ("I would be happy to buy them" vs "He offers to buy")
- Named NPC was just introduced in narrator voice

## Player Voicing NPC

Players sometimes voice their companion NPCs (e.g., Crissdalyn's player voices
Kyzil). The speaker label is still correct — it's that player's voice — but the
content is IC dialogue from a different character. Flag these moments in Pass 2
extraction so the canon is attributed to the NPC, not the PC.

## External Audio Artifacts

Not all unresolved speakers are game participants. The table mic may pick up:
- Phone calls (the other end of a player's real-life call)
- TV/music in the background
- People in another room

Signals: conversation that makes no game sense, names not in the campaign,
real-world logistics ("can you have her call me"), different audio quality.

Resolution: label as "Phone (external)" or "Background" with low confidence.
These lines should be excluded entirely from canon extraction — add a note in
`flags.md` that they're non-game audio, not ambiguous game content.

---

## Speaker Map Format

Record every resolution in `speaker-map.md`:

```markdown
## Speaker Map — Session {NN}

### Resolved

| Label | Resolved To | Confidence | Evidence |
|---|---|---|---|
| Speaker 1 | Crissdalyn | high | Mic drift — complementary line counts, same-second interleaving, responds to Kyzil context |
| Speaker 6 | DM | medium | Short interjections during meta/NPC dialogue, no other speaker absent |
| Speaker 7 | Phone (external) | low | Non-game audio picked up from player's phone call |

### Cold-Pass Labels

If cold-pass chunks exist in `Inbox/` from the same session, also resolve
UNKNOWN labels from those files. These use a different label space
(`UNKNOWN_1`, `UNKNOWN_N`) but represent the same speakers.

| Label | Resolved To | Confidence | Evidence |
|---|---|---|---|
| UNKNOWN_1 | Crissdalyn | high | Same speaker as CSV "Speaker 1" — temporal overlap, complementary gaps |
| UNKNOWN_3 | Perrin | medium | Process of elimination — only unaccounted player |

To check which UNKNOWN labels exist in the chunks:
`grep -h 'UNKNOWN' Inbox/s{NN}-chunk-*.md | sort | uniq -c | sort -rn`

### Evidence Notes

Speaker 1 → Crissdalyn:
- Complementary line counts: Crissdalyn + Speaker 1 together = ~13% of total, a normal single-player share
- Same-second interleaving: voice profile oscillates between labels within seconds
- Responds to Kyzil context — only Crissdalyn's player would track Kyzil's turn
- Speaker 1 appears in every part, correlating with gaps in Crissdalyn's lines
```

### Confidence Levels

| Level | Meaning | Proceed? |
|---|---|---|
| **high** | Multiple evidence types converge | Yes |
| **medium** | One strong signal, no contradicting evidence | Yes, but note in flags.md |
| **low** | Best guess, limited evidence | Flag for DM review before Pass 2 |
| **unknown** | Cannot determine | Block Pass 2, escalate to DM |

---

## Applying Resolutions

The speaker map has two downstream consumers:

1. **Pass 2 (extraction):** The extracting agent reads raw part CSVs and
   mentally replaces Speaker N labels per the map. No intermediate resolved
   CSV is produced.

2. **Pass 1b (voice profile retraining):** The `--speaker-map` flag on
   `shattered-audio retrain` reads the resolution table (including the
   Cold-Pass Labels section) and remaps UNKNOWN labels in the chunk
   markdown during parsing. Only high/medium confidence entries are used.

For `low` confidence resolutions, prefix the resolved name with `?` in extracts
and recap (e.g., `?Perrin`) so downstream consumers know those attributions are
uncertain. Low-confidence entries are excluded from retrain automatically.

---

## Scanning Across Parts

Speaker resolution reads all available part CSVs (`session{NN}-part*.m4a.csv`)
to build a unified map. Useful approaches:

1. **Quick grep** — find all Speaker N lines across parts:
   ```bash
   grep -hn 'Speaker' audio/sessions/session{NN}-part*.m4a.csv
   ```
2. **Sample windows** — for each unknown label, read 10–15 surrounding lines
   from the part where it appears most frequently
3. **Cross-part patterns** — check whether the unknown label appears in every
   part (persistent mic drift) or only a few (isolated event)
