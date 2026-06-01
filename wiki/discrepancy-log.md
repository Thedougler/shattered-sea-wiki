---
type: system
subtype: discrepancy-log
campaign: shattered-sea
status: active
audience: agent
publish: false
summary: "Log of lore contradictions and ambiguous entity identity that need a DM decision. Append on conflict; never auto-resolve identity. Both traces stay visible until resolved."
created: 2026-05-28
updated: 2026-06-01
tags: []
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

---

## OPEN — Felix Aho: prep NPC vs session captive

**Files**

- `wiki/entities/characters/npcs/felix-aho.md` — DM-prepped Vaka elder and fish vendor
  in Port Tidefall. Green grung, Karath defector, destroyed raiding groups on the way out
  8 years ago, built the Vaka community. Never encountered at table.

**Session 04 conflict:** a green Grung named Felix Aho was captured in the Calveno sewers
during the Grung bombing investigation. This Felix is a hired laborer (not ideological),
terrified of the ocean, transported across the Central Strait on the sixth ship, cooperative
prisoner in exchange for protection. He is not a leader, not an elder, and shows no sign of
the prep character's background.

**Source paths:**

- Prep: `Inbox/Felix-Aho.md`
- Session: `audio/sessions/session04/recap.md` (Scene 13), `audio/sessions/session04/extracts.md` (Scene 13)

**Why it's flagged:** the profiles are incompatible. The prep Felix Aho is an anti-Simone
defector who destroyed raiding groups; the session Felix Aho works for Simone's operation
(albeit as unwilling hired labor). Same name, same species, same caste color, contradictory
roles.

**Possible resolutions:**

1. DM reused the name for a different character — rename session captive or prep NPC.
2. DM adapted the character for a different role — session canon overrides prep.
3. Same person, captured and forced into labor — but session Felix says "hired," not coerced.

**Status:** OPEN — awaiting DM decision. Session canon (captive in Calveno) takes precedence
for wiki state per transcript priority rule. Prep page preserved unchanged until resolved.
