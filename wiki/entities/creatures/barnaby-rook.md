---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 3 Dravosi Crown privateer captain. Boarding specialist with Parry reaction, legendary actions, and lair actions aboard the HCS Surety. Phase 3 boss of the Saltwright encounter."
created: 2026-04-14
updated: 2026-05-28
tags: [creature, humanoid, bestiary, dravosi, cr3, named-enemy]
sources: ["Inbox/Barnaby-Rook.md"]
cr: 3
confidence_level: high
relationships:
  - "[[barnaby-rook|Barnaby Rook]] — NPC lore page"
  - "[[hcs-surety|HCS Surety]] — command vessel / lair"
---

# Captain Barnaby Rook — Stat Block

![[Barnaby-Rook.webp|Captain Barnaby Rook on the HCS Surety gangplank with cutlass and spent flintlock]]

> See [[barnaby-rook|Barnaby Rook]] for full lore, appearance, and connections.

```statblock
layout: Basic 5e Layout
name: Captain Barnaby Rook
size: Medium
type: humanoid
subtype: "human"
alignment: "lawful neutral"
ac: 17
hp: 120
hit_dice: "12d8 + 36"
speed: "30 ft."
stats: [14, 16, 16, 13, 12, 14]
saves:
  - dexterity: 5
  - constitution: 5
skillsaves:
  - athletics: 4
  - intimidation: 4
  - perception: 3
senses: "passive Perception 13"
languages: "Common"
cr: 3
source: "Homebrew"
traits:
  - name: Officer's Advantage
    desc: "While at least two allies are within 30 ft. of Rook and can hear him, he has advantage on initiative rolls and cannot be surprised."
  - name: Cornered Wolf
    desc: "When Rook has no living allies within 30 ft., his Parry reaction reduces damage by 1d10 + 6 instead of 1d10 + 4, and it applies to ranged attacks as well as melee. Additionally, he has advantage on saving throws."
  - name: Naval Footwork
    desc: "Rook can Disengage as a bonus action."
bonus_actions:
  - name: Disengage (Naval Footwork)
    desc: "Rook disengages without provoking opportunity attacks and moves up to his speed."
actions:
  - name: Multiattack
    desc: "Rook makes two attacks: each is either a Cutlass attack or a Flintlock Pistol attack. He cannot make more than one Flintlock attack per turn unless he takes an action to reload."
  - name: Cutlass
    desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 9 (1d10 + 4) slashing damage. On a hit, Rook can forgo the damage to shove the target up to 5 ft. in any direction (no save)."
  - name: Flintlock Pistol
    desc: "Ranged Weapon Attack: +5 to hit, range 30/90 ft., one target. Hit: 12 (2d8 + 3) piercing damage. Once fired, requires an action to reload. Rook carries a brace — he has two pistols, each loaded once."
reactions:
  - name: Parry
    desc: "When an attack hits Rook, he reduces the damage by 1d10 + 4 (or 1d10 + 6 if Cornered Wolf is active). He must be holding a melee weapon and be aware of the attacker. Applies to melee only unless Cornered Wolf is active."
legendary_description: "Rook can take 3 legendary actions per round, choosing from the options below. Only one legendary action option can be used at a time, and only at the end of another creature's turn. Rook regains spent legendary actions at the start of his turn."
legendary_actions:
  - name: Reposition (Costs 1 Action)
    desc: "Rook moves up to half his speed without provoking opportunity attacks."
  - name: Cutlass Strike (Costs 2 Actions)
    desc: "Rook makes one Cutlass attack. He can use the shove option on a hit."
  - name: Pistol Reload (Costs 2 Actions)
    desc: "Rook reloads one expended flintlock pistol. He does not fire it — this sets up his next turn or a future legendary action."
lair_actions:
  - desc: "On initiative count 20 (losing initiative ties), Barnaby Rook issues a command to the crew of the HCS Surety, choosing one of the following lair actions. He cannot use the same lair action two rounds in a row."
  - desc: "Arm the Guns. Rook orders the gun crew to uncover the hatches of the Surety's two deck-level cannons and ready them for firing. No immediate effect — the guns are primed. This enables Fire the Guns on the following round."
  - desc: "Fire the Guns. If the Surety's cannons were Armed last round, Rook commands both gun crews to fire. Each cannon discharges in a 30-foot cone extending from its gun port along the deck. Each creature or object in either cone must make a DC 14 Dexterity saving throw, taking 4d10 bludgeoning damage on a failed save, or half on a success. Structures and objects in either cone automatically take the full damage."
  - desc: "Call to Arms. If Rook has been reduced below half his hit point maximum (60 hp), he calls out to all remaining crew aboard the Surety. Up to 1d4+1 Dravosi Deckhands appear at the start of Rook's next turn in unoccupied spaces aboard the Surety."
```

## Related

- [[barnaby-rook|Barnaby Rook]] — full lore and DM notes
- [[hcs-surety|HCS Surety]] — command vessel
- [[dravosi-deckhand|Dravosi Deckhand]] — subordinate crew
- [[dravosi-enforcer|Dravosi Enforcer]] — subordinate crew
