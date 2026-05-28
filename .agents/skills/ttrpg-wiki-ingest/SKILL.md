---
name: ttrpg-wiki-ingest
description: >
  Ingest new Shattered Sea source material into the wiki. Use this skill whenever
  the user says "ingest", "process this into the wiki", "digest this document",
  "decompose this source", "link this into the wiki", "what hasn't been ingested",
  "what's pending", "update the ingest registry", or when new files appear in
  `.raw/` or `Inbox/`. It scans for unprocessed sources, classifies them, extracts
  durable canon without inventing, decomposes large source documents into the right
  wiki pages, updates links/index/log/hot.md, and keeps `wiki/ingest-registry.md`
  current. This is the general ingestion orchestrator; load the narrower reference
  files for transcript ingest and registry maintenance rather than treating them as
  separate top-level skills.
---

# TTRPG Wiki Ingest

Use this skill to move source material from raw notes, transcripts, handouts, rules
drafts, or source documents into the durable Shattered Sea wiki.

The job is not summarization. The job is canon extraction, decomposition, and writeback:
identify what is now true, decide where each fact belongs, update the smallest necessary
set of wiki files, and leave the source traceable.

---

## Required Skill Chain

Load these first:

1. `ttrpg-llm-wiki-init` — boot checks, `wiki/hot.md`, routing, structure.
2. `ttrpg-writing` — DM reference mode, player-facing mode, anti-slop rules.
3. This skill.

Load domain skills only when the source produces that content:

| Output Needed | Load |
|---|---|
| NPC or crew page | `prep-npc` |
| Location page | `prep-location` |
| Faction page or faction clock | `prep-faction`, `faction-clock` |
| Situation with lifecycle or clock | `prep-situation`, `sandbox-narrative` |
| Session note from reviewed transcript | `transcript-ingest.md` reference in this skill |
| Rules/homebrew page | `ttrpg-writing`, relevant rules references |
| Registry-only update | `ingest-registry-update.md` reference in this skill |

If a named downstream skill is missing or only exists as an empty stub, keep going with
the corresponding reference workflow here and write the wiki files directly.

---

## Reference Files

Read only the file needed for the current task.

| File | Read When |
|---|---|
| `references/pending-source-scan.md` | User asks what is pending, or before any ingest run |
| `references/source-triage.md` | A new document needs classification and routing |
| `references/decompose-and-writeback.md` | Any source must be split into wiki pages |
| `references/transcript-ingest.md` | Reviewed clean transcript becomes session/wiki canon |
| `references/ingest-registry-update.md` | Registry must be synced or statuses changed |
| `references/quality-gates.md` | Before finalizing wiki writes |

Helper script:

```bash
python3 .claude/skills/ttrpg-wiki-ingest/scripts/scan_pending.py --include-root-docs
```

Use `--json` when another script or automation needs machine-readable output.

---

## Modes

Choose one mode before reading source content.

| Mode | Trigger | Output |
|---|---|---|
| `scan` | "what's pending?", "what hasn't been ingested?" | Pending-source report; registry sync recommendation |
| `triage` | A source exists but the wiki outputs are unknown | Source classification, planned outputs, blocked/ready state |
| `ingest` | User asks to process a specific ready source | Wiki file edits, registry update, log entry |
| `resume` | Work queue or partial registry entry exists | Continue the last source from the recorded next action |
| `audit` | User suspects stale or missing ingest status | Compare `.raw/`, `Inbox/`, registry, and wiki outputs |

Do not run an unbounded ingest over many files unless the DM explicitly asks. If the scan
finds more than five pending files, report the queue and ask which source to process first.

---

## Standard Workflow

### 1. Preflight

1. Read `CLAUDE.md`.
2. Read `wiki/hot.md`.
3. Read `wiki/system/task-routing.md`.
4. Read `wiki/ingest-registry.md`.
5. Run the pending-source scan if the task is not tied to one explicit source.

Use:

```bash
python3 .claude/skills/ttrpg-wiki-ingest/scripts/scan_pending.py --include-root-docs
```

### 2. Source Handling

Treat the source file as immutable. Never rewrite, clean up, or move the raw source during
ingest unless the user explicitly asks.

For large sources:

- Read headings, frontmatter, and obvious entity names first.
- Use `rg` to locate repeated proper nouns, dates, session numbers, rulings, and canon tags.
- Chunk only the sections needed to answer the ingest plan.
- Preserve uncertainty as uncertainty; do not turn noisy source material into canon.

### 3. Classification

Read `references/source-triage.md`.

Classify the source as one or more of:

- `session`
- `transcript`
- `entity-source`
- `situation-source`
- `location-source`
- `faction-source`
- `rules-or-homebrew`
- `handout-or-player-facing`
- `asset`
- `research-or-guidance`

Then name the expected wiki outputs before writing anything.

### 4. Decompose

Read `references/decompose-and-writeback.md`.

Break the source into durable wiki claims:

- Entity facts
- Situation pressures
- Faction actions or clocks
- Player-facing knowledge
- DM-only secrets
- Rules/mechanics
- Session chronology
- Open questions and contradictions

One fact should have one canonical home. Other pages link to that home instead of copying.

### 5. Write Back

Write the smallest useful set of files. For every wiki file touched:

1. Preserve existing canon unless the source explicitly supersedes it.
2. Set `updated` to today's date.
3. Keep `summary` informative and no longer than two sentences.
4. Use wikilinks for entities, locations, factions, sessions, and situations.
5. Add reciprocal links when the relationship is durable.
6. Add stubs only for concrete referenced entities, not vague possibilities.
7. Update `wiki/index.md`.
8. Append a one-line entry to `wiki/log.md`.

Update `wiki/hot.md` when the source changes current world state, active situations,
faction clocks, PC threads, or predictions.

### 6. Registry

Read `references/ingest-registry-update.md`.

Every ingest run ends by updating `wiki/ingest-registry.md`:

- New discovered source: `pending`
- Source currently being worked: `in-progress`
- Source fully propagated to wiki: `ingested`
- Source intentionally ignored: `skipped` with reason
- Source blocked on DM judgment: `blocked` with the exact question

List concrete wiki output paths in the registry. Do not write "various pages".

### 7. Quality Gates

Read `references/quality-gates.md` before final response.

Minimum checks:

- `git diff --check`
- Run the pending-source scan again if registry status changed.
- Confirm `.claude` and `.agents` skill packages stay mirrored when editing this skill.

---

## Source Truth Rules

- Raw source beats generated prose. If the wiki disagrees with the source, flag the
  contradiction unless the wiki has a later source.
- A clean reviewed transcript beats raw transcript noise.
- DM instruction in the current user request beats old source notes.
- Existing wiki canon beats model inference.
- Never add a secret, motive, relationship, clock, or consequence because it "fits".

If two established facts conflict, append to `wiki/discrepancy-log.md` and leave both
source traces visible. Escalate to the DM instead of resolving it.

---

## Output To User

For scan mode, return:

```markdown
Pending ingest: N files
Ready: ...
Blocked: ...
Recommended next source: ...
```

For ingest mode, return:

```markdown
Ingested: source path
Updated: wiki files
Created: wiki files
Registry: status
Flags for DM: none / list
Verification: commands run
```

Keep the final answer short. The durable record belongs in the wiki, registry, and log.
