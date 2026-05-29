---
name: ttrpg-wiki-ingest
description: >
  Ingest new Shattered Sea source material into the wiki. Use this skill whenever
  the user says "ingest", "process this into the wiki", "digest this document",
  "decompose this source", "link this into the wiki", "what hasn't been ingested",
  "what's pending", "process the inbox", "catch up the wiki", "clear the backlog",
  or when new files appear in `Inbox/` or `.raw/`. It finds pending sources with one
  script, pulls them in batches so a large queue never floods context, pre-compiles
  each source's cross-link map so the agent spends its window reasoning about content
  instead of rediscovering the wiki, classifies each source, extracts durable canon
  without inventing, decomposes the source into the right wiki pages, cross-links them,
  updates index/log/hot.md, then archives the source so it drops off the queue. This is
  the general ingestion orchestrator; load the narrower reference files for transcript
  ingest and decomposition rather than treating them as separate top-level skills.
---

# TTRPG Wiki Ingest

Use this skill to move source material from raw notes, transcripts, handouts, rules
drafts, or source documents into the durable Shattered Sea wiki.

The job is not summarization. The job is canon extraction, decomposition, and writeback:
identify what is now true, decide where each fact belongs, update the smallest necessary
set of wiki files, and leave the source traceable.

---

## Required Skill Chain

Run `ttrpg-llm-wiki-init` once at session start (boot checks, routing). Load `ttrpg-writing`
when you write prose. Cross-cutting rules — reading order, frontmatter, the auto-correct
protocol — are in `wiki/system/doctrine.md`; load it on demand rather than re-deriving them.

Load domain skills only when the source produces that content:

| Output Needed | Load |
|---|---|
| NPC or crew page | `prep-npc` |
| Location page | `prep-location` |
| Faction page or faction clock | `prep-faction`, `faction-clock` |
| Situation with lifecycle or clock | `prep-situation`, `sandbox-narrative` |
| Session note from reviewed transcript | `transcript-ingest.md` reference in this skill |
| Rules/homebrew page | `ttrpg-writing`, relevant rules references |

If a named downstream skill is missing or only exists as an empty stub, keep going with
the corresponding reference workflow here and write the wiki files directly.

These references and skills stay resident in your context across the whole queue — load
each once and reuse it for every source. That shared, loaded-once context is exactly why
processing the queue serially in one agent is cheaper than it looks: the expensive setup is
paid a single time, not re-paid per source.

---

## The Queue Is a Script, Not a Document

One command tells you everything that is left to do:

```bash
python3 .claude/scripts/check_ingest.py            # all pending paths, one per line
python3 .claude/scripts/check_ingest.py --count    # just the number (scan mode)
python3 .claude/scripts/check_ingest.py --limit 6  # only the next 6 pending paths (a batch)
```

It prints one repo-relative path per source that still needs ingesting — every file in
`Inbox/` whose exact content (by hash) is not yet stored anywhere in `.raw/`. It also
deduplicates `Inbox/` automatically and safely on each run:

- If an `Inbox/` file is an exact byte-for-byte match for something already in `.raw/`, it is
  removed because that source was already archived.
- If multiple `Inbox/` files have the same exact content and none is in `.raw/`, it keeps one
  deterministic pending source and removes the extra copies.

**No paths printed means the queue is empty and you are done** (it also says `queue clear` on
stderr). Paths mean those files still need work. `--count` prints only the number, for scan mode.
Use `--dry-run` to preview duplicate removals without deleting; use `--no-dedupe` only when you
explicitly need a diagnostic read without cleanup.

You never need to know what was already ingested, only what remains. The filesystem is the
source of truth: there is no registry to read, reconcile, or trust, because archiving a
finished source (step 6) moves it from `Inbox/` into `.raw/`, and that move is exactly what
removes it from the next run. Ingest fully, archive, and the source disappears from the list.
Stray duplicates are cleaned during the same queue check, so the loop does not accumulate
manual tidy work.

### Pull work in batches, process one source at a time

