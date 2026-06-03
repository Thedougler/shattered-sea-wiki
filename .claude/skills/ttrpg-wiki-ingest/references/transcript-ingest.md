# Transcript Ingest

This preserves the guidance from the narrower `transcript-ingest` workflow inside the
general `ttrpg-wiki-ingest` skill. Use it for reviewed clean transcripts, not raw audio
logs.

## Entry Conditions

Run only when all are true:

- The transcript has already been cleaned.
- The flags file exists if the cleaning workflow generated one.
- `review_status: complete` is present, or the DM explicitly says the flags are resolved.
- `flags_resolved >= flags_total`, if those fields exist.

Do not ingest from a raw or partially reviewed transcript. Raw transcripts are evidence,
not final canon.

## Required Reads

1. `wiki/hot.md`
2. `wiki/system/party-session-primer.md`
3. `wiki/system/players/[pc]-sheet.md` if mechanical state changes are present
4. Existing session note for the same session, if any
5. Entity summaries for named NPCs, factions, places, ships, items, and deities mentioned

Use summary frontmatter first. Expand to full files only when updating them.

## Extraction Targets

Extract:

- `[CANON]` blocks.
- `[LORE]` blocks.
- `[RULING]` blocks.
- NPC appearances, offers, threats, deals, and departures.
- New named entities and aliases.
- Player decisions with forward consequences.
- Items gained, lost, spent, transformed, or promised.
- Faction moves and clues.
- Situation clock triggers.
- Combat data only when it reflects observed table behavior.
- Player interest signals.
- Table jokes only when they became in-world texture or recurring context.

Do not extract:

- OOC jokes with no in-world consequence.
- Player theories as canon.
- Ambiguous speaker text without DM review.
- Noisy transcription guesses.

## Session Note Output

Create or update `wiki/sessions/session-XX.md`.

Use frontmatter:

```yaml
---
type: session
subtype: session-note
campaign: shattered-sea
status: complete
audience: dm
publish: false
summary: "[Two-sentence max summary of what changed in the world]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [session]
sources: ["path/to/clean-transcript.md"]
session_number: XX
session_date: YYYY-MM-DD
---
```

Body sections:

```markdown
# Session XX

## Durable Changes
- ...

## Scene Log
- ...

## Entity Updates
- [[entity]] — change

## Situation And Faction Updates
- ...

## Rules And Rulings
- ...

## Open Questions
- ...

## Follow-Up Queue
- ...
```

Keep the scene log factual. The session note is the bridge from table events to wiki state,
not a dramatic recap.

## Entity Writeback

For each affected entity:

- Append to `## Session Events` or the local equivalent.
- Add relationships created in play.
- Update `summary` only if the entity's role has changed.
- Add source path to `sources` if this session is now evidence for the page.

Never overwrite a playable NPC voice or location key with session recap prose.

## Situation And Faction Writeback

For each pressure:

- If a clock advances, cite the session action or inaction that justifies it.
- If a new situation emerges, create a situation file before adding it to `hot.md`.
- If a situation appears resolved or dormant based on session events, move it to the correct folder immediately — update `lifecycle` and `status` frontmatter, update all inbound links, log the move. No DM confirmation needed.
- If a faction acts off-screen, coordinate with `world-update` or apply its clock citation rule.

## System File Updates

Transcript ingest may reveal needed updates to:

- `wiki/dm/player-interests.md`
- `wiki/dm/combat-analytics.md`
- `wiki/system/party-session-primer.md`
- `wiki/system/party-combat-primer.md`

If a system update is interpretive or strategic, create a "System File Updates Needed" section
in the session note and ask the DM before applying. If it is a direct factual update, apply it
and log it.

## Archive

When complete, archive the clean transcript with `archive_source.py --type transcript` so it
moves into `audio/sessions/` and drops off the `check_ingest.py` queue, then commit. If a raw
transcript of the same session also sits in `Inbox/`, the clean one supersedes it for ingest —
archive the clean version, and archive the raw one too (it becomes retained evidence, not a
second thing to ingest).
