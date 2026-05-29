---
name: prep-faction
description: >
  Create or expand a faction wiki page for the Shattered Sea campaign. Invoke for:
  "create a page for [faction]", "detail [faction]", "who runs [organization]", "expand
  [faction]'s entry", "I need a faction that...", "what does [group] want", "add a
  faction clock", "flesh out [organization]". Generates frontmatter, membership
  structure, agenda, clocks, public vs private face, and relationships to other factions.
  Determines whether the faction warrants a clock in hot.md. Always checks index.md
  for existing stubs before creating a new page.
---

> Cross-cutting rules (reading order, sandbox constraints, PC-connection requirement, frontmatter, auto-correct) live in `wiki/system/doctrine.md`. This skill covers only what's specific to its domain.

## Prerequisites

Prerequisites: see reading order in `wiki/system/doctrine.md`. Always check `wiki/index.md` for an existing stub before creating a new page.

---

## Faction Page Structure

**Frontmatter:** universal/entity fields auto-fill. Author the domain values: `status` (`active | dormant | dissolved`) and a `summary` of 2 sentences (what they want + how they operate).

**Required body sections:**

- **Agenda** — what they are pursuing right now, not just their long-term goal. A
  vector, not a state.
- **Membership** — who belongs, how they're organized, hierarchy shape
- **Methods** — how they operate (coercion, trade, information, violence, politics)
- **Public Face** — what common knowledge says about them (the cover story)
- **Clock** — if active: name, segments (4 or 6), trigger condition, consequence at fill

**Clock decision rule:** If the faction has an agenda that advances independently of the
party, it gets a clock in `hot.md`. Add it there after writing the page.

---

## Filing

- Page path: `wiki/entities/factions/{slug}.md`
- Add to `wiki/index.md` under `## entities/factions`
- If faction gets a clock: add entry to `wiki/hot.md` faction clocks block
- Add reciprocal links to all referenced entities

Load `ttrpg-writing` for prose and formatting standards.

---

## Reference Files

| File | Read when |
|---|---|
| `references/FACTION.md` | Full faction page template, clock format, quality bar |
| `references/faction-simulation.md` | Faction off-screen behavior and simulation heuristics |
