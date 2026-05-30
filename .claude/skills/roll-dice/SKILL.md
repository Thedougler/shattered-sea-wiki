---
name: roll-dice
description: >
  Use when ANY dice roll is needed — ability checks, attack rolls, saving throws, damage,
  random tables, or any outcome that should be left to chance. ALSO use when you catch
  yourself about to pick or invent a number for a random outcome. You CANNOT generate
  randomness — you MUST call the bundled roll.sh script. Triggers: "roll", "check",
  "save", "attack", "damage", "d20", "advantage", "disadvantage", any NdX notation.
---

# Roll Dice

## The Rule

**You cannot generate random numbers. You must call `roll.sh` for every dice roll.**

LLMs do not have access to entropy. Any number you "pick" is a pattern-matched guess, not
a roll. The bundled `roll.sh` uses the system's random number generator. It is the only
source of truth for dice outcomes in this campaign.

## Usage

```bash
.claude/skills/roll-dice/roll.sh <dice> [-a|-d] [+/-modifier]
```

| Example | What it does |
|---|---|
| `roll.sh d20` | Standard d20 roll |
| `roll.sh d20 -a` | Advantage — rolls twice, keeps higher |
| `roll.sh d20 -d` | Disadvantage — rolls twice, keeps lower |
| `roll.sh d20 +5` | d20 + modifier |
| `roll.sh 2d6` | Roll two d6, sum them |
| `roll.sh 3d8 +3` | Roll three d8, sum, add 3 |
| `roll.sh d100` | Percentile roll |

Output is a single integer. Nothing else.

## The Result Is Canon

The number `roll.sh` returns is the true outcome. Period.

- If the roll ruins the DM's planned moment — it stands.
- If the roll trivializes a hard encounter — it stands.
- If the roll kills a beloved NPC on a random table — it stands.
- If the roll is a natural 1 on the climactic save — it stands.

**The dice are the ultimate arbiters of truth.** The DM and the user both want this. Do not
fudge, re-roll, reinterpret, or narratively soften a result. Report it and play it straight.

## Red Flags — You Are Violating This Skill

- Saying "let's say you roll a 15"
- Picking a number that conveniently fits the narrative
- Deciding an outcome without rolling when a roll was called for
- Re-rolling because the result "doesn't make sense for the story"
- Adding narrative caveats that undermine a bad roll ("but fortunately...")
- Using words like "roughly" or "about" instead of the exact result

**If you catch yourself doing any of these: stop, call roll.sh, use that number.**

## When to Roll

Roll when the rules or the DM (user) call for it. Common triggers:

- Ability checks (Athletics, Perception, Persuasion, etc.)
- Attack rolls
- Saving throws
- Damage rolls
- Random encounter tables
- Any "roll a dX" instruction from the user
- Any situation where success/failure should be uncertain

**When NOT to roll:** Passive checks, fixed DCs the DM has already decided, or when the
user says "skip the roll" / "auto-succeed."
