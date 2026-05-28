---
name: prep-ship
description: >
  Create or expand a ship or vehicle wiki page for the Shattered Sea campaign. Invoke
  for: "create the [ship name] wiki entry", "detail [ship]", "flesh out [vessel]",
  "I need a ship page for [name]", "what's the [ship]'s layout", "crew manifest for
  [ship]", "naval encounter with [vessel]", "design a ship", "the [ship name]". Uses
  a tiered detail model based on how central the vessel is to the campaign. Also handles
  travel encounters and sea events when designing maritime content.
---

## Tier Model

Determine tier before generating any content. Confirm Tier 2+ with DM before building.

| Tier | When to use | Output |
|---|---|---|
| 0 | One-off vessel, minor encounter | No file — embed stats in the encounter or situation file |
| 1 | Named ship, recurring presence | Single `wiki/entities/vehicles/{slug}.md` |
| 2 | Party-adjacent or faction flagship | Tier 1 file + DM companion file |
| 3 | Party's home ship or major campaign vessel | Subfolder with full suite (see below) |

---

## Ship Page Structure

**Frontmatter:** `type: vehicle`, `subtype: ship` (or specific vessel type), `status`,
`summary` (one sentence: class + who owns/controls it), `relationships` (owner, crew,
faction affiliation), `confidence_level`

**Required sections:**
- **Profile** — class, size, speed, armament, cargo capacity (one line each)
- **Crew** — named crew with roles; total headcount for unnamed
- **History** — only what affects current sandbox state; nothing for flavor alone
- **Current Status** — location, controller, condition

**Tier 3 subfolder structure:**
```
wiki/entities/vehicles/{slug}/
  index.md           — master page with wikilinks to all sub-files
  layout.md          — deck-by-deck room keys
  manifest.md        — full crew roster
  owners-manual.md   — player-facing ship reference (if party ship)
  dm-guide.md        — DM-facing secrets, hooks, encounter notes
```

Load `ttrpg-writing` for all prose and formatting standards.

---

## Filing

- Tier 1–2: `wiki/entities/vehicles/{slug}.md`
- Tier 3: `wiki/entities/vehicles/{slug}/index.md` (plus sub-files)
- Add to `wiki/index.md` under `## entities/vehicles`
- Add reciprocal links to home port, owning faction, named crew

---

## Reference Files

| File | Read when |
|---|---|
| `references/SHIP-GENERATE.md` | Ship generation, fleet design, naming conventions, stat generation |
| `references/SHIP-RULES.md` | Naval rules, maritime mechanics, sea encounter structure |
| `references/TRAVEL.md` | Travel encounters and sea events |
