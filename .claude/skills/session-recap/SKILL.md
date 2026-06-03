---
name: session-recap
description: >
  Post-session cascade: take session notes and propagate updates across the wiki.
  Invoke for: "session recap", "process session notes", "update the wiki after session",
  "what changed this session", "post-session update", "cascade session". Takes raw session
  notes (from Inbox or pasted) and produces: a session recap file, hot.md updates, situation
  file updates, faction clock review, CLAUDE.md party block update, and spotlight tracking
  refresh. Ensures nothing drifts after a session.
disable-model-invocation: true
---

> Sandbox rules are in CLAUDE.md (always loaded). Operational rules: see `.claude/skills/ttrpg-llm-wiki-init/references/`.

## What this produces

A coordinated update across every file that tracks current world state, triggered by one set of session notes. Without this, post-session updates are scattered across hot.md, situation files, faction pages, and the CLAUDE.md party block — easy to miss one.

## Inputs

One of:
- A file in `Inbox/` (e.g. `Inbox/Session-04-Notes.md`) — raw session notes
- Pasted text in the conversation — the DM's notes from the session
- A request like "process session 4" — look for the most recent unprocessed Inbox file

If no notes are provided, ask for them.

## Workflow

### 1. Read current state

Read in this order, stopping when you have enough:
1. `wiki/hot.md`
2. The most recent `wiki/sessions/session-NN-recap.md` — for continuity and tone
3. Active situation files in `wiki/situations/active/` relevant to the session
4. Entity pages referenced in the notes (summary frontmatter first; full page only if needed)

### 2. Write the session recap

Create `wiki/sessions/session-{NN}-recap.md` following the established pattern:
- Frontmatter: `type: session`, `subtype: recap`, `audience: players`, `publish: true`
- Include `session_number` and `session_date` in frontmatter
- Player-facing prose — what happened as the players experienced it
- Load `ttrpg-writing` for prose standards
- Wikilink every named entity on first mention

### 2b. Generate scene art

Load `ttrpg-visual-aids` to generate session art for each major narrative beat.
Category: **Session art** (16:9 widescreen). Place between narrative sections at
the scene break each image illustrates. One image per major beat, max.

### 3. Update hot.md

Update each section of `wiki/hot.md`:
- **Current Arc** — where the party is now, what changed
- **Open PC Threads** — add new threads, update existing ones, close resolved ones
- **Faction Clocks** — note any advances (defer canon clock writes to `world-update`)
- **Live Situations** — update status, party awareness, next beat for each
- **Predictions** — revise: which came true, which are stale, what's new
- **Spotlight Tracking** — reset "Sessions Since" for PCs who had moments, increment others
- Update the `# hot.md — Updated YYYY-MM-DD` header

### 4. Update situation files

For each active situation affected by the session:
- Update status, notes, and next-beat fields
- Move fully resolved situations to `wiki/situations/resolved/`
- Create new situation files for threads that emerged this session

### 5. Update CLAUDE.md

Update the **Current arc** line and the **Active Factions** table in the repo-root `CLAUDE.md` to match the new hot.md state.

### 6. Create or update entity files

If the session introduced new named NPCs, locations, or items:
- Create stub entity files with proper frontmatter (use `prep-npc`, `prep-location`, etc. patterns)
- Update existing entity files if the session revealed new information

### 7. Commit

Stage all changed files and commit: `ingest: process session NN recap and cascade updates`

## Quality gate

Before committing, verify:
- [ ] Session recap reads as player-facing prose, not DM notes
- [ ] hot.md reflects the world state at the END of the session
- [ ] Every new entity mentioned in the recap has a wikilink and at least a stub page
- [ ] Spotlight tracking is current
- [ ] No situation file still references pre-session state
- [ ] Predictions are revised, not just appended to
