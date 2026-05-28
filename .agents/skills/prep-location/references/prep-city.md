# D&D 5e City Builder (Pointy Hat Theme Park Method)

Build a city with the user through a short interview, then output a complete Obsidian markdown
document filed into the vault.

The goal isn't to build a realistic city — it's to build a theme park and lie to your players
that it's a city. They won't notice. Concentrate all your design energy on what the players will
actually *do* here, not on the city's waste disposal system.

---

## Pre-Flight

Run these in parallel before starting the interview. Do not skip.

```bash
cat wiki/index.md
grep -rl "[City Name or slug]" wiki/ --include="*.md"
```

- If `index.md` contains the city name: stop. Read the existing page. Update/extend it — do not recreate.
- If `grep` returns results: read the top 2–3 matching files for established canon facts. Carry
  those facts into the interview to avoid contradictions.
- If nothing is found: the city is new. Continue to the interview.

Auto-fix any YAML errors encountered silently — wrong `type`, missing required fields, incorrect
`subtype` — correct without asking.

---

## The Method

Three principles:

**Theme.** One strong visual concept. Not abstract emotions — something you can see. It shapes
the look, the structure, and crucially, the ride concepts.

**City Goal.** The party needs something from this city, and getting it requires doing things.
This is the connective tissue that turns isolated attractions into a web of consequences.

**Rides.** Situations the players can engage with. Not shops. Rides. Each one should serve at
least two specific players and connect to the city goal. The theme generates the ride concepts —
don't just flavor a generic template, let the theme suggest what kind of trouble exists here.

---

## Interview Flow

Work through these steps conversationally. Don't dump all questions at once.

### Step 1: The Basics
Ask:
- City **name** (or shall we make one)?
- **Setting context** — where does it sit? (coastal, crossroads, deep wilderness, etc.)
- Roughly what **tier of play**? (levels 1–4, 5–10, 11–16, 17+)

### Step 2: The Theme
Ask what **feeling or visual** the DM wants. Offer 3–5 sharp suggestions based on the setting
context if they're unsure. Push for something immediately visual — if they say something abstract,
redirect.

Good themes: Undeath, Hell, Underwater, Holy, Art, Gold, Rot, Ice, Smoke, Blood, Tides, Glass,
Iron, Carnival, Education, Industry, Hunger, Law, Memory

Weak themes: Hope, Corruption, Mystery, Danger — too abstract. Ask: what does that *look like*?

Once the theme is locked, spend a moment deriving one structural implication — how does this theme
shape how the city actually works? This structural detail is what makes rides feel specific rather
than generic.

Write a **1–2 sentence** city identity blurb and confirm with the user before continuing.

### Step 3: The City Goal
Ask: **What does the party need from this city?** There should be one overarching thing — a vote,
a person, an object, an alliance, a way out. Every ride becomes a step toward it, a complication
of it, or an obstacle between the party and it.

If the DM doesn't have one, offer 2–3 options that fit the theme. Then establish: roughly how
many gatekeepers stand between the party and the goal? (3–4 is a good number for a medium-length
city arc.) Each ride should unlock or complicate one of those gatekeepers.

### Step 4: The Players
Ask the DM to describe each **player** briefly — not just their character's class, but what they
actually gravitate toward at the table. What makes them sit forward?

- Martial builds (fighter, barbarian, paladin) → probably want to hit something meaningful
- Dex/stealth builds (rogue, ranger) → want moments where being sneaky is actually the right call
- Charisma builds (bard, warlock, sorcerer) → want social stakes where what they say matters
- INT builds (wizard, artificer) → want puzzles, investigation, things to figure out
- Support/utility builds (druid, cleric) → want situations where their toolkit solves something
- Anyone with a strong backstory → wants the city to notice that backstory and poke at it

Push past class if the DM knows more. "She's a barbarian but she loves the moral dilemma stuff" is gold.

### Step 5: The Rides
Design **3–5 rides** (fewer for a small town, 4–5 for a major hub). Each ride should:

1. **Connect to the city goal** — completing it should move the party closer to what they need
2. **Serve at least 2 specific players** — not player types, specific people
3. **Have a moral or dramatic complication** — this is what makes players lean in
4. **Flow from the theme** — the theme is what makes this ride possible

**Rides are NOT shops.** If it's just commerce, cut it. The exception: a shop where the
interaction is the adventure.

| Structure | Naturally serves |
|-----------|-----------------|
| Tournament / combat gauntlet | Martial players |
| Infiltration + extraction | Stealth players |
| Ball / masked event / performance | Social players |
| Lab / ruin / abandoned district | Puzzle players |
| Investigation / gathering evidence | INT/social |
| Moral job — assassination, betrayal, blackmail | All players |
| Rally the powerless / find the resistance | Social + martial |

The best rides combine two of these. Present the rides as a short list before writing the full
document. Adjust based on feedback.

