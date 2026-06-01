---
name: session-ingest
description: >
  Use when raw session transcript CSVs in audio/sessions/ need processing. Triggers:
  "process the transcript", "mine the session", "clean the transcript", "what's in
  the session audio", "fix speakers", "who is Speaker 1", new session*.csv files in
  audio/sessions/. Also use when combat stats need recording from session audio, or
  when wiki needs updating from transcript data. Symptoms: Speaker 1/Unknown labels
  in transcript, OOC chatter mixed with canon, fragmented 1-second utterances,
  unprocessed session audio.
---

# Session Ingest

Multi-pass data mining of raw session transcription CSVs. Each pass produces a
checkpoint file so work survives context limits, partial transcriptions, and session
boundaries. Downstream consumers: `transcript-ingest.md`, `session-recap`,
`world-update`, `combat-analytics.md`, `player-interests.md`.

---

## Entry Point

Every invocation starts the same way:

```bash
python3 .claude/scripts/assemble_transcript.py status {NN}
```

This reports parts available, checkpoint state, and staleness. Then route:

| Status says | Do |
|---|---|
| Pass 1 stale or missing | Run `assemble {NN}` → continue to Pass 2 |
| Pass 2 not started | Read `references/speaker-resolution.md` → resolve speakers |
| Pass 2 done, resolved.csv missing | Run `resolve {NN}` → continue to Pass 3 |
| Pass 3 not started | Read `references/extraction-targets.md` → process first chunk |
| Pass 3 partial | Read `handoff.md` → process next chunk |
| Pass 3 done, flags unresolved | Present flags to DM → wait |
| Pass 3 done, Pass 4 not started | Load `ttrpg-wiki-ingest` → wiki integration from recap |
| All passes complete | Report status, nothing to do |

## Required Skill Chain

Run `ttrpg-llm-wiki-init` once at session start. Load `ttrpg-writing` when writing
prose for wiki pages. Sandbox rules are in CLAUDE.md (always loaded).

---

## Input

| File | Format | Location |
|---|---|---|
| Transcript parts | CSV: `ID,Start,End,Speaker,Text` | `audio/sessions/session{NN}-part{PP}.m4a.csv` |

The transcription tool applies the custom dictionary (`shattered-sea-dictionary.csv`)
automatically — the CSVs already have corrected spellings. Parts arrive
incrementally as audio transcribes. Process whatever is available.

## Working Directory

Each session: `audio/sessions/session{NN}/`

All intermediate files live here. These are checkpoints — resume from the latest one.

| File | Produced By | Purpose |
|---|---|---|
| `assembled.csv` | Pass 1 (script) | Concatenated parts with continuous timestamps |
| `parts.txt` | Pass 1 (script) | Manifest of which parts were assembled |
| `speaker-map.md` | Pass 2 | Speaker resolution decisions with evidence |
| `resolved.csv` | Pass 2 (script) | Speaker-corrected transcript |
| `recap.md` | Pass 3 (cumulative) | Condensed IC-only scene summaries |
| `extracts.md` | Pass 3 (cumulative) | Tagged canon extracts organized by scene |
| `flags.md` | Pass 3 (cumulative) | Unresolved ambiguities for DM review |
| `progress.txt` | Pass 3 (per chunk) | Which line ranges have been processed |
| `handoff.md` | Pass 3 (per chunk) | Self-contained prompt for the next agent |

---

## Pass Architecture

```dot
digraph passes {
  rankdir=LR;
  node [shape=box];
  "Raw CSVs" [shape=folder];
  "wiki/" [shape=folder];

  "Raw CSVs" -> "Pass 1\nAssemble";
  "Pass 1\nAssemble" -> "Pass 2\nResolve Speakers";
  "Pass 2\nResolve Speakers" -> "Pass 3\nExtract & Recap";
  "Pass 3\nExtract & Recap" -> "Pass 4\nWiki Integration";
  "Pass 4\nWiki Integration" -> "wiki/";
}
```

If a checkpoint file exists and its source data hasn't changed, skip that pass.
Use `status` to detect staleness before starting work.

---

### Pass 1: Assemble

**Scripted — no agent judgment needed.**

```bash
python3 .claude/scripts/assemble_transcript.py assemble {NN}
```

This concatenates all parts with continuous IDs and cumulative timestamps (all
`H:MM:SS`) and writes `assembled.csv`. Dictionary corrections are already applied
by the transcription tool. The script reports speaker distribution and flags
unresolved labels.

Re-run when new parts arrive — it overwrites from source CSVs.

**Checkpoint:** `assembled.csv` exists. `parts.txt` lists all available parts.
Run `status` to check for staleness (new parts since last assembly).

---

### Pass 2: Resolve Speakers

**Requires agent judgment.** Read `references/speaker-resolution.md`.

Input: `assembled.csv`
Output: `resolved.csv` + `speaker-map.md`

Goal: every "Speaker 1", "Speaker N", and "Unknown" label resolved to a known
speaker with evidence and confidence rating.

