---
title: Black Pudding
type: monster
publish: false
created: 2026-04-25
updated: 2026-05-05
summary: CR 4 ooze that dissolves metal and wood on contact. Splits into smaller puddings when hit with slashing or lightning damage.
tags:
- creature
- ooze
campaign: shattered-sea
subtype: monster
confidence_level: high
sources: XMM
cha: 1
con: 16
cr: 4
creature_type: ooze
cssclasses:
- wiki-monster
dex: 5
environment: underdark
int: 1
page: 42
statblock: inline
str: 16
wis: 6
---

# Black Pudding

```statblock
layout: Basic 5e Layout
name: "Black Pudding"
size: Large
type: ooze
alignment: Unaligned
ac: 7
hp: 68
hit_dice: 8d10 + 24
speed: "20 ft., Climb 20 ft."
stats: [16, 5, 16, 1, 6, 1]
damage_immunities: "acid, cold, lightning, slashing"
condition_immunities: "charmed, deafened, exhaustion, frightened, grappled, prone, restrained"
senses: "Blindsight 60 ft., Passive Perception 8"
languages: "—"
cr: "4"
traits:
  - name: "Amorphous"
    desc: "The pudding can move through a space as narrow as 1 inch without expending extra movement to do so."
  - name: "Corrosive Form"
    desc: "A creature that hits the pudding with a melee attack roll takes 4 (1d8) Acid damage. Nonmagical ammunition is destroyed immediately after hitting the pudding and dealing any damage. Any nonmagical weapon takes a cumulative -1 penalty to attack rolls immediately after dealing damage to the pudding and coming into contact with it. The weapon is destroyed if the penalty reaches -5. The penalty can be removed by casting the Mending|XPHB spell on the weapon. In 1 minute, the pudding can eat through 2 feet of nonmagical wood or metal."
  - name: "Spider Climb"
    desc: "The pudding can climb difficult surfaces, including along ceilings, without needing to make an ability check."
actions:
  - name: "Dissolving Pseudopod"
    desc: "Melee Weapon Attack: +5 to hit, reach 10 ft. Hit: 17 (4d6 + 3) Acid damage. Nonmagical armor worn by the target takes a -1 penalty to the AC it offers. The armor is destroyed if the penalty reduces its AC to 10. The penalty can be removed by casting the Mending|XPHB spell on the armor."
reactions:
  - name: "Split"
    desc: "{@actTrigger} While the pudding is Large or Medium and has 10+ Hit Points|XPHB, it becomes Bloodied|XPHB or is subjected to Lightning or Slashing damage. {@actResponse} The pudding splits into two new Black Puddings. Each new pudding is one size smaller than the original pudding and acts on its Initiative|XPHB. The original pudding's Hit Points|XPHB are divided evenly between the new puddings (round down)."
```