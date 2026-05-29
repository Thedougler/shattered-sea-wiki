---
type: character
subtype: minor-npc
campaign: shattered-sea
status: active
audience: dm
publish: false
aliases:
  - Ruk
summary: "Lizardfolk bodyguard for Nona Black-Jaw. Massive, scarred, incapable of pretending not to notice things. He understands Nona because he understands hatchlings."
created: 2026-05-20
updated: 2026-05-28
tags: [lizardfolk, minor-npc]
sources: ["Inbox/Session-03-Recap.md", "Inbox/Ruk.md"]
---

# Ruk

|               |                                                         |
| ------------- | ------------------------------------------------------- |
| **Species**   | Lizardfolk                                              |
| **Pronouns**  | he/him                                                  |
| **Location**  | [[le-paludi|Le Paludi]], [[warren|The Warren]]          |
| **Role**      | Bodyguard, Black-Jaw Run                                |

---

Ruk understands four things: territory, loyalty, feeding rituals, and the defense of hatchlings. [[nona-black-jaw|Nona]] touches all four. He does not need to understand the politics to understand who she is, and he has decided she is worth protecting with his body.

He cannot pretend not to notice things. This is not a skill gap — it is a philosophical position. If someone is lying, he says so. If something smells wrong, he names it. Nona has found this useful for twenty years and has learned to manage the timing.

> *"He is lying. I can smell the fear-sweat. Also, he looked left before answering."*
>
> *"Ruk, darling, we accuse guests after dessert."*

## Appearance & Manner

Large for a lizardfolk — broad through the chest, scarred across both forearms and the left side of his neck where the scales have grown back lighter and rough. Dark olive-green with darker banding. He sits with his back to the wall, hands on the table, and watches every door.

He is not unfriendly. He is literal. He is more likely to offer someone food than to threaten them — but the threat is clearly available if the food is declined badly.

At the table, [[enzo|Enzo]] manages social reads; Ruk manages physical ones. Ruk's job is presence — he is the reason nobody tries anything.

If combat starts, he moves to put himself between Nona and whatever is moving toward her.

## Session 03

Stood near the door in Nona's kitchen in [[le-paludi|Le Paludi]] when Perrin arrived. Told the crying rattkin mother: *"Don't worry. Nona will take care of it."*

## Statblock

```statblock
layout: Basic 5e Layout
name: Ruk
size: Medium
type: humanoid
subtype: lizardfolk
alignment: neutral
ac: 16
hp: 104
hit_dice: 16d8+48
speed: "30 ft., swim 30 ft."
stats: [20, 10, 18, 8, 14, 7]
saves:
  - strength: 8
  - constitution: 7
skillsaves:
  - perception: 5
  - athletics: 8
  - survival: 5
  - insight: 5
senses: "passive Perception 15"
languages: "Common, Draconic"
cr: 6
source: Homebrew
traits:
  - name: Hold Breath
    desc: "Ruk can hold his breath for 15 minutes."
  - name: Relentless Endurance
    desc: "Once per day, when Ruk is reduced to 0 HP but not killed outright, he drops to 1 HP instead."
  - name: Territorial Senses
    desc: "Ruk cannot be surprised while conscious. He has advantage on Wisdom (Insight) checks."
  - name: Wrestler
    desc: "Ruk has advantage on Strength (Athletics) checks to grapple or shove. He can make attacks against other creatures without releasing a creature he is grappling."
actions:
  - name: Multiattack
    desc: "Ruk makes three attacks: two with his greatclub and one bite."
  - name: Greatclub
    desc: "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 14 (2d8 + 5) bludgeoning damage."
  - name: Bite
    desc: "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 9 (1d8 + 5) piercing damage. On a hit, the target is grappled (escape DC 16). Ruk's attacks against a grappled creature have advantage."
bonus_actions:
  - name: Hungry Jaws
    desc: "Ruk makes one bite attack. On a hit, he regains hit points equal to the damage dealt. Once used, this trait cannot be used again until he finishes a short or long rest."
  - name: Pin Down
    desc: "While Ruk has a creature grappled, he forces it to make a DC 16 Strength saving throw. On a failure, the creature is also restrained until the start of Ruk's next turn."
```
