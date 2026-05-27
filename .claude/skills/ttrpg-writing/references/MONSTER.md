# Wiki DnD — Monster Prep

> **Prerequisite:** `../PREP.md` loaded (philosophy, universal rules, PC gravity, roleplay method, naming conventions).

---

## The Four Laws

1. **One signature moment.** One thing no other monster does — what players describe after the session.
2. **Mechanics tell the story.** Every ability deducible from flavour. Can't explain it in one lore sentence? Cut it.
3. **Players are protagonists.** Design monsters that react to player choices.
4. **Complexity in decisions, not procedures.** Simple to run, rich to fight.

---

## Interview

If the user message doesn't already answer these, ask all at once:

- CR (or party level)
- Role (see table below)
- One-sentence concept
- Culture/origin
- Environment
- Legendary? Lair? Multi-phase?
- Party hook / PC connection

---

## Roles & Stat Arrays

| Role | Priority Stats | Notes |
|---|---|---|
| Solo Boss | STR + CON primary | High across board; legendary actions, lair actions, multi-phase |
| Elite | High single-round damage | Crowd control, 1 legendary action set |
| Standard | Efficient multiattack | One interesting ability, clear weakness |
| Minion | Low HP, pack tactics | Single attack |
| Skirmisher | High speed, medium stats | Bonus action mobility |
| Controller | INT or WIS 18+ | Save DC is the weapon; lower AC acceptable |
| Brute | STR 20+, CON 18+ | Low DEX/INT; advantage-on-damage or high-damage single attacks |
| Lurker | DEX 18+, low STR | Surprise, stealth, and conditions as primary threat vector |
| Artillery | High DPR at range, lower HP | Must have repositioning ability or it dies round 1 |

### Saves & Skills

Assign saves that make narrative sense — two or three maximum. Don't over-assign.

| Type | Typical Saves |
|---|---|
| Aberration | INT, WIS |
| Celestial / Fiend | WIS, CHA |
| Construct | CON |
| Dragon | DEX, CON, WIS |
| Undead | WIS |

Skills: only assign what the creature *actually uses at the table*. Perception on a lurker. Stealth on an ambush predator. Insight on a manipulator. Skip the rest.

---

## Ability Hierarchy

Build in order. Stop when you have enough.

1. **Tier 1 — Core Identity:** Multiattack (CR 2+) + the Signature Ability (one recharge/limited/save-or-suffer)
2. **Tier 2 — Combat Texture (1–2):** Passive trait, reaction, or bonus action that changes fight dynamics
3. **Tier 3 — Flavour (0–1):** Minor mechanical weight only. Skip if Tiers 1–2 aren't solid.

Max 3 unique named abilities on a non-boss. No save-or-die without repeat save and damage on success.

**Anti-patterns — never do these:**
- More than 3 unique named abilities on a non-boss monster
- "Once per day" abilities that will likely never fire in a single combat
- Abilities with no way for players to interact with or counterplay
- Save-or-die with no repeat save and no damage on success
- Conditional damage bonuses with three or more conditions to track simultaneously

---

## CR Calculation

1. Defensive CR — effective HP in CR table (×1.5 for common resistance; ×2 for immunity to common type or B/P/S nonmagical)
2. Offensive CR — average damage per round across 3 rounds (÷3 for recharge 5–6; ÷2 for recharge 4–6)
3. Final CR = average of defensive and offensive CR
4. Adjust: +1 per 3 legendary actions; +1 for lair actions

Load `references/CR-TABLES.md` for full stat table, HP formulas, and damage expressions.

---

## Solo Boss — Legendary Suite

**Legendary Actions (3):** fast/reactive + pressure (terrain, minion, reveal) + 2-cost powerful.  
**Lair Actions (3):** environmental + repositioning + dramatic.  
**Legendary Resistance (3/Day):** include on any boss trivially ended by a single failed save.

Load `content/shattered-sea/reference/rules/Battlefield-Actions.md` for Solo Boss and Elite monsters.

