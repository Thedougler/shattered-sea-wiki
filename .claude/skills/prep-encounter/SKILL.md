---
name: prep-encounter
description: >
  Design a combat encounter for the Shattered Sea campaign. Calibrates enemy count, CR,
  terrain, and mechanics to the specific party's empirical combat patterns. Invoke for:
  "design an encounter", "I need a fight for this session", "build a combat encounter
  with [enemy]", "make an encounter around [location]", "how many [monsters] should I
  use", "balance this fight for my party". Always calibrates to this party — never uses
  generic CR math without party-specific context. Requires combat-data-extract to have
  run at least once before calibrating.
---

> Cross-cutting rules (reading order, sandbox constraints, PC-connection requirement, frontmatter, auto-correct) live in `wiki/system/doctrine.md`. This skill covers only what's specific to its domain.

## Prerequisites

Prerequisites: see reading order in `wiki/system/doctrine.md`. Then read these domain-specific sources before generating any encounter content:
1. `wiki/system/party-combat-primer.md` — party combat patterns, Avoid flags (binding)
2. `wiki/dm/combat-analytics.md` — empirical patterns observed at this table

The party primer's **Avoid** section is binding. If your encounter would violate it, redesign before proceeding.

---

## Calibration Approach

Calibrate to empirical combat patterns, not theoretical class features. Mark anything
not yet observed at table as `[unconfirmed]`.

**Enemy count:** Use `references/CR-TABLES.md` for baseline math, then adjust using
observed action economy, sustained vs. burst damage, and focus-fire behavior from
combat-analytics.

**Terrain:** Always includes 2–3 actionable terrain features. Decorative is not
actionable — each feature must have a mechanical use available to both sides.

**Faction presence:** If this encounter involves a faction from `hot.md`, match their
current resource state (depleted, reinforced, desperate).

---

## Output Structure

1. **Encounter Brief** — one sentence: who, where, why now
2. **Enemy Roster** — names, stat block refs, role (controller / bruiser / skirmisher / artillery)
3. **Terrain** — 2–3 features with mechanical effects
4. **Tactical Notes** — how enemies open, how they escalate, morale/retreat threshold
5. **Stakes** — what changes in the world based on outcome (specific consequences, not generic)

Read `references/ENCOUNTER.md` before finalizing for the full toy template and field rules.

Load `ttrpg-writing` for all prose and formatting standards.

---

## Reference Files

| File | Read when |
|---|---|
| `references/ENCOUNTER.md` | Full encounter toy template, field rules, quality bar |
| `references/CR-TABLES.md` | CR scaling tables, party balance calculations |
| `references/5E-FIELDS.md` | Environment interactions — difficult terrain, cover, lighting, weather |
| `references/STAT-BLOCKS.md` | Encounter enemy stat block references |
