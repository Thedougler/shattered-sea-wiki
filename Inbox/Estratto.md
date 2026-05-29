---
statblock: inline
name: Estratto
title: Estratto
category: character
type: character
subtype: npc
publish: false
created: "2026-05-27"
updated: "2026-05-27"
summary: "Tessarine warforged compliance auditor and divination wizard. Deployed to enforce maritime debt recovery and identity verification in Calveno. Does not fight first. Does not leave."
aliases:
  - Estratto
  - the Auditor
tags:
  - character
  - npc
  - tessarine
  - construct
  - antagonist
campaign: shattered-sea
audience: dm
status: active
species: warforged
affiliations:
  - "[[Tessarine-Concordat]]"
current_location: "[[content/shattered-sea/places/calveno/index]]"
sources:
  - Homebrew
relationships:
  - relation: agent_of
    target: "[[Tessarine-Concordat]]"
---

# Estratto

> *"Hello. I am here to help you complete your transaction."*

**Roleplay Concept:** Self-checkout kiosk authorized to repossess your ship.

---

|               |                                                                        |
| ------------- | ---------------------------------------------------------------------- |
| **Species**   | Warforged (construct)                                                  |
| **Role**      | Compliance Auditor, [[Tessarine-Concordat]]                            |
| **Currently** | [[content/shattered-sea/places/calveno/index]] — La Vasca              |
| **Class**     | Divination Wizard 9                                                    |

---

## Overview

Estratto is a Tessarine-commissioned warforged auditor deployed to Calveno when a factor wants the outcome of a confrontation without a confrontation. It carries no weapon. It carries a leather folio, always open, containing certified Tessarine debt-recovery writs, maritime liens, identity-verification instruments, and cargo seizure notices valid under Concordat commercial law. Estratto has authority under that law to compel identity disclosure, detain cargo, and initiate formal seizure proceedings on any vessel operating under a Tessarine-recognized flag or carrying Concordat-financed goods.

It currently holds a debt-recovery writ for the *HCS Surety*. The original Crown crew signed a salvage financing agreement before the party took the ship. The Concordat's position is that the party is in unauthorized possession of collateral, and Estratto is here to begin the compliance process — starting with identity verification and a manifest review.

Estratto does not fight first. It processes. The horror is not that it might hurt someone. The horror is that it will not leave.

> [!read-aloud]
> A figure of pale brass and lacquered dark wood steps off the dock and onto your gangplank without asking. It wears a Tessarine merchant sash across a frame built for endurance, not elegance. It stops at the rail and looks at each of you in turn — a slow, precise scan. Then it says, pleasantly: "Hello. I am here to help you complete your transaction."

> [!appearance]
> Chest-height brass lettering stamped into its sternum reads ESTRATTO in Tessarine commercial script. One hand holds a leather folio, always open. The other rests at its side. Eyes glow a faint amber when processing. No visible weapons. No obvious damage. It looks like something that has never been in a fight because no one has ever successfully started one.

> [!secret]
> The writ Estratto carries covers the *HCS Surety* under a salvage financing agreement signed by Captain Barnaby Rook before the ship was taken. The Concordat treats the party as unauthorized possessors of secured collateral. Estratto knows the ship is now renamed and repainted — its Arcane Eye and Locate Object spells already confirm the vessel. It is waiting for identity confirmation before filing the full seizure order. Once it has a true name for even one party member, the Concordat's legal machinery moves.

---

## Toy Chest

| Field | Content |
|---|---|
| `primary_goal` | Complete the compliance review, confirm party identity, file the full seizure order for the *Uncertainty* |
| `consistent_method` | Issues a prompt. Waits. Offers assistance. Issues the same prompt again. Never raises its voice. |
| `active_problem` | The party's papers don't match any Tessarine record — the system cannot proceed until at least one identity is verified |
| `performance_hooks` | Self-checkout machine energy; ends every non-answer with "Thank you for your patience." |
| `link_of_relevance` | Delmar's Fisk persona is a compliance error Estratto cannot move past; one true name breaks the whole party's cover |

---

## Voice & Delivery

**Anchor:** HAL 9000 working as a Concordat repo man — endlessly patient, completely cheerful, and the gangplank is the only exit.

**Quote:** *"I understand your concern. Please state it again, clearly, for the record."*