---

## Multi-Phase

Max 2 phases (3 for campaign climax). Trigger at 50% HP. Phase 2 must feel *different* — new threat vector, not just stronger.

**Transition template:** "When [Name] is reduced to [X] Hit Points for the first time, [dramatic description]. [Name]'s statistics change as follows: [what changes]. Initiative order is not interrupted."

---

## Telegraphing

Include at least one of the three layers:

- **Environmental**: Tracks, smells, damage, remnants. Something physically wrong with the space.
- **Social**: An NPC who reacts — goes quiet, refuses to go further, laughs at the wrong moment.
- **Mechanical preview**: A previous victim showing the signature ability's effect. A distant glimpse.

Write telegraphs as concrete, ready-to-use descriptions the DM can drop into an earlier scene.

**After the fight** — always answer: what can be salvaged? What consequence follows in the world? What question is left unanswered?

---

## Lore & Ecology

Write in present tense, third person. Authoritative but not encyclopaedic. One specific detail beats three adjectives. Never mention dice, DMs, or game mechanics in flavour prose.

**Structure:**

1. **Opening Hook** *(1–2 sentences)*: The most arresting thing. A striking image or chilling fact. Must make a DM want to use this creature.
2. **Nature & Origin** *(1 paragraph)*: What is it, where does it come from, what drives it?
3. **Behaviour & Ecology** *(1 paragraph)*: Where it lives, how it hunts, what it wants day-to-day.
4. **In the World** *(1 paragraph)*: What scholars or folk believe — include a rumour or misconception.
5. **Adventure Hooks** *(3 bullets)*: Concrete, ready-to-use. Not "players might hear about this" — a specific person, place, and event.

## Toy Fields

- **Toy fields (5):** `primary_goal`, `consistent_method`, `active_problem`, `performance_hooks`, `link_of_relevance` — same as NPC.
- **Roleplay Concept:** mandatory for intelligent monsters. Skip for mindless beasts/constructs.

## Encounter Brief

Include with every monster. DM-only.

- **Battlefield**: Terrain, choke points, hazards (2–3 sentences)
- **Tactics**: How it opens, what it prioritises, how it responds to being bloodied (3–4 sentences, specific)
- **Pacing**: The emotional arc. When does the signature ability fire?
- **The Moment**: The single most memorable beat. Design backwards from this.

**Tactical Personality** — pick one to govern all decisions:

| Personality | Behaviour |
|---|---|
| Apex Predator | Targets weakest first. Retreats only when cornered |
| Pack Hunter | Coordinates with allies. Piles on one target |
| Territorial | Attacks anything near lair. Won't give chase |
| Cunning | Targets casters/healers. Uses terrain. Feigns weakness |
| Relentless | Fixates on one target. Ignores flanking |
| Protective | Attacks whoever hit its ward. Interposes itself |
| Chaotic | Rolls or chooses randomly. Unsettling and unpredictable |

---

## Final Check

Before presenting any monster, confirm:

- Signature moment identified — describable in one sentence
- Mechanics match the flavour — a player could guess why the ability exists
- Ability count appropriate — non-boss ≤ 3 unique abilities; boss ≤ 5 plus legendary suite
- Encounter brief written — DM knows how to open the fight and what the big moment is
- Telegraph exists — at least one way for players to learn this is coming
- Lore hook present — at least one sentence of why this exists in the world
- CR validated — defensive and offensive CRs calculated and averaged
- No anti-patterns — no generic descriptors, no passive lore, no five-condition mechanics

If more than two are missing, revise before presenting.

## Output

Monster page with inline statblock. Load `../STATBLOCK.md` for the `statblock` codeblock format — required for all monster pages.

For quality and format exemplars, load `references/MONSTER-EXAMPLES.md`.

Default: single-note entry (frontmatter + H1 + inline statblock). Template: `templates/monster.md`.

Run vault filing sequence from `../PREP.md` § Vault Filing after writing.
