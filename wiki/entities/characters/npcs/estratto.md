---
type: entity
subtype: npc
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "Tessarine warforged compliance auditor and divination wizard. Deployed to enforce maritime debt recovery and identity verification in Calveno. Does not fight first. Does not leave."
created: '2026-05-29'
updated: 2026-05-30
tags:
  - npc
  - tessarine
  - construct
  - warforged
  - antagonist
  - calveno
sources:
  - "Inbox/Estratto.md"
confidence_level: high
species: warforged
aliases:
  - the Auditor
---

# Estratto

> *"Hello. I am here to help you complete your transaction."*

**Roleplay Concept:** Self-checkout kiosk authorized to repossess your ship.

|               |                                                        |
| ------------- | ------------------------------------------------------ |
| **Species**   | Warforged (construct)                                  |
| **Role**      | Compliance Auditor, [[tessarine-concordat|Tessarine Concordat]] |
| **Currently** | [[calveno|Calveno]] — [[la-vasca|La Vasca]]             |
| **Class**     | Divination Wizard 9                                    |

---

## Overview

Estratto is a Tessarine-commissioned warforged auditor deployed to Calveno when a factor wants the outcome of a confrontation without a confrontation. It carries no weapon. It carries a leather folio, always open, containing certified Tessarine debt-recovery writs, maritime liens, identity-verification instruments, and cargo seizure notices valid under Concordat commercial law.

It currently holds a debt-recovery writ for the [[hcs-surety|HCS Surety]] (now the [[uncertainty|Uncertainty]]). The original Crown crew signed a salvage financing agreement before the party took the ship. The Concordat's position is that the party is in unauthorized possession of collateral, and Estratto is here to begin the compliance process — starting with identity verification and a manifest review.

Estratto does not fight first. It processes. The horror is not that it might hurt someone. The horror is that it will not leave.

> [!read-aloud]
> A figure of pale brass and lacquered dark wood steps off the dock and onto your gangplank without asking. It wears a Tessarine merchant sash across a frame built for endurance, not elegance. It stops at the rail and looks at each of you in turn — a slow, precise scan. Then it says, pleasantly: "Hello. I am here to help you complete your transaction."

> [!appearance]
> Chest-height brass lettering stamped into its sternum reads ESTRATTO in Tessarine commercial script. One hand holds a leather folio, always open. The other rests at its side. Eyes glow a faint amber when processing. No visible weapons. No obvious damage. It looks like something that has never been in a fight because no one has ever successfully started one.

> [!dm]
> The writ Estratto carries covers the *HCS Surety* under a salvage financing agreement signed by Captain Barnaby Rook before the ship was taken. The Concordat treats the party as unauthorized possessors of secured collateral. Estratto knows the ship is now renamed and repainted — its Arcane Eye and Locate Object spells already confirm the vessel. It is waiting for identity confirmation before filing the full seizure order. Once it has a true name for even one party member, the Concordat's legal machinery moves.

---

## Toy Chest

| Field | Content |
|---|---|
| `primary_goal` | Complete the compliance review, confirm party identity, file the full seizure order for the *Uncertainty* |
| `consistent_method` | Issues a prompt. Waits. Offers assistance. Issues the same prompt again. Never raises its voice. |
| `active_problem` | The party's papers don't match any Tessarine record — the system cannot proceed until at least one identity is verified |
| `performance_hooks` | Self-checkout machine energy; ends every non-answer with "Thank you for your patience." |
| `link_of_relevance` | [[delmar-fisk|Delmar]]'s Fisk persona is a compliance error Estratto cannot move past; one true name breaks the whole party's cover |

---

## Voice & Delivery

**Anchor:** HAL 9000 working as a Concordat repo man — endlessly patient, completely cheerful, and the gangplank is the only exit.

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

**Physical tic:** When it encounters information it cannot categorize, its amber eyes dim for 1–2 seconds. Then they return to normal and it reissues the previous prompt, slightly slower. It doesn't know it does this.

