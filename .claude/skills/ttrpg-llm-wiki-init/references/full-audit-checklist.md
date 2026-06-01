# Full Audit Checklist — TTRPG LLM-Wiki

Read this file when running a Full Audit (`wiki-init` Full Audit mode).
Work through every section in order. Create wiki/work-queue.md before starting
if more than 10 files need correction.

---

## Before Starting

1. Read `CLAUDE.md` fully — extract the Ideal State definition and Automatic Behaviors
2. Read `wiki/work-queue.md` — if active task exists, resume it; do not start a new audit
3. Read `wiki/index.md` — this is the ground truth for what files should exist
4. Create a new work-queue entry if no active task: `AUDIT: Full structural scan — {date}`

---

## Phase 1 — Directory Structure

Check that every required directory in `universal-structure.md` exists.
For each missing directory: create it, log the creation.

```
[ ] VAULT_ROOT/Inbox/ exists
[ ] VAULT_ROOT/.raw/ exists
[ ] audio/sessions/ exists
[ ] .raw/characters/interviews/ exists
[ ] .raw/characters/sheets/ exists
[ ] .raw/homebrew/ exists
[ ] .raw/assets/ exists
[ ] wiki/ exists
[ ] wiki/system/ exists
[ ] wiki/system/players/ exists
[ ] wiki/dm/ exists
[ ] wiki/entities/characters/pcs/ exists
[ ] wiki/entities/characters/npcs/ exists
[ ] wiki/entities/characters/crew/ exists
[ ] wiki/entities/characters/minor/ exists
[ ] wiki/entities/places/ exists (check subfolders per campaign need)
[ ] wiki/entities/factions/ exists
[ ] wiki/entities/items/ exists
[ ] wiki/entities/vehicles/ exists
[ ] wiki/situations/active/ exists
[ ] wiki/situations/dormant/ exists
[ ] wiki/situations/resolved/ exists
[ ] wiki/islands/ exists (if campaign uses island model)
[ ] wiki/lore/ exists (check subfolders per campaign need)
[ ] wiki/rules/ exists (check subfolders per campaign need)
[ ] wiki/sessions/ exists
```

---

## Phase 2 — Required System Files

For each file: check it exists, check it has required sections, check frontmatter is complete.

```
[ ] CLAUDE.md — sections: Campaign, Party, Reading Order, Ideal State, Automatic Behaviors, Frontmatter Requirements
[ ] wiki/hot.md — sections: Current Arc, Open PC Threads, Faction Clocks, Live Situations, Predictions, Spotlight Tracking
[ ] wiki/index.md — entry for every wiki file; grouped by path; [stub] markers present
[ ] wiki/system/task-routing.md — routing table present; system file index present
[ ] wiki/dm/player-interests.md — exists (stub acceptable if campaign is new)
[ ] wiki/dm/combat-analytics.md — exists (stub acceptable if no sessions ingested)
```

For each PC listed in CLAUDE.md:
```
[ ] wiki/entities/characters/pcs/{pc-slug}.md exists
[ ] wiki/system/players/{pc-slug}-primer.md exists
[ ] wiki/system/players/{pc-slug}-sheet.md exists
```

---

## Phase 3 — Naming Convention Scan

Scan all files in `wiki/` and `.raw/`. For each file:
- Does the filename use kebab-case only? (lowercase, hyphens, no spaces, no CamelCase, no underscores)
- Does the filename end in `.md`?

**Violations:** rename to kebab-case; update all inbound wikilinks; commit.

Common violations to check:
- `Nona-Black-Jaw.md` → `nona-black-jaw.md`
- `NPC_profile.md` → `npc-profile.md`
- `Session 03 Notes.md` → `session-03-notes.md`
- `CalvanoDistricts.md` → `calvano-districts.md`

---

## Phase 4 — Frontmatter Completeness

For each file in `wiki/`: check all required frontmatter fields are present for its type.
Add missing fields with defaults from `frontmatter-defaults.md`. Log each addition.

Priority order (process these folders first — they have the most impact on routing):
1. `wiki/system/` files
2. `wiki/entities/characters/npcs/` files
3. `wiki/entities/characters/pcs/` files
4. `wiki/situations/active/` files
5. All remaining files

