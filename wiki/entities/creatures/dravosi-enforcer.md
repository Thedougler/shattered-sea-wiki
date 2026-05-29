---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: true
summary: "A Dravosi Crown veteran built for confined boarding fights, crowd suppression, hooks, gangplanks, and procedural violence."
created: 2026-04-19
updated: 2026-05-28
tags: [creature, humanoid, bestiary, dravosi, cr1/2]
sources: ["Inbox/Dravosi-Enforcer.md"]
cr: "1/2"
confidence_level: medium
relationships:
  - "[[dravosi-crown|Dravosi Crown]] — faction"
---

# Dravosi Enforcer — Stat Block

[[dravosi-crown|Dravosi Crown]] veterans assigned to boarding actions and crowd suppression. Built for confined-space fighting — they know how to use a hook to pull someone off their feet, and they know how to use a gangplank as a kill zone.

```statblock
layout: Basic 5e Layout
name: Dravosi Enforcer
size: Medium
type: humanoid
subtype: "human"
alignment: "lawful neutral"
ac: 12
hp: 32
hit_dice: "5d8 + 10"
speed: "30 ft."
stats: [15, 11, 14, 10, 10, 11]
skillsaves:
  - athletics: 4
  - intimidation: 2
senses: "passive Perception 10"
languages: "Common"
cr: "1/2"
source: "Homebrew"
traits:
  - name: Sea Legs
    desc: "Difficult terrain caused by ship movement, waves, or wet deck does not cost this creature extra movement."
  - name: Pack Tactics
    desc: "The enforcer has advantage on attack rolls against a creature if at least one of the enforcer's allies is within 5 ft. of the creature and the ally isn't incapacitated."
actions:
  - name: Multiattack
    desc: "The enforcer makes two Cutlass attacks, or one Cutlass attack and one Boarding Hook attack."
  - name: Cutlass
    desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 9 (1d10 + 4) slashing damage."
  - name: Boarding Hook
    desc: "Melee Weapon Attack: +4 to hit, reach 10 ft., one target. Hit: 5 (1d6 + 2) piercing damage. On a hit, the target must succeed on a DC 12 Strength saving throw or be pulled up to 5 feet toward the enforcer and knocked prone."
```

## Related

- [[dravosi-deckhand|Dravosi Deckhand]]
- [[dravosi-crown|Dravosi Crown]]