---

## Output Format

Once the interview is complete and the user approves the ride list:

**Step 1 — Resolve the file path.**

```bash
find content/ -iname "*[city-slug]*" -o -iname "*[city-name]*" | sort
```

If a file exists, use its exact path. If nothing is found, create at
`content/shattered-sea/places/[city-slug]/index.md`. If `find` returns multiple matches, read
each and use the location page.

**Step 2 — Prose chain. Execute in order.**

- **2a.** Read `references/dm-reference-standards.md` for DM sections and `references/player-facing-prose.md`
  for the arrival read-aloud block.
- **2b.** Draft the full page.
- **2c.** Apply DM-facing mode to all prose sections (Overview body text, Ride descriptions, Notable Locations).
- **2d.** Apply player-facing mode specifically to the `> [!read-aloud]` arrival block.
- **2e.** Run the anti-slop pass from SKILL.md on the complete page.

```markdown
---
title: "[City Name]"
category: location
type: location
subtype: town
settlement_type: [city | port | harbour | village | free-port | fortress-port | other]
publish: true
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
summary: "[One sentence: what kind of settlement, where it is, why it matters]"
aliases: []
tags:
- [city | harbour | village | town]
campaign: shattered-sea
audience: players
region: "[region_slug]"
parent_location: "[[Region or Island Name]]"
governance: "[who runs it]"
access: "[open port | restricted | hidden | other]"
confidence_level: medium
sources:
- Homebrew
relationships:
- relation: part_of
  target: "[parent place]"
---

# [City Name]

> [1–2 sentence theme-flavored identity blurb.]

| Field | Detail |
|---|---|
| **Theme** | [Core visual theme word] |
| **Tier** | [Levels X–Y] |
| **Party Goal** | [What the party needs from this city — one sentence] |
| **Location** | [Where it sits, what region] |
| **Controlled By** | [[Faction or power]] |

---

## Overview

> [!read-aloud]
> [Arrival read-aloud: 3–4 sentences. Second-person present tense. Slow zoom — atmosphere →
> specific detail → one unresolved sensory hook. Three senses minimum. No em dashes.]

[2–3 sentences of DM-facing follow-up. What structural detail shows how the theme actually runs
the place? What does the GM need to know that the read-aloud didn't say?]

---

## Rides

### [Ride Name]
*Players: [actual player names/handles]*
*Goal connection: [what this ride unlocks or complicates]*

[3–4 sentences: what the situation is, how the players get drawn in, what's at stake, and what
the moral or dramatic complication is. Open outcomes — don't script what the players choose.]

---

## How the Rides Connect

[1–2 sentences per ride: what happens if the party completes it, skips it, or makes the wrong
call on the complication?]

---

## Entry Hooks

[One hook per ride. Something the party physically encounters in the first hour. Land each hook
on a specific player — use their backstory, class, or known want.]

- **[Ride Name]:** [Hook — who it lands on and how]

---

## Notable Locations

[3–5 locations that anchor the city spatially. Only locations that connect to a ride.]

- **[Location Name]** — [One sentence.]

---

## NPCs

[Only NPCs who run a ride or gate the city goal. Two sentences max: name, role, one gimmick.
All NPCs are inline — no separate pages.]

- **[Name]** — [Role]. [Gimmick.]

---

## See Also

- [[Parent region or island]]
- [[Related faction]]
```

---

## Post-Write Vault Sequence

Run in order after writing the city page:

**1. Validate the written file.**

```bash
grep -c "^title:" [file-path]
grep -c "^category:" [file-path]
grep -c "^subtype:" [file-path]
```

If any required frontmatter field is missing or wrong: fix it silently.

**2. Check all `[[wikilinks]]` in the file.**

```bash
find content/ -iname "*target-slug*"
```

If a linked file exists: use its actual path. If it does not exist: remove the brackets and
leave the text bare. Never leave a broken wikilink.

**3. Update `wiki/index.md`.**

Add the city under the appropriate location section.

**4. Commit.**

```bash
git add wiki/
git commit -m "location: add [City Name]"
```

**5. Refresh `wiki/hot.md`.**

Update the `updated:` frontmatter field to today's date. Prepend one line to Recent Activity:

```
[YYYY-MM-DD] location: add [City Name] — [theme], [tier]
```

---

## Skill Handoffs

**NPCs needing a voice at the table:** if the DM wants to actually *perform* an NPC, use the
NPC Roleplay Prompt + Anchor system in SKILL.md to generate an immediately playable build.

**Rides that become live campaign threads:** once a ride goes active, file it as a situation
document using the template in `content/shattered-sea/situations/active/`. The ride description
in the city page is the seed; the situation file is the live operational document.

**Subsequent location pages** (individual buildings, districts, sub-sites within the city):
route through `references/LOCATION.md` and the matching template in `templates/`.
