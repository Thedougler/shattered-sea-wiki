---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 6 juvenile elemental kraken from the Elemental Plane of Water — eyeless, flat-black, eight-armed surface hunter. Designed as a challenging but winnable solo encounter for a CR 5 party with a tier 1 ship."
created: 2026-05-17
updated: 2026-05-28
tags: [creature, elemental, aquatic, boss, bestiary, cr6, planar]
sources: ["Inbox/Krakling.md"]
cr: 6
confidence_level: high
aliases: ["Krakling", "Young Kraken"]
relationships:
  - "[[the-drowned-maw|The Drowned Maw]] — area of incursion"
  - "[[perrin-black-jaw|Perrin Black-Jaw]] — planar water incursion connects to his thread"
---

# Krakling

```statblock
layout: Basic 5e Layout
name: Krakling
size: Large
type: elemental
alignment: unaligned
ac: 15
ac_class: natural armor
hp: 143
hit_dice: "15d10 + 60"
speed: "10 ft., swim 40 ft."
stats: [18, 10, 18, 5, 12, 4]
saves:
  - strength: 7
  - constitution: 7
skillsaves:
  - perception: 4
  - stealth: 3
damage_resistances: "cold"
condition_immunities: "prone, exhaustion"
senses: "blindsight 60 ft., passive Perception 14"
languages: "—"
cr: 6
source: "Homebrew"
traits:
  - name: "Void Hide"
    desc: "The krakling's skin is flat black and non-reflective. While fully submerged, it has advantage on Dexterity (Stealth) checks. Creatures without darkvision or blindsight have disadvantage on Wisdom (Perception) checks to spot it in deep water."
  - name: "Siege Monster"
    desc: "The krakling deals double damage to objects and structures."
  - name: "Water Breathing"
    desc: "The krakling can breathe only underwater."
actions:
  - name: "Multiattack"
    desc: "The krakling makes two Tentacle attacks. It can replace one Tentacle attack with a Bite if it has a creature grappled."
  - name: "Tentacle"
    desc: "Melee Weapon Attack: +7 to hit, reach 15 ft., one target. Hit: 15 (2d10 + 4) bludgeoning damage. The target is Grappled (escape DC 15) and Restrained until the grapple ends. The krakling can have up to four creatures grappled simultaneously."
  - name: "Bite"
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one creature grappled by the krakling. Hit: 18 (4d6 + 4) piercing damage."
  - name: "Thrashing Ink (Recharge 5–6)"
    desc: "The krakling thrashes its arms across the deck of a vessel within 20 feet and vents a cloud of ink. Each creature on the vessel must succeed on a DC 15 Dexterity saving throw or take 21 (6d6) bludgeoning damage and be knocked prone (half on success, not prone). The vessel takes 21 bludgeoning damage (42 as Siege Monster). The krakling creates a heavily obscured 20-foot-radius cloud of ink centered on itself that lasts until the start of its next turn. The krakling is unaffected by the cloud."
  - name: "Wrenching Pull (Bonus Action)"
    desc: "One creature grappled by the krakling is dragged up to 15 feet toward it. If this movement would carry the creature off the edge of a vessel's deck, the creature must succeed on a DC 15 Dexterity saving throw or fall overboard."
```

## Overview

The krakling is what sailors are calling the arm-thing that has started appearing in the outer Shattered Sea — the eight-armed, eyeless predator that comes up under ships in the dark and starts pulling people into the water. At CR 6, it is designed as a solo encounter for a party of four 5th-level characters aboard a tier 1 ship. It will disengage if reduced below 40 HP, diving and not resurfacing.

It is the third known elemental from the Plane of Water. Like the [[leviathan|Leviathan]] and the [[ridgeback|Ridgeback]], it has no eyes, black skin, and breathes only water. Unlike either of them, it is a surface hunter.

> [!dm]
> [[perrin-black-jaw|Perrin Black-Jaw]]'s connection to the Plane of Water incursion runs through the Leviathan and the Vestra sinking. A third elemental creature appearing is part of the same pattern the Pearl of Souls is driving. Perrin will recognize the flat-black skin and the absence of eyes if he gets a good look — they match Clyde's Bestiary notes on planar fauna.

## Behavior

It hunts by feel. The arms go up over the railing first, testing — then one locks onto something solid and the grapple begins. It can hold four crew members simultaneously, working them toward the water's edge with Wrenching Pull while continuing to grab more.

**Morale:** At 40 HP or below, the krakling releases all grapples and dives. It does not chase ships. If driven off twice, it retreats.

Three ships have reported arm-related attacks in the outer Midchain in the past month. One has not made port.

## Related

- [[leviathan|The Leviathan]]
- [[ridgeback|Ridgeback]]
- [[perrin-black-jaw|Perrin Black-Jaw]]
