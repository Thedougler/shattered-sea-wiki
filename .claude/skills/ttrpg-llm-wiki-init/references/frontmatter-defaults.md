# Frontmatter Defaults — TTRPG LLM-Wiki

Read when adding missing fields to files during auto-correction passes.
These are the universal defaults. Campaign CLAUDE.md may specify overrides.

---

## Default Values by Field

When a required field is missing, add it with the default below and log the addition.

| Field | Default | Notes |
|---|---|---|
| `type` | Inferred from path — see Type Inference table | If path is ambiguous, use `unknown` and flag |
| `subtype` | Inferred from subfolder — see Subtype Inference table | |
| `campaign` | Read from CLAUDE.md | If CLAUDE.md absent, use `"unknown"` |
| `status` | `unknown` | Safer than guessing; DM corrects on review |
| `audience` | `dm` | Safer default; DM promotes to `players` when ready |
| `publish` | `false` | Same reasoning as audience default |
| `summary` | `"Stub — no summary yet."` | Flag the file for DM attention |
| `confidence_level` | `medium` | For entity files |
| `relationships` | `[]` | For entity files |
| `created` | Today's date | Only set if field was never present |
| `updated` | Today's date | Set on content change; not on structural fix |
| `tags` | `[]` | |
| `sources` | `["Unknown"]` | |
| `lifecycle` | `dormant` | For situation files |
| `island` | `null` | For situation files |
| `portable` | `false` | For island files |
| `entry_points` | `[]` | For island files |
| `contains_situations` | `[]` | For island files |
| `rooms` | `0` | For dungeon files — integer room count |
| `cr_range` | `""` | For dungeon files — e.g. `"1/2–3"` |
| `topology` | `""` | For dungeon files — `linear \| branching \| hub \| loop` |
| `detail_tier` | `1` | For vehicle files |
| `session_number` | `0` | For session files; DM corrects |
| `session_date` | `"unknown"` | For session files |
| `system_role` | `"unknown"` | For system/ files (audience: agent) |
| `token_profile` | `on-demand` | For system/ files |
| `mandatory_for` | `[]` | For system/ files |
| `update_trigger` | `""` | For system/ files |

---

## Type Inference from Path

| Path contains | `type` value |
|---|---|
| `wiki/entities/` | `entity` |
| `wiki/situations/` | `situation` |
| `wiki/islands/` | `island` |
| `wiki/sessions/` | `session` |
| `wiki/system/` | `system` |
| `wiki/lore/` | `lore` |
| `wiki/rules/` | `rules` |
| `wiki/dm/` | `dm-intelligence` |
| `.raw/` | `raw` |
| Root-level | `governance` |

---

## Subtype Inference from Path

| Path contains | `subtype` value |
|---|---|
| `entities/characters/pcs/` | `pc` |
| `entities/characters/npcs/` | `npc` |
| `entities/characters/crew/` | `crew` |
| `entities/characters/minor/` | `minor-npc` |
| `entities/places/regions/` | `region` |
| `entities/places/islands/` | `island-place` |
| `entities/places/settlements/` | `settlement` |
| `entities/places/buildings/` | `building` |
| `entities/places/dungeons/` | `dungeon` |
| `entities/places/sites/` | `site` |
| `entities/places/planes/` | `plane` |
| `entities/factions/` | `faction` |
| `entities/deities/` | `deity` |
| `entities/items/` | `item` |
| `entities/vehicles/` | `vehicle` |
| `situations/active/` | `active-situation` |
| `situations/dormant/` | `dormant-situation` |
| `situations/resolved/` | `resolved-situation` |
| `islands/` | `island` |
| `lore/species/` | `species` |
| `lore/creatures/` | `creature` |
| `lore/history/` | `history` |
| `lore/geography/` | `geography` |
| `lore/cultures/` | `culture` |
| `lore/religions/` | `religion` |
| `lore/magic/` | `magic` |
| `lore/languages/` | `language` |
| `rules/core/` | `core-rule` |
| `rules/subsystems/` | `subsystem` |
| `rules/encounter-design/` | `encounter-design` |
| `rules/tables/` | `table` |
| `rules/items/` | `item-type` |
| `rules/spells/` | `spell` |
| `rules/classes/` | `class` |
| `sessions/` (summary) | `session-summary` |
| `sessions/` (recap) | `session-recap` |
| `system/players/` (primer) | `pc-primer` |
| `system/players/` (sheet) | `pc-sheet` |
| `system/` | `system-file` |
| `dm/` | `dm-file` |
| `audio/sessions/` | `raw-session` |
| `.raw/characters/` | `raw-character` |
| `.raw/homebrew/` | `raw-homebrew` |

---

## Relationship Labels (Standardized)

Use these relationship type labels consistently across all entity files.
Bidirectionality rule: if A has label X pointing to B, B must have the reciprocal label pointing to A.

| Label on A | Reciprocal label on B | Use for |
|---|---|---|
| `leads` | `led_by` | Hierarchical authority |
| `member_of` | `has_member` | Organizational membership |
| `located_in` | `contains` | Place hierarchy |
| `part_of` | `includes` | Structural containment |
| `allies` | `allied_with` | Cooperative faction relationship |
| `rivals` | `rival_of` | Competitive or hostile relationship |
| `captained_by` | `captain_of` | Vehicle command |
| `family_of` | `family_of` | Kinship (symmetric) |
| `formerly_was` | `former_identity_of` | Identity transitions (renames, etc.) |
| `seeks` | `sought_by` | Active pursuit (bounties, quests) |
| `commissioned_by` | `commissioned` | Task or job origin |
| `owns` | `owned_by` | Possession |
| `created_by` | `created` | Authorship or creation |
| `worships` | `worshipped_by` | Religious devotion |

Use `see_also` for any cross-reference that doesn't fit a directional relationship.

---

## Summary Field Quality Guide

The summary field is the most important field in the wiki. It is often the ONLY field the
agent reads before deciding whether to open the full file. Bad summaries cause hallucinations.

**Required qualities:**
- Present on every file without exception
- Under 2 sentences (target ≤50 words)
- Current — updated when entity status changes (this counts as a content change)
- Concrete: facts, not descriptions
- Written from DM perspective, not player perspective
- Answers: *What is this entity RIGHT NOW, and why does it matter to the current campaign?*

**Bad summaries:**
- `"An important NPC with a complex background."` — no facts
- `"Rattkin NPC in Calveno."` — no context, no current state
- `"See nona-black-jaw.md for details."` — useless summary

**Good summaries:**
- `"Rattkin matriarch of the Black-Jaw Run and senior Tangle elder; reunited with Perrin in Calveno, has a favor to ask."`
- `"Active situation: Grung raid on Calveno is imminent; clock at 4/6; fires when Beffa festival window opens."`
- `"The Uncertainty's cook, one arm, devoted to Perrin, knows something about the Warren she hasn't said."`

**Auto-flag summary for rewrite when:**
- Session notes reference an entity in a way the current summary doesn't reflect
- Entity status, location, or allegiance changes
- A situation the entity is involved in resolves
- Summary is still the stub default: `"Stub — no summary yet."`
