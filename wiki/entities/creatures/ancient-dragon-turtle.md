---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: players
publish: true
summary: "CR 24 dragon (mythic). Gargantuan amphibious; Blessing of the Sea resets to 350 HP and activates mythic actions. Hunts the Drowned Maw and Outer Reach."
created: 2026-04-25
updated: 2026-05-28
tags: [creature, dragon, bestiary, cr24, mythic]
sources: ["Inbox/ancient-dragon-turtle.md"]
cr: 24
confidence_level: medium
relationships:
  - "[[the-drowned-maw|The Drowned Maw]] — hunting ground"
  - "[[perrin-black-jaw|Perrin Black-Jaw]] — connection; survived the Vestra disaster near the Maw"
---

# Ancient Dragon Turtle

```statblock
layout: Basic 5e Layout
name: "Ancient Dragon Turtle"
size: Gargantuan
type: dragon
alignment: Neutral
ac: 22
hp: 409
hit_dice: 21d20 + 189
speed: "30 ft., Swim 60 ft."
stats: [28, 12, 29, 14, 19, 15]
saves:
  - dexterity: 8
  - constitution: 16
  - wisdom: 11
skillsaves:
  - perception: 11
damage_immunities: "cold, fire"
condition_immunities: "charmed, frightened, poisoned"
senses: "truesight 120 ft., Passive Perception 21"
languages: "Aquan, Draconic"
cr: "24"
traits:
  - name: "Amphibious"
    desc: "The dragon turtle can breathe air and water."
  - name: "Blessing of the Sea (Recharges after a Short or Long Rest)"
    desc: "If the dragon turtle would be reduced to 0 hit points, its current hit point total instead resets to 350 hit points, and it recharges its Steam Breath. Additionally, the dragon turtle can now use Mythic Actions for 1 hour."
  - name: "Legendary Resistance (3/Day)"
    desc: "If the dragon turtle fails a saving throw, it can choose to succeed instead."
actions:
  - name: "Multiattack"
    desc: "The dragon turtle makes one Bite or Tail attack and two Claw attacks."
  - name: "Bite"
    desc: "Melee Weapon Attack: +16 to hit, reach 15 ft. Hit: 15 (1d12 + 9) piercing damage plus 13 (2d12) lightning damage."
  - name: "Claw"
    desc: "Melee Weapon Attack: +16 to hit, reach 15 ft. Hit: 18 (2d8 + 9) slashing damage."
  - name: "Tail"
    desc: "Melee Weapon Attack: +16 to hit, reach 15 ft. Hit: 20 (2d10 + 9) bludgeoning damage. If the target is a creature, it must succeed on a DC 24 Strength saving throw or be knocked prone."
  - name: "Steam Breath (Recharge 5–6)"
    desc: "DC 24 Constitution save, 90-foot Cone. Failure: 67 (15d8) fire damage. Success: half. Being underwater doesn't grant resistance to this damage."
legendary_actions:
  - name: "Attack"
    desc: "The dragon turtle makes one Claw or Tail attack."
  - name: "Move"
    desc: "The dragon turtle moves up to its speed. If swimming, this movement doesn't provoke opportunity attacks."
  - name: "Boiling Aura (Costs 3 Actions)"
    desc: "Until the start of the dragon turtle's next turn, creatures that start their turn within 20 feet must succeed on a DC 24 Constitution saving throw or take 40 (9d8) fire damage."
```

## In The Shattered Sea

Ancient dragon turtles belong in the parts of the Sea where the chart stops being useful: the [[the-drowned-maw|Drowned Maw]], the open water beyond it, and the deep indigo edge around the Keth-Naar Blue Hole. Sailors do not usually identify them cleanly. They report heat first: warm brine, softened pitch, fog lying low on water that had been still a moment before.

The most useful public account is indirect. [[perrin-black-jaw|Perrin Black-Jaw]] survived the destruction of the *Vestra* near the Maw and later washed ashore at Keth-Naar. His account describes boiling water, a burned rail, and a deliberate strike from below. That evidence is not enough to prove an ancient dragon turtle rather than the older [[leviathan|Leviathan]] rumor — but it is enough that experienced sailors now treat the Maw-to-Sunken-Crown run as dragon-turtle water.

## Related

- [[dragon-turtle|Dragon Turtle]]
- [[young-dragon-turtle|Young Dragon Turtle]]
- [[dragon-turtle-wyrmling|Dragon Turtle Wyrmling]]
- [[perrin-black-jaw|Perrin Black-Jaw]]
