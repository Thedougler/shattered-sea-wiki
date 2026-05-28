# Wiki DnD — Location Prep

> **Prerequisite:** `../PREP.md` loaded (philosophy, universal rules, PC gravity, naming conventions).

---

## Interview

If the user message doesn't already answer these, ask all at once:

- Campaign context
- Which PC has a thread connecting here, and how
- Location type (dungeon, city district, island, wilderness, etc.)
- Cultural root (who built/inhabits it)

---

## Toy Fields (4)

| Field | Content |
|---|---|
| `verb` | What this location *does* — its active principle, even when untouched |
| `unstable_condition` | What's about to break, shift, or boil over |
| `consequence` | What happens if no one intervenes |
| `link_of_relevance` | Which PC's thread connects here |

**Verb vocabulary** — choose one:

| Verb | Meaning |
|---|---|
| **Defend** | Walls, checkpoints, secrets kept in |
| **Attract** | Draws people, resources, or danger toward it |
| **Consume** | Takes things in and changes them |
| **Conceal** | Hides something; the location exists to keep a secret |

**Unstable Condition** — the situation only. A concrete state, not a vibe.
- ✓ "The east gate guard rotation has a two-minute gap no one has officially reported."
- ✗ "Tensions are high and the guards are on edge."

**Consequence** — what happens if players don't interact with it.
- ✓ "The gap gets noticed and filled permanently within three days."
- ✗ "Things will get worse."

---

## Read-Aloud

3–5 sentences, player-facing prose mode. Load `ttrpg-writing` and read `references/player-facing-prose.md`. Second-person present tense. Slow zoom: atmosphere → specific detail → trailing hook. Minimum three senses. No em dashes. End on something unresolved.

Full Mercer for first impressions. Mercer-lite (2–3 sentences) for revisits or minor spaces.

---

## Key Rules

- Every room was built for a purpose — traces remain. No "empty" rooms.
- NPCs are `[[wikilinks]]` to existing pages — don't describe inline.
- Notable sub-locations get their own read-aloud + mini verb/condition/link.
- Don't describe a location by its history first — PCs experience places through senses.

---

## Output Sections

1. Overview (`> [!read-aloud]` opening)
2. `## Lore` — 2–4 sentences of concrete facts
3. `## Notable Locations` — sub-locations with their own verb/condition/link
4. `## Known Inhabitants` — wikilinks only
5. `## Connections`

---

## Filing

Read the appropriate location template before generating page content — subtype templates live in `templates/` (region, island, town, building, site, plane) and define required frontmatter and section structure. See `templates/CLAUDE.md` for the full subtype→directory map. Run vault filing sequence from `../PREP.md` § Vault Filing after writing.
