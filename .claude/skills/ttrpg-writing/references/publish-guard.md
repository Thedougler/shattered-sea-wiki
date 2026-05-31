# Publish Guard

The wiki serves two audiences with completely different needs. Published pages go to players —
they must be immersive, in-world, and free of spoilers. Unpublished pages are DM tools — they
must be concise, direct, and fast to scan at the table. Letting these layers bleed into each
other is the most common failure mode in this vault: it either exposes secrets to players or
buries the DM in prose they have to parse mid-session.

The quick rules are in SKILL.md. This file covers pairing decisions, naming conventions,
violation diagnosis, DRY enforcement, routing, and audit mode.

---

## When to Create Paired Pages vs. a Single Page

| Situation | Pattern |
|-----------|---------|
| Entity introduced to players (met, visited, heard about in play) | **Paired**: public page + DM companion |
| Entity not yet revealed (secret NPC, unrevealed faction, unvisited location) | **Single DM-only page** (`publish: false`). Convert to paired when introduced. |
| Entity has nothing private (mundane location, fully-revealed NPC, common item) | **Single public page** (`publish: true`) |
| All secrets revealed in-session | **Merge** DM companion into public page; archive the DM file |

When in doubt, create the DM companion — it is easier to delete a file than to untangle merged
content later.

---

## Linking Companion Pages

Every paired entity uses a consistent link pattern so agents can always navigate between layers.

**On the DM companion page** — first line of body, before any other content:
```
**Public profile:** [[Entity-Name]]
```

**On the public page** — in frontmatter only, never in the body (players see body content):
```yaml
dm_companion: "[[path/to/Entity-Name-DM]]"
```

The public page body never references or hints at the DM companion. The DM page freely links
to the public page and any related private files.

**Naming convention for DM companion files:**
DM companions live alongside their entity in the same directory, with a `-dm` suffix:
- NPC: `npc-name-dm.md` in `wiki/entities/characters/npcs/`
- Location: `location-name-dm.md` in `wiki/entities/places/`
- Faction: `faction-name-dm.md` in `wiki/entities/factions/`
- Ship: `ship-name-dm.md` in `wiki/entities/vehicles/`

Always run `find wiki/ -iname "*name*dm*"` before creating a companion — it may already exist.

---

## Deciding What's Public vs. Private

The line is **player knowledge, not GM knowledge**. Ask: could any party member know this,
observe this, or reasonably infer this?

**Public if:**
- Any party member has been told it or witnessed it in play
- It's immediately observable (appearance, mannerisms, public title, location)
- It's common knowledge in the world (open rumors, established facts)

**Private if:**
- It hasn't been revealed in session yet
- It requires knowledge the party doesn't have (hidden motivations, true loyalties, secret identities)
- It's mechanical data hidden from players (HP, AC, CR, abilities, save DCs for non-party creatures)
- It's author-voice commentary ("this NPC will betray the party," "the players don't know yet")
- It's GM prep: encounter design, run notes, session scaffolding

When the call is genuinely ambiguous, lean public. The DM file is where secrets live.

---

## Diagnosing a Violation

When reading any wiki file, check in both directions before doing anything else. Fix violations
immediately and note them inline as `[publish-guard: fixed violation in Filename.md]`.

### Violation A: DM content in a published file (`publish: true`)

Signals: undisclosed motivations, mechanical stats, author-voice commentary, information the
party hasn't learned, future plot elements.

Determine scope:
- **Entirely DM-only** (planned NPC not yet introduced, secret faction, prepared encounter):
  set `publish: false` and `audience: dm`. No extraction needed.
- **Mixed content**: extract the private sections, route them to the right private destination
  (see Routing below), and rewrite what remains in in-world voice.

### Violation B: Prose bloat in a DM-only file (`publish: false`)

Signals: multi-sentence atmospheric descriptions with no actionable content, flowery in-world
language, narrative mood-setting that doesn't help the DM at the table.

DM files are scanned under pressure, mid-session. Rewrite to one clear idea per sentence.
Cut anything that doesn't give the DM something to say, do, or decide.

### Violation C: Frontmatter inconsistency

Signals: `publish: true` with `audience: dm`, `publish: false` with `audience: players`, or
either field missing entirely.

- Files in `wiki/situations/`, `wiki/dm/`, or `wiki/system/` → default
  `publish: false` / `audience: dm` unless clearly public content
- Files in `wiki/entities/` → default `publish: true` / `audience: players` unless
  DM-only material (companion files with `-dm` suffix default to `publish: false`)
- If `publish` is absent: flag as broken frontmatter and add the missing field

---

## DRY Between Public and Private

When a public file and a DM companion both exist for the same entity, each owns its layer and
neither duplicates the other.

- The public file owns observable facts. The DM file adds only what the public file cannot say.
- If the DM file restates the NPC's appearance or public role verbatim, delete the restatement
  and link to the public page: `See [[Entity-Name]] for public profile.`
- Duplication causes drift — when a fact changes, one file gets updated and the other goes stale.

---

## Routing Extracted DM Content

When pulling DM content out of a published file, route to the right destination:

| Content type | Destination |
|---|---|
| Active plot thread, DM-facing scenario | `wiki/situations/active/` |
| Resolved or background lore | `wiki/situations/resolved/` or inline in entity page |
| NPC secrets, DM primer | Companion file alongside entity (e.g., `wiki/entities/characters/npcs/npc-name-dm.md`) |
| Session prep, encounter design, run notes | `wiki/sessions/` |
| System references, agent guides | `wiki/system/` or `wiki/dm/` |

Check whether a companion private file already exists before creating a new one.

---

## Writing Standards

**Published files — in-world voice:**

Write as a knowledgeable inhabitant of the world would describe the subject. Present tense for
current facts. The reader is a player; they should feel immersed, not briefed.

> Violation: "Nona appears friendly but is actually running a smuggling ring. Her CR is 9."
> Corrected: "Nona greets visitors with easy warmth — the Warren's matriarch, and the person
> everyone in Calveno quietly defers to."

**DM-only files — agent-optimized:**

Lead with the most actionable fact. One idea per sentence. No atmosphere for its own sake.
No invented mystery or withholding beats — if the DM needs to know something, say it plainly.

> Violation: "There is something deeply unsettling about the way Nona watches the party."
> Corrected: "Nona knows about the Passage's interest in Aldric. She will not volunteer this.
> If asked directly, she deflects with a question."

---

## Integration with Entity Creation

When creating or significantly editing any wiki entity:

1. **Decide the split first.** Set `publish` and `audience` in frontmatter before writing
   body content. The decision shapes what you write.
2. **Create the DM companion immediately** if the entity is introduced to players and has
   private content. Don't defer this.
3. **Wire the links** before committing.
4. **On any public entity edit:** verify the public page body contains no DM-only material
   that may have been added since last review.

---

## Audit Mode (`/publish-audit [path]`)

Scan every file at the specified path. For each file:

1. Read frontmatter `publish` and `audience`
2. Check body content for violations
3. Report: file path, violation type, recommended fix

Before editing more than 3 files in a single sweep, confirm with the user — misclassifying
content at scale can corrupt the public layer. Single-file fixes always proceed immediately.

Without a path, default to `wiki/` and note that a full scan may take time.
