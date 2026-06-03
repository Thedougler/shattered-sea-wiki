# System File Templates — TTRPG LLM-Wiki

Read when creating required system files from scratch during Init or Fast Check.
Fill in `{placeholders}` from CLAUDE.md or ask the DM if unknown.
Leave placeholders as-is if information is not yet available — they signal what's missing.

---

## CLAUDE.md Template

```markdown
# CLAUDE.md — {Campaign Name} Wiki Governance
# Under 200 lines. Agent reads this first, every session.

---

## Campaign

**Name:** {Campaign Name}
**System:** {Game System, e.g. D&D 5e 2024}
**Status:** Active
**Philosophy:** {One sentence describing the campaign's core creative philosophy}
**Style:** {e.g. Sandbox, railroad, BLM-inspired, etc.}

---

## Party

| PC | Player | Notes |
|---|---|---|
| {PC Name} | {Player Name} | {Key trait, mortis, or special condition} |

**Home base:** {ship/stronghold/city} — `wiki/entities/{type}/{slug}/`
**Current arc:** {One sentence on current situation}

---

## Active Factions (Clock Status)

Update this block after every session or world-update run.

| Faction | Clock | Next Trigger |
|---|---|---|
| {Faction} | {X/Y — brief description} | {Condition} |

---

## Reading Order (Context Budget Protocol)

Read in this order. Stop when you have enough context for the task.

1. `wiki/hot.md` — always, always first. Current state, live threads, predictions.
2. `wiki/system/task-routing.md` — routing. Find which skill and files apply to this task.
3. Entity files for relevant NPCs, locations, factions — read `summary` frontmatter first.
   If summary answers the question, do not read the full file.
4. Situation files for active threads — `wiki/situations/active/`
5. Session notes — `wiki/sessions/` — only when continuity or sequence matters.
6. Raw transcripts — `audio/sessions/` — only when the compiled note is insufficient.

**Never read the full vault before generating content.**

---

## Ideal State

The wiki is in ideal state when every file satisfies all of the following:

- Complete YAML frontmatter (all required fields present, `updated` is current)
- Informative `summary` field answering "what is this?" in ≤2 sentences
- Wikilinks resolve (no broken links; stubs exist for all referenced entities)
- Bidirectional relationships (if A links B, B links A)
- Correct path per content type
- No duplicate information (cross-link instead of copy)
- No orphaned files (every file has at least one inbound link)
- `hot.md` reflects actual current world state
- Git history records all structural changes (use `git log` to review)

---

## Automatic Behaviors

**On every file write:**
1. Validate all required frontmatter fields — add missing fields with defaults, log additions
2. Set `updated` to today's date
3. Validate all `[[wikilinks]]` resolve — create stubs for any that don't
4. Add reciprocal links where applicable
5. Update `wiki/index.md` entry for this file
6. Commit with a brief message

**On structural violation (correct immediately, no confirmation needed):**

| Error | Auto-Correction |
|---|---|
| File in wrong path | Move to correct path; update all inbound links; log move |
| Missing frontmatter field | Add field with sensible default; log addition |
| Broken wikilink | Create stub at correct path; log stub creation |
| Naming convention violation | Rename to kebab-case; update all inbound links; log |
| Missing bidirectional link | Add reciprocal link to target file; log |
| Orphaned file | Add to index; find natural parent and link; log |

**Escalate to DM only for:**
- Genuine lore contradictions between two established facts
- Ambiguous entity identity (two pages may describe the same entity)
- Lifecycle decisions (moving situation active → resolved)

---

## Frontmatter Requirements by Type

**All files (universal):**
`type`, `subtype`, `campaign`, `status`, `audience`, `publish`, `summary`,
`created`, `updated`, `tags`, `sources`

**Entities (characters, places, factions, items, vehicles):**
+ `confidence_level`, `relationships`

**Situations:**
+ `lifecycle` (dormant/active/resolved), `island` (wikilink or null), optionally `clocks`

**Islands:**
+ `portable` (true/false), `entry_points`, `contains_situations`

**Sessions:**
+ `session_number`, `session_date`

**System files (audience: agent):**
+ `system_role`, `token_profile`, `mandatory_for`, `update_trigger`

---

## Change Log

See `git log` for all structural changes.
See `wiki/discrepancy-log.md` for all lore contradictions (created on first conflict).
```

---

## wiki/hot.md Template

