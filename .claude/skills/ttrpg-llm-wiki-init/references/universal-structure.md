# Universal Structure — TTRPG LLM-Wiki

Read when initializing a new vault or verifying the folder tree against the standard.
This is the universal baseline. Campaign-specific additions go in CLAUDE.md.

---

## Governing Principles

**P1 — The agent navigates by path prediction, not search.**
If the agent knows what something IS, it should know where it LIVES without searching.
Paths encode type. Type encodes path. The taxonomy is bidirectional.

**P2 — Folders encode one dimension of specificity per level.**
Three to four levels maximum. Deeper than four levels creates navigation complexity
that exceeds the organizational benefit. When in doubt: flatter.

**P3 — Audience is frontmatter, not folder.**
`audience: dm` hides content from player output. A folder named `private/` or `dm-only/`
is a structural smell — use the field. The single exception: `wiki/system/` is implicitly
`audience: agent` because its whole purpose is agent operational context.

**P4 — Situations have lifecycles. Entities do not.**
Entities live in their folders regardless of whether they are alive, dead, destroyed, or
forgotten. Situations move through lifecycle folders as the campaign progresses.

**P5 — Depth is proportional to player engagement.**
Everything starts as a stub. Player interest signals drive expansion. The mile-wide-inch-deep
model is an editorial policy, not a structural one.

**P6 — Every wiki file knows its source; every source is retained.**
Wiki files cite their origin via `sources` frontmatter, and fully-ingested sources are
archived into `.raw/` rather than deleted. Provenance lives in those two places plus git
history — there is no separate registry ledger to keep in sync.

**P7 — Large tasks are never abandoned. They are queued.**
Any multi-file reorganization creates a `wiki/work-queue.md` entry before starting.
Each file processed updates the queue. Any agent resuming work reads the queue first.

---

## Canonical Folder Tree

```
VAULT_ROOT/
│
├── CLAUDE.md                                    ← governance doc; always read first
│                                                   contains: campaign info, party, reading order,
│                                                   ideal state, automatic behaviors, frontmatter reqs
│
├── Inbox/                                       ← human write zone; unprocessed drops
│                                                   anything here needs to be filed via wiki-categorize
│
├── .raw/                                        ← IMMUTABLE SOURCE MATERIAL
│   │                                               files here are never edited; all work in copies
│   ├── sessions/
│   │   └── sNNN/                                ← one folder per session
│   │       ├── sNNN-raw.md                      ← exact transcription output; never touch
│   │       ├── sNNN-clean.md                    ← agent-cleaned version; DM may edit
│   │       └── sNNN-flags.md                    ← items needing DM review
│   │
│   ├── characters/
│   │   ├── interviews/                          ← session zero player interviews
│   │   └── sheets/                              ← exported character sheet data
│   │
│   ├── homebrew/                                ← DM-authored game material
│   ├── reference/
│   │   └── clippings/                           ← third-party rules text, stat blocks
│   └── assets/                                  ← media; never text-ingested
│       ├── session-art/
│       ├── maps/
│       └── banners/
│
└── wiki/                                        ← COMPILED KNOWLEDGE
    │
    ├── hot.md                                   ← read first, always; current world state
    ├── index.md                                 ← master catalog; every wiki file listed
    ├── work-queue.md                            ← active multi-step task tracker
    ├── discrepancy-log.md                       ← lore contradictions (created on first conflict)
    │
    ├── system/                                  ← audience: agent; mandatory pre-reads
    │   ├── task-routing.md                      ← maps task types to required files + skills
    │   ├── party-combat-primer.md               ← party combat capabilities; mandatory before encounters
    │   ├── party-session-primer.md              ← party session context; mandatory before session prep
    │   └── players/                             ← one primer + one sheet per PC
    │       ├── {pc-slug}-primer.md
    │       └── {pc-slug}-sheet.md
    │
    ├── dm/                                      ← audience: dm; planning intelligence
    │   ├── player-interests.md                  ← what each player is engaged with; drives content depth
    │   └── combat-analytics.md                  ← empirical combat data; drives encounter calibration
    │
    ├── entities/                                ← discrete named things in the world
    │   ├── characters/
    │   │   ├── pcs/                             ← player characters
    │   │   ├── npcs/                            ← significant named NPCs (named, has wants, has history)
    │   │   ├── crew/                            ← named crew; one defining trait; not full NPCs
    │   │   └── minor/                           ← mentioned once; stub only
    │   │
    │   ├── places/
    │   │   ├── regions/                         ← large geographic zones
    │   │   ├── islands/                         ← specific landmasses (if nautical/island campaign)
    │   │   ├── settlements/                     ← cities, towns, ports
    │   │   ├── buildings/                       ← specific buildings, shops, rooms
    │   │   ├── dungeons/                        ← keyed exploration sites
    │   │   ├── sites/                           ← standalone landmarks, ruins, salvage fields
    │   │   └── planes/                          ← extraplanar locations
    │   │
    │   ├── factions/                            ← groups with shared identity and agenda
    │   ├── deities/                             ← gods/divine entities with wants and agency
    │   ├── items/                               ← named objects; subdivided by rarity
    │   │   ├── common/
    │   │   ├── uncommon/
    │   │   ├── rare/
    │   │   ├── legendary/
    │   │   └── artifact/
    │   │
    │   ├── creatures/                           ← stat blocks; subdivided by usage
    │   │   ├── active/                          ← used in a session
    │   │   ├── planned/                         ← in prep/run guides
    │   │   └── background/                      ← not yet utilized
    │   │
    │   └── vehicles/                            ← named vessels/vehicles (ships, wagons, etc.)
    │       └── {vehicle-name}/                  ← subfolder for detail_tier 3 vehicles
    │
    ├── situations/                              ← atomic dynamic conditions
    │   ├── active/                              ← clock ticking now
    │   ├── dormant/                             ← prepped; condition-gated; no clock yet
    │   └── resolved/                            ← concluded; archive; never delete
    │
    ├── islands/                                 ← narrative content clusters (if used)
    │   └── {island-name}/                       ← subfolder for complex multi-part islands
    │       └── index.md
    │
    ├── lore/                                    ← abstract world knowledge (not named entities)
    │   ├── species/                             ← playable/world species (biology, culture)
    │   ├── creatures/                           ← creature types, monster classes
    │   ├── history/                             ← historical events, timelines
    │   ├── geography/                           ← geographic overview, world maps
    │   ├── cultures/                            ← cultural practices, social structures
    │   ├── religions/                           ← theology, divine systems (not the deity itself)
    │   ├── magic/                               ← magic systems, arcane theory
    │   └── languages/                           ← in-world languages
    │
    ├── rules/                                   ← how the game works (not how the world works)
    │   ├── core/                                ← campaign-defining mechanics
    │   ├── subsystems/                          ← larger rule systems (ship combat, bastions)
    │   ├── encounter-design/                    ← encounter tools
    │   ├── tables/                              ← random and encounter tables
    │   ├── items/                               ← generic item type guides
    │   ├── spells/                              ← homebrew spells
    │   └── classes/                             ← homebrew classes, subclasses, feats
    │
    └── sessions/                               ← compiled session records
        ├── sNNN-summary.md                      ← agent-facing; dense intelligence doc
        └── sNNN-recap.md                        ← player-facing; narrative prose
```

