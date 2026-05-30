---

title: Giant Octopus
type: monster
publish: true
created: '2026-04-25'
updated: '2026-05-03'
summary: Public statblock reference for Giant Octopus, a CR 1 beast in the Shattered
  Sea bestiary.
tags:
- creature
- beast
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Giant Octopus
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: hunts_in
  target: The Central Strait
- relation: hunts_in
  target: The Sunken Crown
cha: 4
con: 13
cr: 1
creature_type: beast
cssclasses:
- wiki-monster
dex: 13
environment: underwater
int: 5
page: 358
statblock: inline
str: 17
wis: 10
---

# Giant Octopus

```statblock
layout: Basic 5e Layout
name: "Giant Octopus"
size: Large
type: beast
alignment: Unaligned
ac: 11
hp: 45
hit_dice: 7d10 + 7
speed: "10 ft., Swim 60 ft."
stats: [17, 13, 13, 5, 10, 4]
skillsaves:
  - perception: 4
  - stealth: 5
senses: "Darkvision 60 ft., Passive Perception 14"
languages: "—"
cr: "1"
traits:
  - name: "Water Breathing"
    desc: "The octopus can breathe only underwater. It can hold its breath for 1 hour outside water."
actions:
  - name: "Tentacles"
    desc: "Melee Weapon Attack: +5 to hit, reach 10 ft. Hit: 10 (2d6 + 3) Bludgeoning damage. If the target is a Medium or smaller creature, it has the Grappled|XPHB condition (escape 13) from all eight tentacles. While Grappled|XPHB, the target has the Restrained|XPHB condition."
reactions:
  - name: "Ink Cloud (1/Day)"
    desc: "{@actTrigger} The octopus takes damage while underwater. {@actResponse} The octopus releases ink that fills a 10-foot Cube [Area of Effect]|XPHB|Cube centered on itself, and the octopus moves up to its Swim Speed|XPHB. The Cube [Area of Effect]|XPHB|Cube is Heavily Obscured|XPHB for 1 minute or until a strong current or similar effect disperses the ink."
```

## Related

- [[giant-constrictor-snake]] — Giant Constrictor Snake
- [[giant-axe-beak]] — Giant Axe Beak