For a large queue, don't read all 300 paths into context — pull a batch with `--limit N`
(N≈6), process **each source in that batch to completion, one at a time**, then archive the
batch, commit, and run the script again for the next batch. The `--limit` flag exists precisely
so your working context holds one short batch, never the whole backlog. The list is shorter
every pass, and that is the point.

Do this even when the queue is hundreds deep. Do not summarize the whole queue or plan all the
sources up front.

Two reasons this discipline matters:

- **Quality does not degrade with queue depth.** A source gets the same full decomposition
  and cross-linking whether it is the only file waiting or the three-hundredth. Working through
  a short batch one source at a time is what protects that — you are never tempted to batch-skim
  ten transcripts. A backlog is not permission to rush; the last source's NPCs deserve the same
  reciprocal links as the first.
- **Interruptions cost almost nothing.** Re-running the script each pass confirms the previous
  archive actually landed (the file is gone from the list), and a run that stops halfway resumes
  correctly with no state to reconstruct — just run the script and keep going.

### Picking the next source

The script lists paths alphabetically; it does not rank them. When more than one remains,
use judgment from the filename and a quick look at the top of the file:

1. Reviewed clean session transcripts and session notes (they set the chronology others link to).
2. DM-declared canon updates.
3. Entity / location / faction / situation notes.
4. Rules and homebrew with table impact.
5. Player-facing handouts needing publish control.
6. Assets and research/guidance documents.

For a one-pass run this order barely matters — every source is processed eventually. It matters
only when a session can't finish the whole queue: do the spine first.

---

## Compile the Cross-Link Map Before Decomposing

A source's hardest, most context-hungry step is figuring out what it connects to: which named
people, places, factions, and situations already have pages (link them by slug) versus which are
new (maybe a stub). Re-deriving that map by reading `index.md` for every source burns the context
you want spent on the source itself. One script does the lookup for you:

```bash
python3 .claude/scripts/ingest_packet.py Inbox/<Source>.md
```

It scans the source for `[[wikilinks]]`, frontmatter targets, and capitalized proper nouns,
matches them against `index.md`, and prints a compact packet:

- **Existing pages** the source likely links to, as `slug — summary` — so you link by slug
  without opening the page.
- **Candidate stubs** — concrete names with no page yet, which you should create a stub for only
  if they are durable campaign objects.

The packet is advisory, not authoritative: you still decide what is a real durable link versus a
passing mention. It just starts you from the map instead of making you rebuild it. Run it once per
source as you begin step 4.

---

## Reference Files

Read only the file needed for the current task.

| File | Read When |
|---|---|
| `references/source-triage.md` | A new document needs classification and routing |
| `references/decompose-and-writeback.md` | Any source must be split into wiki pages |
| `references/transcript-ingest.md` | Reviewed clean transcript becomes session/wiki canon |
| `references/quality-gates.md` | Before finalizing wiki writes |

---

## Modes

| Mode | Trigger | Output |
|---|---|---|
| `scan` | "what's pending?", "what hasn't been ingested?" | Count from `check_ingest.py`; recommended next source |
| `ingest` | "ingest", "process the inbox", "catch up the wiki" | Run the loop below: triage → decompose → write → archive → commit, one source at a time in batches, until the script returns nothing |

For `scan`, run the script and report the count and the recommended next source. Don't dump
the whole list into chat unless the user asks. For `ingest`, process the queue autonomously in
priority order without stopping to ask which to do first. The only reasons to pause are a
genuine lore contradiction or ambiguous entity identity (see the auto-correct protocol in
`doctrine.md`); flag those, leave that one source in `Inbox/`, and keep going on the rest.

---

## Standard Workflow

This is the per-source body of the loop. Run steps 2–5 for each path in the current batch, then
finalize the batch once in step 6.

### 1. Preflight (once per session)

Read `wiki/hot.md` for current world state. CLAUDE.md is already in context; load `doctrine.md`
only if you need the cross-cutting rules.

### 2. Source Handling

The source content is immutable — never rewrite or clean it up. It is **relocated** once fully
ingested: archiving moves it from `Inbox/` into `.raw/<type>/` (step 6). During ingest, read it
in place.

