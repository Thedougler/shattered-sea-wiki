---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 8 elemental serpent from the Plane of Water — the second entity through the Maw fissure. Territorial tribute-warden: attacks vessels that cross its claimed water without offering. Announces approach via visible rolling humps."
created: 2026-05-16
updated: 2026-05-28
tags: [creature, elemental, aquatic, boss, bestiary, cr8, planar]
sources: ["Inbox/Ridgeback.md"]
cr: 8
confidence_level: high
aliases: ["The Ridgeback", "The Roller", "The Hump"]
relationships:
  - "[[the-drowned-maw|The Drowned Maw]] — territory"
  - "[[auralis|Auralis]] — knows something crossed"
---

# Ridgeback

![[Ridgeback.webp|Ridgeback rolling toward a ship, three matte-black humps breaking the Shattered Sea surface]]

```statblock
layout: Basic 5e Layout
name: Ridgeback
size: Huge
type: elemental
alignment: unaligned
ac: 15
ac_class: natural armour
hp: 138
hit_dice: "12d12 + 60"
speed: "10 ft., swim 50 ft."
stats: [24, 8, 20, 4, 14, 5]
saves:
  - strength: 10
  - constitution: 8
skillsaves:
  - perception: 5
  - stealth: 2
damage_resistances: "cold, lightning"
condition_immunities: "prone, exhaustion"
senses: "blindsight 60 ft., passive Perception 15"
languages: "—"
cr: 8
source: "Homebrew"
traits:
  - name: "Planar Camouflage"
    desc: "The ridgeback's scales are non-reflective jet black. While fully submerged, it has advantage on Dexterity (Stealth) checks."
  - name: "Rolling Wake"
    desc: "When the ridgeback moves at full swim speed while within 30 feet of the water's surface, its undulating body creates arching humps that break the surface. Any creature with line of sight can spot this from up to 1 mile away in clear conditions. The ridgeback cannot suppress this while moving at speed."
  - name: "Deep Warden"
    desc: "The ridgeback senses vibrations through water with preternatural precision. It is aware of any vessel larger than a rowboat within 500 feet. If a vessel passes through this range without tribute being offered to the deep — objects of meaningful weight dropped deliberately into the water — the ridgeback pursues that vessel until it clears the claimed area or offers tribute."
  - name: "Siege Monster"
    desc: "The ridgeback deals double damage to objects and structures."
  - name: "Water Breathing"
    desc: "The ridgeback can breathe only underwater."
actions:
  - name: Multiattack
    desc: "The ridgeback makes one Bite attack and one Tail Slam attack."
  - name: Bite
    desc: "Melee Weapon Attack: +10 to hit, reach 15 ft. Hit: 25 (4d8 + 7) piercing damage. The target is Grappled (escape DC 18). Until this grapple ends, the ridgeback cannot use Bite against another target."
  - name: Tail Slam
    desc: "Melee Weapon Attack: +10 to hit, reach 20 ft. Hit: 20 (3d8 + 7) bludgeoning damage. If the target is a creature, it must succeed on a DC 17 Strength saving throw or be knocked prone."
  - name: "Crushing Coil (Recharge 5–6)"
    desc: "The ridgeback wraps its body around a vessel section or one creature within 20 feet. A targeted creature must succeed on a DC 17 Strength saving throw or take 35 (10d6) bludgeoning damage and be Restrained until the start of the ridgeback's next turn; on a success, half damage and not Restrained. A targeted vessel section takes 35 bludgeoning damage (70 as a siege monster)."
legendary_actions:
  - name: "Detect"
    desc: "The ridgeback makes a Wisdom (Perception) check."
  - name: "Thrash"
    desc: "One creature currently Grappled takes 14 (2d6 + 7) bludgeoning damage."
  - name: "Broach (Costs 2 Actions)"
    desc: "The ridgeback surges upward, arching its full body out of the water. Each creature within 20 feet must succeed on a DC 17 Dexterity saving throw or take 14 (4d6) bludgeoning damage and be knocked prone. The ridgeback can then move up to half its swim speed."
```

## Overview

The ridgeback is the second entity to follow the Pearl of Souls signal through the Maw fissure. Its type, behaviour, and origin are unknown to anyone in the Shattered Sea. [[auralis|Auralis]] knows something crossed. Beyond that, nothing is established above the waterline.

It does not ambush. It announces itself. The humps appear on the horizon, roll toward the ship, and close the distance at a pace that is neither slow nor panicked. There is time to make a decision before it arrives.

**Tribute mechanic:** If a creature aboard a targeted vessel throws an object of meaningful weight (weapons, tools, coinage) into the water, the ridgeback stops its approach for 1d4 rounds and reassesses (Wisdom DC 14). On a success it disengages. On a failure it resumes. A copper piece is not the same as a sword.

The *Pale Commission* made it back to [[kalowe|Kalowe]] with four survivors. The deckhand who survived by throwing everything loose into the water — boots, coins, a bronze fitting — still hasn't spoken publicly about it.

## Related

- [[leviathan|The Leviathan]]
- [[krakling|Krakling]]
- [[auralis|Auralis]]
- [[kalowe|Kalowe]]
