---
type: system
subtype: reference
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: Controlled tag vocabulary for the Shattered Sea wiki. Read this before assigning tags to any page.
created: 2026-05-31
updated: 2026-06-05
tags:
  - dm-prep
sources: []
system_role: unknown
token_profile: on-demand
mandatory_for: []
update_trigger: ""
---

# Tag Taxonomy — Shattered Sea

Canonical tag vocabulary for the wiki. Max 5 tags per page. Use only tags from this list.

## Rules

- **Max 5 tags per page.** `visibility/` tags don't count toward this limit.
- **Lowercase, hyphenated.** No spaces, no camelCase.
- **No frontmatter duplicates.** Never tag what `type`, `subtype`, `status`, or `audience` already says.
- **No entity names.** Named NPCs, places, ships — use wikilinks, not tags.
- **Prefer cross-cutting.** A tag earns its place if it helps find related content across entity types.
- **`visibility/` is reserved.** Only one per page; not subject to alias mapping; managed separately.

---

## Canonical Tags

### Faction (8)

Tags for major factions that cut across NPCs, locations, situations, and narrative islands.

| Tag | Covers |
|---|---|
| `dravosi` | Dravosi Crown — naval/colonial power |
| `tessarine` | Tessarine Concordat — commercial/colonial power |
| `passage` | The Passage — Rattkin smuggling network |
| `waveservants` | Umberlee's practical clergy and institutions |
| `sunken-crown` | The Sunken Crown — deep historical power |
| `drowned-maw` | The Drowned Maw — planar/abyssal threat region |
| `fisk-fleet` | Fisk's Fleet — destroyed fleet with active consequences |
| `five-blades` | Five Blades — Moucheron mercenary company |

### Theme / Domain (6)

Cross-cutting content domains. Tag when the topic is central, not incidental.

| Tag | Covers |
|---|---|
| `umberlee` | Divine influence of Umberlee (distinct from `waveservants` institution) |
| `undead` | Undead creatures, necromantic threats, lich plots |
| `antheri` | Ancient Antheri civilization — ruins, artifacts, lore |
| `rattkin` | Rattkin species and culture (broader than `passage`) |
| `grung` | Grung species, culture, Verdant Teeth connections |
| `moucheron` | Moucheron species and mercenary tradition |

### Narrative (3)

Thematic tags for cross-cutting story concerns.

| Tag | Covers |
|---|---|
| `maritime` | Ships, sailing, naval operations, sea travel |
| `mystery` | Unsolved questions, hidden info, investigation hooks |
| `salvage` | Wreck recovery, prize claiming, Red Lady money thread |

### Content Type (2)

| Tag | Covers |
|---|---|
| `homebrew` | Custom content not from published 5e sources |
| `late-game` | Tier 3–4 content; end-game revelations; don't surface early |

### Prep / Workflow (7)

Tags that help during session prep and at the table.

| Tag | Covers |
|---|---|
| `needs-detail` | Page exists but needs significant expansion (stats, description, mechanics) |
| `encounter-ready` | Stat block, read-aloud, and DM notes complete — grab and run |
| `read-aloud` | Contains boxed player-facing narration |
| `player-resource` | Content the DM might hand or show to players |
| `dm-prep` | Session prep material — scene guides, run guides, encounter designs |
| `recurring` | NPCs, locations, or encounters that appear across multiple sessions |
| `combat` | Encounters, stat blocks, tactical content |

---

## Alias Map

When you find these tags, replace with the canonical form.

| Alias | → Canonical |
|---|---|
| `dravosi-crown`, `crown` (as faction) | `dravosi` |
| `tessarine-concordat` | `tessarine` |
| `the-passage` | `passage` |
| `maw` | `drowned-maw` |
| `waveservant` | `waveservants` |
| `fisks-fleet` | `fisk-fleet` |
| `Homebrew` (wrong case) | `homebrew` |
| `late_game` | `late-game` |
| `dm-craft`, `dm-notes`, `dm-reference`, `prep` | `dm-prep` |
| `player-facing`, `primer` | `player-resource` |
| `lich` | `undead` |
| `antheri-adjacent` | `antheri` |

---

## Deprecated Tags

These tags were used before the taxonomy was established. Remove them on any page you touch.

### Frontmatter duplicates — remove, the field already says it

`situation`, `session`, `rules`, `lore`, `system`, `index`, `narrative-island`, `reference`, `entity`,
`item`, `place`, `npc`, `creature`, `subclass`, `scene`, `faction`, `ship`, `vehicle`, `species`,
`deity`, `thread`, `run-guide`, `equipment`, `encounter`, `conflict`, `obligation`, `question`,
`secret`, `pursuit`, `event`

`active`, `dormant`, `resolved`, `dead`, `destroyed`

`dm-only`, `players`, `player-facing` (when meaning `audience: players`)

### Entity-name tags — replace with wikilinks

PC names: `perrin`, `delmar`, `jean-claude`, `crissdalynn`

NPC names: `nona`, `grigori`, `kyzil`, `hollowell`

Place names: `calveno`, `warren`, `port-tidefall`, `kalowe`, `midchain`, `crown-islands`,
`verdant-teeth`, `calders-tooth`, `fort-crestwall`, `cape-solitude`, `aruhe`, `takowan`

Ship names: `surety`, `saltwright`

### Source-reference tags — move to `sources:` frontmatter

`bestiary`, `XMM`, `XPHB`, `PHB`, `DMG`

### System/process tags — not content tags

`current-state`, `work-queue`, `lint`, `review`, `log`, `discrepancy`

### Too granular / better in body text

D&D class names (`bard`, `warlock`, `rogue`, `ranger`, `monk`, `fighter`, etc.),
D&D species names (`aarakocra`, `tabaxi`, `rattkin` is an exception — it's a cultural tag),
CR ratings (`cr1`–`cr24`), session numbers (`session-01`–`session-04`),
item properties (`rare`, `uncommon`, `legendary`, `attunement`, `wondrous`, `magic-item`),
occupation labels (`pirate`, `captain`, `merchant`, `sailor`, etc.)

---

## Choosing Tags for a New Page

1. Read this file.
2. Pick up to 5 from the canonical list:
   - 0–2 faction tags (what factions are entangled?)
   - 0–2 theme/domain tags (what domain does this cross-cut?)
   - 0–1 prep/workflow tags (what's the DM-prep state?)
3. If nothing fits, the page may not need tags — or a new tag is warranted (propose it).

## Adding a New Tag

Before adding, verify no existing tag covers the concept. If genuinely new:

1. It must appear or be needed on 5+ files across 3+ entity types.
2. Add it to the appropriate section above with a one-line description.
3. Add any aliases to the alias map.
4. Mirror the change in `.claude/scripts/tag_taxonomy.py` (the machine-readable source of
   truth), then run `python3 .claude/scripts/check_taxonomy_sync.py` to confirm the two stay
   in sync.
