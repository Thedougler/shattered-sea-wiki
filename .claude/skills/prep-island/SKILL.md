---
name: prep-island
description: >
  Create or expand a narrative island for the Shattered Sea campaign — a self-contained,
  portable cluster of situations, NPCs, and locations organized around a coherent premise.
  Invoke for: "create a narrative island", "prep [location] as a sandbox node", "create
  a portable scenario around [entity]", "design an island I can drop anywhere", "make a
  self-contained adventure site", "prep [thing] as an island". Islands contain situations
  — if the content is a single condition with a clock, use prep-situation instead.
  Always loads sandbox-narrative for anti-railroading review.
---

> Cross-cutting rules (reading order, sandbox constraints, PC-connection requirement, frontmatter, auto-correct) live in `wiki/system/doctrine.md`. This skill covers only what's specific to its domain.

## Prerequisites

Prerequisites: see reading order in `wiki/system/doctrine.md`. Always check `wiki/index.md` for an existing stub before creating a new page.

Domain-specific: **Is this actually an island?** A single condition with one clock is a situation (`prep-situation`). An island is a *cluster* of interconnected situations, NPCs, and locations with a coherent premise. If in doubt, start with a situation — islands can grow from them.

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

Load `ttrpg-writing` for all prose and formatting standards.
Load `sandbox-narrative` for anti-railroading review of all content.

---

## Filing

- Island file: `wiki/islands/{slug}.md` (or `wiki/entities/places/islands/{slug}.md`)
- Add to `wiki/index.md`
- Add reciprocal links to all contained situations, NPCs, and locations

---

## Reference Files

| File | Read when |
|---|---|
| `references/ISLAND-TEMPLATE.md` | Full island template, quality criteria, failure modes |
