---
type: monster
subtype: monster
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 2 humanoid; blue-caste handlers and purple-caste warriors. Multiattack, poison, Mesmerizing Chirr stun. The operational backbone of Simone's raid infrastructure."
created: 2026-06-01
updated: 2026-06-02
tags:
  - grung
  - combat
sources:
  - VGM
confidence_level: high
aliases:
  - Grung Elite Warrior
  - Blue-Caste Handler
  - Purple-Caste Warrior
cha: 12
con: 15
cr: 2
creature_type: humanoid
dex: 16
environment: forest, swamp, urban
int: 10
page: 157
statblock: inline
str: 7
wis: 11
---

# Grung Elite Warrior

```statblock
layout: Basic 5e Layout
name: "Grung Elite Warrior"
size: Small
type: humanoid
subtype: grung
alignment: Typically Lawful Evil
ac: 13
ac_note: natural armor
hp: 49
hit_dice: 9d6 + 18
speed: "25 ft., Climb 25 ft."
stats: [7, 16, 15, 10, 11, 12]
saves:
  - dexterity: 5
skillsaves:
  - athletics: 2
  - perception: 2
  - stealth: 5
  - survival: 2
damage_immunities: "poison"
condition_immunities: "poisoned"
senses: "Passive Perception 12"
languages: "Grung"
cr: "2"
traits:
  - name: "Amphibious"
    desc: "The grung can breathe air and water."
  - name: "Poisonous Skin"
    desc: "Any creature that grapples the grung or otherwise comes into direct contact with the grung's skin must succeed on a DC 12 Constitution saving throw or become poisoned for 1 minute. A poisoned creature no longer in direct contact with the grung can repeat the saving throw at the end of each of its turns, ending the effect on a success."
  - name: "Standing Leap"
    desc: "The grung's long jump is up to 25 feet and its high jump is up to 15 feet, with or without a running start."
actions:
  - name: "Multiattack"
    desc: "The grung makes two attacks with its dagger or shortbow."
  - name: "Dagger"
    desc: "Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 5 (1d4 + 3) piercing damage plus 5 (2d4) poison damage."
  - name: "Shortbow"
    desc: "Ranged Weapon Attack: +5 to hit, range 80/320 ft., one target. Hit: 6 (1d6 + 3) piercing damage plus 5 (2d4) poison damage."
  - name: "Mesmerizing Chirr (Recharge 6)"
    desc: "The grung makes a chirring noise to which grung are immune. Each humanoid or beast within 15 feet of the grung that can hear it must succeed on a DC 12 Wisdom saving throw or be stunned until the end of the grung's next turn."
```

## Tactical Behavior

Elite warriors serve two roles in the [[calveno-sewers-grung-magazines|Calveno sewer network]]:

**Blue-caste handlers (secondary sites):** Coordinate sentry teams of 2 green-caste laborers. Standing orders are hide-and-report. The handler fights only to cover the laborers' escape, then retreats. Opens with shortbow from concealment, uses Standing Leap to reposition across water channels.

**Purple-caste warriors (primary site):** Shoot-on-sight security. Opens from concealment with hand crossbow (use shortbow stats). Uses Mesmerizing Chirr if two or more targets cluster within 15 ft, then focuses fire on stunned targets. Fights from elevated positions (scaffolding, ledges) to exploit ranged advantage.

**Morale threshold:** Blue-caste breaks at half HP or if the magazine is compromised. Purple-caste at the primary site fights to the death to protect the summoning circle.

## Encounter Notes

Mesmerizing Chirr is a stun — one of the most powerful conditions. At DC 12 and Recharge 6, it fires once per fight on average. In the primary chamber with 4 Elite Warriors, the party faces up to 4 Chirr attempts if the fight lasts long enough. Stagger their use: the first warrior Chirrs on round 1, others hold theirs.

The party's concentration-dependent controller ([[perrin-black-jaw|Perrin]]) is particularly vulnerable to the stun — if he loses concentration on Tasha's Hideous Laughter, the tactical landscape shifts hard.

## Related

- [[grung-npc|Grung (Green-Caste NPC)]]
- [[grung-wildling|Grung Wildling]]
- [[grung-clans|Grung Clans (Faction)]]
- [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]]
