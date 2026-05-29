---
name: wiki-pipeline
description: >
  Run the whole Shattered Sea startup-to-ingest pipeline in one autonomous pass: health-check
  the vault, find every pending source in Inbox/ and .raw/, ingest each one into the wiki,
  archive the source, regenerate the index, and commit per source — no prompts. Use this
  whenever the user says "run the pipeline", "process the inbox", "catch up the wiki", "ingest
  everything", "ingest everything pending", "sync the wiki", "clear the inbox", "process all the
  pending sources", or drops a pile of new files into Inbox/ and wants them all folded in. This
  is the batch orchestrator — for a single named source the user points at, ttrpg-wiki-ingest is
  enough; reach for this skill when the job is "everything that's waiting".
---

# Wiki Pipeline — Startup → Ingest, Autonomous

One invocation takes the vault from "files are waiting in Inbox/" to "everything is ingested,
archived, indexed, and committed." It chains the existing skills and the `.claude/scripts/`
helpers — it does not reimplement them. Cross-cutting rules live in `wiki/system/doctrine.md`.

The contract: **process the whole pending queue without asking for permission at each step.**
Commit per source. The only reasons to stop are a genuine lore contradiction or ambiguous
entity identity (see the auto-correct protocol in `doctrine.md`) — flag those, leave that one
source in `Inbox/`, and keep going on the rest.

---

## 1. Health check (fast)

Run `ttrpg-llm-wiki-init` in Fast Check mode. If Phase A is clean and no work-queue is active,
that's enough — don't deep-garden. Then regenerate the index baseline:

```bash
python3 .claude/scripts/regen_index.py --write
```

## 2. Find the queue

```bash
python3 .claude/scripts/sync_registry.py
python3 .claude/skills/ttrpg-wiki-ingest/scripts/scan_pending.py --include-root-docs
```

`sync_registry.py` lists `unregistered` sources (on disk, no registry row) — these are real
pending work even if the registry's own Pending Queue says "(none)". Build one ordered work
list from both: transcripts and sessions first, then entities/factions/locations/situations,
then lore/species, then handouts/assets, then research. Note the count to the user up front
("12 pending — processing now") so the scope is visible, then proceed.

## 3. Ingest each source (loop)

For every source in the work list, load `ttrpg-wiki-ingest` and run its standard workflow:
triage → decompose → write back. Then close it out per source:

```bash
python3 .claude/scripts/archive_source.py Inbox/<Source>.md   # → .raw/<type>/, fixes registry path
python3 .claude/scripts/regen_index.py --write
git add wiki .raw Inbox
git commit -m "ingest: <Source> — <short output summary>"
```

Update `wiki/hot.md` only when a source actually changes current world state (a session, a
faction move, a new active situation) — not for static lore. When you do, fold the hot.md edit
into that source's commit.

If a source is blocked (contradiction / ambiguous identity): record `blocked` with the exact
question in the registry, leave the file in `Inbox/`, and continue. Never let one blocked source
stall the queue.

## 4. Finalize

After the queue is drained:

```bash
python3 .claude/scripts/sync_registry.py     # expect: 0 unregistered, Inbox/ empty of ingested sources
git diff --check
```

If you edited a skill during the run, regenerate the mirror:
```bash
python3 .claude/scripts/sync_skills.py --apply
```

## Output to user

Keep it short — the durable record is in the wiki, registry, log, and commits.

```markdown
Pipeline complete: N sources ingested
- <Source> → <key outputs>  (committed)
- ...
Archived to .raw/: N files
Blocked (left in Inbox/): none / <source> — <question>
hot.md: updated / unchanged
```
