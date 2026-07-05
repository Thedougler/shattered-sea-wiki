---
type: monster
subtype: monster
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: CR 6 grung lieutenant. Fearless alchemist-brawler soused on his own reagent-spirits; hurls acid/poison flasks, teleports through reeking steps, and can invoke a self-buff rite (Shed the Years) that sheds decades and turns his lash magical. Prepped for the back half of the Calveno sewer magazine dungeon.
created: 2026-07-01
updated: 2026-07-01
tags:
  - grung
  - combat
sources:
  - Inbox/Bazzoth-Statblock.md
confidence_level: high
aliases:
  - Bazzoth
  - The Steeped
cr: 6
creature_type: humanoid
environment: sewer, urban
statblock: inline
---

# Bazzoth, the Steeped

```statblock
layout: Basic 5e Layout
name: Bazzoth, the Steeped
size: Small
type: humanoid
subtype: grung
campaign: shattered-sea
alignment: lawful evil
ac: 15
ac_class: bone-plate apron and bench-harness
hp: 132
hit_dice: 24d6 + 48
speed: "25 ft., climb 25 ft., swim 25 ft."
stats: [9, 14, 15, 18, 12, 15]
saves:
  - constitution: 5
  - intelligence: 7
skillsaves:
  - arcana: 7
  - medicine: 7
  - nature: 7
  - insight: 4
damage_immunities: "poison"
condition_immunities: "poisoned"
senses: "passive Perception 14"
languages: "Grung, Common"
cr: 6
traits:
  - name: Steeped
    desc: "Bazzoth is soused on the same reagent-spirits he distils, and it has pickled fear and doubt out of him. He has advantage on saving throws against being charmed or frightened, and on Constitution saving throws made to maintain concentration. A creature relying on scent to track or read him works at a disadvantage."
  - name: Toxic Secretion
    desc: "A creature that touches Bazzoth or hits him with a melee attack while within 5 feet, or that grapples him, must succeed on a DC 13 Constitution saving throw or take 5 (2d4) poison damage and be poisoned until the start of its next turn."
  - name: Standing Leap
    desc: "Bazzoth's long jump is 25 feet and his high jump is 15 feet, with or without a running start. He rarely bothers — until the rite is on him (see Shed the Years)."
  - name: Master of the Bench
    desc: "Bazzoth is never surprised while conscious, and is immune to the effects of his own concoctions. A creature that is poisoned has disadvantage on saving throws against his concoctions until the end of its next turn."
  - name: "Legendary Resistance (1/Day)"
    desc: "If Bazzoth fails a saving throw, he can choose to succeed instead. The old vintage does not go over on the first push — and the rite does not break on the first good hit."
actions:
  - name: Multiattack
    desc: "Bazzoth makes two attacks, using Hurled Flask or Envenomed Lash in any combination. While Shed the Years is active, he makes one additional Envenomed Lash attack."
  - name: Hurled Flask
    desc: "Ranged Weapon Attack: +6 to hit, range 30/90 ft., one target. Hit: 11 (2d8 + 2) acid or poison damage (his choice each throw), and the target has disadvantage on the next saving throw it makes against one of Bazzoth's concoctions before the end of Bazzoth's next turn."
  - name: Envenomed Lash
    desc: "Melee Weapon Attack: +6 to hit, reach 10 ft., one target. Hit: 9 (2d6 + 2) poison damage, and the target must succeed on a DC 15 Constitution saving throw or be poisoned until the end of its next turn. While Shed the Years is active, this attack is magical, is made at +8 to hit, and deals an extra 5 (1d10) force damage."
  - name: "Sump-Reek Bomb (Recharge 5–6)"
    desc: "Bazzoth hurls a sealed bone flask that bursts into a 20-foot-radius cloud centred on a point he can see within 60 feet. Each creature in that area makes a DC 15 Constitution saving throw, taking 21 (6d6) poison damage on a failure, or half as much on a success. A creature that fails is also poisoned and repeats the save at the end of each of its turns, ending the effect on a success. The cloud lingers and heavily obscures its area until the start of Bazzoth's next turn; a creature that enters it for the first time on a turn, or starts its turn there, is subjected to the save."
bonus_actions:
  - name: Clinging Ichor
    desc: "Bazzoth lobs a flask of sump-glue at a point he can see within 30 feet, coating a 10-foot-radius area that is difficult terrain until the start of his next turn. A creature in the area when it lands, or that enters it for the first time on a turn, must succeed on a DC 15 Strength saving throw or have its speed reduced to 0 until the end of its next turn. He cannot use this the same turn he invokes Shed the Years."
  - name: "Shed the Years"
    desc: "Bazzoth swigs from his gourd and speaks a red-caste rite over his own body, and decades unspool from it. He concentrates to maintain the rite (as if concentrating on a spell); it lasts up to 1 minute. While active: his walking speed increases by 15 feet and his movement no longer provokes opportunity attacks; he gains a +2 bonus to AC and has advantage on Dexterity saving throws; his melee attacks become magical, more accurate, and harder-hitting (see Envenomed Lash); and his Multiattack includes one additional Envenomed Lash. If his concentration is broken, the rite ends."
reactions:
  - name: "Reeking Step (3/Day)"
    desc: "When Bazzoth takes damage, or a creature ends its turn within 5 feet of him, he speaks a short rite and steps through a puff of stinging reek, teleporting to an unoccupied space he can see within 30 feet. This movement does not provoke opportunity attacks."
```

## Notes

**Appearance:** an old red-caste grung — thick and heavyset, brick-red hide dulled and mottled with age, sagging wattled throat; bone-plate apron over a bench-harness of reagent vials, an ever-present drinking gourd.

Guards **Room 5 (Magazine Beta)** in the [[wiki/sessions/calveno-sewers-grung-magazines|Calveno sewer magazine dungeon]], alongside 2 Grung laborers (assigned 2026-07-01 — party had reached Room 6/Ruma and neutralized Room 4/Magazine Alpha). This escalates Room 5 well past its original "Hard" rating (~4,800 adj. XP) — verify against current party resources before running.

Shed the Years is a concentration self-buff — breaking his concentration (any damage, DC 15+ half-damage Con save at the poisoned-disadvantage penalty) strips the extra attack, magical damage, and mobility. Reeking Step (3/day) makes him hard to pin in melee; Sump-Reek Bomb is his AoE anchor at Recharge 5-6.

## Related

- [[vashu-the-weeping-veil|Vashu, the Weeping Veil]]
- [[ozvok-the-vermillion-distiller|Ozvok, the Vermillion Distiller]]
- [[ozzeth-the-twiceborn|Ozzeth, the Twiceborn]]
- [[grung-elite-warrior|Grung Elite Warrior]]
- [[grung-clans|Grung Clans (Faction)]]
- [[wiki/sessions/calveno-sewers-grung-magazines|Calveno Sewer Magazines]]
- [[simone-tabarnack|Simone Tabarnack]]
