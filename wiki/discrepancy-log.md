---
type: system
subtype: discrepancy-log
campaign: shattered-sea
status: active
audience: agent
publish: false
summary: "Log of lore contradictions and ambiguous entity identity that need a DM decision. Append on conflict; never auto-resolve identity. Both traces stay visible until resolved."
created: 2026-05-28
updated: 2026-05-28
tags: [system, discrepancy]
sources: []
---

# Discrepancy Log — Shattered Sea

Genuine lore contradictions and ambiguous-identity calls live here (per
`wiki/system/doctrine.md`). The linter detects *structural* drift; these need human
judgment. Leave both traces visible until the DM resolves the entry.

---

## OPEN — Leviathan: one entity, two audience-split pages

**Files**
- `wiki/entities/creatures/leviathan.md` — player-facing legend, `publish: true`,
  `audience: players`. The in-world rumor (sightings, boiling water, no confirmed body).
- `wiki/entities/characters/npcs/leviathan.md` — DM-only truth, `audience: dm`. The
  reality: an entity forced through the Drowned Maw from the Elemental Plane of Water
  after the Pearl of Souls shifted the breach; Auralis reads it as a parasitic invader.

**Why it's flagged:** both share the slug `leviathan`, so `[[leviathan]]` is ambiguous
(duplicate-slug). They are the *same entity* but deliberately split by audience, so a
plain merge would leak DM-only truth into a published page.

**Signal:** nearly every inbound `[[leviathan]]` link means the **DM-truth** entity
(campaign-timeline, pearl-of-souls incursion, the-drowned-maw, vestra, auralis, the
other Plane-of-Water elementals). The truth is the primary referent; the legend is the
secondary, in-world version.

**Recommendation (DM to confirm):** keep the DM-truth page as the canonical `leviathan`
(it's what the graph points at) and rename the published legend to `leviathan-legend`
(or `leviathan-rumor`), keeping it `publish: true`. Do **not** fold the truth into the
published page. Alternatively, if section-level visibility is ever supported, one page
with a DM-only callout.

**Status:** OPEN — awaiting DM decision. Until then both pages stand; `[[leviathan]]`
resolves arbitrarily.
