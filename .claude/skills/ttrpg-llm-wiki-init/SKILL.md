---
name: ttrpg-llm-wiki-init
metadata:
  version: "2.0"
description: >
  Foundation skill for all TTRPG LLM-wiki operations. Run this skill first, every
  session, before any other skill or content task — even if the task seems simple.
  Validates vault structure, auto-corrects deviations without asking, resumes any
  interrupted work, and routes to the correct downstream skill. Trigger on: any new
  wiki session, wiki health questions, structural repair, vault initialization, task
  routing needs, or any of these phrases: "set up the wiki", "initialize", "audit
  the wiki", "check the wiki", "fix the structure", "what's the wiki status", "start
  fresh". The health check is fast. The routing is mandatory. Never skip this skill.
---

# TTRPG LLM-Wiki — Foundation Skill v2.0

**Runs first. Every session. No exceptions.**
Three responsibilities: validate the vault, resume interrupted work, route to the right skill.

---

## Mode Selection

Determine mode before doing anything else:

```
Is CLAUDE.md present?
  NO  → INIT MODE

  YES → Is there an active task in wiki/work-queue.md?
          YES → RESUME MODE (execute queue → then run remaining Fast Check items)

          NO  → User said "audit", "check all files", "full scan", "fix the structure"?
                  YES → FULL AUDIT MODE

                  NO  → User said "initialize", "start fresh", "new vault"?
                          YES → INIT MODE

                          NO  → FAST CHECK MODE (default)
```

---

## Step 0 — Context Already Loaded (All Modes Except Init)

`CLAUDE.md` is already in context every session — do not re-read it. It carries campaign name,
party, factions, and sandbox rules (always loaded). Operational references (auto-correct,
wikilinks, frontmatter defaults) are in this skill's `references/` folder — load on demand.

If `CLAUDE.md` is absent from context → switch to **Init Mode**.

---

## Fast Check Protocol

Phase A is structural and cheap — always run it. **Early exit:** if all Phase A checks pass and
there is no active task in `wiki/work-queue.md`, the vault is healthy — skip Phase B and go
straight to routing. Phase B is for when something in Phase A was off or the session just
ingested new material. Don't burn context gardening a vault that's already clean.

Fix each violation immediately and commit it (`fix: …`). Frontmatter completeness is handled by
the write hook, not by you — see `references/auto-correct.md`.

### Phase A — Structural (Checks 1–7, Always Auto-Fix)

```
[ ] 1.  CLAUDE.md exists and is readable
[ ] 2.  Inbox/ directory exists (create if missing)
[ ] 3.  wiki/ directory exists (create if missing → trigger Init)
[ ] 4.  wiki/hot.md exists (create from template if missing → references/system-file-templates.md)
[ ] 5.  wiki/index.md exists (create stub if missing)
[ ] 6.  wiki/system/ exists with task-routing.md (create stub if missing; flag for DM)
[ ] 7.  wiki/work-queue.md — if present and active task found → RESUME before continuing
```

### Phase B — Content Integrity (Checks 9–14)

```
[ ] 9.  Inbox/ — run check_ingest.py; surface the count of pending sources for ingest
[ ] 10. Spot-check 3 wiki files for a concrete (non-stub) summary — the hook handles fields
[ ] 11. git log --oneline -5 — surface last 5 commits as the operation history (one line)
[ ] 12. wiki/hot.md — curate ONLY if sessions were ingested since its updated date (see below)
[ ] 13. wiki/index.md — regenerate deterministically (see below)
```

Count pending sources (also safely removes exact duplicate Inbox files):
```bash
python3 .claude/scripts/check_ingest.py --count
```

### Check 13 — hot.md Curation (Conditional)

Don't re-read and re-garden `hot.md` every session. Check whether anything actually changed:
`git log --oneline --since="{hot.md updated date}"` — if no sessions or world-state ingests
landed since, `hot.md` is current; skip. Only when new material landed, route to the `hot-update`
skill (or, if absent, rewrite the affected sections inline) and commit
`curation: hot.md updated — {what changed}`. hot.md must be accurate before downstream tasks,
but accurate ≠ rewritten-from-scratch-every-time.

### Check 14 — index.md Regeneration (Deterministic)

The index is auto-generated from frontmatter — never hand-curated. Regenerate it:
```bash
python3 .claude/scripts/regen_index.py --write
```
If `git status` shows the index changed, commit `curation: index.md regenerated`. That's the
whole check — no manual scanning or diffing.

### Check 15 — Lint & DM Review Queue (Surface, Don't Grind)

