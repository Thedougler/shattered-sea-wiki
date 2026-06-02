# Dungeon Reference

Full template, room key examples, and topology patterns for `prep-dungeon`.

---

## Dungeon Frontmatter Template

```yaml
---
type: entity
subtype: dungeon
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "[One sentence: what this site is, who occupies it, why it matters now.]"
tags: []
sources: []
region: ""
verb: ""                    # Defend | Attract | Consume | Conceal
unstable_condition: ""      # Concrete state — not a vibe
consequence: ""             # What happens if no one intervenes — observable, specific
link_of_relevance: ""       # Which PC connects, one sentence
rooms: 0                   # Integer room count
cr_range: ""                # e.g. "1/2–3"
topology: ""                # linear | branching | hub | loop
---
```

---

## Room Key — Worked Example

This is the target format. Every room in Phase 4 should look like this.

```markdown
## Room 3 — The Shrine Nave

**Dimensions:** 40 × 25 ft. Ceiling 10 ft. Three exits: archway from Room 2,
stone door to Room 4, crawl passage to Room 5 (DC 12 STR or DEX to squeeze through).

> [!read-aloud]
> The plaster ends here. Bare stone, carved with hundreds of open hands — different
> sizes, overlapping, no obvious pattern except density. At the far end, a wide stone
> basin, waist-high, holds standing water that smells like rain, not canal.

**Features:**
- **Basin**: Clean water, faintly saline. Characters who drink taste salt briefly,
  then fresh. Not threatening — simply anomalous. (Detect Magic: faint transmutation)
- **Pressure Stone**: Original shrine mechanism, 5 ft in front of basin. (DC 14
  Perception to spot before triggering. On trigger: jet of canal water from concealed
  pipe — loud, not damaging, soaks carried paper. Audible in Rooms 2 and 4.)
- *Gold Coin*: Pre-Tessarine Calven mint in the basin among copper and silver
  offerings. (2 gp face, 10 gp to a collector)
- Carved inscription on archway lintel, archaic script. (DC 15 History to read
  partially: "...receive what the tide returns...")

> [!dm]
> Orientation room for the shrine mystery. Let players absorb the pre-Umberlee
> iconography without forcing conclusions. The pressure stone teaches: probe before
> you approach.
```

**What makes this work:**
- Point-first: each element starts with its noun
- Typographic encoding: bold for threats, italic for treasure, plain for environment
- Mechanics in parentheses, never buried in prose
- Read-aloud is 3 sentences — under the 4-sentence cap
- DM note states authorial intent (Skerples standard)
- Objective third person throughout

---

## Topology Patterns

### Linear
```
1 → 2 → 3 → 4 → 5 → 6
```
Worst topology. Only use for a lair with one natural passage (a cave, a tunnel).
Even then, add at least one shortcut or secret connection.

### Branching
```
1 → 2 → 3
      ↘ 4 → 5
           ↘ 6
```
Better. Players choose paths. But dead ends feel punishing — add loops where possible.

### Hub
```
    2
    ↑
4 ← 1 → 3
    ↓
    5 → 6
```
Central room connects to most others. Good for lairs, temples, throne rooms.
The hub room should be the most interesting space — players return to it repeatedly.

### Loop
```
1 → 2 → 3
↑       ↓
6 ← 5 ← 4
```
Best topology. Players circle back, discover new angles on rooms they passed, and
can approach encounters from multiple directions. Reward players who explore fully.

### Combined (recommended for 6+ rooms)
```
1 → 2 → 3 → 4
    ↕       ↕
    5 → 6 → 7
```
Mix hub and loop. At least two routes between the entrance and the most important room.
Secret connections add a third route for resourceful parties.

---

## The Chokepoint Test

Draw the room connections as a graph. Remove the entrance. If removing any single
non-entrance room disconnects the graph (i.e., rooms beyond it become unreachable),
that room is a chokepoint.

Chokepoints force linearity — the party MUST pass through that room. Fix by adding
an alternate connection that bypasses it.

**Exception:** A chokepoint is acceptable if it IS the encounter — a guardian, a locked
gate, a collapsed passage — AND the party has at least two ways to approach it.

---

## Dungeon-Specific Anti-Slop Checklist

Run after Phase 4, before finalizing:

- [ ] Every room starts with its noun, not an atmospheric opener
- [ ] No room description exceeds 3 supporting sub-points (Rule of Threes)
- [ ] Read-aloud callouts are 3–4 sentences max
- [ ] No "you" in DM-facing sections (only in `[!read-aloud]`)
- [ ] Negative constructions: max two per room
- [ ] No adjective survives the Deletion Test unless it signals a mechanic
- [ ] No contrastive reframes, "kind of" constructions, or rhetorical questions
- [ ] After any atmospheric sentence, the next sentence is plain and mechanical
- [ ] All DCs, stat values, and damage dice are looked up, not invented
- [ ] Every NPC has a proactive objective, not a reactive posture
- [ ] Treasure is specific: exact gp values, physical descriptions, named items
- [ ] Every wikilink verified via `rg --files wiki | rg -i "target"`

---

## Empty Room Test

No room should be empty. Every room was built for a purpose — traces of that purpose
remain. If a room has no current function, it must have:
- Evidence of its original function (architectural traces, faded markings, worn fixtures)
- Environmental texture (something the DM can describe that makes the space feel real)
- At least one interactable element (even if it's just a door, a lever, a loose stone)

"Nothing here" is never an acceptable room key entry.

---

## Encounter Placement

Not every room needs combat. A 6-room dungeon should have:
- 1–2 combat encounters
- 1 social encounter (NPC who can be talked to)
- 1 puzzle/exploration room (mystery, discovery, environmental challenge)
- 1–2 atmosphere/transition rooms (treasure, clues, environmental texture)

This ratio keeps pacing varied. Three combat rooms in a row is a slog. Three
exploration rooms in a row is a museum. Alternate.

---

## Treasure Calibration

Use the DMG treasure hoard tables as a ceiling, not a floor. Dungeon treasure
should feel earned and specific:

| Party Level | Total Dungeon Value (gp) | Notes |
|---|---|---|
| 1–4 | 50–200 gp | Working stash, not a hoard |
| 5–10 | 200–1000 gp | Accumulated wealth, one notable item |
| 11–16 | 1000–5000 gp | Significant cache, 1–2 notable items |

Every magical item must have:
- A specific physical description (what does it look like?)
- The exact manipulation to activate it (if applicable)
- One narrative hook (why would players care beyond the mechanic?)

"+1 sword" fails this test. A *corroded bronze falcata that hums when pointed
north and deals an extra d6 radiant damage against undead* passes it.
