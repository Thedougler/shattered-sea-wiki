---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 9 undead. Not a lich — an undead born from slain humanoids that pursues its prey indefinitely across planes by draining their sleep and vitality."
created: 2026-05-15
updated: 2026-05-28
tags: [creature, undead, bestiary, cr9]
sources: ["Inbox/Restless.md"]
confidence_level: high
cr: 9
aliases: ["Restless"]
---

# Restless

```statblock
layout: Basic 5e Layout
name: "Restless"
size: Large
type: undead
alignment: Typically Chaotic Neutral
ac: 17
hp: 104
hit_dice: 16d10
speed: "30 ft."
stats: [14, 20, 10, 17, 16, 11]
saves:
  - intelligence: 9
  - wisdom: 7
skillsaves:
  - investigation: 7
  - perception: 7
  - survival: 7
damage_resistances: "Cold, Necrotic"
condition_immunities: "Charmed, Exhaustion, Frightened, Paralyzed, Poisoned"
senses: "Darkvision 120 ft., Passive Perception 17"
languages: "The languages it knew in life"
cr: "9"
traits:
  - name: "Restless"
    desc: "Cannot be magically put to sleep."
  - name: "Tired Pursuer"
    desc: "Can teleport to any location where a creature it has Siphoned has rested within the last 24 hours."
  - name: "No Rest for the Weary"
    desc: "If a humanoid dies from Consume Vitality or Siphon, there is a 1-in-4 chance it rises as a new Restless in 1d4 hours."
  - name: "Dream Stealer"
    desc: "Can see and use abilities against Material Plane creatures from the Ethereal Plane. Returns to the Material Plane when it makes an attack or uses an ability."
actions:
  - name: "Multiattack"
    desc: "Two Claw attacks, or one Claw plus one ability (Consume Vitality or Siphon)."
  - name: "Claw"
    desc: "Melee Weapon Attack: +9 to hit, reach 5 ft. Hit: 14 (2d8+5) slashing damage. Target must succeed on a DC 14 Dexterity saving throw or be grappled."
  - name: "Consume Vitality"
    desc: "Target within 5 feet makes a DC 16 Constitution saving throw. On a failure, the target's Constitution score is reduced by 1d4 until a short or long rest. A creature whose Constitution reaches 0 dies."
  - name: "Siphon"
    desc: "Target grappled by the Restless makes a DC 16 Constitution saving throw. On a failure, the target gains 1 level of exhaustion and the Restless has advantage on its next attack roll."
  - name: "Ethereal Jump"
    desc: "Vanish into the Ethereal Plane until the start of its next turn."
```

## Lore

Not a traditional lich — the Restless is an undead born from slain humanoids, a parasitic presence that haunts its chosen targets across planes. It feeds on sleep deprivation and drained vitality, teleporting to wherever its marked victims last rested. A target the Restless has Siphoned is permanently marked; there is no safe distance, only a safe moment.

The most dangerous feature is propagation: victims who die from its drain may rise as new Restless, spreading the haunting.

*Source: Pointy Hat*
