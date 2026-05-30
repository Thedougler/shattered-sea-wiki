---

title: Swarm of Ravens
type: monster
publish: true
created: '2026-04-25'
updated: '2026-05-03'
summary: Public statblock reference for Swarm of Ravens, a CR 1/4 beast in the Shattered
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
- Swarm of Ravens
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: habitat
  target: Vel-Orn — Sunken Crown
- relation: habitat
  target: Ral-Arn
cha: 6
con: 12
cr: 1/4
creature_type: beast
cssclasses:
- wiki-monster
dex: 14
environment: hill, swamp, urban
int: 5
page: 371
statblock: inline
str: 6
wis: 12
---

# Swarm of Ravens

```statblock
layout: Basic 5e Layout
name: "Swarm of Ravens"
size: Medium
type: beast
alignment: Unaligned
ac: 12
hp: 11
hit_dice: 2d8 + 2
speed: "10 ft., Fly 50 ft."
stats: [6, 14, 12, 5, 12, 6]
skillsaves:
  - perception: 5
damage_resistances: "bludgeoning, piercing, slashing"
condition_immunities: "charmed, frightened, grappled, paralyzed, petrified, prone, restrained, stunned"
senses: "Passive Perception 15"
languages: "—"
cr: "1/4"
traits:
  - name: "Swarm"
    desc: "The swarm can occupy another creature's space and vice versa, and the swarm can move through any opening large enough for a Tiny raven. The swarm can't regain Hit Points|XPHB or gain Temporary Hit Points|XPHB."
actions:
  - name: "Beaks"
    desc: "Melee Weapon Attack: +4 to hit, reach 5 ft. Hit: 5 (1d6 + 2) Piercing damage, or 2 (1d4) Piercing damage if the swarm is Bloodied|XPHB."
  - name: "Cacophony"
    desc: "wis 10, one creature in the swarm's space. {@actSaveFail} The target has the Deafened|XPHB condition until the start of the swarm's next turn. While Deafened|XPHB, the target also has Disadvantage|XPHB on ability checks and attack rolls."
```

## Related

- [[giant-constrictor-snake]] — Giant Constrictor Snake
- [[giant-axe-beak]] — Giant Axe Beak

## Sources

- [[raw/swarm-of-ravens|Swarm of Ravens — stat block]]