For each file, check in order:
```
[ ] type field present and matches path
[ ] subtype field present and matches folder
[ ] campaign field present and matches CLAUDE.md campaign name
[ ] status field present (not missing)
[ ] audience field present
[ ] publish field present
[ ] summary field present AND not the stub default
[ ] created field present (YYYY-MM-DD format)
[ ] updated field present (YYYY-MM-DD format)
[ ] tags field present ([] acceptable)
[ ] sources field present ([] acceptable only for generated content)
[ ] Type-specific additional fields (see frontmatter-defaults.md)
```

---

## Phase 5 — type/subtype Path Alignment

For each file: confirm `type` and `subtype` frontmatter values match the file's actual path.
Path is authoritative. If mismatch: fix frontmatter, not the path (unless path is wrong).

Check path is also correct per universal-structure content decision tree.
If file is in wrong path: move it (path fix), then fix frontmatter to match new path.

---

## Phase 6 — Wikilink Resolution

For every wikilink `[[slug]]` or `[[slug|Display Name]]` in every file:
1. Resolve the slug to a file path
2. If file exists: link is valid ✓
3. If file doesn't exist:
   - Check for typo (case mismatch, extra hyphen, spelling variant)
   - If typo: fix the link, log
   - If entity genuinely absent: create stub at correct path, add to index.md, log

Process order: start with `wiki/hot.md` and `wiki/index.md` (highest traffic), then
entity files by frequency of reference.

---

## Phase 7 — Bidirectional Relationship Check

For every relationship entry in every entity file's frontmatter:
1. Open the target file
2. Check for a reciprocal relationship entry pointing back
3. If missing: add the reciprocal entry to the target file, log

Relationship pairs to check (from `frontmatter-defaults.md` relationship labels table).

---

## Phase 8 — Orphan Detection

An orphaned file has zero inbound wikilinks from any other file.
Check `wiki/index.md` — any file not linked from at least one other wiki file is a candidate orphan.

For each orphan:
1. Search wiki for any natural parent (by content, faction, location, or campaign)
2. If natural parent found: add link from parent file; log
3. If no natural parent: add to `wiki/index.md` with a note; log FLAG

Exception: `wiki/hot.md`, `wiki/index.md`, `CLAUDE.md` are not orphans
by definition — they are root-level navigation files.

---

## Phase 9 — Summary Quality Check

For each file: flag summary for rewrite if:
- Summary is still `"Stub — no summary yet."`
- Summary is under 5 words
- Summary contains no concrete facts (all descriptions, no data)
- Session notes or situation files contradict the current summary

Flag in the file body with a lint comment: `FLAG: summary-stale — {reason}`
If the correct summary is obvious from the file's content: rewrite it. Commit the rewrite.
If ambiguous: flag only. Do not guess.

---

## Phase 10 — Index Completeness

Every file in `wiki/` must have an entry in `wiki/index.md`.
Every file in `wiki/index.md` must correspond to an existing file.

Check both directions:
- Files in wiki/ not in index.md → add to index.md
- Entries in index.md with no corresponding file → remove entry (or create stub if the
  entity is referenced elsewhere; decide based on whether other files link to it)

Index entry format:
```markdown
- [[slug|Display Name]] — one-line summary (from frontmatter summary field)
- [[slug|Display Name]] [stub] — one-line summary
```

---

## Phase 11 — hot.md Staleness Check

1. Read the `updated` date in hot.md
2. Run `git log --oneline --since="{hot.md updated date}" -- wiki/sessions/` — count SESSION-INGESTED commits
3. If 2 or more sessions have been ingested since hot.md was updated: prepend a staleness flag
   ```markdown
   > FLAG: hot.md may be stale — last updated {DATE}, {N} sessions since. Update before next task.
   ```
4. Check hot.md has all required sections: Current Arc, Open PC Threads, Faction Clocks,
   Live Situations, Predictions, Spotlight Tracking

---

## Phase 12 — Pending Ingest Check

1. Run `python3 .claude/scripts/check_ingest.py --count` — the number of `Inbox/` sources not
   yet present in `.raw/`. There is no registry to reconcile; the filesystem is the queue.
2. If the count is > 0, surface it to the DM and recommend running `ttrpg-wiki-ingest`.
3. Log: `AUDIT: {N} sources pending ingest`

---

## Closing the Audit

1. Update `wiki/work-queue.md` — mark audit task complete
2. Commit: `audit: {N} files checked, {N} corrections made, {N} flags raised`
3. Report to DM:
   - Total files audited
   - Corrections made (categorized by type)
   - Flags requiring DM attention (list each)
   - Health status: CLEAN | CORRECTED | FLAGS PENDING DM REVIEW