Run the linter to surface vault health — it's the engine, don't hand-check files:
```bash
sea lint --summary    # one line: errors · warnings · quality
```
If there are **errors**, regenerate the persistent DM queue and point the DM at it — these are
decisions that must not be forgotten:
```bash
sea lint --report     # refreshes wiki/dm/review-queue.md
```
Surface the open-decision count in the health line below. Do **not** silently grind the whole
backlog at session start — route deliberate cleanup through `ttrpg-wiki-lint`.

### Health Summary Output

After completing all 15 checks, output **exactly one line** before routing:
```
WIKI HEALTH: OK | {N} issues found and fixed | {N} DM decisions open (wiki/dm/review-queue.md) | Last session: {one-line from git log}
```

---

## Full Audit Protocol

> **Read `references/full-audit-checklist.md` before starting.** Do not improvise the
> audit sequence — the reference file defines all 12 phases with their exact checks.
>
> Summary of phases (detail in reference):
> Phase 1: Directory structure · Phase 2: Required system files · Phase 3: Naming conventions ·
> Phase 4: Frontmatter completeness · Phase 5: type/subtype path alignment ·
> Phase 6: Wikilink resolution · Phase 7: Bidirectional relationships · Phase 8: Orphan detection ·
> Phase 9: Summary quality · Phase 10: Index completeness · Phase 11: hot.md staleness ·
> Phase 12: Ingest registry sync
>
> If more than 10 files need correction: create `wiki/work-queue.md` before starting.
> Never abandon a Full Audit mid-run.

After Full Audit, report to DM:
- Total files audited
- Corrections made (categorized by type)
- Flags requiring DM attention (list each)
- Status: `CLEAN | CORRECTED | FLAGS PENDING DM REVIEW`

---

## Init Protocol — New Vault

When `CLAUDE.md` is absent, scaffold the vault. Ask the DM for:
1. Campaign name
2. Game system (D&D 5e, PF2e, SWADE, etc.)
3. Party size and PC names (can be deferred)
4. DM name or handle

Create the full directory tree from `references/universal-structure.md`.
Create all required system files from templates in `references/system-file-templates.md`.

Abbreviated structure:
```
VAULT_ROOT/
├── CLAUDE.md
├── Inbox/
├── .raw/
│   └── sessions/ characters/interviews/ characters/sheets/ homebrew/ assets/
└── wiki/
    ├── hot.md  index.md  work-queue.md
    ├── system/ task-routing.md  players/
    ├── dm/ player-interests.md  combat-analytics.md
    ├── entities/ characters/pcs/ npcs/ crew/ minor/
    │            places/  factions/  deities/  items/  vehicles/
    ├── situations/ active/  dormant/  resolved/
    ├── narrative-islands/   (portable plot-device clusters — NOT geographic islands,
    │                         which are places under entities/places/islands/)
    ├── lore/  rules/  sessions/
```

Log: `INIT: vault scaffolded for campaign {name} — {N} directories, {N} files created`
Then run Fast Check to confirm health before routing.

---

## Auto-Correct Protocol

Structural problems are fixed immediately — never ask for confirmation. Full protocol
(violation table, escalation rules, commit format): `references/auto-correct.md`.

---

## Frontmatter Standards

