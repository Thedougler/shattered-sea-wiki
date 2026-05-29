---
title: Beaumont Sel
type: entity
subtype: npc
category: character
publish: true
campaign: shattered-sea
audience: players
status: active
species: tortle
aliases:
  - Beau
  - Captain Sel
tags: [npc, tortle, captain, midchain, ally]
sources:
  - Inbox/Session-01-Recap.md
  - Inbox/Beaumonts-Crew.md
  - Inbox/Beaumont-Sel.md
confidence_level: observed
relationships:
  - "[[delmar-fisk|Delmar Fisk]] — allied, fought alongside"
  - "[[barnaby-rook|Barnaby Rook]] — antagonist; Rook shot at him"
  - "[[saltwright|Saltwright]] — captain"
  - "[[bisou|Bisou]] — companion"
  - "[[lenne-vor|Lenne Vor]] — navigator"
  - "[[drav-holke|Drav Holke]] — bosun"
  - "[[wessa|Wessa]] — cook"
  - "[[fen|Fen]] — ordinary sailor"
---

# Beaumont Sel

![[raw/assets/portraits/Beaumont-Sel.webp|Beaumont Sel, a tough old alligator-snapping tortle captain with a leather eye cover, pipe, Bisou on his shoulder, and mirror-bright Antheri plate on his shell]]

**Quote:** *"Boy, I shit out harder things than you every mornin'."*

---

| | |
|---|---|
| **Species** | Tortle |
| **Role** | Captain, *[[saltwright|Saltwright]]* |
| **Home Port** | [[kalowe|Kalowe]] |
| **Route** | [[midchain|Midchain]] |

---

## Overview

Beaumont Sel is the captain of the *[[saltwright|Saltwright]]*, a merchant brig out of [[kalowe|Kalowe]] working the [[midchain|Midchain]] route. He has run the same route for eleven years. Same vessel, same patched shell, same monkey on his left shoulder. He handles the route's complications — and the Midchain has plenty — with the patience of someone who has seen most things before and knows that alarm rarely helps.

He speaks in an unhurried patois. He does not volunteer information about himself, but he is not unfriendly. When he pulled [[crissdalynn-khinriss|Crissdalynn Khinriss]] and [[delmar-fisk|Delmar Fisk]] from the water after their fleet went down, he did not ask questions. He gave them passage west and left it there.

## Role

Beaumont is the party's current captain, host, and practical moral baseline aboard the [[saltwright|Saltwright]]. He controls the ship, knows the Midchain route, and can force uncomfortable conversations without turning them into speeches.

## Appearance & Manner

Wide and low, built like something that has survived a long time by being hard to move. His shell is river-mud brown, ridged along the edges in angular spikes worn blunt by salt air. On the upper-right panel there is a fist-sized dent and a chipped spike — patched now with a [[salvaged-antheri-plate|Salvaged Antheri Plate]], mirror-bright and flush-fitted. He has never explained either.

One eye is covered in sun-bleached leather. His jaw is undershot and broad, the beak worn flat, his neck thick and heavily scaled. He carries a short-stemmed clay pipe — unlit as often as lit — in the corner of his mouth. On his left shoulder, a small capuchin monkey named [[bisou|Bisou]] rides with her tail looped once around his neck like a collar she put there herself.

Beaumont does not hurry. He handles problems like bad weather: he waits them out when he can, pays what he must when he can't, and does not let his face show which he thinks it is.

**Roleplaying:**
- Holds eye contact too long, says too little, then moves.
- Never looks surprised. Looks inconvenienced at best.
- Bisou reads the room before Beaumont reacts — watch the monkey.

## Bisou

The capuchin on his shoulder is [[bisou|Bisou]]. She has been riding that shoulder for the full eleven years he has run the Midchain. She steals his pipe regularly and shows no remorse about it. Beaumont takes it back after a drag or two.

## Wants

Beaumont wants the [[saltwright|Saltwright]] and its passengers alive, paid for, and clear of avoidable Crown trouble. He is willing to help, but he does not mistake the party's chaos for his responsibility.

## Route Knowledge

Beaumont knows the Midchain route, the Saltwright's crew and cargo, local port habits, and the practical difference between ordinary inspection pressure and the sharper posture [[barnaby-rook|Barnaby Rook]] brought aboard.

## Crew

