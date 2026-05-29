---
title: Captain Dorian Bishop
category: character
type: character
subtype: npc
campaign: shattered-sea
created: 2026-05-11
updated: 2026-05-16
publish: false
audience: gm
status: active
reveal_status: unrevealed
summary: "Dravosi Crown Captain commanding the HCS Tangent. Twice as dangerous as Rook in single combat. Known for lateral, unpredictable approaches where others charge straight. The next escalation."
tags:
  - dravosi
  - npc
  - dm-only
sources:
  - Homebrew
relationships:
  - relation: commands
    target: HCS Tangent
  - relation: serves
    target: Dravosi Crown
  - relation: chess_tier_above
    target: Barnaby Rook
---

# Captain Dorian Bishop

*Unrevealed. Not yet in play.*

---

|                |                                                       |
| -------------- | ----------------------------------------------------- |
| **Species**    | Human (Dravosi)                                       |
| **Title**      | Crown Captain, HCS *Tangent*, Dravosi Navy            |
| **Status**     | Active — next escalation after [[Barnaby-Rook\|Rook]]    |
| **CR**         | 6                                                     |

---

## Overview

Dorian Bishop is what happens when the Crown decides that Rook's approach wasn't working. Where Rook charged — into holds, into arguments, into problems — Bishop comes at everything from the side. He does not go through obstacles. He goes around them, angles into them from a direction they weren't watching, and arrives at an outcome that looks obvious in hindsight and wasn't visible ten seconds before.

He commands the *[[HCS-Tangent]]*, a Dravosi Crown warship significantly heavier than Rook's cutter. The *Tangent* does not do inspections.

---

## Manner

Precise, cultured, and patient in the way that genuinely dangerous people sometimes are. He does not underestimate opponents. He does not telegraph. He does not repeat himself.

He was aware of Rook the way a senior surgeon is aware of a general practitioner — not contemptuous, exactly, but conscious of the difference in scope. Rook's death will reach him eventually, filtered through the reporting chain. He will note it, assess whether it requires a response, and respond only if the answer is yes.

His methods are not subtle for the sake of subtlety. He takes indirect approaches because they work. He has studied the pattern of how direct approaches fail and built a fighting style — and a command style — around going where that pattern leaves a gap.

---

## Tactics

He does not come straight at you. That is the short version.

The longer version: Bishop reads the field, identifies the angle of approach the opponent has already committed to defending, and takes a different one. In single combat he uses footwork that makes attack predictions unreliable — he is never where you aimed at the moment you swing. At sea, he positions the *Tangent* wide, forces his opponent to track and correct, and engages at the moment they've overcommitted to the correction.

Opponents who survive encounters with Bishop consistently report the same thing: at some point during the fight, they realised they were defending against a move he'd already abandoned.

---

## The HCS Tangent

A Dravosi Crown warship — heavier armament, full naval crew, proper gun deck. Not a patrol cutter. The *Tangent* does not dock quietly at merchant vessels to run manifests. When it appears, something has already gone wrong for someone, and that someone is the person it's pointing at.

The name was Bishop's choice. Nobody asked him to explain it.

---

## Threat Tier

Bishop sits between [[Barnaby-Rook|Rook]] and [[Rupert-Knighton|Knighton]] in the Dravosi apparatus. Rook was enforcement — a privateer doing shakedowns. Bishop is investigation and suppression — the Crown's response when enforcement stops reporting back.

He is twice the problem Rook was. Treat him accordingly.

**Do not deploy until Rook is fully resolved.**

## Escalation Logic

Bishop enters when the Crown needs investigation and suppression rather than ordinary enforcement. His presence means someone has decided the party is no longer a dockside problem.

---

## Statblock

```statblock
layout: Basic 5e Layout
name: Captain Dorian Bishop
size: Medium
type: humanoid
subtype: human
alignment: lawful neutral
ac: 17
hp: 165
hit_dice: 22d8+66
speed: "35 ft."
stats: [14, 18, 16, 15, 14, 14]
saves:
  - dexterity: 7
  - constitution: 6
skillsaves:
  - athletics: 5
  - deception: 5
  - insight: 5
  - perception: 5
senses: "passive Perception 15"
languages: "Common"
cr: 6
source: "Homebrew"
traits:
  - name: Uncanny Footwork
    desc: "Opportunity attacks against Bishop are made at disadvantage."
bonus_actions:
  - name: Disengage
    desc: "Bishop can Disengage as a bonus action."
actions:
  - name: Multiattack
    desc: "Bishop makes three Naval Blade attacks, or one Flintlock Pistol attack and two Naval Blade attacks."
  - name: Naval Blade
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 10 (1d10 + 5) slashing damage."
  - name: Flintlock Pistol
    desc: "Ranged Weapon Attack: +7 to hit, range 30/90 ft., one target. Hit: 12 (2d8 + 3) piercing damage. Once fired, requires an action to reload."
reactions:
  - name: Parry
    desc: "When an attack hits Bishop, he reduces the damage by 1d10 + 5. Applies to melee and ranged attacks. He must be holding a melee weapon and be aware of the attacker."
```

---

## Relationships

- [[HCS-Tangent]]
- [[Barnaby-Rook]]
- [[Rupert-Knighton]]
- [[Dravosi-Crown]]

## Pressure Points

- Rook's death or humiliation can move Bishop from background escalation to active pursuit.
- The *Tangent* should appear only when the campaign is ready for Crown pressure to become naval rather than procedural.

## Related Pages

- [[content/shattered-sea/ships/HCS-Tangent|HCS Tangent]]
- [[content/shattered-sea/factions/Dravosi-Crown|Dravosi Crown]]
