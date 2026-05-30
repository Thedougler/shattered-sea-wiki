---
title: Ochre Jelly
type: monster
publish: false
created: 2026-04-25
updated: 2026-05-05
summary: CR 2 ooze that deals acid damage and splits when struck by lightning or slashing weapons.
tags:
- creature
- ooze
campaign: shattered-sea
subtype: monster
confidence_level: high
sources: XMM
cha: 1
con: 14
cr: 2
creature_type: ooze
cssclasses:
- wiki-monster
dex: 6
environment: underdark
int: 2
page: 230
statblock: inline
str: 15
wis: 6
---

# Ochre Jelly

```statblock
layout: Basic 5e Layout
name: "Ochre Jelly"
size: Large
type: ooze
alignment: Unaligned
ac: 8
hp: 52
hit_dice: 7d10 + 14
speed: "20 ft., Climb 20 ft."
stats: [15, 6, 14, 2, 6, 1]
damage_resistances: "acid"
damage_immunities: "lightning, slashing"
condition_immunities: "charmed, deafened, exhaustion, frightened, grappled, prone, restrained"
senses: "Blindsight 60 ft., Passive Perception 8"
languages: "—"
cr: "2"
traits:
  - name: "Amorphous"
    desc: "The jelly can move through a space as narrow as 1 inch without expending extra movement to do so."
  - name: "Spider Climb"
    desc: "The jelly can climb difficult surfaces, including along ceilings, without needing to make an ability check."
actions:
  - name: "Pseudopod"
    desc: "Melee Weapon Attack: +4 to hit, reach 5 ft. Hit: 12 (3d6 + 2) Acid damage."
reactions:
  - name: "Split"
    desc: "{@actTrigger} While the jelly is Large or Medium and has 10+ Hit Points|XPHB, it becomes Bloodied|XPHB or is subjected to Lightning or Slashing damage. {@actResponse} The jelly splits into two new Ochre Jellies. Each new jelly is one size smaller than the original jelly and acts on its Initiative|XPHB. The original jelly's Hit Points|XPHB are divided evenly between the new jellies (round down)."
```