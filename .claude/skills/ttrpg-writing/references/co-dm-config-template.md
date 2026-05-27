# Co-DM Configuration

> Copy this to `content/shattered-sea/private/system/co-dm-config.md` on first use.
> Keep it short enough to scan. Store changing campaign state here only when it helps co-DM routing; canonical lore still belongs on wiki pages.

## Contents

- Identity
- Core References
- Active Campaign
- Party Roster
- Active Threads
- Active Factions
- Table Guidance
- Wiki Paths

---

## Identity

```yaml
campaign: shattered-sea
display_name: "Shattered Sea"
style: sandbox-blm
setting: "Nautical D&D 5e sandbox with faction clocks, ship play, political pressure, and player-driven consequences."
system: dnd5e-2024
```

## Core References

```yaml
dm_philosophy_ref: "content/shattered-sea/private/system/guides/DM-Philosophy.md"
tone_guide_ref: "content/shattered-sea/private/system/guides/Shattered-Sea-Tone-Guide.md"
living_world_ref: "content/shattered-sea/private/system/guides/Living-World-Design.md"
spotlight_ref: "content/shattered-sea/private/system/guides/Spotlight-Management.md"
player_gravity_ref: "content/shattered-sea/private/system/players/Player-Gravity-Wells.md"
```

## Active Campaign

```yaml
active_campaign: "Shattered Sea"
last_completed_session: 0
next_session_number: 1
next_session_date: "YYYY-MM-DD"
party_level: 1
party_location_ref: ""
ship_ref: ""
```

## Party Roster

```yaml
party:
  - pc: "PC Name"
    player: "Player Name"
    class: "Class/Subclass"
    wiki_ref: "content/shattered-sea/characters/player/PC-Slug.md"
    primer_ref: "content/shattered-sea/private/system/players/PC-Primer.md"
    last_spotlight_session: 0
    active_hooks: []
```

## Active Threads

Use situation files for active campaign pressure. Factions can appear here when they are the direct owner of the pressure.

```yaml
active_threads:
  - name: "Thread Name"
    situation_ref: "content/shattered-sea/situations/active/Thread-Slug.md"
    owner_ref: "content/shattered-sea/factions/Faction-Slug.md"
    current_pressure: "What is moving now"
    next_move_if_ignored: "What changes without player action"
    urgency: low        # low | medium | high | critical
    visible_to_players: false
```

## Active Factions

```yaml
factions:
  - name: "Faction Name"
    wiki_ref: "content/shattered-sea/factions/Faction-Slug.md"
    current_goal: "What they are pursuing right now"
    last_action: "What they did most recently"
    next_move: "What they do next if nobody interferes"
    clock_urgency: low  # low | medium | high | critical
```

## Table Guidance

```yaml
tone_notes: |
  Keep prep actionable, consequence-driven, and grounded in established wiki canon.

recurring_themes: []
off_limits: []
house_rules_refs: []
```

## Wiki Paths

```yaml
wiki_root: "."
index_doc: "content/index.md"
hot_doc: "content/hot.md"
log_doc: "content/log.md"
templates_index: "templates/CLAUDE.md"
sessions_dir: "content/shattered-sea/sessions"
situations_dir: "content/shattered-sea/situations"
active_situations_dir: "content/shattered-sea/situations/active"
factions_dir: "content/shattered-sea/factions"
characters_dir: "content/shattered-sea/characters"
player_characters_dir: "content/shattered-sea/characters/player"
npcs_dir: "content/shattered-sea/characters/npcs"
minor_npcs_dir: "content/shattered-sea/characters/minor"
private_root: "content/shattered-sea/private"
system_guides_dir: "content/shattered-sea/private/system/guides"
```
