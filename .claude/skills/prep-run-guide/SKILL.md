---
name: prep-run-guide
description: >
  Use when building or revising a session run guide — the at-the-table operating document for
  one session of play. Triggers: "/run-guide [N]", "prep tonight's session", "build a run guide",
  "what do I run Saturday", "help me run tonight". Also use when a guide feels hard to use at the
  table: NPC info scattered across files, content organized by in-game day instead of thread,
  images breaking scanning flow, too many files open during play, dense tables that don't scan.
---

## What this produces

A **session run guide**: one file the DM opens at the table and never leaves. Every NPC handle, every read-aloud, every roll, every consequence is at the point where they need it. Not a story, not a script, not a table of contents linking elsewhere.

## The iron rule: one file, one session

A run guide fails the moment the DM opens a second file. It also fails when it tries to cover more content than one session can hold.

**One file.** Everything the DM needs to run tonight is inline. Wikilinks are for depth chased between sessions, never for retrieval mid-play. A guide that is secretly a table of contents — even a well-organized one with day-by-day links — violates this rule.

**One session.** A run guide covers 3–5 hours of play, not a multi-session arc. A city sandbox that spans four sessions gets four run guides, each focused on the beats most likely to fire that night. The sandbox run guide or situation files hold the full arc; the session guide extracts and inlines.

**Max 5–7 scene cards.** More than 7 means you're prepping multiple sessions. Cut to the threads the party is most likely to pull, and point to the sandbox/situation files for overflow. Multiple cards may share a thread when that thread has distinct beats with different registers (e.g., a social "Nona names the favor" card and an exploratory "JC descends the tunnels" card both tagged *(Grung Raid)*).

**Scoping a multi-session arc.** If a sandbox spans more in-game days than one session can cover, ask: "what is the party most likely to pull on *tonight*?" Prep those threads. The remaining beats stay in the sandbox run guide (the arc-level parent document) or situation files — they'll feed the *next* session's guide.

### What you must never do

- Split a run guide into multiple linked files (day files, scene files, beat files)
- Organize scenes by in-game day — organize by thread instead
- Embed images in the operating text — art goes in a collapsed callout at the end or stays in situation files
- Prep more than 3 in-game days in a single guide — that's multiple sessions

## Three-zone architecture

Every run guide has three visual zones. The DM's eye moves through them predictably:

| Zone | Purpose | DM reaches for it | Position |
|---|---|---|---|
| **Dashboard** | State, strong start, thread status, NPC roster | Every 10 minutes | Top of file — first screen |
| **Scenes** | Self-contained scene cards, one per beat | When the party pulls a thread | Middle of file |
| **Reference** | Secrets, stall hooks, surprise procedure, cliffhanger | Once per session or on lookup | Bottom of file |

**Dashboard first.** One upward scroll always reaches the snapshot, thread strip, and NPC bench.

**Scenes organized by thread, not by day.** The DM thinks "they're pulling on the Warren thread," not "it's Day 2." Each scene card is tagged with its thread. For multi-day sessions, a compact Day Tracker in the dashboard shows what changes overnight — never separate day files.

**Reference for lookup.** Secrets, stall hooks, and the surprise procedure live at the bottom. The DM reaches for them by need (Ctrl+F), not by scrolling position.

## Visual aids

Scene art helps the DM set the tone and gives players something to look at during narration. Load `ttrpg-visual-aids` and `openrouter-image-gen` to generate images for the guide.

- **One image per scene card, max.** Place it at the top of the card, before the read-aloud. Follow `ttrpg-visual-aids` placement rules: blank line above and below, never inside callouts.
- **Dashboard has no images.** The dashboard is pure text and tables — the DM scans it every 10 minutes and images slow that down.
- **Scene art and tactical maps go inline.** A scene-setting image (Nona's kitchen, the shrine at dawn, a Grung handler in the crowd) anchors the DM in the beat. A tactical map (raid strike points, sewer layout) is operational. Both belong at the scene card where they're used.
- **Generate during prep, not at the table.** Run the generation workflow from `ttrpg-visual-aids` while writing the guide. If generation fails, leave a `[!visual-aid]` callout with the full prompt for later fulfillment.

## Formatting for speed

The guide is an operating document read under pressure with four players waiting:

- **Tables for scanning, prose for running.** Dashboard = all tables. Scene cards = callouts and tight bullets.
- **One-line NPC handles in the bench.** Full NPC detail (first line, wants, reveals) lives in the scene card where they appear. The bench is a 3-column quick-ref: name, grab-when, handle.
- **Thread tags on scene cards.** Parenthetical `*(Thread Name)*` after the scene title. Searchable.
- **Register tags.** `social`, `combat`, `revelation`, `exploratory` — energy level at a glance.

## Workflow

1. **Ground in current state.** Read `wiki/hot.md` (always) → latest recap → active situations near the party → relevant entity pages (summaries first). Stop when you have enough.
2. **Scope the session.** What is the party in the middle of? Which 3–5 threads can fire tonight? How many in-game days will this session likely cover (max 3)? Cut aggressively.
3. **Build the dashboard.** Session Snapshot, Strong Start (load `prep-session/references/STRONG-START.md` and `PACING.md`), Thread Strip, NPC Quick-Ref, Day Tracker (if multi-day).
4. **Write scene cards.** One per active beat, tagged by thread. Follow the Inline-First Contract in `references/run-guide-spec.md` — each card is runnable with the rest of the wiki closed.
5. **Fill the reference zone.** Secrets & Clues, Stall Hooks, If They Surprise You, Possible Cliffhanger, Capture For Next Time, Context Read.
6. **Run the quality gate** from `references/run-guide-spec.md`.
7. **Save and commit.** `wiki/sessions/session-NN-run-guide.md`. Fill frontmatter. Update `hot.md` if prep revealed a state change.

**Decompose before drafting.** Write sections one at a time. A single-pass draft produces thin, inconsistent scene cards.

Load `ttrpg-writing` before writing prose. **DM-facing reference** for scene cards and
NPC handles. **Player-facing prose** for `[!read-aloud]` callouts. Load `sandbox-narrative`
for an anti-railroading pass on the finished guide.

## Voice

Concise, direct, and quietly encouraging. Cut every word that doesn't help run a beat. Be direct and devoid of mystery — state what is true, what the NPC wants, what the roll reveals. Encourage by removing fear: "you have what you need and nothing breaks if they wander."

## Reference Files

| File | Read when |
|---|---|
| `references/run-guide-spec.md` | Building or revising a run guide — the inline-first contract, scene card template, section specs with examples, file template, and quality gate. |
| `../ttrpg-writing/references/dm-reference-standards.md` | Writing DM-facing scene cards, NPC handles |
| `../ttrpg-writing/references/player-facing-prose.md` | Writing `[!read-aloud]` callouts |
| `../ttrpg-writing/references/callout-standard.md` | Callout type enforcement |

Cross-reference from `prep-session`:

| File | Read when |
|---|---|
| `prep-session/references/STRONG-START.md` | Writing the opening — the five strong-start types, failure modes, and anti-patterns. |
| `prep-session/references/PACING.md` | Choosing threads and shaping session rhythm. |