- [[lenne-vor|Lenne Vor]] — navigator
- [[drav-holke|Drav Holke]] — bosun
- [[wessa|Wessa]] — cook
- [[fen|Fen]] — ordinary sailor

## Session Events

- **Session 01** — Held Rook's attention at the Saltwright's wheel during the hold ambush; joined the fight on deck; deflected Rook's flintlock round off the [[salvaged-antheri-plate|Salvaged Antheri Plate]].
- **Session 02** — Solved the cannon problem by throwing [[bisou|Bisou]] through a gun port (she pissed in the powder). Settled accounts: gave [[perrin-black-jaw|Perrin]] "Friend of the Passage" status and delivered [[nona-black-jaw|Nona Black-Jaw]]'s message; gave [[jean-claude-tabarnack|Jean-Claude]] the [[truth-stone|Truth Stone]]. Retrieved Rook's admiral hat. Departed at dawn on the Saltwright. Said he can be found in [[kalowe|Kalowe]] when off route. [[bisou|Bisou]] removed 15 gp of shinies from the Surety before departure; Beaumont called it fair business.

## Stat Block

```statblock
layout: Basic 5e Layout
name: Beaumont Sel
size: Medium
type: humanoid
subtype: tortle
alignment: neutral good
ac: 19
hp: 44
hit_dice: 8d8+8
speed: "15 ft."
stats: [18, 8, 14, 12, 14, 13]
saves:
  - strength: 6
  - constitution: 4
skillsaves:
  - athletics: 6
  - perception: 4
  - intimidation: 3
senses: "passive Perception 14"
languages: "Common, Aquan"
cr: 2
source: "Homebrew"
traits:
  - name: Salvaged Antheri Plate
    desc: "Ranged weapon attacks against Beaumont are made at disadvantage. The Antheri alloy's mirror-bright surface throws a hard glare at anyone trying to draw a bead on it."
  - name: Hold Breath
    desc: "Beaumont can hold his breath for 1 hour."
  - name: Old Bones
    desc: "Beaumont's speed is 15 ft. When he Dashes, he moves 20 ft. total rather than doubling his speed."
actions:
  - name: Multiattack
    desc: "Beaumont makes one Uppercut and one Jab. He can replace either attack with a Throw."
  - name: Uppercut
    desc: "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 8 (1d8 + 4) bludgeoning damage."
  - name: Jab
    desc: "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 6 (1d4 + 4) bludgeoning damage."
  - name: Throw
    desc: "One creature within 5 ft. makes a contested Strength (Athletics) check against Beaumont (+6). On a failure, the target takes 7 (1d6 + 4) bludgeoning damage, is moved up to 10 ft. in a direction Beaumont chooses, and falls prone."
  - name: The Kalowe Maneuver
    desc: "Beaumont tosses a potion of healing alongside Bisou to a creature within 30 ft. that is unconscious or at half hit points or fewer. Bisou lands, uncorks the potion, and empties it into the target's mouth — the target regains 2d4 + 2 hit points. Bisou returns to Beaumont's shoulder at the start of his next turn. Requires one available potion of healing; Bisou must not be incapacitated. Beaumont currently has three potions."
  - name: The Calveno Maneuver
    desc: "Beaumont hands Bisou an alchemical item. Bisou moves up to 60 ft., delivers it to a point of Beaumont's choosing, triggers it, and drops it there. The item activates at the start of Beaumont's next turn. Bisou then moves 15 ft. away as a free reaction. Requires an available alchemical item; Bisou must not be incapacitated."
  - name: The Tidefall Maneuver
    desc: "Beaumont tosses Bisou toward a target creature within 30 ft. Bisou locates and soaks any exposed black powder on the target. The target must succeed on a DC 12 Dexterity saving throw or have all black powder weapons rendered inoperable until dried. Bisou returns to Beaumont's shoulder at the start of his next turn. Bisou must not be incapacitated."
```

## Hooks

- Beaumont can confront the party when their secrets endanger his ship.
- His maneuvers with [[bisou|Bisou]] give him practical combat utility without making him a party member.
- The [[salvaged-antheri-plate|Antheri plate]] on his shell can point toward [[calveno|Calveno]], the Shelfworks, or older salvage stories.

## See Also

- [[bisou|Bisou]]
- [[saltwright|Saltwright]]
- [[beaumonts-crew|Beaumont's Crew]]
