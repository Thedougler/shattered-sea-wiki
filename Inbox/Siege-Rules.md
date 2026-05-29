---


campaign: standalone
confidence_level: high
created: '2026-04-24'
sources:
- raw/ingested/Storm-Rising-Adventure
subtype: mechanic
tags:
- siege
- storm_rising
- pointy_hat
title: Siege Rules
type: concept
updated: '2026-04-24'
summary: "Siege Rules are a combat overlay for battles where normal 5e combat cannot represent the scale: armies besieging a fortress, enormous monsters attacking a city, or conflicts wit..."
---

# Siege Rules

Siege Rules are a combat overlay for battles where normal 5e combat cannot represent the scale: armies besieging a fortress, enormous monsters attacking a city, or conflicts with too many participants to run individually. They do not replace character combat. They add a large-scale **Siege Phase** at initiative count 20, before lair actions, while PCs and monsters still take normal turns.

## Core Procedure

- Each side is represented by a party with AC, HP, attack bonus, damage bonus, abilities, and Siege Actions.
- Siege Actions happen on initiative count 20, winning initiative ties and resolving before lair actions.
- At the start of each Siege Phase, each party rolls 1d20. Higher roll chooses and resolves a Siege Action first, then the lower roll resolves one, alternating until both sides have used their available actions.
- Each party can take up to 3 Siege Actions per Siege Phase unless a rule changes that limit.
- Each Siege Action can be used only once per round.
- The GM chooses enemy Siege Actions. The players collectively choose allied Siege Actions.
- Siege Attack Actions deal damage to the opposing party; on a miss, they deal half damage.
- Siege Effect Actions apply a debuff or disable; on a miss, they have no effect and any limited use is not consumed.
- Natural 20s do not double Siege damage dice.

## Cape Coral Siege Block

**AC:** 15, or 17 with [[Saltmother-Cathaysa|Harridan's Help]].
**HP:** 50, or 60 with Safe Haven.
**Attack Bonus:** +5.
**Damage Bonus:** +2.

**Casualties:** When [[Cape-Coral]] drops below each 10-HP threshold (40, 30, 20, 10), one named NPC may die. With Safe Haven, no casualty occurs at 50 HP.

**Blaze of Glory:** When an NPC dies and their Siege Action is lost, that action resolves one last time immediately. This use does not count against Cape Coral's 3 actions in that Siege Phase.

| Action | Type | Effect | Source |
|---|---|---|---|
| Armada Attack | Siege Attack | +5 to hit; 7 (2d4 + 2) damage | [[Rita]] |
| Artillery | Siege Attack | +5 to hit; 5 (1d4 + 2) damage | [[Fernan]] |
| Pirate Quartering | Siege Attack | +5 to hit; 7 (1d8 + 2) damage, or 8 (1d10 + 2) if the Kraken is below 25 HP | [[Aurum]] |
| Kindred Song | Siege Effect | +5 to happen; Kraken attacks have disadvantage until the start of the next Siege Phase | [[Atop-a-Rock]] |
| Trapping Net | Siege Effect, 1 use | +5 to happen; Kraken has 2 Siege Actions per Siege Phase until it frees itself | [[Mama-Magda]] |
| Whaler Turned Hunter | Siege Effect, 1 use | +5 to happen; permanently disables the last Siege Action the Kraken performed | [[Rayco]] |

## Kraken Siege Block

**AC:** 15.
**HP:** 50.
**Attack Bonus:** +5.
**Damage Bonus:** +2.

**As Above So Below:** The Kraken's Siege Actions determine which lair actions become available during character-scale combat.

| Action | Type | Effect | Linked Lair Action |
|---|---|---|---|
| Lightning Crown | Siege Attack | +5 to hit; 5 (1d4 + 2) damage | Lightning damage attacks have advantage and add one damage die until next round |
| Monstrous Wave | Siege Attack | +5 to hit; 5 (1d4 + 2) damage; if used directly before Lightning Crown, Lightning Crown deals +1 damage | Replenish Dredge Scullions and Dredge Servitors as needed |
| Tentacle Slam | Siege Attack | +5 to hit; 7 (2d4 + 2) damage | Grounded creatures make DC 14 Dexterity saves or fall prone |
| Targeted Attack | Siege Effect | +5 to happen; disables a selected Cape Coral Siege Action until the end of the next Siege Phase | None specified |
| Unchaining | Siege Effect, costs 2 actions | +5 to happen; ends one ongoing negative effect, and the source action is disabled until next Siege Phase | Hostile creatures make DC 14 Wisdom saves or become frightened of Kraken Tentacles until next round |

## Character-Scale Fight

The Kraken cannot be targeted directly. The fight uses 1-2 Kraken Tentacles, 3 Dredge Scullions, and 1 Dredge Servitor as the starting encounter. The encounter ends when the Kraken retreats, not when all minions are dead; Monstrous Wave should replenish enemies to preserve pressure.

Round order:

1. Creatures above initiative 20 act.
2. Siege Phase resolves.
3. One available Kraken lair action resolves.
4. Mariano's ritual counter decreases by 1 if present and concentration held.
5. Creatures below initiative 20 act.

## Mariano's Ritual

If the party helped Mariano, he arrives knowing the Kraken is Princess Lua. His ritual starts with a counter at 4 and decreases at initiative count 20 after the Kraken's lair action. Mariano has AC 14, +4 Constitution saves for concentration, no tracked HP, immunity to Dredge Servitor's Call of the Deep, and a position outside Kraken Tentacle reach. A failed concentration save prevents the counter from decreasing that round but does not reset it.

## Encounter End States

| End State | Result |
|---|---|
| Kraken HP reaches 0 | The Kraken retreats. If Mariano was helped, continue to Act IV; otherwise use Act V endings. |
| Cape Coral HP reaches 0 | The Kraken has destroyed the town enough to satisfy its goal and retreats. If Mariano was helped, continue to Act IV; otherwise use Act V endings. |
| Mariano completes ritual | Lua's transformation is disrupted and she flees toward [[Kings-Cove]]. Continue to Act IV. |

## Connections

- [[raw/ingested/Storm-Rising-Adventure]]
- [[Cape-Coral]]
- [[Princess Lua]]
- [[SRD-Actions]]
- [[Dravosi-Crown]]
