---

title: Kraken
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Kraken, a CR 23 monstrosity in the Shattered Sea bestiary.
tags:
- creature
- monstrosity
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Kraken
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: hunts_in
  target: The Drowned Maw
- relation: hunts_in
  target: The Outer Reach
cha: 20
con: 26
cr: 23
creature_type: monstrosity
cssclasses:
- wiki-monster
dex: 11
environment: underwater
int: 22
page: 187
statblock: inline
str: 30
wis: 18
---

# Kraken

```statblock
layout: Basic 5e Layout
name: "Kraken"
size: Gargantuan
type: monstrosity
alignment: Chaotic Evil
ac: 18
hp: 481
hit_dice: 26d20 + 208
speed: "30 ft., Swim 120 ft."
stats: [30, 11, 26, 22, 18, 20]
saves:
  - strength: 17
  - dexterity: 7
  - constitution: 15
  - wisdom: 11
skillsaves:
  - history: 13
  - perception: 11
damage_immunities: "cold, lightning"
condition_immunities: "frightened, grappled, paralyzed, restrained"
senses: "Truesight 120 ft., Passive Perception 21"
languages: "understands Abyssal, Celestial, Infernal, and Primordial but can't speak; telepathy 120 ft."
cr: "23"
traits:
  - name: "Amphibious"
    desc: "The kraken can breathe air and water."
  - name: "Legendary Resistance (4/Day, or 5/Day in Lair)"
    desc: "If the kraken fails a saving throw, it can choose to succeed instead."
  - name: "Siege Monster"
    desc: "The kraken deals double damage to objects and structures."
actions:
  - name: "Multiattack"
    desc: "The kraken makes two Tentacle attacks and uses Fling, Lightning Strike, or Swallow."
  - name: "Tentacle"
    desc: "Melee Weapon Attack: +17 to hit, reach 30 ft. Hit: 24 (4d6 + 10) Bludgeoning damage. The target has the Grappled|XPHB condition (escape 20) from one of ten tentacles, and it has the Restrained|XPHB condition until the grapple ends."
  - name: "Fling"
    desc: "The kraken throws a Large or smaller creature Grappled|XPHB by it to a space it can see within 60 feet of itself that isn't in the air. dex 25, the creature thrown and each creature in the destination space. {@actSaveFail} 18 (4d8) Bludgeoning damage, and the target has the Prone|XPHB condition. {@actSaveSuccess} Half damage only."
  - name: "Lightning Strike"
    desc: "dex 23, one creature the kraken can see within 120 feet. {@actSaveFail} 33 (6d10) Lightning damage. {@actSaveSuccess} Half damage."
  - name: "Swallow"
    desc: "dex 25, one creature Grappled|XPHB by the kraken (it can have up to four creatures swallowed at a time). {@actSaveFail} 23 (3d8 + 10) Piercing damage. If the target is Large or smaller, it is swallowed and no longer Grappled|XPHB. A swallowed creature has the Restrained|XPHB condition, has Cover|XPHB|Total Cover against attacks and other effects outside the kraken, and takes 24 (7d6) Acid damage at the start of each of its turns. If the kraken takes 50 damage or more on a single turn from a creature inside it, the kraken must succeed on a 25 Constitution saving throw at the end of that turn or regurgitate all swallowed creatures, each of which falls in a space within 10 feet of the kraken with the Prone|XPHB condition. If the kraken dies, any swallowed creature no longer has the Restrained|XPHB condition and can escape from the corpse using 15 feet of movement, exiting Prone|XPHB."
legendary_actions:
  - name: "Storm Bolt"
    desc: "The kraken uses Lightning Strike."
  - name: "Toxic Ink"
    desc: "con 23, each creature in a 15-foot Emanation [Area of Effect]|XPHB|Emanation originating from the kraken while it is underwater. {@actSaveFail} The target has the Blinded|XPHB and Poisoned|XPHB conditions until the end of the kraken's next turn. The kraken then moves up to its Speed|XPHB. {@actSaveSuccessOrFail} The kraken can't take this action again until the start of its next turn."
```

## Related

- [[Leviathan]] — The Leviathan
- [[Sawek]] — Sawek
- [[Whip-Shark]] — Whip Shark
