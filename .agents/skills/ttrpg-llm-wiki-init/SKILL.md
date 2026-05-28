---
name: ttrpg-llm-wiki-init
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

## Step 0 — Read CLAUDE.md First (All Modes Except Init)

Read `CLAUDE.md` completely before any check. It overrides defaults in this skill. Extract:

- Campaign name and system
- Party composition (PCs and players)
- Folder structure expectations
- Frontmatter requirements beyond universal defaults
- Automatic behavior rules
- Ideal State definition

If `CLAUDE.md` is missing → switch to **Init Mode**.
If `CLAUDE.md` is malformed or missing required sections → flag and continue with universal
defaults. Do not halt.

---

## Fast Check Protocol

Run all 14 checks in order. Fix each violation immediately before continuing to the next.
Commit each fix with a brief message. Target: complete before any content task begins.

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
[ ] 9.  Inbox/ contents — list any files present; flag each for processing via wiki-categorize
[ ] 10. Spot-check 5 random wiki files for frontmatter validity (type, summary, updated fields)
[ ] 11. wiki/ingest-registry.md — if exists, count pending items; surface count to DM
[ ] 12. git log --oneline -5 — surface last 5 commits as the operation history (one line)
[ ] 13. wiki/hot.md — READ FULLY and actively garden (see Check 13 Protocol)
[ ] 14. wiki/index.md — SCAN directory and actively garden (see Check 14 Protocol)
```

### Check 13 — hot.md Active Curation (Required, Not Optional)

`hot.md` is a **living document**, not a file to check for staleness and move on.
Read it fully. Cross-reference against `git log --oneline --since="{hot.md updated date}"` to see what sessions have been ingested.

For each section, ask: *Does this reflect actual current world state?*

- Faction clocks advanced since last update? → rewrite Faction Clocks section
- Situations resolved or advanced? → rewrite Live Situations section
- PC threads shifted? → rewrite Open PC Threads section
- Spotlight changed? → rewrite Spotlight Tracking section

Update the `updated` date. Write the file. Commit: `curation: hot.md updated — {what changed}`

hot.md **must** be accurate before any downstream task runs.

### Check 14 — index.md Active Curation (Required, Not Optional)

Scan the `wiki/` directory tree. Compare against `wiki/index.md` entries.

- Files present in wiki/ but absent from index → add entries with current frontmatter summary
- Index entries pointing to non-existent files → remove entry (or create stub if referenced elsewhere)
- Entries where frontmatter summary has changed → update one-line entry

Write the file. Commit: `curation: index.md updated — {N entries added/removed/updated}`

The index is the agent's navigation map. A stale index causes routing failures downstream.

### Health Summary Output

After completing all 14 checks, output **exactly one line** before routing:
```
WIKI HEALTH: OK | {N} issues found and fixed | {N} flags for DM | Last session: {one-line from git log}
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
    ├── hot.md  index.md  ingest-registry.md  work-queue.md
    ├── system/ task-routing.md  players/
    ├── dm/ player-interests.md  combat-analytics.md
    ├── entities/ characters/pcs/ npcs/ crew/ minor/
    │            places/  factions/  deities/  items/  vehicles/
    ├── situations/ active/  dormant/  resolved/
    ├── islands/  lore/  rules/  sessions/
```

Log: `INIT: vault scaffolded for campaign {name} — {N} directories, {N} files created`
Then run Fast Check to confirm health before routing.

---

## Auto-Correction Rules

Apply during Fast Check and Full Audit. **Fix immediately, then commit.**
**Never ask for confirmation on structural corrections.**
**Escalate to DM only for:** lore contradictions, ambiguous entity identity.

| Violation | Auto-Correction |
|---|---|
| File in wrong path | Move to correct path; update all inbound wikilinks; commit |
| Missing frontmatter field | Add with default from `references/frontmatter-defaults.md`; commit |
| Broken wikilink | Create stub at correct path; add to index.md; commit |
| Naming convention violation | Rename to kebab-case; update all inbound wikilinks; commit |
| Missing bidirectional relationship | Add reciprocal link to target file; commit |
| Orphaned file | Add to index; find natural parent and link; commit |
| Situation/island in wrong lifecycle folder | Move to correct folder; update `lifecycle` and `status` frontmatter; update all inbound links; commit |
| Stub summary still default text | Flag: `FLAG: summary-stale — {file}` — do not guess content |

Commit message format for corrections:
```
fix: {correction-type} — {file} — {description}
```

---

## Frontmatter Standards (Universal)

Full defaults and type inference tables → `references/frontmatter-defaults.md`

**Universal fields (every file):**
`type` · `subtype` · `campaign` · `status` · `audience` · `publish` · `summary` ·
`created` · `updated` · `tags` · `sources`

**Additional fields by type:**
- Entity files: + `confidence_level` · `relationships`
- Situation files: + `lifecycle` · `island`
- Island files: + `portable` · `entry_points` · `contains_situations`
- Session files: + `session_number` · `session_date`
- System files: + `system_role` · `token_profile` · `mandatory_for` · `update_trigger`

**Summary quality bar:**
- BAD: `"An important NPC with a complex background."` — no facts
- GOOD: `"Rattkin matriarch of the Black-Jaw Run; reunited with Perrin in Calveno, has a favor to ask."` — concrete, current

Every summary answers: *What is this entity RIGHT NOW, and why does it matter?*

---

## Routing Table

After Fast Check: identify the user's task and route to the correct skill.
**Read the target skill before generating any content.**

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
| Advance faction clocks | `faction-clock` |
| Simulate world / NPC activity off-screen | `world-simulator` |
| Update player interests | `player-interest-tracker` |
| Update ingest registry | `ingest-registry-update` |
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
| Large sandbox generation (dungeon, region, hex map) | `sandbox-narrative` |
| Write lore or world content | `lore-generation` |

### Maintenance & System
| User Intent | Route To |
|---|---|
| Update character sheets or primers | `system-file-update` |
| File content in Inbox/ | `wiki-categorize` |
| Audit or fix wiki structure | Stay in this skill → Full Audit Mode |

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

- Always alias: `[[npc-slug|NPC Display Name]]` — never bare slugs in body text
- First mention of any named entity in a section → wikilink. Subsequent mentions in the same section → no link.
- When a wikilink target doesn't exist:
  1. Create stub immediately at the correct path
  2. Stub frontmatter: `status: stub`, `summary: "Stub — referenced in [[source]]. No page yet."`
  3. Stub body: `# {Title} — Stub`
  4. Add to `wiki/index.md` with `[stub]` marker
  5. Log: `AUTO-CORRECT: stub-created — {path}`

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