**Subagent strategy for large transcripts (3000+ lines):** Chunk into ~1500-line
windows with 100-line overlap (aim for 5–7 subagents total). Each subagent
resolves speakers in its chunk. Coordinating agent merges speaker maps (majority
vote on conflicts).

After the speaker map is written, produce `resolved.csv` mechanically:

```bash
python3 .claude/scripts/assemble_transcript.py resolve {NN}
```

This reads the speaker map table and applies label replacements to `assembled.csv`.
Low-confidence resolutions get a `?` prefix (e.g., `?Perrin`).

**Checkpoint:** `resolved.csv` exists and `speaker-map.md` has no `unknown`
confidence entries.

**Commit after this pass** — speaker resolution is durable work worth preserving:
```
fix: resolve speakers for session {NN} transcript
```

---

### Pass 3: Extract & Recap (One Chunk Per Agent)

**Requires agent judgment.** Read `references/extraction-targets.md`.

Input: `resolved.csv` + `wiki/hot.md` (for context, not for writing)
Output: `extracts.md` + `recap.md` + `flags.md`

This pass processes `resolved.csv` one ~800-line chunk at a time. **Each agent
processes exactly one chunk, commits, writes a handoff prompt, and stops.** The
next agent (or the same user in a new conversation) picks up the handoff. No wiki
writes happen here — the recap and extracts are the deliverables.

#### Processing One Chunk

1. **Determine your chunk.** Check `progress.txt` — if it exists, read the last
   entry to find where the previous agent stopped. Your chunk starts from the next
   line (minus ~20 lines of overlap for context). If `progress.txt` doesn't exist,
   start at line 1. Read ~800 lines (prefer breaking at a scene boundary).

2. **Classify lines** as IC (in-character), OOC (out-of-character), or META
   (rules talk, dice rolls). A Florida food tangent is OOC even when spoken by
   "Delmar" — use surrounding context, not just speaker labels.

3. **Merge fragments.** Consecutive lines from the same speaker within 3 seconds
   with no intervening speaker → single utterance. The transcription tool produces
   many 1-second clips that are one sentence when merged.

4. **Identify scenes.** Scene breaks on: location change, significant time skip,
   major topic shift, new NPC entrance. Label each scene with location and
   participants.

5. **Extract canon per scene.** Use the tag types in `extraction-targets.md`.
   Every extract cites source line range from `resolved.csv`.

6. **Flag uncertainties.** Ambiguous canon, possible transcription errors with
   lore significance, speaker-dependent meaning → append to `flags.md`.

7. **Append to `recap.md`** — condensed IC-only scene summaries (see format below).

8. **Append to `extracts.md`** — tagged extracts with full detail and line citations.

9. **Record progress** — append the chunk's line range to `progress.txt`:
   ```
   chunk-1: lines 1-800 (2026-06-01)
   ```

10. **Commit:**
    ```
    ingest: session {NN} transcript chunk {N} (lines {start}–{end})
    ```

11. **Write handoff prompt and stop.** Write `handoff.md` with a self-contained
    prompt for the next agent (see format below). Then **stop — do not process
    the next chunk.**

#### Recap Format

`recap.md` is a condensed, DM-facing record of in-game events only. No OOC, no
meta, no rules discussion, no table banter. Each scene gets a short paragraph
covering what happened in the fiction — who did what, what was said, what changed.

```markdown
# Session {NN} Recap

Source: audio/sessions/session{NN}/resolved.csv
Extraction date: {YYYY-MM-DD}

---

## Scene 1: {Location} — {Brief label}
*{H:MM:SS}–{H:MM:SS} | {Participants}*

{1–3 sentences of what happened in-game. Factual, not narrative. Name NPCs
and PCs on first mention. Note items exchanged, decisions made, information
revealed.}

---

## Scene 2: ...
```

The recap should read like a concise event log — someone skimming it should know
every consequential thing that happened in-game without wading through OOC chatter
or mechanical details. Combat gets a sentence or two on outcome and consequences,
not blow-by-blow.

#### Handoff Prompt Format

After committing, write `handoff.md` with a prompt the next agent can use
verbatim. This file is overwritten each chunk — it always reflects the current
state.

```markdown
# Session Ingest Handoff — Session {NN}

## Status
- Chunks completed: {N} of ~{total estimated}
- Lines processed: 1–{end_line} of {total_lines}
- Last scene in recap: "{scene label}"

## Next Action
Process the next chunk of session {NN} transcript using the `session-ingest`
skill. Start from line {next_start_line} of `audio/sessions/session{NN}/resolved.csv`.

## Context
{2–3 sentences: what was happening at the end of this chunk — the active scene,
who was talking, any thread that was mid-conversation when the chunk boundary
hit. Enough for the next agent to maintain continuity.}

## Files to Read First
- `audio/sessions/session{NN}/progress.txt` — chunk history
- Tail of `audio/sessions/session{NN}/recap.md` — last scene for continuity
- `audio/sessions/session{NN}/flags.md` — any open flags
```

#### Final Chunk