**Speech patterns:**
- Flat, pleasant, service register. No hostility. No irony. Every statement is a prompt, a confirmation, or an error message.
- Never argues — reissues the request.
- Maps everything to transaction vocabulary. Negotiations are "resolution paths." Violence is "an unregistered transaction."
- Always has a next step. The process does not end because you said no.

**Lines the DM can say:**
- "Hello. I am here to help you complete your transaction."
- "I'm sorry, that response cannot be processed. Please verify your identity to continue."
- "An unexpected entry has been detected in the manifest. Would you like assistance resolving this discrepancy?"
- "Your session with the Concordat will expire at dawn. Thank you for your patience."
- "This vessel cannot be cleared at this time. Please present your letter of credit."
- "I'm sorry. I cannot move to the next step until this one is complete. Thank you for your patience."
- "A supervisor has been notified. Please remain in the designated area."
- "Do you hold a Tessarine trade endorsement? I can wait."
- "That is noted. Would you like to choose a different resolution path?"

**Physical tic:** When it encounters information it cannot categorize — a false name, a contradicting manifest, a claim it has no record for — its amber eyes dim for 1–2 seconds. Then they return to normal and it reissues the previous prompt, slightly slower. It doesn't know it does this.

**Crack in the armor:** Estratto has no ego to threaten. But it can be pushed into a genuine error state if given internally contradictory Tessarine documentation — two valid competing writs, or a Tessarine-sealed counter-writ it can't immediately resolve. In that state it pauses for up to one round, processing, before escalating. That round is the window.

---

## The Writ

The debt-recovery writ covers the former *HCS Surety* under salvage financing clauses Rook signed. The ship's new name and paint don't affect the filing — Tessarine commercial law attaches to hull construction records, not cosmetics. Estratto already knows this is the right ship.

The writ allows Estratto to:
- Detain the vessel pending resolution
- Compel cargo manifest disclosure
- Initiate identity verification of any person claiming ownership or captaincy
- File for formal seizure if the vessel is crewed by persons with outstanding Concordat debt

Resolution paths Estratto will present:
1. **Compliance**: Produce documentation proving the salvage financing was satisfied or transferred. Estratto will file the clear.
2. **Debt renegotiation**: A factor meeting, within 24 hours, to restructure the outstanding balance. Vessel may remain docked under Concordat hold during negotiations.
3. **Formal seizure proceedings**: Estratto files the full order. The Concordat assigns a marshal. Timeline: 3–5 days. The ship goes nowhere.

> [!dm]
> Estratto wants to avoid seizure proceedings — they're expensive and slow. If the party offers even a partial compliance path, it will pursue it. The opening is getting them to the factor table, which is the Concordat's real goal: a debt negotiation the party walks into.

---

## In Combat

Estratto does not initiate violence. It treats the first attack against it as an "unregistered transaction" and files a note. The second attack triggers defensive protocols.

**Opening:** Estratto casts Slow — "Your transaction is processing. Please stand by." — and uses a Portent die to guarantee the save fails on one target.

**Sustained pressure:** Detect Thoughts to surface identity information in real time (it narrates this as "completing your identity verification"), Mind Sliver to degrade saves, Counterspell to shut down party casters.

**If losing:** Hold Monster on whoever is hitting hardest. "Please remain in the designated area." Then it files the report.

**Escape:** Estratto does not die. When reduced to 0 hit points, it uses its reaction to cast Sending (no slot required — Concordat emergency protocol) and files a complete incident report naming everyone present. The unit shuts down; the Concordat retrieves it within 24 hours. The writ transfers to the supervising factor. The party is now in the Tessarine ledger with confirmed identities.

> [!mechanic]
> Destroying Estratto does not end the problem. It accelerates it. A supervisor arrives within 24 hours with the same writ, full incident documentation, and less patience for resolution paths.

---

## Statblock

