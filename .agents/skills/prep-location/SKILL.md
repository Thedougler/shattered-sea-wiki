---
name: prep-location
description: >
  Create or expand a location wiki page for the Shattered Sea campaign. Invoke for:
  "create a page for [place]", "detail [location]", "what does [place] look like",
  "flesh out [settlement/building/dungeon/island]", "design this location". Generates
  frontmatter, toy fields, read-aloud opening, lore, notable sub-locations, inhabitants.
  Applies to all location subtypes: regions, islands, settlements, buildings, dungeons, planes.
---

## Prerequisites

1. Check `wiki/index.md` — stub exists? Expand it.
2. Read `wiki/hot.md` — what's currently true about this location?

---

## Interview

If user message doesn't answer these, ask all at once:
- Which PC has a thread connecting to this location, and how?
- Location subtype: region, island settlement, building, dungeon, plane?
- Cultural root (who built or inhabits it)?
- Campaign context — what is this location's current role?

PC connection is required. If you cannot name it, ask before generating.

---

## Toy Fields (Frontmatter + Body)

| Field | Content |
|---|---|
| `verb` | What this location *does* — its active principle, even when untouched. One of: Defend, Attract, Consume, Conceal. |
| `unstable_condition` | Concrete state, not vibe. ✓ "The east gate guard rotation has a two-minute gap." ✗ "Tensions are high." |
| `consequence` | What happens if players don't interact with it. ✓ Specific, observable. ✗ "Things will get worse." |
| `link_of_relevance` | Which PC's thread connects here. Required. |

**Verb vocabulary:**
- **Defend** — Walls, checkpoints, secrets kept in
- **Attract** — Draws people, resources, or danger toward it
- **Consume** — Takes things in and changes them
- **Conceal** — Hides something; the location exists to keep a secret

---

## Read-Aloud

3–5 sentences, player-facing prose mode. Apply player-facing prose mode (see `ttrpg-writing`):
- Second-person present tense
- Slow zoom: atmosphere → specific detail → trailing hook
- Minimum three senses
- No em dashes
- End on something unresolved

**Full mode** for first impressions. **Lite mode** (2–3 sentences) for revisits.

---

## Key Rules

- Every room/space was built for a purpose — traces remain. No "empty" rooms.
- NPCs are `[[wikilinks]]` — don't describe inline.
- Notable sub-locations get their own read-aloud + mini verb/condition/link.
- Don't describe a location by its history first — PCs experience places through senses.

---

## Output Sections

1. `> [!read-aloud]` — opening impression
2. `## Lore` — 2–4 sentences of concrete facts (DM voice)
3. `## Notable Locations` — sub-locations with verb/condition/link each
4. `## Known Inhabitants` — wikilinks only
5. `## Connections` — wikilinks to related entities, factions, situations

---

## Frontmatter

```yaml
---
type: entity
subtype: [region|island|settlement|building|dungeon|plane]
campaign: shattered-sea
status: active
audience: players
publish: true
summary: "[One-liner: what it is right now and why it matters]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [place, relevant-tags]
sources: [Homebrew]
confidence_level: established
relationships: []
verb: ""
unstable_condition: ""
consequence: ""
link_of_relevance: ""
---
```

---

## Filing

Path by subtype:
- `wiki/entities/places/regions/slug.md`
- `wiki/entities/places/islands/slug.md`
- `wiki/entities/places/settlements/slug.md`
- `wiki/entities/places/buildings/slug.md`
- `wiki/entities/places/dungeons/slug.md`
- `wiki/entities/places/planes/slug.md`

After writing: add to `wiki/index.md`, add reciprocal links, commit.

---

Load `ttrpg-writing` for all prose and formatting standards — mode selector, Brennan
voice, and callout types all apply to location pages.

---

## Reference Files

| File | Read when |
|---|---|
| `references/LOCATION.md` | Full location template, read-aloud examples, dungeon room key format |
| `references/prep-city.md` | City and settlement building via Pointy Hat Theme Park Method |
