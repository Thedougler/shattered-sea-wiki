---
name: prep-session
description: >
  Build the at-the-table operating document for one session of the Shattered Sea sandbox — a
  scannable run guide the DM runs cold, written like a professional adventure module. Invoke for:
  "prep for next session", "give me a session plan", "what do I run Saturday", "help me run
  tonight", "session prep", "build a run guide", "prep tonight's session", "/run-guide",
  "/strong-start", "/thread-review", "/spotlight". Also use when an existing guide is hard to use
  at the table: NPC info scattered across files, content organized by in-game day instead of
  thread, images breaking scan flow, too many files open during play, dense tables that don't
  scan. Grounds every beat in hot.md, active situations, the last recap, and entity pages.
  Presents a scene menu the players choose from — never a plot. Inlines what the DM needs to run
  each beat (NPC wants, key rolls, stat lines, secrets); links only for depth. Always spotlights
  the PC who has been waiting.
---

# Prep Session — Session Run Guide

A **session run guide**: one DM-only file you open at the table and never leave. Not a story, not
a script, not a recap, not a table of contents linking elsewhere. Written in the voice and
density of a published adventure module, built for a sandbox where the party can do anything in
any order. The vault's [[calveno-sandbox-run-guide|Calveno Sandbox Run Guide]] is the quality
target.

This skill also applies the shared prep discipline (PC connection, spotlight, prose pass) — see
`../ttrpg-llm-wiki-init/references/prep-family-standards.md`.

## The iron rule: one file, one session

A run guide fails the moment the DM has to open a second file, and when it tries to cover more
than one session can hold.

- **One file.** Everything needed to run tonight is inline. Wikilinks are for depth chased
  *between* sessions, never for retrieval mid-play. A guide that is secretly a (well-organized)
  table of contents violates this.
- **One session.** A guide covers 3–5 hours, not a multi-session arc. A city sandbox spanning
  four sessions gets four guides. The sandbox run guide / situation files hold the full arc; the
  session guide extracts and inlines.
- **Max 5–7 scene cards.** More than 7 means you're prepping multiple sessions. Cut to the
  threads the party is most likely to pull; point to sandbox/situation files for overflow.

**Never:** split into linked day/scene/beat files; organize scenes by in-game day (organize by
thread); embed images in operating text (art goes in a collapsed callout or stays in situation
files); prep more than 3 in-game days in one guide.

## No mid-session hunting

At the point a beat is used, the guide already carries: the **read-aloud** (boxed, ready to
speak); the **NPC's want right now** + a one-line handle for how to play them; the **one roll**
that matters (DC, ability, what success/failure each reveal); a **compact stat line** if it can
turn violent (AC, HP, to-hit/save DC, key damage, one tactic — full block linked); the **secret
or clue** in play and what surfaces it; **if engaged / if ignored** consequences. Density of
*useful* information wins; link-chasing loses.

## Three-zone architecture

| Zone | Purpose | DM reaches for it | Position |
|---|---|---|---|
| **Dashboard** | State, strong start, thread strip, NPC roster | Every 10 min | Top — first screen |
| **Scenes** | Self-contained scene cards, one per beat, tagged by thread | When a thread is pulled | Middle |
| **Reference** | Secrets, stall hooks, surprise procedure, cliffhanger | Once/session or on lookup | Bottom |

