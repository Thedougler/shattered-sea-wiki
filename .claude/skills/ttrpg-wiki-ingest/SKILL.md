---
name: ttrpg-wiki-ingest
description: >
  Use when ingesting source material into the Shattered Sea wiki. Triggers: "ingest",
  "process this into the wiki", "digest this document", "decompose this source",
  "what hasn't been ingested", "what's pending", "process the inbox", "catch up the
  wiki", "clear the backlog", or new files appearing in Inbox/. Also use when the user
  asks about ingest status or wants to check what remains to process.
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

## Dedup Before Anything Else (Mandatory Gate)

**Before reading a single source, run:**

```bash
python3 .claude/scripts/check_ingest.py --count
```

This does two things atomically:

1. **Prunes duplicates** — removes any `Inbox/` file whose bytes already exist in `.raw/`
   (already archived) or that is a duplicate of another pending file. Removals print to stderr.
2. **Reports the true queue depth** — only genuinely new sources remain. The count printed to
   stdout is the real work.

If the prune removed tracked files (`git rm`), commit the cleanup before starting ingest:

```bash
git add Inbox/ && git diff --cached --quiet || git commit -m "fix: prune already-ingested duplicates from Inbox"
```

**Do not skip this step.** A large Inbox can be 50–70% duplicates. Processing them wastes
context, produces no wiki output, and risks conflicting writes if a source is half-ingested
and also present in `.raw/`. The script is cheap (hashes + byte compare); the ingest loop is
expensive. Gate the expensive work behind the cheap check.

Only after the count is stable (zero removals reported) do you proceed to the ingest loop.

## The Queue

After dedup, the same script gives you your work list:

```bash
python3 .claude/scripts/check_ingest.py            # all pending paths, one per line
python3 .claude/scripts/check_ingest.py --limit 6  # next batch of 6
```

**No paths printed means the queue is empty and you are done** (it also says `queue clear` on
stderr). `--dry-run` previews removals without deleting; `--no-dedupe` skips cleanup for
diagnostic reads only.

The filesystem is the source of truth. Archiving a finished source (step 6) moves it from
`Inbox/` into `.raw/`, which removes it from the next run. There is no registry to keep in sync.

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
| `scan` | "what's pending?", "what hasn't been ingested?" | Run dedup, report removals + true pending count |
| `ingest` | "ingest", "process the inbox", "catch up the wiki" | Dedup gate → loop: triage → decompose → write → archive → commit, until queue empty |

For `scan`, run the script (which prunes duplicates) and report: how many were pruned, how many
genuinely remain, and the recommended next source. Don't dump the whole list unless asked.

For `ingest`, run the full dedup gate (step 0), then process the queue autonomously in priority
order without stopping to ask which to do first. The only reasons to pause are a genuine lore
contradiction or ambiguous entity identity (see the auto-correct protocol in `doctrine.md`);
flag those, leave that one source in `Inbox/`, and keep going on the rest.

---

## Standard Workflow

### 0. Dedup Gate (once per session, before any source work)

Run `python3 .claude/scripts/check_ingest.py --count`. Let it prune. Commit removals if any
tracked files were cleaned. This is a hard prerequisite — do not proceed to step 1 until the
gate passes cleanly (the count reflects only genuinely pending sources, and stderr shows no
further removals on re-run).

### 1. Preflight (once per session)

Read `wiki/hot.md` for current world state. CLAUDE.md is already in context; load `doctrine.md`
only if you need the cross-cutting rules.

Then pull your first batch: `python3 .claude/scripts/check_ingest.py --limit 6`

Steps 2–5 run for each path in the current batch; step 6 finalizes the batch.

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
Dedup: removed N already-archived duplicates from Inbox
Pending ingest: M files
Recommended next source: ...
```

For ingest mode:

```markdown
Dedup: removed N duplicates (Inbox 841 → 307 pending)
Ingested: source path(s) → archived to .raw/<type>/
Created/Updated: wiki files
Committed: <commit subject(s)>
Flags for DM: none / list
```

Keep the final answer short. The durable record belongs in the wiki and the git history, not
in chat.
