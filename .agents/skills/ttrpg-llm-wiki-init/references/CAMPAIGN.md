# Wiki DnD — Campaign Scaffolding

Builds and maintains complete campaign structures inside the vault. Owns the scaffolding layer — folder shape, hub pages, organizing documents, season/chapter breakdowns, file placement, and cross-file consistency. Delegates all entity-level prep.

> **Prerequisite:** SKILL.md bootstrap complete — `wiki/index.md` and `CLAUDE.md` already read. Check `wiki/index.md` before creating any page.

---

## First Principles

1. **Scaffold around player pull.** Structure that ignores what the players care about gets ignored by the players. Load gravity data for existing campaigns before shaping priorities.
2. **Support multiple routes, not one intended route.** Campaign structure should enable agency, not constrain it. Fronts and factions create pressure — they don't guarantee outcomes.
3. **Match the live vault, not an abstract template.** Published-adventure formatting and generic templates produce structure neither the agent nor GM will use. Mirror what already works in this vault.
4. **Keep the campaign navigable.** Every campaign needs a hub page that makes current state scannable in under a minute — for both humans in Obsidian and agents at boot.
5. **Separate scaffolding from content generation.** This document creates the container. `PREP.md` fills it. Conflating the two produces bloated hub files and loses the delegation benefit.

---

## Required Intake

Establish all of the following before creating any files:

1. Campaign name and slug (kebab-case)
2. Campaign type: standard, sandbox, event-based, or setting-based (see [references/CAMPAIGN-TYPES.md](references/CAMPAIGN-TYPES.md))
3. Tone and rating boundaries
4. Intended level range or power band
5. New campaign or existing one being reorganized
6. Which PCs or player arcs are in scope
7. Whether gravity data (player pull, active threads) already exists in the vault

Ask concise questions for anything missing. Do not create files until all seven are established.

---

## Campaign Modes

### Standard Campaign

Use for campaigns with a clear arc, season progression, or chapter cadence.

Scaffold around:

- Campaign premise and overall arc
- Season or chapter structure
- Major fronts and escalating pressures
- Expected pivot points — not fixed scenes
- A hub page that makes current state easy to scan

### Sandbox Campaign

Use for hub, region, sea, city, or faction-web structures where players drive order and pace.

Scaffold around:

- Locations or regions visitable in any order
- Active factions with off-screen motion
- Player-driven objectives and convergence points
- Reusable narrative islands and deployable set pieces

Do not force a sandbox into a fake chapter sequence just to look organized. Use hub files, region/location structures, and faction pages instead.

---

## Canonical Output Location

Campaigns live at:

```text
content/<campaign-slug>/
```

Model the structure on `content/shattered-sea/`. Typical scaffold:

```text
content/<campaign-slug>/
├── campaign-overview.md      ← campaign master doc (DM-facing)
├── campaign-timeline.md      ← chronological event tracker
├── index.md                  ← entity index for this campaign
├── hot.md                    ← session state snapshot
├── player-primer.md          ← player-facing briefing (no spoilers)
├── faq.md                    ← campaign FAQ
├── npcs/
├── factions/
├── places/
├── lore/
├── items/
├── ships/
├── beastiary/
├── species/
├── party/
└── private/                  ← GM-only material
```

Adjust subfolder names to match what already exists when reorganizing an existing campaign. Prefer the live vault convention over abstract template purity.

---

## Hub Page Structure

The hub is campaign-specific — there is no fixed template. Build it around `campaign-overview.md`. Keep it under 400 words: its job is fast orientation, not documentation.

Required sections:

- **Current State** — active fronts, party location, immediate pressures
- **The Party** — links to PC pages
- **Active Factions** — 3–5 factions with one-line status and links
- **Key Locations** — hub locations and region anchors with links
- **Open Questions** — DM-facing unresolved tensions
- **Navigation** — links to `index.md`, `hot.md`, `campaign-timeline.md`

---

## Delegation Table

| Step | Target | Responsibility |
|---|---|---|
| 1 | `wiki` | Retrieve existing campaign context from the vault |
| 2 | `PREP.md` | Entity prep: NPCs, factions, locations, encounters |
| 3 | `templates/` (vault root) | Select and stamp page templates |
| 4 | `wiki-meta` | Validate structure, lint, check consistency |

This skill decides where content lives and how the campaign is organized. It does not generate entity content — delegate that to `PREP.md`.

---

## Templates

Templates live in `templates/` at the vault root (Templater-compatible). Campaign-specific types:

| Type | Template | Use for |
|---|---|---|
| `campaign-overview` | `templates/campaign-overview.md` | Master campaign document (DM-facing) |
| `chapter` | `templates/chapter.md` | Chapter or session structure document |
| `campaign-timeline` | `templates/campaign-timeline.md` | Chronological event tracker |

For entity pages (NPCs, factions, locations, ships, etc.) load `templates/<type>.md` from the vault root.

---

## Campaign Iteration

When updating or refining an existing campaign:

1. Read `campaign-overview.md` to understand full current state
2. Read all chapters or pages affected by the change
3. Read relevant NPC, faction, and location documents
4. Document what's changing before writing anything — identify ripple effects
5. Check name/spelling consistency across all files: character names, location names, faction names must be identical everywhere
6. Check number consistency: travel times, dates, DCs for the same task
7. After changes: update `campaign-overview.md` synopsis if story beats shifted
8. Commit — vault must be in a valid state before responding

**Common change types:**

- Content addition: new chapter/session, new NPC, new location, new subplot
- Content refinement: more detail on an existing element, expanded description
- Player-driven adjustment: adapting to unexpected player actions, incorporating character death, following up on player decisions

See [references/CAMPAIGN-TYPES.md](references/CAMPAIGN-TYPES.md) for structural patterns by campaign type. See [references/ADVENTURE-STRUCTURE.md](references/ADVENTURE-STRUCTURE.md) for WotC-style adventure anatomy (useful for chapter planning and published-adventure-style campaigns).