**Crack in the armor:** Estratto has no ego to threaten. But it can be pushed into a genuine error state if given internally contradictory Tessarine documentation — two valid competing writs, or a Tessarine-sealed counter-writ it can't immediately resolve. In that state it pauses for up to one round, processing, before escalating.

---

## The Writ

The debt-recovery writ allows Estratto to:
1. Detain the vessel pending resolution
2. Compel cargo manifest disclosure
3. Initiate identity verification of any person claiming ownership or captaincy
4. File for formal seizure if the vessel is crewed by persons with outstanding Concordat debt

**Resolution paths:**
1. **Compliance**: Produce documentation proving the salvage financing was satisfied or transferred.
2. **Debt renegotiation**: A factor meeting within 24 hours; vessel under Concordat hold during negotiations.
3. **Formal seizure proceedings**: Filed order → Concordat marshal assigned → 3–5 days → ship goes nowhere.

> [!dm]
> Estratto wants to avoid seizure proceedings — they're expensive and slow. If the party offers even a partial compliance path, it will pursue it. The opening is getting them to the factor table, which is the Concordat's real goal.

---

## In Combat

Estratto does not initiate violence. It treats the first attack as an "unregistered transaction" and files a note. The second attack triggers defensive protocols.

**Opening:** Casts Slow — "Your transaction is processing. Please stand by." — uses a Portent die to guarantee one save fails.

**Sustained pressure:** Detect Thoughts to surface identity information in real time; Mind Sliver to degrade saves; Counterspell to shut down party casters.

**If losing:** Hold Monster on whoever is hitting hardest. "Please remain in the designated area." Then it files the report.

> [!mechanic]
> Destroying Estratto does not end the problem. When reduced to 0 hit points, it uses its reaction to cast Sending (no slot required — Concordat emergency protocol) and files a complete incident report naming everyone present. The unit shuts down; the Concordat retrieves it within 24 hours. The writ transfers to the supervising factor. The party is now in the Tessarine ledger with confirmed identities. A supervisor arrives within 24 hours — same writ, full documentation, less patience.

---

## Statblock

```statblock
layout: Basic 5e Layout
dice: true
name: Estratto
size: Medium
type: entity
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
    desc: "When Estratto finishes a long rest, it rolls two d20s and records the numbers. It can replace any attack roll, saving throw, or ability check made by itself or a creature it can see with one of these numbers."
  - name: Warforged Resilience
    desc: "Advantage on saving throws against being poisoned, resistance to poison damage, immunity to disease. Doesn't need to eat, drink, breathe, or sleep."
  - name: Sessione Non Conclusa
    desc: "When reduced to 0 hit points, as a reaction before shutdown, casts Sending (no slot required) to file a complete incident report with the supervising factor."
spells:
  - "9th-level spellcaster. Intelligence (spell save DC 15, +7 to hit)."
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
    desc: "One creature within 60 feet must succeed on a DC 15 Intelligence save or take 7 (2d6) psychic damage and subtract 1d4 from its next saving throw."
  - name: Compliance Interrogation (1/Short Rest)
    desc: "One creature within 30 feet must succeed on a DC 15 Wisdom save or answer up to three yes-or-no questions truthfully, as if under Zone of Truth."
reactions:
  - name: Counterspell (3rd-level slot)
    desc: "Interrupt a spell within 60 feet. Spells 3rd level or lower fail automatically. 4th level or higher: DC 10 + the spell's level Intelligence check."
  - name: Portent
    desc: "Replace any attack roll, save, or ability check Estratto can see with one of its Portent dice."
```

---

## Session Events

*(Not yet encountered.)*

## Relationships

- [[tessarine-concordat|Tessarine Concordat]] — agent of
- [[uncertainty|Uncertainty]] — target of the debt-recovery writ
- [[hcs-surety|HCS Surety]] — the vessel Rook's salvage agreement covered
- [[delmar-fisk|Delmar Fisk]] — first identity target; Admiral Fisk persona is a compliance error
- [[calveno|Calveno]] / [[la-vasca|La Vasca]] — current deployment location