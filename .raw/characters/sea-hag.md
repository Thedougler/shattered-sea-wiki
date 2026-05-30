---

title: Sea Hag
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Sea Hag, a CR 2 fey in the Shattered Sea bestiary.
tags:
- creature
- fey
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Sea Hag
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: hunts_in
  target: The Drowned Maw
cha: 13
con: 16
cr: 2
creature_type: fey
cssclasses:
- wiki-monster
dex: 13
environment: coastal, underwater
int: 12
page: 271
statblock: inline
str: 16
wis: 12
---

# Sea Hag

```statblock
layout: Basic 5e Layout
name: "Sea Hag"
size: Medium
type: fey
alignment: Chaotic Evil
ac: 14
hp: 52
hit_dice: 7d8 + 21
speed: "30 ft., Swim 40 ft."
stats: [16, 13, 16, 12, 12, 13]
senses: "Darkvision 60 ft., Passive Perception 11"
languages: "Common, Giant, Primordial (Aquan)"
cr: "2"
traits:
  - name: "Amphibious"
    desc: "The hag can breathe air and water."
  - name: "Vile Appearance"
    desc: "wis 11, any Beast or Humanoid that starts its turn within 30 feet of the hag and can see the hag's true form. {@actSaveFail} The target has the Frightened|XPHB condition until the start of its next turn. {@actSaveSuccess} The target is immune to this hag's Vile Appearance for 24 hours."
actions:
  - name: "Claw"
    desc: "Melee Weapon Attack: +5 to hit, reach 5 ft. Hit: 10 (2d6 + 3) Slashing damage."
  - name: "Death Glare 5"
    desc: "wis 11, one Frightened|XPHB creature the hag can see within 30 feet. {@actSaveFail} If the target has 20 Hit Points|XPHB or fewer, it drops to 0 Hit Points|XPHB. Otherwise, the target takes 13 (3d8) Psychic damage."
spells:
  - "While within 30 feet of at least two hag allies, the hag can cast one of the following spells, requiring no Material components, using the spell's normal casting time, and using Intelligence as the spellcasting ability (spell save 11): Augury|XPHB, Find Familiar|XPHB, Identify|XPHB, Locate Object|XPHB, Scrying|XPHB, or Unseen Servant|XPHB. The hag must finish a Long Rest|XPHB before using this trait to cast that spell again."
  - "The hag casts Disguise Self|XPHB, using Constitution as the spellcasting ability (spell save 13). The spell's duration is 24 hours."
  - "At will: Disguise Self|XPHB"
```

## Related

- [[Leviathan]] — The Leviathan
- [[Sawek]] — Sawek
- [[Whip-Shark]] — Whip Shark