Dashboard is pure text and tables (no images — it's scanned every 10 minutes). Scenes are
organized by thread, not by day; for multi-day sessions a compact Day Tracker in the dashboard
shows what changes overnight. Reference is reached by Ctrl+F, not scroll position.

## Modes

| Mode | Produces |
|---|---|
| `/run-guide [N]` | The full run guide (default). Follow the Workflow below and the spec in `references/run-guide-spec.md`. |
| `/strong-start` | Just the opening: one in-medias-res scene, one image, one pressure, no recap. Read `references/STRONG-START.md`. |
| `/thread-review` | Active threads grouped *immediate / simmering / dormant / gap-or-contradiction*. Read-only — do not write unless asked. |
| `/spotlight` | Spotlight targets, each attached to an existing pressure. Never a scene whose only job is "give X a moment." |

For **pending faction pressure** shown in a guide: simulate likely off-screen movement as
*pending* (observable effect, never the mechanic) — this is not a canon write. Actual world/clock
advancement is `world-update`'s job (its on-demand mode owns canon clock writes).

## Workflow

1. **Ground in current state.** Read in the CLAUDE.md reading order, stopping when you have
   enough: `wiki/hot.md` (always — Open PC Threads, Faction Clocks, Live Situations, Predictions,
   Spotlight Tracking) → most recent `wiki/sessions/session-NN-recap.md` → active situation files
   near the party → relevant entity pages (summaries first; open full pages only when needed).
   Supplementary if populated: `wiki/dm/player-interests.md`, `wiki/system/party-session-primer.md`.
2. **Name what is already in motion** before inventing: where the party is, the last hard break,
   what they promised/broke/ignored, which situations and factions have reason to act now, which
   PC hooks are hot.
3. **Spotlight check.** Read Spotlight Tracking in `hot.md`. Find the PC who has gone longest
   without a meaningful moment; ensure ≥1 scene gives them one, attached to a real pressure.
4. **Scope & pace.** Use `references/PACING.md` to pick the 2–3 threads worth advancing and to
   vary register so the session has rhythm. How many in-game days (max 3)? Cut aggressively.
5. **Build the dashboard, then the scene cards, then the reference zone.** One section at a time —
   a single-pass draft produces thin, inconsistent cards. Each scene card must be runnable with
   the rest of the wiki closed (the Inline-First Contract in `references/run-guide-spec.md`).
6. **Run the quality gate** in `references/run-guide-spec.md` before finalizing.
7. **Save and commit.** `wiki/sessions/session-NN-run-guide.md`. Fill frontmatter. Update
   `hot.md` only if prep revealed a state change.

Ground every claim in a page you read this session. If a fact isn't in the wiki, mark it a
**proposal**. If two pages conflict, surface a `> [!contradiction]` with both sources.

## Visual aids

Load `ttrpg-visual-aids` and `openrouter-image-gen`. One image per scene card max, at the top of
the card before the read-aloud (blank line above/below, never inside callouts). No dashboard
images. Generate during prep, not at the table; if generation fails, leave a `[!visual-aid]`
callout with the full prompt.

## Voice: concise, direct, quietly encouraging

The DM is busy and about to perform for hours. Cut every word that doesn't help run a beat —
atmosphere belongs in read-aloud text; DM notes are instructions. Be direct and devoid of
mystery: state what is true, what the NPC wants, what the roll reveals. Encourage by removing
fear, not adding pep talk: mark ignored content as resurfacing rather than wasted, give a Surprise
procedure, remind them the menu is theirs to react to. "You have what you need and nothing breaks
if they wander."

Load `ttrpg-writing` before writing prose (**DM-facing reference** for cards/handles,
**player-facing prose** for `[!read-aloud]`). Load `sandbox-narrative` for an anti-railroading
pass on the finished guide.

## Reference Files

| File | Read when |
|---|---|
| `references/run-guide-spec.md` | Building or revising a guide — inline-first contract, scene card template, section specs with examples, file template, quality gate |
| `references/STRONG-START.md` | Writing the opening — the five strong-start types, failure modes, anti-patterns |
| `references/PACING.md` | Choosing threads, shaping rhythm, register variation, off-screen pressure |
| `../ttrpg-llm-wiki-init/references/prep-family-standards.md` | Shared prep discipline (PC connection, spotlight, prose pass) |
| `../ttrpg-writing/references/dm-reference-standards.md` | DM-facing scene cards, NPC handles |
| `../ttrpg-writing/references/player-facing-prose.md` | `[!read-aloud]` callouts |
| `../ttrpg-writing/references/callout-standard.md` | Callout type enforcement |
