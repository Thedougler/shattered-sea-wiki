---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: true
summary: "A Dravosi Crown support officer who turns shipboard supplies, medicinals, and weaponized compounds into tactical leverage."
created: 2026-04-19
updated: 2026-05-28
tags: [creature, humanoid, bestiary, dravosi, cr1]
sources: ["Inbox/Dravosi-Alchemist.md"]
confidence_level: medium
cr: 1
relationships:
  - "[[dravosi-crown|Dravosi Crown]] — faction"
---

# Dravosi Alchemist — Stat Block

A [[dravosi-crown|Dravosi Crown]] warrant officer responsible for shipboard stores, medicinals, and — when the situation calls for it — weaponised compounds. She does not consider herself a combatant. She considers herself a logistics officer who has correctly identified a threat to Crown property.

```statblock
layout: Basic 5e Layout
name: Dravosi Alchemist
size: Medium
type: humanoid
subtype: "human"
alignment: "lawful neutral"
ac: 13
hp: 22
hit_dice: "4d8 + 4"
speed: "30 ft."
stats: [9, 14, 12, 16, 12, 10]
saves:
  - intelligence: 5
skillsaves:
  - arcana: 5
  - medicine: 3
  - nature: 3
senses: "passive Perception 11"
languages: "Common"
cr: 1
source: "Homebrew"
traits:
  - name: Sea Legs
    desc: "Difficult terrain caused by ship movement, waves, or wet deck does not cost this creature extra movement."
  - name: Alchemical Bandolier
    desc: "The alchemist carries a bandolier of labelled compounds. Her throwable attacks draw from this stock; each is limited as noted. If she is killed or incapacitated, the bandolier and its remaining contents can be looted."
actions:
  - name: Dagger
    desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 4 (1d4 + 2) piercing damage."
  - name: "Poison Gas Canister (2/Day)"
    desc: "The alchemist hurls a sealed canister at a point within 30 ft. The canister shatters on impact and releases a toxic cloud in a 10-ft radius. Each creature in the area must succeed on a DC 13 Constitution saving throw or be poisoned until the start of the alchemist's next turn. The cloud persists until the start of the alchemist's next turn; any creature that ends its turn in the area must repeat the save."
  - name: "Incendiary Flask (2/Day)"
    desc: "The alchemist hurls a flask at a point within 30 ft. Each creature within 5 ft. of that point must succeed on a DC 13 Dexterity saving throw or take 7 (2d6) fire damage and catch fire. A burning creature takes 2 (1d4) fire damage at the start of each of its turns. A creature or an adjacent creature can use an action to extinguish the flames."
  - name: "Frag Canister (2/Day)"
    desc: "The alchemist hurls a canister at a point within 30 ft. The canister detonates on impact, spraying shrapnel in a 10-ft radius. Each creature in the area must succeed on a DC 13 Dexterity saving throw, taking 10 (3d6) piercing damage on a failed save or half as much on a successful one."
```

## Related

- [[dravosi-deckhand|Dravosi Deckhand]]
- [[dravosi-enforcer|Dravosi Enforcer]]
- [[barnaby-rook|Barnaby Rook]]
- [[dravosi-crown|Dravosi Crown]]
