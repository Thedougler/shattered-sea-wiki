---
type: system
subtype: task-routing
campaign: shattered-sea
status: unknown
audience: agent
publish: false
summary: "Read second after hot.md. Maps every task type to its required pre-reads and skill. Never generate content without completing the listed reads."
created: 2026-05-27
updated: 2026-05-27
tags: []
sources: [Unknown]
system_role: task-routing
token_profile: map
mandatory_for: []
update_trigger: "New system file added; task type added; mandatory read list changes"
---

# Task Routing — Shattered Sea

> Read this immediately after `wiki/hot.md`. Find your task type below.
> Read every listed file at the specified depth before generating any content.
> Required reads are not optional.

---

## Read Depth Notation
- `[FULL]` — read the complete file
- `[FAST-READ]` — read the summary/Fast Read section only; expand if insufficient
- `[SECTION: X]` — read only the named section
- `[SUMMARY-ONLY]` — read the frontmatter summary field only
- `[ON-DEMAND]` — read only if this specific entity is directly involved

---

## Routing Table

### Task: `encounter-design`
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `wiki/system/party-combat-primer.md` | `[FULL]` | Party capabilities and design rules |
| 2 | `wiki/dm/combat-analytics.md` | `[SECTION: Design Adjustments]` | Active design flags |
| 3 | `wiki/system/players/[pc]-sheet.md` (all PCs) | `[FAST-READ]` | Current resource state |

### Task: `session-prep`
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `wiki/system/party-session-primer.md` | `[FULL]` | Party context for this session |
| 2 | `wiki/dm/player-interests.md` | `[SECTION: Content Priority Queue]` | What to emphasize |
| 3 | `wiki/situations/active/[relevant]` | `[FAST-READ]` | Active threads |

### Task: `transcript-ingestion`
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `wiki/system/players/[all-pcs]-sheet.md` | `[FULL]` | Current mechanical state |
| 2 | `wiki/hot.md` | `[FULL]` | World state at session start |

### Task: `wiki-audit`
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `wiki/index.md` | `[FULL]` | Master catalog |
| 2 | `CLAUDE.md` | `[SECTION: Ideal State]` | Correction rules |

### Task: `live-co-dm`
> Mid-session, real-time. Latency beats completeness. SKIP init/lint/audit/index/frontmatter.
| # | File | Depth | Why |
|---|---|---|---|
| 1 | `latest_session_context.py` output | `[FULL]` | Live transcript tail + hot.md, one fast bundle |
| 2 | any single entity page | `[ON-DEMAND]` | Only via `ttrpg-wiki-query` for one specific fact |

See `.claude/skills/live-co-dm/SKILL.md`.

---

## System File Index

| File | system_role | mandatory_for | token_profile |
|---|---|---|---|
| `wiki/system/task-routing.md` | task-routing | all tasks | map |
| `wiki/system/party-combat-primer.md` | party-primer | encounter-design | always-read |
| `wiki/system/party-session-primer.md` | party-primer | session-prep | always-read |
| `wiki/dm/player-interests.md` | dm-intelligence | content-creation, session-prep | quick-ref |
| `wiki/dm/combat-analytics.md` | dm-intelligence | encounter-design | quick-ref |
