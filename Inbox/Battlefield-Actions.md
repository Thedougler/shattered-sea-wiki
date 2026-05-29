---


title: Battlefield Actions
type: concept
publish: false
created: '2026-04-24'
updated: '2026-04-24'
tags:
- rule
- reference
- combat
subtype: rule
confidence_level: medium
sources:
- raw/ingested/Pointy Hat Battlefield Actions
summary: "Pointy Hat's system for making boss fights dynamic. Each Battlefield Action shifts the players' objective away from pure damage-dealing for one full initiative round. Boss-only ..."
---

# Battlefield Actions

Pointy Hat's system for making boss fights dynamic. Each Battlefield Action shifts the players' objective away from pure damage-dealing for one full initiative round. Boss-only — never assign to minions or two monsters in the same encounter.

## How They Work

Every Battlefield Action has exactly two phases:

**Tell** — Announced at the *end* of the boss's turn. No damage. A vivid cue telegraphing what is coming and how to stop it.

**Resolution** — Triggers at the *start* of the boss's next turn. Players have the full initiative order between Tell and Resolution to respond.

Each action is either:

- **Neutralized** — players fully stop the effect (it doesn't trigger)
- **Mitigated** — players reduce but cannot prevent the effect

Give a boss at least 2 Battlefield Actions so the action rotates each round.

## Damage by CR

| Boss CR | BA Damage |
|---------|-----------|
| 3–9 | 3d10 |
| 10–16 | 9d10 |
| 17–23 | 11d10 |
| 24+ | 13d10 |

**Optional:** Use the monster's highest single-action damage instead for a less punishing variant.

**Save DC:** `8 + key ability modifier + Proficiency Bonus`

Damage type is determined by the monster's identity — a giant with a metal club deals Bludgeoning; a fiend with a flaming whip deals Fire. Never leave damage type ambiguous.

## Canonical BA Templates

### Summoning Minions

**Tell:** Two 10-foot-radius summoning circles appear on the battlefield. The faint outline of a monster begins to coalesce within each.

**Neutralization:** A creature stepping on a circle stops that minion from being summoned.

**Resolution:** If not neutralized, two minions are summoned to assist the boss.

---

### Cleave

**Tell:** The boss raises its weapon, readying a devastating attack. Whenever a creature deals damage to the boss, it faces that creature — changing the Cleave's [[Area-of-Effect|area of effect]].

**Mitigation:** A hardy character holds their attack until just before the boss's turn, ensuring the Cleave targets them. A ranged combatant hits last while others clear the cone. A rogue hits, disengages, and runs, pulling the Cleave toward themselves while remaining outside the area.

**Resolution:** The boss Cleaves a 15-foot cone in the direction it's facing. Each creature in the area makes a Dexterity save — full damage on failure, half on success.

---

### Ray

**Tell:** The boss coalesces magical energy into a ball on its palm. Whenever a creature deals damage to the boss, it faces that creature — changing the ray's direction.

**Mitigation:** A hardy character holds their attack until just before the boss's turn to redirect the ray toward themselves. Players must manage positioning to avoid the ray's path.

**Resolution:** A 5-foot-wide, 60-foot-long ray fires in the direction the boss faces. Each creature in the path makes a Dexterity save — full damage on failure, half on success.

---

### Enchanting Ballad

**Tell:** The boss enters deep concentration and begins a haunting melody. Creatures that hear it feel a growing sense of camaraderie with the boss.

**Neutralization:** Break the boss's Concentration as normal, or use *Silence* to prevent the song entirely.

**Resolution:** The creature with the lowest Wisdom score that can hear the song gains the Charmed condition until the song ends. It may repeat the save at the end of each of its turns.

---

### Watchful Eye

**Tell:** The boss opens its eyes; dreadful magical energy gathers as a pinprick of light in its pupil. Creatures its gaze falls on feel mounting dread.

**Neutralization:** Players must not be visible to the boss when Resolution triggers. Options: use the environment to block line of sight, take the [[Hide]] action, cast *Darkness*.

**Resolution:** All creatures the boss can see gain the Frightened condition. They may make a Wisdom save at the end of each of their turns to end the effect.

---

### Perfect Illusion

**Tell:** The boss creates three illusory copies of itself. Each copy begins to gather magical energy, preparing to attack.

**Neutralization:** Illusory copies share the boss's ability scores and AC but have only 1 HP. Players must destroy them before the boss's next turn.

**Resolution:** Each surviving illusory copy makes one attack against a creature, using an attack from the boss's stat block (not BA damage).

---

### Tactical Retreat

**Tell:** The boss concentrates on a spell; its form begins to slowly dematerialize.

**Neutralization:** Break the boss's Concentration as normal.

**Resolution:** If not neutralized, the boss teleports to a location of its choice, escaping the battle.

---

### Danse Macabre

**Tell:** The boss begins an enchanting dance. Creatures watching it feel an increasing urge to join.

**Neutralization:** Break the boss's Concentration as normal, or reduce the boss's speed to 0 (e.g., Restrained condition).

**Resolution:** All creatures hostile to the boss are under the effects of *Irresistible Dance* until the end of their next turn.

---

### Eruption

**Tell:** The boss punches the ground; cracks snake outward from the impact. Energy shines through the cracks, brightest at the epicenter, growing in power.

**Mitigation:** Players must move as far as possible from the impact point.

**Resolution:** The ground erupts. Creatures within 20 feet of the impact make a Dexterity save — full damage on failure, half on success. Creatures 25+ feet away make a Dexterity save — half damage on failure, none on success.

---

### Eye of the Hurricane

**Tell:** The boss generates a massive wind vortex centered on itself. Characters lose their footing, pushed outward and upward. The only calm zone is directly adjacent to the boss.

**Mitigation:** Players must move as close to the boss as possible.

**Resolution:** Creatures more than 10 feet from the boss make a Dexterity save — full damage and pushed 30 feet away on failure, half damage and pushed 15 feet on success. Creatures within 10 feet make a Dexterity save — half damage and pushed 15 feet on failure, no damage on success.

## Design Notes

- Mix action types: at least one that forces movement, one that targets Concentration.
- Too many movement-forcing actions can feel obstructive; too many Concentration-targeting actions feel repetitive.
- Adapt templates with monster-specific flavor; original actions are preferred when the monster has strong thematic identity.

## External Links

- [Pointy Hat: Battlefield Actions (written guide)](https://docs.google.com/document/d/e/2PACX-1vTjTP_2coEPSTQXcUX4AMlZGYRE2j0-5u9rV5nyjJUzYEMbRtTIGi46SrvNfBiPxgNWwH0Pig4Z2QuE/pub)

## Connections

- [[Villain-Design-Framework]]
- [[SRD-Actions]]
- [[Monsters]]
- [[Guide]]
- [[raw/ingested/Restrained]]

## Source

- [[raw/ingested/Pointy Hat Battlefield Actions|Source: Pointy Hat — Battlefield Actions]]