For large sources:

- Read headings, frontmatter, and obvious entity names first.
- Use `rg` to locate repeated proper nouns, dates, session numbers, rulings, and canon tags.
- Chunk only the sections needed to answer the ingest plan.
- Preserve uncertainty as uncertainty; do not turn noisy source material into canon.

### 3. Classify

Read `references/source-triage.md`. Classify the source (it may be more than one type), then
name the expected wiki outputs before writing anything.

### 4. Decompose

Run `ingest_packet.py` on the source (see "Compile the Cross-Link Map" above) to get its existing
links and candidate stubs. Then read `references/decompose-and-writeback.md` and break the source
into durable claims — entity facts, situation pressures, faction moves, player-facing knowledge,
DM secrets, rules, session chronology, open questions — giving each claim one canonical home.
Other pages link to that home instead of copying.

### 5. Write Back

Write the smallest useful set of files. For every wiki file touched:

1. Preserve existing canon unless the source explicitly supersedes it.
2. Keep `summary` informative and no longer than two sentences.
3. Use wikilinks for entities, locations, factions, sessions, and situations.
4. Add reciprocal links when the relationship is durable.
5. Add stubs only for concrete referenced entities, not vague possibilities.
6. Append a one-line entry to `wiki/log.md`.

Frontmatter completeness and `updated` are handled by the write hook — don't hand-maintain them.
Do not hand-edit `wiki/index.md`; it is regenerated in step 6.

Update `wiki/hot.md` when the source changes current world state, active situations, faction
clocks, PC threads, or predictions.

### 6. Archive, Regenerate Index, and Commit

Archive each source as you finish it (this is the per-source completion signal), then regenerate
the index and commit **once per batch** rather than once per source — the index is deterministic,
so regenerating it after the whole batch is identical to doing it N times and far cheaper, and a
batch commit matches how these ingests are already grouped in history.

```bash
# per source, as each is fully written back:
python3 .claude/scripts/archive_source.py Inbox/<Source>.md --type <triage-type>

# once, after the batch is fully ingested:
python3 .claude/scripts/regen_index.py --write
git add wiki .raw Inbox
git commit -m "ingest: <Source A>, <Source B>, … — <short output summary>"
```

Do not ask the DM for permission to commit routine ingests. (Blocked or contradiction-flagged
sources are the exception: leave them in `Inbox/` un-archived, flag the question, and move on —
they will still show up in `check_ingest.py` until resolved, which is correct.) If a run is
interrupted mid-batch, archived-but-uncommitted sources show in `git status` and any un-archived
source still appears in `check_ingest.py`, so the next run resumes cleanly either way.

### 7. Quality Gates

Read `references/quality-gates.md` before moving to the next batch.

Then run the script again:

```bash
python3 .claude/scripts/check_ingest.py --limit 6
```

The sources you just finished should be gone from the output. If one isn't, its archive didn't
land — check before continuing. If the output is now empty, the queue is clear and you're done.
Otherwise, take the next batch and repeat from step 2.

If you edited this skill itself, run `python3 .claude/scripts/sync_skills.py --apply` to
regenerate `.agents/skills/`.

---

## Source Truth Rules

- Raw source beats generated prose. If the wiki disagrees with the source, flag the
  contradiction unless the wiki has a later source.
- A clean reviewed transcript beats raw transcript noise.
- DM instruction in the current user request beats old source notes.
- Existing wiki canon beats model inference.
- Never add a secret, motive, relationship, clock, or consequence because it "fits".

If two established facts conflict, append to `wiki/discrepancy-log.md` and leave both source
traces visible. Escalate to the DM instead of resolving it.

---

## Output To User

For scan mode:

```markdown
Pending ingest: N files
Recommended next source: ...
```

For ingest mode:

```markdown
Ingested: source path(s) → archived to .raw/<type>/
Created/Updated: wiki files
Committed: <commit subject(s)>
Flags for DM: none / list
```

Keep the final answer short. The durable record belongs in the wiki and the git history, not
in chat.
