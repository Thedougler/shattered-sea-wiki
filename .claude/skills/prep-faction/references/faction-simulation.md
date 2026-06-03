# Faction And Thread Simulation Reference

Use this reference for `world-update`, thread review, run-guide clock prep, and any request to determine what factions, NPCs, or active situations do offscreen.

## Contents

- Modes
- Canon Discipline
- Context Loading
- Eligibility
- Planning Mode
- Advancement Mode
- Collisions
- Urgency
- Write Targets
- Faction Page Requirements
- Quality Checks

## Modes

### Planning Mode

Use during session prep. Identify likely offscreen pressure for the next session, but do not write canon changes unless the user explicitly asks.

Output: table-ready pending pressure.

### Advancement Mode

Use when the user asks to advance factions, tick clocks, run a world tick, or update the wiki between sessions. This may write canon changes after reading sources and confirming assumptions.

Prefer the `world-tick` skill for collaborative post-session advancement with rolls.

### Review Mode

Use when the user asks "what are my factions doing?", "thread review", "what happens next?", or similar. Summarize current state and likely next moves. Do not write.

## Canon Discipline

- Read the owning situation, faction, NPC, or location page before describing its state.
- Treat DM design notes as intent, not canon, unless a session record says they happened.
- Do not start a clock unless its trigger has fired.
- Do not invent NPC knowledge. Verify what the NPC could know.
- Do not assume where the party goes next.
- A low or stalled result should still change pressure, information, exposure, or positioning. "Nothing happens" is rarely useful.

## Context Loading

Read in this order:

1. `wiki/system/task-routing.md`
2. `wiki/hot.md`
3. `wiki/situations/active/`
4. Last session summary or recap
5. Relevant active situation files
6. Relevant faction pages
7. Relevant NPC, place, ship, item, and PC pages

Use `rg --files wiki | rg -i "slug-or-name"` and `rg -n "Exact Name" wiki/` to verify paths and inline mentions.

## Eligibility

Prioritize threads that the players can feel soon.

A thread qualifies if:

- The party directly engaged with it this session or recently.
- A known faction or NPC has a reason to react to party action.
- The party ignored an active pressure they had reason to know about.
- The situation has a visible ticking clock near the party.
- The config marks it as active for co-DM tracking.

Usually skip:

- Distant factions the party has never encountered.
- Background lore with no current pressure.
- Threads whose trigger condition has not happened.
- Secrets that would only advance because they are dramatically convenient.

## Planning Mode

For each eligible faction or thread, produce:

```markdown
| Thread | Current state | Likely offscreen move | What becomes visible | Source |
|---|---|---|---|---|
| [[Thread]] | ... | ... | ... | [[Source]] |
```

Keep planning language conditional:

- "If unopposed, they will..."
- "Likely pressure for next session..."
- "Visible sign the party may notice..."

Do not update source pages in planning mode.

## Advancement Mode

When canon should advance:

1. Present the proposed tick list and one-line rationale for each item.
2. Ask the DM to confirm additions, removals, or order unless the user explicitly asked for autonomous advancement.
3. For each thread, read the owning file in full and the relevant entity pages.
4. State the entity's concrete offscreen goal in one sentence.
5. Resolve using the DM's chosen method:
   - If using `world-tick`, ask for a d20 and apply its bands.
   - If no roll is requested, choose the most plausible result from established resources, opposition, time, and player interference.
6. Write the result to every page that now owns changed state.
7. Update `updated: YYYY-MM-DD` on every touched page.
8. Refresh `wiki/hot.md`.

World-tick roll bands:

| Roll | Result | Meaning |
|---|---|---|
| 1-5 | Setback | Attempt fails or backfires; pressure shifts in a visible way. |
| 6-15 | Partial | Real progress with friction, exposure, cost, or complication. |
| 16-20 | Full | Goal is accomplished; world state changes cleanly. |

## Collisions

If two factions or situations act against each other, resolve the collision instead of advancing both independently.

Check:

- Resources and leverage
- Proximity
- Knowledge
- Timing
- Temperament
- Player interference

Output:

```markdown
**Collision:** [[Faction A]] and [[Faction B]] both move on [target]. [Result]. [What the party can notice].
```

## Urgency

Use urgency to decide placement in a run guide.

| Level | Meaning | Use |
|---|---|---|
| low | Active but background | DM reminder or clue list |
| medium | Consequences become noticeable soon | Scene menu candidate |
| high | Consequence likely before or during next session | Scene menu priority |
| critical | Goal resolves this session if uncontested | Strong Start candidate |

## Write Targets

When advancement writes canon, update every relevant source of truth:

- **Situation file:** current state, clock, session log, consequences
- **Faction page:** goals, resources, offscreen action, relationships
- **NPC page:** status, location, wants, relationships
- **Place page:** current hooks or visible state
- **Session overview/run guide:** only if the prep document itself changed
- **`wiki/hot.md`:** active campaign state and recent activity

Do not bury changed state only in `hot.md` or a run guide. The owning page must change too.

## Faction Page Requirements

Active faction pages should follow `templates/faction.md` and include:

```yaml
---
title: "Faction Name"
category: faction
type: faction
subtype: faction-summary
publish: true
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
summary: "One-line role and campaign relevance."
tags:
  - political
  - active_arc
campaign: shattered-sea
audience: players
sources:
  - Homebrew
---
```

Useful sections for clock work:

- `## Goals`
- `## Off-Screen Action`
- `## Key Members`
- `## Relationships`
- `## Hooks`
- `## Related Pages`

If a faction page lacks these, update only the fields needed for the current task unless the user asked for a full page repair.

## Quality Checks

- Every advanced thread had an eligible reason to move.
- Every state claim was read from an owning page or marked as a proposal.
- Clock triggers were verified.
- Player action from the last session was accounted for.
- Faction collisions were resolved once, not double-counted.
- Results create visible pressure or information, not invisible bookkeeping.
- No private design note was treated as public canon.
- Every changed state was written to its owning page.
- `wiki/hot.md` was updated after writes.