```markdown
---
type: system
subtype: hot-file
campaign: {campaign}
audience: agent
publish: false
summary: "Current world state, open threads, faction clocks, and predictions. Read first, always."
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

# hot.md — Updated {DATE}

## Current Arc
{One paragraph: where the party is, what they're in the middle of, what's pressing.
Be concrete. No vague mood-setting. Facts only.}

## Open PC Threads
- {PC Name}: {one-line summary of their active personal thread}
- {PC Name}: {one-line summary}

## Faction Clocks
| Faction | Clock | If Ignored This Session | Next Trigger |
|---|---|---|---|
| {Faction} | {X/Y — brief} | {consequence} | {condition} |

## Live Situations
| Situation | Status | Party Awareness | Next Beat |
|---|---|---|---|
| {situation} | {active/ticking} | {knows/suspects/unaware} | {what happens next} |

## Predictions
{3–5 things likely to happen in the next 1–2 sessions based on current clock states.
Probabilistic, not certain. Update as events unfold.}

1. {prediction}
2. {prediction}
3. {prediction}

## Spotlight Tracking
| PC | Last Meaningful Moment | Sessions Since |
|---|---|---|
| {PC} | {description} | {N} |
```

---

## wiki/index.md Template

```markdown
---
type: system
subtype: index
campaign: {campaign}
audience: agent
publish: false
summary: "Master catalog of all wiki files. Grouped by path. Updated on every write operation."
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

# Wiki Index — {Campaign Name}

## entities/characters/pcs
{- [[slug|Display Name]] — one-line summary}

## entities/characters/npcs
{- [[slug|Display Name]] — one-line summary}

## entities/characters/crew
{(empty)}

## entities/characters/minor
{(empty)}

## entities/places
{(empty)}

## entities/factions
{(empty)}

## entities/items
{(empty)}

## entities/vehicles
{(empty)}

## situations/active
{(empty)}

## situations/dormant
{(empty)}

## situations/resolved
{(empty)}

## islands
{(empty)}

## lore
{(empty)}

## rules
{(empty)}

## sessions
{(empty)}

## system
- [[task-routing|Task Routing]] — maps task types to required pre-reads and skills
- [[party-combat-primer|Party Combat Primer]] — party combat capabilities and design rules
- [[party-session-primer|Party Session Primer]] — party context for session prep

## dm
- [[player-interests|Player Interests]] — what each player is engaged with
- [[combat-analytics|Combat Analytics]] — empirical combat patterns
```

---

## wiki/system/task-routing.md Template

```markdown
---
type: system
subtype: task-routing
campaign: {campaign}
audience: agent
publish: false
system_role: task-routing
token_profile: map
mandatory_for: []
update_trigger: "New system file added; task type added; mandatory read list changes"
summary: "Read second after hot.md. Maps every task type to its required pre-reads and skill. Never generate content without completing the listed reads."
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

# Task Routing — {Campaign Name}

> Read this immediately after `wiki/hot.md`. Find your task type below.
> Read every listed file at the specified depth before generating any content.
> Required reads are not optional.

---

## Read Depth Notation
- `[FULL]` — read the complete file
- `[FAST-READ]` — read the summary/Fast Read section only; expand if insufficient
- `[SECTION: X]` — read only the named section
- `[SUMMARY-ONLY]` — read the frontmatter summary field only
- `[ON-DEMAND]` — read only if this specific entity is directly involved

---

## Routing Table

### Task: `encounter-design`
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `wiki/system/party-combat-primer.md` | `[FULL]` | Party capabilities and design rules |
| 2 | `wiki/dm/combat-analytics.md` | `[SECTION: Design Adjustments]` | Active design flags |
| 3 | `wiki/system/players/[pc]-sheet.md` (all PCs) | `[FAST-READ]` | Current resource state |

### Task: `session-prep`
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `wiki/system/party-session-primer.md` | `[FULL]` | Party context for this session |
| 2 | `wiki/dm/player-interests.md` | `[SECTION: Content Priority Queue]` | What to emphasize |
| 3 | `wiki/situations/active/[relevant]` | `[FAST-READ]` | Active threads |

### Task: `transcript-ingestion`
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `wiki/system/players/[all-pcs]-sheet.md` | `[FULL]` | Current mechanical state |
| 2 | `wiki/hot.md` | `[FULL]` | World state at session start |

### Task: `wiki-audit`
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `wiki/index.md` | `[FULL]` | Master catalog |
| 2 | `CLAUDE.md` | `[SECTION: Ideal State]` | Correction rules |

---

## System File Index

| File | system_role | mandatory_for | token_profile |
|---|---|---|---|
| `wiki/system/task-routing.md` | task-routing | all tasks | map |
| `wiki/system/party-combat-primer.md` | party-primer | encounter-design | always-read |
| `wiki/system/party-session-primer.md` | party-primer | session-prep | always-read |
| `wiki/dm/player-interests.md` | dm-intelligence | content-creation, session-prep | quick-ref |
| `wiki/dm/combat-analytics.md` | dm-intelligence | encounter-design | quick-ref |
```
