---
type: monster
subtype: monster
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: CR 1/4 humanoid; green-caste laborers and scouts. Poison skin, standing leap, amphibious. The expendable workforce of Grung operations.
created: 2026-06-01
updated: 2026-06-05
tags:
  - grung
  - combat
sources:
  - VGM
confidence_level: high
aliases:
  - Grung
  - Green-Caste Grung
cha: 10
con: 15
cr: 1/4
creature_type: humanoid
dex: 14
environment: forest, swamp, urban
int: 10
page: 156
statblock: inline
str: 7
wis: 11
---

# Grung

```statblock
layout: Basic 5e Layout
name: "Grung"
size: Small
type: humanoid
subtype: grung
alignment: Typically Neutral Evil
ac: 12
ac_note: natural armor
hp: 11
hit_dice: 2d6 + 4
speed: "25 ft., Climb 25 ft."
stats: [7, 14, 15, 10, 11, 10]
saves:
  - dexterity: 4
skillsaves:
  - athletics: 2
  - perception: 2
  - stealth: 4
  - survival: 2
damage_immunities: "poison"
condition_immunities: "poisoned"
senses: "Passive Perception 12"
languages: "Grung"
cr: "1/4"
traits:
  - name: "Amphibious"
    desc: "The grung can breathe air and water."
  - name: "Poisonous Skin"
    desc: "Any creature that grapples the grung or otherwise comes into direct contact with the grung's skin must succeed on a DC 12 Constitution saving throw or become poisoned for 1 minute. A poisoned creature no longer in direct contact with the grung can repeat the saving throw at the end of each of its turns, ending the effect on a success."
  - name: "Standing Leap"
    desc: "The grung's long jump is up to 25 feet and its high jump is up to 15 feet, with or without a running start."
actions:
  - name: "Dagger"
    desc: "Melee or Ranged Weapon Attack: +4 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 4 (1d4 + 2) piercing damage plus 5 (2d4) poison damage."
```

## Tactical Behavior

Green-caste grung are laborers, not fighters. In the [[calveno-sewers-grung-magazines|Calveno sewer magazines]], they serve as sentries alongside a blue-caste handler. Standing orders: hide at the sound of movement (Stealth +4, advantage in dim light near water), let intruders pass, report after. They break cover only if the party interacts with the blackpowder barrels. If discovered, they attempt to flee and report rather than fight.

**Morale threshold:** Flees immediately if the handler is killed or if reduced below half HP. Will not fight to the death under any circumstance.

## Grung Poison

Grung weapons are coated with poison secreted from their skin. On a hit, the target takes an additional 2d4 poison damage. The Poisonous Skin trait is separate — it triggers on direct physical contact (grappling, unarmed strikes against the grung).

**Party note:** DC 12 Constitution is moderate. Multiple grung means multiple poison saves per round. The poisoned condition (disadvantage on attacks and ability checks) stacks in effect with the ongoing save requirement.

## Related

- [[grung-elite-warrior|Grung Elite Warrior]]
- [[grung-wildling|Grung Wildling]]
- [[grung-clans|Grung Clans (Faction)]]
- [[simone-tabarnack|Simone Tabarnack]]
