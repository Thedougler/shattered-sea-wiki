---
type: monster
subtype: monster
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 1 humanoid; red-caste operatives with druidic spellcasting. Spike Growth in tight corridors, Cure Wounds for self-sustain. The ritual specialist of Grung operations."
created: 2026-06-01
updated: 2026-06-02
tags:
  - grung
  - combat
sources:
  - VGM
confidence_level: high
aliases:
  - Grung Wildling
  - Red-Caste Operative
cha: 11
con: 15
cr: 1
creature_type: humanoid
dex: 16
environment: forest, swamp, urban
int: 10
page: 157
statblock: inline
str: 7
wis: 15
---

# Grung Wildling

```statblock
layout: Basic 5e Layout
name: "Grung Wildling"
size: Small
type: humanoid
subtype: grung
alignment: Typically Neutral Evil
ac: 13
ac_note: natural armor
hp: 27
hit_dice: 5d6 + 10
speed: "25 ft., Climb 25 ft."
stats: [7, 16, 15, 10, 15, 11]
saves:
  - dexterity: 5
skillsaves:
  - athletics: 2
  - perception: 4
  - stealth: 5
  - survival: 4
damage_immunities: "poison"
condition_immunities: "poisoned"
senses: "Passive Perception 14"
languages: "Grung"
cr: "1"
traits:
  - name: "Amphibious"
    desc: "The grung can breathe air and water."
  - name: "Poisonous Skin"
    desc: "Any creature that grapples the grung or otherwise comes into direct contact with the grung's skin must succeed on a DC 12 Constitution saving throw or become poisoned for 1 minute. A poisoned creature no longer in direct contact with the grung can repeat the saving throw at the end of each of its turns, ending the effect on a success."
  - name: "Standing Leap"
    desc: "The grung's long jump is up to 25 feet and its high jump is up to 15 feet, with or without a running start."
  - name: "Spellcasting"
    desc: "The grung is a 9th-level spellcaster. Its spellcasting ability is Wisdom (spell save DC 12, +4 to hit with spell attacks). It has the following spells prepared:\nCantrips (at will): Druidcraft, Poison Spray\n1st level (4 slots): Cure Wounds, Entangle, Jump\n2nd level (3 slots): Barkskin, Spike Growth"
actions:
  - name: "Dagger"
    desc: "Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 5 (1d4 + 3) piercing damage plus 5 (2d4) poison damage."
  - name: "Shortbow"
    desc: "Ranged Weapon Attack: +5 to hit, range 80/320 ft., one target. Hit: 6 (1d6 + 3) piercing damage plus 5 (2d4) poison damage."
```

## Tactical Behavior

The red-caste operative at the [[calveno-sewers-grung-magazines|primary detonation chamber]] prioritizes the summoning circle's integrity above all else. Tactical sequence:

1. **Round 1:** Spike Growth in the main entrance corridor (20-ft radius, 2d4 piercing per 5 ft of movement). In a 5-6 ft wide tunnel, this is devastating — the party cannot flank or bypass without taking damage.
2. **Round 2+:** Shortbow from behind the Spike Growth zone, using scaffolding as half cover. Uses Cure Wounds on herself or wounded Elite Warriors if the line holds.
3. **Last resort:** Entangle to lock down a PC who breached the Spike Growth, then poisons them in melee.

**Morale threshold:** Fights to the death. Will destroy the summoning circle herself (Action to disrupt) rather than let the party capture it intact — but only if it is clear the chamber is lost. Until that point, she defends it.

## Encounter Notes

Spike Growth is concentration. If the party can break her concentration (forced save via damage, or targeting WIS saves), the corridor opens. [[perrin-black-jaw|Perrin]]'s Tasha's Hideous Laughter targets WIS (the wildling saves at +2) and would break Spike Growth concentration.

Poison Spray (cantrip) is a DC 12 Constitution save for 2d12 poison damage at 10 ft range. Strong against melee attackers who close the distance.

## Related

- [[grung-npc|Grung (Green-Caste NPC)]]
- [[grung-elite-warrior|Grung Elite Warrior]]
- [[grung-clans|Grung Clans (Faction)]]
- [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]]