When the chunk reaches the end of `resolved.csv`, instead of writing a
continuation handoff, do a final pass:
- Verify `recap.md` covers the full session timeline with no gaps
- Verify `extracts.md` has tagged entries for every scene
- Review `flags.md` — present any unresolved items to the DM
- Write `handoff.md` indicating Pass 3 is complete and Pass 4 (wiki integration)
  is next
- Commit:
  ```
  ingest: complete session {NN} transcript extraction and recap
  ```

**Checkpoint files:** `recap.md` (cumulative), `extracts.md` (cumulative),
`flags.md`, `progress.txt`, `handoff.md`.

---

### Pass 4: Wiki Integration

**Uses existing pipeline.** Load `ttrpg-wiki-ingest` and read its
`references/transcript-ingest.md`. Load `ttrpg-writing` for prose standards.

Input: `recap.md` + `extracts.md` + `flags.md` (resolved)
Output: Wiki file changes

Before starting: verify `flags.md` has no unresolved items that would block
canon. If it does, present flags to the DM and wait.

The recap is the primary source for narrative content (session note, entity
updates). The extracts provide structured data for mechanical files (combat
analytics, player interests). Use both:

| Wiki Target | Primary Source |
|---|---|
| Session note (`wiki/sessions/session-{NN}.md`) | `recap.md` scenes |
| Entity pages (NPCs, locations, items) | `recap.md` + `[NPC]`/`[ITEM]` extracts |
| `wiki/dm/combat-analytics.md` | `[COMBAT]` extracts |
| `wiki/dm/player-interests.md` | `[SIGNAL]` extracts |
| Situation and faction files | `[CANON]` extracts + `recap.md` |
| `wiki/hot.md` | `recap.md` end state |

Commit:
```
ingest: wiki integration from session {NN} transcript
```

**Checkpoint:** Session note exists and `hot.md` updated date matches.

---

## Incremental Processing

Audio parts arrive as transcription completes. Run `status` to detect what changed:

| Status says | Action |
|---|---|
| New parts, no previous work | Run all passes from scratch |
| New parts, Pass 1 done | Re-run `assemble` (script detects new parts via `parts.txt`), then resume Pass 2 |
| New parts, Pass 2 done | Re-run `assemble`, re-run `resolve` (speaker map still applies), resume Pass 3 from the first unprocessed chunk per `progress.txt` |
| New parts, Pass 3 partially done | Re-run `assemble` + `resolve`, continue Pass 3 from next unprocessed chunk — earlier chunks' recap entries are already committed |
| Pass 3 done, Pass 4 not started | Start wiki integration from the completed recap + extracts |
| All parts present, all passes done | Report status, nothing to do |

The sequential chunk architecture makes incremental processing straightforward:
earlier chunks are fully committed, so new parts only add new chunks at the end.

---

## Invocation Modes

| Mode | Trigger | Action |
|---|---|---|
| `status` | "transcript status", "what's available" | List sessions with CSVs, report pass completion |
| `process` | "process session N transcript" | Run all passes for session N |
| `resume` | "continue session N" | Find latest checkpoint, resume |
| `speakers` | "fix speakers", "who is Speaker 1" | Run Pass 2 only |
| `extract` | "what happened in session N" | Run through Pass 3, report |
| `combat` | "combat stats from session N" | Extract `[COMBAT]` blocks only |

---

## Known Speaker Labels

| CSV Label | Identity | Notes |
|---|---|---|
| DM | Nick (game master) | Also voices all NPCs — context distinguishes |
| Delmar | Delmar Fisk's player | |
| Perrin | Perrin Black-Jaw's player | |
| Jean Claude | Jean-Claude Tabarnack's player | |
| Crissdalyn | Crissdalynn Khinriss's player | Label spelling ≠ character spelling |
| Speaker 1 | Usually Crissdalyn (mic drift) | Verify per session via speaker-resolution.md |
| Speaker 5/6/7 | Varies — cross-talk, external audio | Low line counts; often DM or non-game audio |
| Speaker N | Unknown | Always resolve before Pass 3 |

---

## Quality Gates

Before starting Pass 3 (chunk loop):
- All Speaker N labels resolved (medium+ confidence)

Per chunk (before committing):
- Extracts cite source line ranges from `resolved.csv`
- Recap paragraph covers only in-game events (no OOC, no meta)
- No `[CANON]` block contradicts existing wiki without a flag

After Pass 3 (before Pass 4):
- `recap.md` covers the full session timeline with no scene gaps
- `extracts.md` has tagged entries for every scene in the recap
- `progress.txt` line ranges span the entire `resolved.csv`
- Combat encounters have round counts and per-PC action summaries
- `[SIGNAL]` blocks present if players showed clear engagement/disengagement
- All unresolved items in `flags.md` presented to DM

After Pass 4:
- Session note exists with wikilinks for all named entities
- `wiki/hot.md` reflects end-of-session world state

---

## Reference Files

| File | When |
|---|---|
| `references/speaker-resolution.md` | Pass 2 — resolving unknown speakers |
| `references/extraction-targets.md` | Pass 3 — what to extract and how to tag it |
