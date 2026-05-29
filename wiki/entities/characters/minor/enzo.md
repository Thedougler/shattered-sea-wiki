---
type: character
subtype: minor-npc
campaign: shattered-sea
status: active
audience: dm
publish: false
aliases:
  - Enzo
summary: "Black jaguar tabaxi bodyguard for Nona Black-Jaw. Impeccable suit, polished claws, lit cigar. The most dangerous person in the room who will not be the first one to speak."
created: 2026-05-20
updated: 2026-05-28
tags: [tabaxi, minor-npc]
sources: ["Inbox/Session-03-Recap.md", "Inbox/Enzo.md"]
---

# Enzo

|               |                                                         |
| ------------- | ------------------------------------------------------- |
| **Species**   | Tabaxi (Jaguar)                                         |
| **Pronouns**  | he/him                                                  |
| **Location**  | [[le-paludi|Le Paludi]], [[warren|The Warren]]          |
| **Role**      | Bodyguard, [[the-passage|The Passage]] / Black-Jaw Run  |

---

Enzo does not threaten. He holds doors, pulls chairs, and keeps a lit cigar balanced in two fingers for the duration of any meal [[nona-black-jaw|Nona]] is hosting. The cigar is a timer — it burns whether the conversation is going well or not. When it has burned down far enough and Nona is still waiting for an answer, he sets it on the edge of the table and unsheathes one claw. That is generally all it takes.

His sentence, delivered with complete politeness: *"Nona asked you a question."*

## Appearance & Manner

Medium-built black jaguar tabaxi — obsidian fur with rosette patterning visible when light catches it, broken by a long pale scar across the left side of his jaw. Dark tailored suit, collar buttoned tight, shoes mirror-polished. Claws maintained to a shine.

He does not raise his voice. He does not hurry. He stands slightly behind and to Nona's right, weight on his back foot, one hand always free.

At the table, he reads guests faster than [[ruk|Ruk]] does and communicates his read through small signals — a tap of the cigar, a shift of weight, a glance at Nona. If he moves between a guest and Nona, the conversation is over.

He is comfortable with people. He is more comfortable with violence.

## Session 03

Present in Nona's kitchen in Le Paludi when Perrin arrived. Leaned against the far wall. After Nona met with the party, she sent Enzo to arrange consolation for the Vestra's surviving crew and to call off the attacks she'd set in motion against [[perrin-black-jaw|Perrin]].

## Statblock

```statblock
layout: Basic 5e Layout
name: Enzo
size: Medium
type: humanoid
subtype: tabaxi
alignment: neutral
ac: 16
hp: 78
hit_dice: 12d8+24
speed: "30 ft., climb 20 ft."
stats: [12, 20, 14, 14, 14, 15]
saves:
  - dexterity: 8
  - wisdom: 5
skillsaves:
  - perception: 5
  - stealth: 8
  - intimidation: 5
  - acrobatics: 8
senses: "darkvision 60 ft., passive Perception 15"
languages: "Common, Thieves' Cant"
cr: 5
source: Homebrew
traits:
  - name: Feline Agility
    desc: "Once before finishing a short or long rest, Enzo can double his speed until the end of his turn. He cannot use this trait again until he moves 0 feet on one of his turns."
  - name: Cat's Claws
    desc: "Enzo can use his claws to climb at 20 ft. They function as natural weapons."
  - name: Evasion
    desc: "When Enzo is subjected to an effect that allows a Dexterity saving throw for half damage, he takes no damage on a success and half damage on a failure."
actions:
  - name: Multiattack
    desc: "Enzo makes three attacks: two with his rapier and one with his claws."
  - name: Rapier
    desc: "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 9 (1d8 + 5) piercing damage."
  - name: Claws
    desc: "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 8 (1d6 + 5) slashing damage."
  - name: Cut Clean
    desc: "Once per turn, when Enzo hits with his rapier and has advantage on the attack roll or an ally is within 5 ft. of the target, he deals an extra 10 (3d6) piercing damage."
bonus_actions:
  - name: Cunning Step
    desc: "Enzo takes the Dash, Disengage, or Hide action."
reactions:
  - name: Uncanny Dodge
    desc: "When an attacker Enzo can see hits him with an attack, he halves the attack's damage against him."
  - name: Interpose
    desc: "Replaces Uncanny Dodge. When a creature Enzo can see targets [[nona-black-jaw|Nona Black-Jaw]] with an attack, Enzo moves up to his speed toward the attacker without provoking opportunity attacks, and that attack roll is made with disadvantage."
```
