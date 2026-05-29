---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: players
publish: true
summary: "CR 5 monstrosity. Shark head, octopus rear — ambush predator in blue holes. Kalowe divers call it the Blue Devil. Grapples two targets simultaneously, drags them into its lair."
created: 2026-04-12
updated: 2026-05-28
tags: [creature, monstrosity, aquatic, lair, bestiary, cr5]
sources: ["Inbox/Sawek.md"]
cr: 5
confidence_level: medium
aliases: ["Sawek", "Blue Devil"]
relationships:
  - "[[midchain|The Midchain]] — primary habitat"
  - "[[kalowe|Kalowe]] — Kalowe divers mark claimed holes with cord"
---

# Sawek (Blue Devil)

![[Sawek.webp|Sawek lurking underwater, with a shark-like head and octopus tentacles emerging from a rocky blue hole]]

```statblock
layout: Basic 5e Layout
name: Sawek
size: Huge
type: monstrosity
alignment: unaligned
ac: 14
ac_class: natural armour
hp: 95
hit_dice: 9d12 + 36
speed: "5 ft., swim 40 ft."
stats: [20, 16, 18, 6, 14, 4]
saves:
  - strength: 8
  - constitution: 7
skillsaves:
  - perception: 5
  - stealth: 6
senses: "blindsight 60 ft. (underwater only), darkvision 120 ft., passive Perception 15"
languages: "—"
cr: 5
traits:
  - name: Keen Smell
    desc: "The Sawek has advantage on Wisdom (Perception) checks that rely on smell."
  - name: Patient Hunter
    desc: "While stationary in its lair, the Sawek makes no sound and requires no Stealth check. A creature looking directly into the lair entrance must succeed on a DC 18 Wisdom (Perception) check to detect movement in the dark below."
  - name: Water Breathing
    desc: "The Sawek can breathe only underwater."
actions:
  - name: Multiattack
    desc: "The Sawek makes one Bite attack and two Tentacle attacks."
  - name: Bite
    desc: "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 18 (3d8 + 5) piercing damage. The Sawek has advantage on this attack roll if the target is Grappled."
  - name: Tentacle
    desc: "Melee Weapon Attack: +8 to hit, reach 20 ft., one target. Hit: 12 (2d6 + 5) bludgeoning damage. The target is Grappled (escape DC 16) and Restrained until the grapple ends. The Sawek can maintain up to two grapples simultaneously."
  - name: "Crush (Recharge 5-6)"
    desc: "One Grappled creature takes 28 (4d12) bludgeoning damage and must succeed on a DC 16 Constitution saving throw or be Incapacitated until the end of its next turn."
bonus_actions:
  - name: Drag Under
    desc: "The Sawek moves one Grappled creature up to 30 feet directly toward the lair entrance. If this carries the creature into the blue hole, the creature enters the lair: total darkness, fully submerged."
```

## Lore

[[kalowe|Kalowe]]'s reef divers call it the sawek. Colonial sailors call it the blue devil, after its preference for the caves that line blue holes as its lair.

The front half is shark: broad, muscle-dense, jaws wide enough to take a man at the shoulder, skin a deep blue-grey that reads as black in dim water. The rear half is octopus: eight tentacles, each up to twenty feet long at full extension. It fits inside a cave entrance that looks too small to hold anything of note.

It is an ambush predator — the tentacles emerge from the entrance and grab whatever is within range. The shark half takes over once prey is in reach. [[kalowe|Kalowe]] divers mark claimed holes with a length of cord tied to a reef stake.

## Connections

- [[kalowe|Kalowe]]
- [[whip-shark|Whip Shark]]
- [[midchain|The Midchain]]
