# Decompose And Write Back

Use this when the source is ready to become durable wiki content.

## Decomposition Principle

A source is not one wiki page by default. It is a bundle of claims.

Extract claims, group them by canonical owner, then write each claim once. Other pages link
to that owner instead of copying the same information.

## Claim Buckets

| Claim | Canonical Home |
|---|---|
| NPC identity, public role, observable traits | `wiki/entities/characters/...` |
| NPC secrets, agendas, mechanics | DM companion or audience: dm page |
| Location facts and visitable features | `wiki/entities/places/...` |
| Faction agenda, resources, membership | `wiki/entities/factions/...` |
| Active pressure with timeline | `wiki/situations/active/...` |
| Waiting pressure with trigger | `wiki/situations/dormant/...` |
| Resolved pressure | `wiki/situations/resolved/...` only with DM approval |
| Portable scenario cluster | `wiki/islands/...` |
| Session chronology | `wiki/sessions/...` |
| Homebrew/ruling | `wiki/rules/...` |
| Player-facing handout | publish-safe page with `audience: players` |
| Current state and next pressure | `wiki/hot.md` |
| Structural operation | Git commit message |

## Extraction Pass

Make one pass for facts, not prose:

- Names and aliases.
- Places and paths.
- Relationships.
- Decisions made.
- Promises, threats, debts, obligations.
- Faction moves.
- Deadlines and clocks.
- Rules/rulings.
- Secrets the DM must know.
- Open questions.

Use exact source wording only for short names, quotes, and table-critical phrasing. Rewrite
everything else into concise wiki reference text.

## Canon Discipline

Do not promote a claim into canon if it is:

- Noisy transcript text.
- A joke with no in-world consequence.
- Speculation by players.
- An inference made by the agent.
- A possible future outcome rather than an established pressure.

Preserve useful non-canon material in session notes or DM notes as speculation, not fact.

## Writeback Order

1. Create missing concrete stubs first.
2. Update owner pages.
3. Add reciprocal links.
4. Update situation/faction clocks if current state changed.
5. Update `wiki/hot.md` if the table-facing state changed.
6. Regenerate `wiki/index.md` (`regen_index.py --write`).

This order prevents links from pointing to nowhere: stubs exist before owners reference them,
owners exist before reciprocal links, and the index reflects the finished file set.

## Page Update Pattern

When updating an existing wiki file:

1. Read frontmatter and the relevant section only.
2. Preserve existing facts unless the source clearly supersedes them.
3. Append session/source-specific events to activity logs instead of rewriting history.
4. Keep body prose DM-usable: terse, concrete, scannable.
5. Use `sources` frontmatter to cite the ingested source path when appropriate.

## Stub Creation

Create a stub only for a concrete entity or place with enough identity to route.

Minimum stub:

```yaml
---
type: entity
subtype: npc
campaign: shattered-sea
status: stub
audience: dm
publish: false
summary: "Stub created from source ingest; identity needs DM expansion."
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [stub]
sources: ["path/to/source.md"]
confidence_level: inferred
relationships: []
---
```

Body:

```markdown
# Name

> [!dm]
> Stub created during ingest from `path/to/source.md`. Expand before use at table.
```

Do not create stubs for vague references like "the crown", "a sailor", or "the old temple"
unless the source identifies them as a durable campaign object.

## Hot File Updates

Update `wiki/hot.md` only for live state:

- Party location or immediate arc changed.
- A PC thread advanced.
- A faction clock advanced or new trigger appeared.
- A situation became active, changed clock state, or resolved.
- A prediction is now outdated.
- Spotlight tracking changed after a session.

Do not use `hot.md` as a general summary bucket.

## Contradictions

When two established sources conflict:

1. Create `wiki/discrepancy-log.md` if missing.
2. Record both claims, source paths, and affected files.
3. Leave the wiki pages conservative.
4. Leave the source un-archived in `Inbox/` so it stays on the `check_ingest.py` queue.
5. Ask the DM for a ruling.

Do not pick the more interesting version.