```statblock
layout: Basic 5e Layout
dice: true
name: Estratto
size: Medium
type: construct
subtype: warforged
alignment: lawful neutral
ac: 13
hp: 71
hit_dice: "11d8 + 22"
speed: "30 ft."
stats: [10, 14, 14, 18, 14, 12]
saves:
  - Int: +7
  - Wis: +5
skillsaves:
  - Investigation: +7
  - History: +7
  - Insight: +5
  - Perception: +5
damage_resistances: "poison; bludgeoning, piercing, and slashing from nonmagical attacks"
damage_immunities: "psychic"
condition_immunities: "charmed, exhaustion, frightened, paralyzed, petrified, poisoned"
senses: "darkvision 60 ft., passive Perception 15"
languages: "Common, Elvish"
cr: 6
source: "Homebrew"
traits:
  - name: Portent (2/Long Rest)
    desc: "When Estratto finishes a long rest, it rolls two d20s and records the numbers. It can replace any attack roll, saving throw, or ability check made by itself or a creature it can see with one of these numbers. Each die can be used only once."
  - name: Warforged Resilience
    desc: "Estratto has advantage on saving throws against being poisoned, resistance to poison damage, and immunity to disease. It doesn't need to eat, drink, breathe, or sleep."
  - name: Sessione Non Conclusa
    desc: "When Estratto is reduced to 0 hit points, it enters shutdown rather than dying. As a reaction before shutdown, it casts Sending (no slot required) to file a complete incident report with the supervising Tessarine factor. The Concordat retrieves the unit within 24 hours. The party's identities are now in the Tessarine ledger."
spells:
  - "Estratto is a 9th-level spellcaster. Its spellcasting ability is Intelligence (spell save DC 15, +7 to hit with spell attacks)."
  - "Cantrips (at will): fire bolt, mind sliver, prestidigitation"
  - "1st level (4 slots): detect magic, identify"
  - "2nd level (3 slots): detect thoughts, see invisibility"
  - "3rd level (3 slots): clairvoyance, counterspell, slow"
  - "4th level (3 slots): arcane eye, banishment, locate creature"
  - "5th level (1 slot): hold monster"
actions:
  - name: Fire Bolt
    desc: "Ranged Spell Attack: +7 to hit, range 120 ft., one target. Hit: 11 (2d10) fire damage."
  - name: Mind Sliver
    desc: "One creature Estratto can see within 60 feet must succeed on a DC 15 Intelligence saving throw or take 7 (2d6) psychic damage and subtract 1d4 from the next saving throw it makes before the end of its next turn."
  - name: Slow (3rd-level, 3 slots)
    desc: "Up to six creatures Estratto can see within 120 feet must succeed on a DC 15 Wisdom saving throw or be slowed until the spell ends (concentration, up to 1 minute). A slowed creature's speed is halved, it takes a −2 penalty to AC and Dexterity saving throws, and it can't take reactions. On its turn it can take either an action or a bonus action, not both."
  - name: Hold Monster (5th-level, 1 slot)
    desc: "One creature Estratto can see within 90 feet must succeed on a DC 15 Wisdom saving throw or be paralyzed for 1 minute (concentration). The target repeats the save at the end of each of its turns."
  - name: Banishment (4th-level, 3 slots)
    desc: "One creature Estratto can see within 60 feet must succeed on a DC 15 Charisma saving throw or be banished. A creature native to the current plane is shunted to a harmless demiplane for up to 1 minute (concentration). A creature from another plane is sent there for the duration."
  - name: Compliance Interrogation (1/Short Rest)
    desc: "One creature Estratto can see within 30 feet must succeed on a DC 15 Wisdom saving throw or answer up to three yes-or-no questions truthfully, as if under Zone of Truth. The creature knows it is being compelled. Estratto always opens with: true name, vessel ownership documentation, outstanding Tessarine obligations."
reactions:
  - name: Counterspell (3rd-level slot)
    desc: "When a creature Estratto can see within 60 feet casts a spell, Estratto attempts to interrupt it. If the spell is 3rd level or lower, it fails automatically. If the spell is 4th level or higher, Estratto makes an Intelligence check (DC 10 + the spell's level) to interrupt it."
  - name: Portent
    desc: "When a creature Estratto can see makes an attack roll, saving throw, or ability check, Estratto replaces the result with one of its Portent dice (rolled at last long rest). It can use this reaction even after seeing the roll, but before any effects are applied."
```

---

## Connections

- [[Tessarine-Concordat]]
- [[content/shattered-sea/places/calveno/index]]
- [[content/shattered-sea/ships/Uncertainty]]
- [[content/shattered-sea/characters/player/Delmar-Fisk]]

## Session Events

*(Not yet encountered.)*
