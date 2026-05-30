---

title: Ancient Bronze Dragon
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Ancient Bronze Dragon, a CR 22 dragon in the Shattered Sea bestiary.
tags:
- creature
- dragon
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: medium
aliases:
- Ancient Bronze Dragon
sources:
- XMM
- Homebrew
relationships:
- relation: listed_in
  target: Bestiary
- relation: guards
  target: The Shelfworks
- relation: watches
  target: The Drowned Maw
cha: 25
con: 27
cr: 22
creature_type: dragon
cssclasses:
- wiki-monster
dex: 10
environment: coastal
int: 18
page: 60
statblock: inline
str: 29
wis: 17
---

# Ancient Bronze Dragon

```statblock
layout: Basic 5e Layout
name: "Ancient Bronze Dragon"
size: Gargantuan
type: dragon
alignment: Lawful Good
ac: 22
hp: 444
hit_dice: 24d20 + 192
speed: "40 ft., Fly 80 ft., Swim 40 ft."
stats: [29, 10, 27, 18, 17, 25]
saves:
  - dexterity: 7
  - wisdom: 10
skillsaves:
  - insight: 10
  - perception: 17
  - stealth: 7
damage_immunities: "lightning"
senses: "Blindsight 60 ft., Darkvision 120 ft., Passive Perception 27"
languages: "Common, Draconic"
cr: "22"
traits:
  - name: "Amphibious"
    desc: "The dragon can breathe air and water."
  - name: "Legendary Resistance (4/Day, or 5/Day in Lair)"
    desc: "If the dragon fails a saving throw, it can choose to succeed instead."
actions:
  - name: "Multiattack"
    desc: "The dragon makes three Rend attacks. It can replace one attack with a use of (A) Repulsion Breath or (B) Spellcasting to cast Guiding Bolt|XPHB (level 2 version)."
  - name: "Rend"
    desc: "Melee Weapon Attack: +16 to hit, reach 15 ft. Hit: 18 (2d8 + 9) Slashing damage plus 9 (2d8) Lightning damage."
  - name: "Lightning Breath 5"
    desc: "dex 23, each creature in a 120-foot-long, 10-foot-wide Line [Area of Effect]|XPHB|Line. {@actSaveFail} 82 (15d10) Lightning damage. {@actSaveSuccess} Half damage."
  - name: "Repulsion Breath"
    desc: "str 23, each creature in a 30-foot Cone [Area of Effect]|XPHB|Cone. {@actSaveFail} The target is pushed up to 60 feet straight away from the dragon and has the Prone|XPHB condition."
legendary_actions:
  - name: "Guiding Light"
    desc: "The dragon uses Spellcasting to cast Guiding Bolt|XPHB (level 2 version)."
  - name: "Pounce"
    desc: "The dragon moves up to half its Speed|XPHB, and it makes one Rend attack."
  - name: "Thunderclap"
    desc: "con 22, each creature in a 20-foot-radius Sphere [Area of Effect]|XPHB|Sphere centered on a point the dragon can see within 120 feet. {@actSaveFail} 13 (3d8) Thunder damage, and the target has the Deafened|XPHB condition until the end of its next turn."
spells:
  - "The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save 22, +14 to hit, to hit with spell attacks):"
  - "At will: Detect Magic|XPHB, Guiding Bolt|XPHB (level 2 version), Shapechange|XPHB (Beast or Humanoid form only), Speak with Animals|XPHB, Thaumaturgy|XPHB"
  - "1e: Control Water|XPHB, Detect Thoughts|XPHB, Scrying|XPHB, Water Breathing|XPHB"
```

---

## In The Shattered Sea

The [[Shelfworks|Shelfworks]] have rules that every experienced salvager knows: do not dive tired, do not chase something below the agreed depth, do not work the edge alone. There is a less-discussed one that veteran crews hold without advertising: do not touch the sealed rooms on the lower northwest hall.

Nobody has posted a sign. Nobody has been told directly. The rule exists because three separate crews who broke it — across different seasons, without knowing about each other — all reported the same thing: a current that wasn't there before, cold water arriving from no clear source, and their lines going taut in a direction that had nothing to do with the drift. Two of the three surfaced without the pieces they went down for. The third surfaced without two of its divers. The current behavior in those incidents matches what the ancient's Control Water ability would produce if something very large and very deliberate decided a particular area was closed. ^[inferred]

The [[Drowned-Maw|Drowned Maw]] has been watched from above by the [[High-Eyrie|Sentinels of the High Eyrie]] for two centuries. Their records note, without editorial comment, that a Gargantuan creature matching no ordinary marine animal has been observed moving through the western shelf waters at irregular intervals since the records began. It does not attack vessels. It avoids the dive lines. It is present more often when the [[Tessarine-Concordat|Tessarine Concordat]] or [[Dravosi-Crown|Dravosi Crown]] increase extraction operations, and less often when they don't. The Sentinels have drawn no conclusions in their public records. The Sentinels are careful observers. ^[inferred]

An ancient bronze dragon old enough to have watched the Antheri ruins since before the current colonial era would have opinions about how they are being used. It is Lawful Good. It has not destroyed the Shelfworks. What it has done is establish, through current and cold water and the occasional very direct repositioning of a dive line, that there are parts of the ruins it considers outside the scope of the salvage gold rush. Whether the faction offices at the surface camp have quietly factored this into their site maps is not something either faction has chosen to document. ^[inferred]

## Related

- [[High-Eyrie]] — The High Eyrie
- [[Antheri-Ruins]] — Antheri Ruins