Frontmatter requirements by type, default values, and the summary quality bar live in
`Full default/inference tables in
`references/frontmatter-defaults.md`). The write hook completes missing fields automatically;
your only frontmatter job is writing a concrete, current `summary` — the hook flags any that are
still stub defaults.

---

## Routing Table

After Fast Check: identify the user's task and route to the correct skill.
**Read the target skill before generating any content.**

When a routed skill's required reads include a primer or intelligence file (e.g.
`party-combat-primer.md`, `player-interests.md`), check its `status:` first — if it's still
`stub`, skip it. Reading an empty template wastes context; note "primer is a stub" and proceed.

### Session Pipeline
| User Intent | Route To |
|---|---|
| Clean/process a raw transcript | `transcript-clean` |
| Ingest a reviewed transcript into the wiki | `transcript-ingest` |
| Resolve a session flags file | `session-flags-review` |
| Write session recap (player-facing) | `session-recap-write` |
| Write session summary (agent-facing) | `session-summary-write` |

### World Intelligence
| User Intent | Route To |
|---|---|
| Advance faction clocks | `world-update` |
| Simulate world / NPC activity off-screen | `world-simulator` |
| Update player interests | `player-interest-tracker` |
| Targeted update to hot.md from a specific event | `hot-update` |

### Prep & Content Creation
| User Intent | Route To |
|---|---|
| Design a combat encounter | `prep-encounter` |
| Session prep / run a session | `prep-session` |
| Write a strong start | `prep-strong-start` |
| Create or expand an NPC | `prep-npc` |
| Create or expand a location | `prep-location` |
| Create or expand a faction | `prep-faction` |
| Create or expand a situation | `prep-situation` |
| Create or expand an island | `prep-island` |
| Create or expand a ship or vehicle | `prep-ship` |
| Create or expand a creature or monster | `prep-creature` |
| Homebrew a magic item or custom item | `prep-hb-item` |
| Large sandbox generation (dungeon, region, hex map) | `sandbox-narrative` |
| Write lore or world content | `lore-generation` |

### Maintenance & System
| User Intent | Route To |
|---|---|
| Update character sheets or primers | `system-file-update` |
| File content in Inbox/ | `wiki-categorize` |
| Audit wiki content (frontmatter, links, lore) | Stay in this skill → Full Audit Mode |
| Reorganize wiki files/folders, fix misplaced files | `ttrpg-wiki-organize` |

If the task is not in this table:
1. Check `wiki/system/task-routing.md` — the campaign may define custom task types.
2. Still unclear → apply best judgment and log: `FLAG: unrouted-task — {description}`

---

## Missing Skill Protocol

When routing identifies a required skill that is not installed:
**Do not improvise. Do not proceed without the skill.** Save state, build the skill, return.

### Step 1 — Save Current Objective

Write or update `wiki/work-queue.md`:
```markdown
## Suspended Objective: {description of original task}
**Suspended:** YYYY-MM-DD
**Reason:** Required skill `{skill-name}` not installed
**Resume:** After skill is installed, return here and continue
**Context:** {relevant state — files in progress, decisions made, etc.}
```

### Step 2 — Invoke skill-creator

Read `references/skill-registry.md`. Locate the entry for the missing skill.
That entry is the build brief — hand it to `skill-creator` as opening context.

Follow the full `skill-creator` workflow:
- Use the registry entry as the intent-capture starting point
- Research: read relevant project files, installed skills, and wiki system files the new skill will interact with
- Draft `SKILL.md` with correct frontmatter, description, and body
- Self-evaluate against the registry entry's critical behaviors
- Iterate until the skill meets production quality — proper frontmatter, reliable trigger description, instructions complete enough for a fresh agent instance without this conversation's context
- Package the skill

If the missing skill is not in `references/skill-registry.md`: derive intent from the
routing table entry that triggered the gap, then proceed with the same workflow.

### Step 3 — Return to Suspended Objective

1. Read `wiki/work-queue.md` — find the Suspended Objective entry
2. Close suspension entry: move to `## Completed Tasks`, note "skill built — resuming"
3. Log: `SKILL-BUILT: {skill-name} — created to unblock {original-task}`
4. Read the newly installed skill
5. Continue the original task from where it was suspended

### If skill-creator itself is missing

```
BLOCKED: skill-creator not installed. Cannot build missing skill `{skill-name}`.
Install skill-creator manually to unblock this operation.
```
Then proceed with the original task using best judgment, clearly noting the gap.

---

## Wikilink Standards

Aliasing, stub creation, and bidirectional link rules: `references/wikilink-standards.md`.

---

## Work Queue Protocol

Any task touching more than 10 files **must** use a work queue.

**Before starting any new task:** check `wiki/work-queue.md` for an active entry.
If an active entry is found, **resume it immediately** — do not start new work until it is closed.

Queue entry format:
```markdown
## Active Task: {description}
**Started:** YYYY-MM-DD
**Last completed:** {last file processed}
**Resume from:** {next file to process}

## Queue
- [ ] {file} → {action}
- [x] {file} → {action} (done)
```

After every file: update `[x]` status and the `Resume from` field.
Close the entry (move to `## Completed Tasks`) only when all items are `[x]`.

**Quality is never traded for speed. Never mark a task complete if files remain.**

---

## Reference Files

Read these when the SKILL.md body is insufficient for the task at hand.

| File | Read When |
|---|---|
| `references/universal-structure.md` | Initializing vault; verifying folder tree; content categorization questions |
| `references/frontmatter-defaults.md` | Adding missing frontmatter fields; inferring type or subtype from path |
| `references/full-audit-checklist.md` | Starting a Full Audit — read this first, before any audit action |
| `references/system-file-templates.md` | Creating hot.md, CLAUDE.md, index.md, or task-routing.md from scratch |
| `references/skill-registry.md` | Missing Skill Protocol triggered; need the build brief for skill-creator |
| `references/PREP.md` | Universal entity prep doctrine — philosophy, volatile situations, reactive systems |
| `references/CAMPAIGN.md` | Campaign scaffolding: folder shape, hub pages, season/chapter organization |
| `references/CAMPAIGN-TYPES.md` | Campaign structure types — linear, sandbox, episodic, reference when scaffolding |
| `references/REFERENCE.md` | Condition, class, and rule reference page format (DM-facing technical docs) |
| `references/auto-correct.md` | Fixing structural issues — violations, corrections, escalation, commit format |
| `references/wikilink-standards.md` | Writing or fixing wikilinks — aliasing, stub creation, bidirectional rule |