---

## Minimum Required Files

These files must exist for the wiki to be operational. Create them if absent.

| File | Required | If Missing |
|---|---|---|
| `CLAUDE.md` | Yes | Run Init Protocol |
| `Inbox/` | Yes | Create empty directory |
| `wiki/hot.md` | Yes | Create from template |
| `wiki/index.md` | Yes | Create stub |
| `wiki/system/task-routing.md` | Yes | Create stub; flag for DM completion |
| `wiki/work-queue.md` | On demand | Create when first multi-file task begins |
| `wiki/discrepancy-log.md` | On demand | Create on first lore contradiction |

---

## Content Type → Path Decision Tree

```
Does it have a lifecycle (starts, runs, and ends)?
  YES, single condition → wiki/situations/
    Clock running now?         → active/
    Triggered but not fired?   → dormant/
    Concluded?                 → resolved/
  YES, content cluster (multiple entry points, contains situations) → wiki/islands/

Is it a named individual (person, creature with identity)?
  YES → wiki/entities/characters/
    Player character?           → pcs/
    Named, has wants, has history, will appear again → npcs/
    Named crew member, one trait → crew/
    Named but thin, mentioned once → minor/

Is it a named place, space, or region?
  YES → wiki/entities/places/
    Large geographic zone → regions/
    Specific landmass → islands/
    City, town, port → settlements/
    Specific building, shop → buildings/
    Keyed exploration site → dungeons/
    Standalone landmark, ruins, salvage field → sites/
    Extraplanar location → planes/

Is it a group, organization, movement, or crew?
  YES → wiki/entities/factions/

Is it a god or divine entity with wants and agency?
  YES → wiki/entities/deities/
  (Theological LORE about that deity → wiki/lore/religions/)
  (Religious FACTION → wiki/entities/factions/)

Is it a named vessel or vehicle?
  YES → wiki/entities/vehicles/
    detail_tier 0: no file — embed in situation
    detail_tier 1-2: single file in vehicles/
    detail_tier 3: subfolder vehicles/{name}/

Is it a named object with history or mechanical significance?
  YES → wiki/entities/items/{rarity}/
    common/uncommon/rare/legendary/artifact by rarity field

Is it abstract world knowledge (true of the world, not a specific entity)?
  YES → wiki/lore/
    Species/culture → lore/species/
    Creature type → lore/creatures/
    Historical event → lore/history/
    Theology/divine system → lore/religions/
    Magic system → lore/magic/

Is it how the GAME works (mechanics, not world)?
  YES → wiki/rules/
    Core campaign mechanics → rules/core/
    Larger rule systems → rules/subsystems/
    Encounter tools → rules/encounter-design/

Is it a session record?
  Raw transcript → audio/sessions/ (CSV per part)
  Agent-facing summary → wiki/sessions/sNNN-summary.md
  Player-facing recap → wiki/sessions/sNNN-recap.md

Cannot categorize?
  → Inbox/ with one-line note explaining why
  → Commit: `flag: uncategorizable — {file} — {reason}`
  → Never create a new top-level folder without DM approval
```
