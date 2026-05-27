# Session Run Guide Reference

Use this reference when creating or revising a DM-only session run guide, Strong Start, scene menu, or table-prep packet. A run guide is a scannable operating document for the DM. It is not a script.

## Contents

- Workflow
- Context Loading
- Session State
- Scene Menu
- Strong Start
- Clocks And Threads
- NPC Faces
- Spotlight
- Secrets And Clues
- Cliffhanger
- Run Guide Template
- Quality Checks

## Workflow

1. Load context and verify paths.
2. Identify what is already in motion.
3. Choose the correct structure: scene menu, scene order, or hybrid.
4. Write the Strong Start.
5. Prepare active threads and clocks.
6. Draft NPC faces, spotlight targets, secrets, and possible cliffhanger.
7. Write or return the guide.
8. Run quality checks.

## Context Loading

Read in this order:

1. `content/shattered-sea/private/system/co-dm-config.md`
2. DM philosophy file from `dm_philosophy_ref`
3. `content/hot.md`
4. `content/shattered-sea/situations/index.md`
5. Most recent session material:
   ```bash
   rg --files content/shattered-sea/sessions | rg -i "session-.*(summary|recap|run-guide)|recap|summary" | sort
   ```
6. Relevant active situation files
7. Relevant PC, NPC, location, faction, item, ship, and rules pages
8. Relevant templates if writing a new page

If any required file is missing, say exactly what is missing and proceed only with the user's confirmation or a clearly marked assumption.

## Session State

Start by answering these from the wiki:

- Where is the party at session open?
- What was the last hard break point?
- What did players accomplish, reveal, break, promise, or ignore last session?
- Which situations are already active near the party?
- Which NPCs or factions have a reason to act now?
- Which PC hooks are hot?
- Which unresolved threads are close enough to be felt at the table?

Do not infer future party destination unless the wiki or the user explicitly says it.

## Scene Menu

Default to a scene menu: 2-4 simultaneous situations the players can approach in any order.

Each scene needs:

- **Situation:** What is happening right now and why it has pressure.
- **If engaged:** What players can discover, alter, prevent, gain, or worsen.
- **If ignored:** What changes without them.
- **Table hook:** A 1-2 sentence read-aloud or sensory opener.
- **Relevant pages:** Verified wikilinks the DM should open.

Use a scene order only when canon has already put the party inside a specific sequence, such as an unresolved combat, a cliffhanger, a ship crisis, or an arrival already established in the last session. Even then, keep later material modular.

Anti-railroad check: if scene B only works when players chose scene A, rewrite the prep. A scene may depend on established canon, not on a future player choice.

## Strong Start

Pick the highest-pressure current situation. Write the first thing the DM reads or says at the table.

Rules:

- Present tense.
- Second person when addressing the party.
- One concrete image.
- One immediate pressure.
- No recap.
- No "you wake up" opening unless waking is the crisis itself.
- No player emotion, decision, or interpretation.
- Load `ttrpg-writing`, apply player-facing prose mode.

Strong Start shape:

```markdown
## Strong Start

> [!read-aloud]
> [One short paragraph. The world is already moving. End at the decision point.]
```

Weak: "You wake up at the inn. It is morning. What do you do?"

Strong: "The longboat is already taking on water when Fisk's name cuts across the dock in a voice you recognize. Three men are running after the caller. One of them has a Crown pistol half-raised."

## Clocks And Threads

For session prep, clocks are usually pending pressure, not canon writes. Use `references/faction-simulation.md` if the user asks to advance clocks or write world changes.

For each active situation or faction near the session:

- Current state from the wiki
- What they want now
- What they do if unopposed during this session
- What the party can notice
- What page owns the source of truth

Format:

```markdown
| Thread | Current pressure | If ignored | Visible sign |
|---|---|---|---|
| [[Thread]] | ... | ... | ... |
```

## NPC Faces

List only NPCs likely to matter at the table. Cap at 8 unless the session is explicitly social or festival-scale.

For each NPC:

- Role in this session
- What they want right now
- What they know or can reveal
- Roleplay Prompt + Anchor from `ttrpg-writing` when NPC performance matters at table
- Verified page link or note that the NPC is inline/unfiled

Use this format:

```markdown
| NPC | Role | Wants now | Roleplay anchor |
|---|---|---|---|
| [[NPC]] | ... | ... | ... |
```

## Spotlight

Read the party roster, PC pages or primers, and recent session material. Identify PCs or players who have not had a meaningful moment recently.

A spotlight suggestion must attach to an existing pressure. Do not manufacture a scene whose only purpose is "give X spotlight."

Format:

```markdown
- **PC / Player:** [Existing scene or pressure] can spotlight them because [specific connection to their choices, hooks, dials, or current problem].
```

## Secrets And Clues

Prepare 5-10 discoverable facts. Do not bind them to one required scene.

Rules:

- State what is true.
- Offer several possible discovery vectors.
- Separate DM-only truths from player-safe clues.
- Do not make a critical clue available through only one roll.

Format:

```markdown
- [Truth] - could surface through [NPC], [environment], [document], or [consequence].
```

## Cliffhanger

Do not plan an ending. Identify the highest-tension state worth recognizing if it happens.

Format:

```markdown
## Possible Cliffhanger

If the session ends here, [specific unresolved pressure is visible and active].
```

## Run Guide Template

When writing to the wiki, use verified session numbering and existing folder patterns.

```markdown
---
title: "Session NN - Run Guide"
campaign: shattered-sea
type: concept
subtype: plan
publish: false
audience: dm
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
session_number: N
tags:
  - session-prep
  - guide
sources:
  - Homebrew
summary: "At-table run guide for Session NN: [primary pressure, key scenes, expected duration]."
---

# Session NN - Run Guide

## Session State At Open

| Field | State |
|---|---|
| Party location | [[Verified Location]] |
| Immediate pressure | ... |
| Last session break | ... |
| Expected table time | ... |

## Strong Start

> [!read-aloud]
> ...

## Have Open At The Table

| What | Why | File |
|---|---|---|
| ... | ... | [[Verified Page]] |

## Scene Menu

> These are live situations, not a required sequence.

### [Scene Name]

**Situation:** ...
**If players engage:** ...
**If players ignore it:** ...
**Hook:** ...
**Relevant pages:** [[...]]

## Active Threads And Clocks

| Thread | Current pressure | If ignored | Visible sign |
|---|---|---|---|
| [[Thread]] | ... | ... | ... |

## NPC Faces

| NPC | Role | Wants now | Roleplay anchor |
|---|---|---|---|
| [[NPC]] | ... | ... | ... |

## Spotlight Targets

- **PC / Player:** ...

## Secrets And Clues

- ...

## Possible Cliffhanger

If the session ends here, ...

## DM Reminders

- ...

## Context Read

- [[Source Page]]
```

If the session is already in a fixed immediate sequence, rename `Scene Menu` to `Scene Order` for the fixed opening and add `Open Menu` for everything after the established crisis resolves.

## Quality Checks

- Strong Start has one image, one pressure, and no recap.
- Read-aloud text uses `> [!read-aloud]` and does not dictate player feelings or actions.
- Every scene has an "if ignored" consequence or is a resolved/required table logistics beat.
- No future scene depends on a specific player choice.
- Active clocks are visible through clues, rumors, NPC action, or changed environment.
- NPC count is table-manageable.
- Spotlight suggestions connect to existing PC hooks or choices.
- Secrets have multiple discovery vectors.
- Private information stays DM-only.
- Every wikilink was path-verified.
- If written to the wiki, frontmatter, `content/hot.md`, `content/log.md`, and relevant index updates are complete.
