---
type: rules
subtype: rule
campaign: shattered-sea
status: active
audience: players
publish: true
summary: "Rules for ship's guns, broadsides, shot types, and multi-deck volleys — expands the 2024 DMG vehicle rules."
created: '2026-05-29'
updated: '2026-05-29'
tags: [rule, reference, ship, combat, naval]
sources: [Homebrew]
title: Ship Combat
confidence_level: medium
---

# Ship Combat

Expands the **2024 DMG vehicle rules**. Covers movement, chases, ramming, and campaign-specific gun rules.

---

## Ship Movement

**Helm action.** A creature acting as helmsman uses their action to move the ship up to its speed. The ship can turn up to 90 degrees before, during, or after this movement; each 90-degree turn costs 5 feet of movement. A ship cannot move backward.

---

## Chases

Ships move on their turns in initiative order. A helmsman can Dash to move the ship its speed a second time. Each round compare total distance covered — if the pursuer outpaces the quarry, the gap closes by the difference. Roll a d20 for Chase Complications at the start of each participant's turn.

**Escape:** The quarry escapes when the gap exceeds 500 feet in open water, or they reach impassable terrain. The pursuer catches up when the gap reaches 0.

---

## Ramming

A ship that moves at least 20 feet in a straight line and ends within 5 feet of another vessel may ram (part of the Helm action).

- Target takes **4d10 bludgeoning damage**.
- **Self-damage by angle:** Striking port/starboard/aft: ramming ship takes 2d10. Fore-to-fore: both take 4d10.
- Target makes DC 15 Strength save; failure: pushed 10 feet.
- Unsecured crew: DC 13 Dexterity save or fall prone and take 1d6.

---

## Gun Crew Requirements

Each gun requires a crew of three.

| Crew | Effect |
|---|---|
| 3 (full) | Fires and reloads normally. Counts as a fully crewed gun. |
| 2 | Reload takes twice as long. Counts as half a gun for damage. |
| 1 | Reload takes three times as long. Half a gun; attack at disadvantage if firing independently. |
| 0 | Cannot fire. |

**Attack:** Ranged attack roll vs target Hull AC. **Hit:** Roll damage. **Miss:** Half damage. **Critical Hit:** Roll damage twice, take higher.

---

## Gunner Actions

A PC filling the **Gunner** role takes one ship action per round:

**Salvo.** Fire all manned guns on one side simultaneously.
1. Choose port or starboard.
2. Roll one attack (Dexterity + proficiency vs Hull AC). Advantage if one Gunner per gun deck.
3. Hit: full damage from all fully crewed guns that side. Miss: half that damage.
4. All guns that fired must reload.

**Aimed Shot.** Fire a single gun at a specific target location (Targeting table below). Uses both the Gunner's ship action and that gun crew's action.

**Reload — All Guns.** Order all gun crews to reload simultaneously (single ship action).

---

## Gun Classes

| Gun | Die | Range | Reload | Notes |
|---|---|---|---|---|
| Swivel Gun | d6 | 100/400 ft | 1 action | Anti-crew only; cannot damage hull. |
| 12-lb Long Cannon | d8 | 600/2,400 ft | 1 action | Standard upper-deck gun. |
| 24-lb Long Cannon | d10 | 500/2,000 ft | 2 actions | Primary fleet gun. |
| 32-lb Long Cannon | d12 | 400/1,600 ft | 2 actions | Maximum hull damage; slow. |
| Heavy Carronade | d12 | 150/600 ft | 1 action | Close quarters only; devastating. |
| 12-lb Chaser | d8 | 600/2,400 ft | 1 action | Fixed forward or aft arc. |

---

## Shot Types

| Shot | Attack Mod | Hit Effect | Miss | Notes |
|---|---|---|---|---|
| Round Shot | — | Xd[Y] hull damage | Half hull | Default; all guns |
| Chain Shot | −2 | Xd[Y] speed loss (mi/day); no hull | Half speed | 12-lb+; not carronades |
| Grapeshot | — | Exposed crew: DC 14 Dex or incapacitated; PCs take Xd6 (save half) | PCs save with advantage | Max 150 ft; all guns |
| Bar Shot | −4 | Mast hit: speed halved; 2nd hit: speed 0 | None | 12-lb+; Aimed Shot only |
| Heated Shot | — | Xd[Y] hull + ship saves DC 12 or fire starts | Half hull, no fire | Not carronades; requires prep |
| Incendiary Shot | — | Half Xd[Y] hull + fire starts (d[Y]/round, stacks) | Half hull; fire at d[Y]/2/round | Not carronades; specialist ammo |

---

## Targeting (Aimed Shots)

| Target | Attack Mod | Effect on Hit |
|---|---|---|
| Hull | — | d[Y] hull damage |
| Rigging | −2 | Speed reduced by d[Y] mi/day |
| Mast | −4 | Speed halved; bar shot is built for this |
| Crew (deck) | −4 | 1 crew incapacitated; grapeshot does this as Salvo |
| Powder Magazine | −6 | Target ship saves DC 16 or magazine detonates |

---

## Crew Casualties

- Every 50 Hull Point damage in a single round: 1d4 crew casualties.
- Grapeshot on exposed deck: DC 14 Dex save or incapacitated.
- Below minimum crew: all ship checks at disadvantage; speed reduced 20%.

---

## Tier 4 (First-Rate Only)

A Tier 4 ship cannot be matched in direct exchange. **Multi-Deck Salvo:** Roll one attack per deck using Gunner's modifier. Each deck resolves independently. All three decks reload — no full broadside for 3 rounds.

Practical counters: fire ships, shallow water (first-rates draw 25+ ft), fast running escape, multiple fast targets. When the *Sovereign* is an enemy, it is not a combat encounter — it is a situation.

---

## Related

- [[bastions|Ship Bastion]] — facility rules
- [[hcs-sovereign|HCS Sovereign]] — Tier 4 stat block
