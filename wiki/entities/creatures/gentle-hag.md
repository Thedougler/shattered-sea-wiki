---
type: monster
subtype: monster
campaign: shattered-sea
status: unknown
audience: dm
publish: false
summary: CR 7 fey hag that builds persistent charm networks — once a victim has been charmed for 24 hours, they can never resist her again without magical intervention.
created: 2026-05-15
updated: 2026-05-31
tags: [combat, homebrew]
sources:
  - Homebrew
  - Pointy Hat
confidence_level: high
aliases:
  - Gentle Hag
cha: 19
con: 18
cr: 7
creature_type: fey
dex: 16
environment: forest, urban
int: 17
page: 0
statblock: inline
str: 14
wis: 15
---

# Gentle Hag

```statblock
layout: Basic 5e Layout
name: "Gentle Hag"
size: Medium
type: fey
alignment: Typically Chaotic Neutral
ac: 16
hp: 102
hit_dice: 12d8 + 48
speed: "30 ft."
stats: [14, 16, 18, 17, 15, 19]
saves:
  - charisma: 7
skillsaves:
  - deception: 7
  - insight: 5
  - perception: 5
  - persuasion: 7
damage_resistances: "Necrotic, Psychic; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks"
condition_immunities: "Charmed"
senses: "Darkvision 120 ft., Passive Perception 15"
languages: "Common, Halfling, Sylvan"
cr: "7"
traits:
  - name: "Fey Clarity"
    desc: "Immune to all Enchantment school spells."
  - name: "Persistent Charm"
    desc: "A creature that has been Charmed by the Gentle Hag for 24 or more hours cannot make saving throws to end the charm. It lasts until the hag dies or Greater Restoration is cast on the target."
  - name: "Joyous Loyalty"
    desc: "A creature Charmed by the hag within 5 feet of the hag or an attacker can redirect any attack meant for the hag to itself."
  - name: "Magic Resistance"
    desc: "Advantage on saving throws against spells and other magical effects."
spells:
  - "CHA-based spellcasting (spell save DC 15, +7 to hit). Requires no material components."
  - "At will: Command, Guiding Bolt, Sleep"
  - "3/day each: Blur, Hold Person, Misty Step, Suggestion"
  - "2/day each: Counterspell, Slow"
actions:
  - name: "Painful Glamor"
    desc: "Ranged Spell Attack: +7 to hit, range 60 ft. Hit: 11 (2d6+4) Psychic damage, plus 1 additional Psychic damage per charmed creature within 120 feet of the hag."
  - name: "Gentle Charm"
    desc: "One creature within 30 feet that can see the hag makes a DC 15 Charisma saving throw or is Charmed until the hag dies or the target reaches 0 HP. At the end of each of its turns, the target can repeat the save (DC increases by 1 for each prior failure, resets if target takes damage). After 24 hours, Persistent Charm applies."
  - name: "Gentle Push"
    desc: "Grant one Charmed creature 5 (1d10) temporary HP and an additional weapon attack on its next turn."
  - name: "Summon Happiness (1/Day)"
    desc: "Choose up to 1d6+1 Charmed creatures anywhere. Teleport them to within 60 feet of the hag."
```

## Coven Actions (with 2 other hags within 30 ft.)

- **Shared Spellcasting:** 3/day: Alarm, Bless, Calm Emotions, Charm Person; 2/day: Beacon of Hope, Counterspell, Hallucinatory Terrain, Haste; 1/day: Dominate Person, Heroes' Feast, Mass Cure Wounds, Modify Memory.
- **Siphon Joy:** Sacrifice a Charmed thrall (DC 15 CON; disadvantage if charmed 24+ hours). Deals half the thrall's max HP as force damage. Each coven hag heals for one-third of this.
- **Gentle Gaze:** Create a magic item (10,000 gp, 1 hour). User can see through it to read a target's deepest desire.

## Lore

A fey hag that specializes in persistent charm. Once the initial resistance is worn down, the Gentle Hag's victims become permanent retainers — joyful, loyal, and impossible to free without high-level magic. She cultivates thralls the way a gardener tends plants, offering real warmth and protection to those she has already caught. The horror is not that she is cruel. It is that she is not.

## Related

- [[haunt-hag|Haunt Hag]]