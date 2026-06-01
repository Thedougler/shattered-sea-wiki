# Source Triage

Use this after a source is selected and before making wiki edits.

## Triage Questions

Answer these from the source and current wiki context:

1. What is the source?
2. Is it raw, cleaned, reviewed, or DM-authored?
3. What durable facts does it contain?
4. Which wiki files should own those facts?
5. Which facts are uncertain, contradictory, or not yet canon?
6. Does it change current world state in `wiki/hot.md`?
7. Does it create new entities, situations, factions, locations, sessions, or rules?
8. Does it contain player-facing material that must be publish-safe?

## Source Types

| Type | Signs | Primary Output |
|---|---|---|
| `session` | session number, chronology, player decisions | `wiki/sessions/`, hot updates, entity activity logs |
| `transcript` | `.csv` with ID, Speaker, Text columns (no timestamps) | reviewed transcript workflow |
| `entity-source` | named NPC/item/vehicle/deity details | entity pages and reciprocal links |
| `situation-source` | pressure, deadline, unresolved conflict | active/dormant situation file |
| `location-source` | place, settlement, room keys, travel site | location page or island |
| `faction-source` | group agenda, membership, moves | faction page and clocks |
| `rules-or-homebrew` | mechanics, table rulings, class options | `wiki/rules/` and relevant character links |
| `handout-or-player-facing` | in-world text, public lore, recap | publish-safe player page |
| `character-sheet` | PDF form fields, ability scores, class/level, equipment | PC sheet page, combat reference, entity links |
| `asset` | image/audio/map supporting wiki content | asset source tracking and embeds |
| `research-or-guidance` | process guidance, writing standards | system/reference page only if useful |

## Ready, Blocked, or Skip

Mark a source `ready` only when:

- Its authority is clear.
- The owner wiki files are clear.
- Contradictions are either absent or logged.
- No unresolved DM judgment changes the facts being written.

Mark it `blocked` when:

- Two established facts conflict.
- A page identity is ambiguous.
- A situation lifecycle move is required.
- A player-facing/private boundary is unclear.
- A transcript still has unresolved flags.

Mark it `skipped` when:

- It is process research that should not enter campaign canon.
- It is a duplicate of a more authoritative source.
- It is an asset with no wiki use yet.
- The DM explicitly says not to ingest it.

A skipped source still has a content hash absent from `.raw/`, so it will keep showing up in
`check_ingest.py`. If the skip is permanent, archive it with `archive_source.py` so it moves
into `.raw/` and drops off the queue; note the skip reason in the commit message. If the skip
might be reconsidered later, leave it in `Inbox/` and tell the DM why.

## Triage Output

Before editing, write a brief working plan:

```markdown
Source: path
Authority: raw | cleaned | reviewed | DM-authored | derived
Status: ready | blocked | skipped
Expected outputs:
- wiki/path.md — why
Facts to preserve:
- ...
Flags:
- none
```

Keep this plan in chat. It is working scratch for the one source in front of you, not a
durable artifact — once the source is written back and archived, the plan's job is done.
There is no work-queue file to maintain; an interrupted run resumes by re-running
`check_ingest.py`, which still lists every source that hasn't been archived yet.
