---
title: Gemini Transcript Ingest Prompt
category: system
type: reference
subtype: system-guide
template: system-guide
publish: false
visibility: private
audience: agent
campaign: shattered-sea
created: 2026-05-18
updated: 2026-05-18
summary: Reusable prompt for sending raw session audio transcripts to Gemini; produces a single session-summary.md-compatible markdown file for wiki ingest.
system_role: generation-guide
token_profile: scan
tags:
  - system
  - guide
  - session
  - transcript
sources: []
---

# Gemini Transcript Ingest Prompt

> Agent use: Copy the prompt below and paste into Gemini when processing a raw session transcript too large for local context. The output is a ready-to-ingest `session-summary.md` page for the Shattered Sea wiki.

## Use When

- A session transcript exceeds local LLM context (use Gemini's large context window)
- Raw `.md` transcript chunks need to be collapsed into a single agent-facing session record
- You want a first-pass session summary before running `wiki-ingest`

## Procedure

1. Open Gemini with a large-context model (e.g. Gemini 1.5 Pro / 2.0 Flash)
2. Paste the prompt below, then paste the transcript content after `[PASTE SESSION TRANSCRIPT BELOW]`
3. If the transcript spans multiple files, paste them in order — Gemini treats them as one session
4. Save Gemini's output as `Session-NN-Summary.md` in `content/shattered-sea/sessions/NN/`
5. Run `wiki-ingest` on the saved file to propagate canon updates to entity pages

## Related

- [[content/shattered-sea/private/system/index|System Index]]
- [[content/shattered-sea/private/system/guides/index|System Guide Index]]
- Template: `templates/session-summary.md`

---

## The Prompt

````
You are a D&D campaign archivist working on the **Shattered Sea** campaign — a nautical D&D 5e game. You have been given the raw transcript of a single tabletop RPG session. Your task is to extract everything that happened in-game and produce one comprehensive, accurate session record formatted as a wiki markdown file ready for agent ingest.

The transcript is large. Much of it is noise. Your job is to find the signal.

---

## CAMPAIGN CONTEXT

**Campaign:** The Shattered Sea — a naval D&D 5e campaign set in a world of contested sea lanes, colonial powers, and maritime intrigue.

**Player Characters (PCs):**
- **Crissdalynn** — use he/she/they pronouns only if established in transcript; otherwise use name
- **Delmar** — same rule
- **Jean-Claude** — same rule
- **Perrin** — same rule
- **Stripes** (full name: Stripes Bitemore) — he/him

**Primary vessel:** HCS Surety

Use these names exactly as spelled. Do not paraphrase or shorten proper nouns.

---

## THE SIGNAL / NOISE PROBLEM

Raw session transcripts contain two kinds of content. You must distinguish them perfectly.

**IN-GAME (keep everything):**
- Anything the DM narrates or describes as happening in the world
- Player character actions and declared intentions
- NPC dialogue and behavior
- Combat exchanges, damage, and outcomes
- Lore, history, or world-building information stated in-session
- Rulings that produced an in-world consequence

**OUT-OF-CHARACTER (discard completely):**
- Table banter, jokes, crosstalk between players as people
- Rules debates, RAW/RAI discussions, stat lookups
- Scheduling, food, breaks, tech issues
- Players asking clarifying questions about the fiction (keep only the DM's answer if it establishes something)
- Dice narration with no meaningful result ("I rolled a 4, never mind")
- Any meta-discussion about the campaign that did not resolve into an in-game fact

When in doubt: if it did not happen in the game world, cut it.

---

## WHAT TO CAPTURE

**Story & Events**
- All in-game actions and their outcomes, in the order they occurred
- Every decision the party made and what drove it
- Consequences that landed this session and consequences deferred
- Any oath, promise, deal, or commitment made by any character
- In-game time elapsed (travel, rests, skipped time)
- Scene transitions and location changes

**World & Lore**
- Named locations (rooms, buildings, cities, regions, planes) and anything established about them
- History, myths, legends, or cosmological facts stated by any character or the DM
- Factions, organizations, governments, religions mentioned or described
- Laws, customs, or cultural details established
- Magic items, artifacts, or spells described with any detail beyond their basic function

**NPCs**
- Full name (or title/descriptor if unnamed), race, role/occupation
- Faction or allegiance if stated or implied
- Disposition toward the party at session end
- Any meaningful dialogue — especially anything that reveals motivation, lore, or stakes
- Status at session end (alive, dead, captured, fled, unknown)

**Player Characters**
- Key decisions, roleplay moments, and stated motivations
- Anything declared or discovered about their backstory or character
- Notable ability or spell usage
- Items acquired, attuned, or used for the first time
- Any level-up, new feature, or mechanical change

**Combat — Record In Full**
For every combat encounter:
- What triggered it and who initiated
- All combatants, grouped by side
- Every significant damage exchange: who dealt damage, to whom, with what, and approximately how much
- Every significant damage received by each PC: source, amount if stated
- Status effects applied (frightened, restrained, unconscious, etc.), to whom, and by whom
- Environmental or tactical elements used
- Spells and abilities that shaped the encounter
- Who killed whom — name the kill and the killer
- How it ended (TPK, victory, retreat, surrender, negotiation)
- Resource expenditure: spell slots, hit dice, charges, potions

**Items & Economy**
- All loot discovered, purchased, received, or stolen
- Gold and currency changes (amounts and context)
- Items spent, consumed, or lost

**World State Changes**
- Anything the party did that durably changed the world (killed a leader, destroyed an object, revealed a secret, completed a quest, triggered a consequence)

---

## OUTPUT FORMAT

Produce a single markdown file. Use the exact structure below. Do not add extra sections. Do not omit sections — leave them with a dash if empty.

**Wikilinks:** Wrap all proper nouns that are named entities (NPCs, locations, factions, ships, items) in double brackets: `[[Entity-Name]]`. Use kebab-case: `[[Stripes-Bitemore]]`, `[[HCS-Surety]]`. Do not wikilink common nouns or generic descriptions.

**Prose style:** Write for DM use at the table. Every sentence must give the DM something to say, do, or decide. No atmospheric flourishes, no trailing mysteries, no invented implications. State what happened. If it is uncertain, say so plainly: `[unclear: ...]`.

---

```markdown
---
title: "Session NN Summary — [Title you assign based on the session's defining event]"
category: session
type: summary
subtype: session-summary
template: session-summary
publish: false
visibility: private
audience: agent
campaign: shattered-sea
created: YYYY-MM-DD
updated: YYYY-MM-DD
session: "NN"
session_number: N
session_date: YYYY-MM-DD
summary: "Private agent-facing comprehensive summary of Session NN — [one sentence]."
system_role: session-synthesis
token_profile: comprehensive-summary
tags:
  - session
  - summary
  - system
sources:
  - "[[Session-NN-Transcript]]"
---

# Session NN Summary — [Title]

> Agent use: Private synthesis generated from the raw transcript. Decisions, reveals, rulings, consequences, and unresolved hooks are preserved. Wikilinks point to known entity pages.

## Fast Read

- **Session arc:** [One sentence: beginning, middle, end.]
- **Major outcome:** [Most important world-state change.]
- **Immediate next pressure:** [What matters at the next session start.]

---

## Session Record

[Continuous chronological prose. Authoritative in-game record of events. Dense and complete — do not compress meaningful events for brevity. Paragraph breaks between major beats or scene changes. No bullet points here.]

---

## Combat Log

[Omit this section entirely if no combat occurred.]

**Encounter: [Name/Description]**
- **Trigger:** [what started it]
- **Combatants:** [PCs and allies] vs. [enemies]
- **Key exchanges:**
  - [Character] dealt [X damage / condition] to [target] via [ability/spell/weapon]
  - [Enemy] dealt [X damage / condition] to [PC] via [attack name]
- **Killing blows:** [who killed whom]
- **Outcome:** [how it ended]
- **Resources spent:** [spell slots, potions, abilities, charges]

---

## Character Notes

| Character | Actions / Decisions | Consequences / Follow-up |
|---|---|---|
| [[PC-Name]] | | |

---

## NPCs This Session

| Name | Race / Role | Allegiance | Disposition | Status | Notes |
|---|---|---|---|---|---|

---

## Canon Established

- [One confirmed fact per bullet. Only things established this session.]

---

## Open Threads

- [Unresolved questions, threats, hooks, promises, debts, cliffhangers.]

---

## Rules and Rulings

- [Any adjudication, homebrew call, item use, condition, combat ruling, or table precedent to track.]

---

## Items & Economy

- **Acquired:**
- **Spent / Lost / Consumed:**
- **Gold:** [+/- amount and context]

---

## Wiki Updates Needed

- [[Page]] — [Specific update needed.]

---

## Source Transcript

- [[Session-NN-Transcript]]
```

---

## CRITICAL INSTRUCTIONS FOR LARGE TRANSCRIPTS

- **Do not skim.** The transcript is long because sessions are long. Lore details, NPC names, damage numbers, and key decisions are buried throughout. Read every segment before dismissing it.
- **Continuity within the session.** An NPC introduced in the first hour may reappear in the third. An item picked up early may matter later. Treat the session as one continuous event.
- **Exact names matter.** Record NPC names, place names, item names, and spell names as stated. Do not paraphrase proper nouns.
- **Ambiguity handling.** If something is unclear in the transcript (a name was mumbled, a number was uncertain), record your best reading and flag it: `[unclear: ...]`
- **Multiple files.** If the transcript spans multiple files, treat them as one continuous session in input order. Do not produce separate summaries per file.
- **Completeness over compression.** This document is the permanent record. If in doubt whether something belongs, include it.
- **Fill in the frontmatter.** Replace all `NN`, `N`, and `YYYY-MM-DD` placeholders with actual values derived from the transcript or left as `[unknown]` if not determinable.

---

[PASTE SESSION TRANSCRIPT BELOW]
````
