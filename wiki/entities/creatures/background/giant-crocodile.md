---
type: entity
subtype: monster
campaign: shattered-sea
status: unknown
audience: players
publish: true
summary: The Giant Crocodile, a CR 5 beast in the Shattered Sea bestiary.
created: 2026-04-25
updated: 2026-06-04
tags:
  - combat
sources:
  - XMM
confidence_level: high
aliases:
  - Giant Crocodile
cha: 7
con: 17
cr: 5
creature_type: beast
dex: 9
environment: coastal, swamp
int: 2
page: 356
statblock: inline
str: 21
wis: 10
---

# Giant Crocodile

Midchain pilots treat giant crocodiles as a channel problem, not an open-water one. These are saltwater animals, and the Scatter's warm coastal passages suit them well — they cross open reef where they need to and are not uncommon in brackish cuts where the mangrove fringe meets the sea. They prefer the shadow side of mangrove channels, the silted margins of tidal flats, and anywhere the water sits too shallow for a keel but deep enough to hide a Huge body. They hold still long enough that sailors learn to distrust stillness in those places — a floating log, a shadow that doesn't move with the current, a patch of surface disturbed by nothing visible.

The [[dreth|Dreth]]–[[orak|Orak]] channel has the most consistent reports. A [[kalowe|Kalowe]] pilot named Tessavane came back from a supply run to the eastern Teeth missing two fingers and describing a crocodile that took her skiff's port rail, held it, and dragged backward until the hull folded. She made the bank by leaving the boat behind. Most survivors make similar trades. ^[inferred]

```statblock
layout: Basic 5e Layout
name: "Giant Crocodile"
size: Huge
type: beast
alignment: Unaligned
ac: 14
hp: 85
hit_dice: 9d12 + 27
speed: "30 ft., Swim 50 ft."
stats: [21, 9, 17, 2, 10, 7]
skillsaves:
  - stealth: 5
senses: "Passive Perception 10"
languages: "—"
cr: "5"
traits:
  - name: "Hold Breath"
    desc: "The crocodile can hold its breath for 1 hour."
actions:
  - name: "Multiattack"
    desc: "The crocodile makes one Bite attack and one Tail attack."
  - name: "Bite"
    desc: "Melee Weapon Attack: +8 to hit, reach 5 ft. Hit: 21 (3d10 + 5) Piercing damage. If the target is a Large or smaller creature, it has the Grappled|XPHB condition (escape 15). While Grappled|XPHB, the target has the Restrained|XPHB condition and can't be targeted by the crocodile's Tail."
  - name: "Tail"
    desc: "Melee Weapon Attack: +8 to hit, reach 10 ft. Hit: 18 (3d8 + 5) Bludgeoning damage. If the target is a Large or smaller creature, it has the Prone|XPHB condition."
```

## Related

- [[midchain|The Midchain]]
- [[shattered-sea|The Shattered Sea]]
- [[verdant-scatter|Verdant Scatter]]
- [[kalowe|Kalowe]]
- [[giant-constrictor-snake|Giant Constrictor Snake]]
- [[giant-axe-beak|Giant Axe Beak]]
