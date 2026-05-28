# AGENTS.md — Shattered Sea Wiki Governance
# Under 200 lines. Agent reads this first, every session.

---

## Campaign

**Name:** Shattered Sea
**System:** D&D 5e 2024
**Status:** Active
**Philosophy:** {One sentence describing the campaign's core creative philosophy}
**Style:** Sandbox

---

## Party

| PC | Player | Notes |
|---|---|---|
| {PC Name} | {Player Name} | {Key trait, mortis, or special condition} |

**Home base:** {ship/stronghold/city} — `wiki/entities/{type}/{slug}/`
**Current arc:** {One sentence on current situation}

---

## Active Factions (Clock Status)

Update this block after every session or faction-clock run.

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
6. Raw transcripts — `.raw/sessions/` — only when the compiled note is insufficient.

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
- `wiki/log.md` has a record of every structural change

---

## Automatic Behaviors

**On every file write:**
1. Validate all required frontmatter fields — add missing fields with defaults, log additions
2. Set `updated` to today's date
3. Validate all `[[wikilinks]]` resolve — create stubs for any that don't
4. Add reciprocal links where applicable
5. Update `wiki/index.md` entry for this file
6. Append one-line entry to `wiki/log.md`

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

See `wiki/log.md` for all structural changes.
See `wiki/discrepancy-log.md` for all lore contradictions (created on first conflict).
