---
name: prep-island
description: >
  Create or expand a narrative island for the Shattered Sea campaign — a self-contained,
  portable cluster of situations, NPCs, and locations organized around a coherent premise.
  Invoke for: "create a narrative island", "prep [location] as a sandbox node", "create
  a portable scenario around [entity]", "design an island I can drop anywhere", "make a
  self-contained adventure site", "prep [thing] as an island". A narrative island is a
  PLOT DEVICE (a portable scenario cluster), not a geographic landmass — for an actual
  island place (a real landmass like Calder's Tooth) use prep-location instead. Narrative
  islands contain situations — if the content is a single condition with a clock, use
  prep-situation instead. Always loads sandbox-narrative for anti-railroading review.
---

> **Shared prep conventions** — stub check, interview + PC-connection requirement, combat calibration, prose pass, and filing — live in [`prep-family-standards`](../ttrpg-llm-wiki-init/references/prep-family-standards.md). Read it before generating; this file covers only what's specific to this content type.
Domain-specific: **Is this actually a narrative island?** Two things this is NOT, because the word "island" is overloaded:

- **A geographic island** (an actual landmass in the world — Calder's Tooth, Aldenmere) is a *place*. Use `prep-location`; it files under `wiki/entities/places/islands/` as `type: entity`. A narrative island is a *plot device*, not a place — it can sit on a ship, in a city quarter, anywhere.
- **A single condition with one clock** is a situation (`prep-situation`).

A narrative island is a *portable cluster* of interconnected situations, NPCs, and locations with a coherent premise — it lives in `wiki/narrative-islands/` with `type: narrative-island`. If in doubt, start with a situation; islands can grow from them.

---

## Island-Specific Frontmatter Fields

Universal fields auto-fill. You must author these island-specific fields:

```yaml
portable: true/false          # can it be lifted and dropped into other campaign contexts?
entry_points:                 # hooks that pull players in — minimum 2
  - "[Entry hook 1]"
  - "[Entry hook 2]"
contains_situations:          # wikilinks to situation files this island contains
  - "[[situation-slug|Display Name]]"
linked_islands:               # other islands this connects to
  - "[[island-slug|Display Name]]"
```

---

## Island Structure

**Situation files first.** Create all situation files (`prep-situation`) before writing
the island index. The island page wikilinks to situations — it doesn't contain them inline.

**Scene Spine** — 3–5 scenes that *could* happen, not scenes that *must* happen. Each
scene: pressure + NPC position + 2+ possible outcomes. No scripted sequence.

**Strong Start** — entry scene already in motion. Players arrive at a moment of pressure,
not a briefing. Options: faction conflict in progress, discovery in progress, NPC in
immediate need.

**Toy Fields** — what makes this island reusable: the portable element (what works
regardless of campaign context), the hook that doesn't depend on specific prior events.

**Run Guide** — how to present at the table: NPC interplay, natural scene progression
hints, exit points that lead somewhere interesting.

Load `ttrpg-writing` before writing any prose. **DM-facing reference** for run guide and
DM notes. **Player-facing prose** for strong start and scene spine read-aloud.
Load `sandbox-narrative` for anti-railroading review of all content.

---

## Filing

- Narrative-island file: `wiki/narrative-islands/{slug}.md`, `type: narrative-island`
- Add to `wiki/index.md`
- Add reciprocal links to all contained situations, NPCs, and locations

---

## Reference Files

| File | Read when |
|---|---|
| `references/ISLAND-TEMPLATE.md` | Full island template, quality criteria, failure modes |
| `../ttrpg-writing/references/dm-reference-standards.md` | Writing run guide, DM notes, toy fields |
| `../ttrpg-writing/references/player-facing-prose.md` | Writing strong start and scene read-aloud |
| `../ttrpg-writing/references/callout-standard.md` | Callout type enforcement and conversion |
| `../ttrpg-llm-wiki-init/references/auto-correct.md` | Fixing structural issues during or after content creation |
| `../ttrpg-llm-wiki-init/references/wikilink-standards.md` | Creating or fixing wikilinks |
