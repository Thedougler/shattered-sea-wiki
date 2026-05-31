---
name: prep-session
description: >
  Generate a complete, at-the-table session run guide for the Shattered Sea sandbox
  campaign — a scannable operating document the DM can run cold, written like a
  professional adventure module. Invoke for: "prep for next session", "give me a session
  plan", "what do I run Saturday", "help me run tonight", "session prep", "/run-guide",
  "/strong-start", "/thread-review", "/spotlight", "/faction-clock". Reads hot.md, active
  situations, the last session recap, and relevant entity pages first, then grounds every
  beat in established lore. Presents a scene menu the players choose from — never a plot.
  Inlines what the DM needs to run each beat (NPC wants, key rolls, stat lines, secrets)
  so they never flip between files mid-session; links only for depth. Always spotlights
  the PC who has been waiting.
---

## What this produces

A **session run guide**: a DM-only operating document for one session of play. Not a story, not a script, not a recap. The DM opens this one file at the table and runs the whole session from it — written in the voice and density of a published adventure module, but built for a sandbox where the party can do anything in any order.

The vault's own [[calveno-sandbox-run-guide|Calveno Sandbox Run Guide]] is the quality target: every line is actionable, every NPC has a one-line "table handle," every secret is unassigned, every clock has a visible tick, and there is a procedure for when the party goes somewhere you didn't prep.

## The rule that shapes everything: no mid-session hunting

A run guide fails the moment the DM has to open a second file to keep play moving. At the table there is no time to read an NPC's whole page or look up a stat block — the player just asked a question and four people are waiting.

So **inline what the DM needs to run a beat, link only what they might want to explore later.** At the point a beat is used, the guide already carries:

- the **read-aloud** (boxed, ready to speak),
- the **NPC's want right now** and a one-line handle for *how to play them*,
- the **one roll** that matters (DC, ability, what success and failure each reveal),
- a **compact stat line** if the beat can turn to violence (AC, HP, to-hit/save DC, key damage, one tactic) — full block linked,
- the **secret or clue** in play and what surfaces it,
- **if engaged / if ignored** consequences.

Wikilinks are for depth the DM chooses to chase between sessions, never for information they need in the next ten seconds. This is the difference between "comprehensive" and "a pile of links" — the comprehensive guide brings the answer to the DM; the pile sends them looking. When the two goals collide, density of *useful* information wins and link-chasing loses.

## Modes

| Mode | Produces |
|---|---|
| `/run-guide [N]` | Full session run guide for session N. Read `references/session-run-guide.md` and follow its workflow. |
| `/strong-start` | Just the opening: one in-medias-res scene, one image, one pressure, no recap. Read `references/STRONG-START.md`. |
| `/thread-review` | Active threads grouped *immediate / simmering / dormant / gap-or-contradiction*. Read-only — do not write unless asked. |
| `/spotlight` | Spotlight targets, each attached to an existing pressure. Never a scene whose only job is "give X a moment." |
| `/faction-clock` | **For prep:** simulate likely off-screen pressure as *pending* (do not write canon). **For post-session world advancement:** defer to the `faction-clock` skill, which owns canon clock writes. |

## Workflow

1. **Ground in current state.** Read in the CLAUDE.md reading order, stopping when you have enough:
   `wiki/hot.md` (always — it carries Open PC Threads, Faction Clocks, Live Situations, Predictions, and Spotlight Tracking) → the most recent `wiki/sessions/session-NN-recap.md` → the active situation files in `wiki/situations/active/` that are near the party → relevant entity pages (read the `summary` frontmatter first; open the full page only if the summary doesn't answer the beat you're writing).
   Supplementary if present and populated: `wiki/dm/player-interests.md`, `wiki/system/party-session-primer.md`. These are aids, not gates — `hot.md` is the source of truth for current state.
2. **Name what is already in motion** before inventing anything: where the party is, the last hard break, what they promised/broke/ignored, which situations and factions have reason to act now, which PC hooks are hot.
3. **Spotlight check.** Read the Spotlight Tracking table in `hot.md`. Find the PC who has gone longest without a meaningful moment and make sure at least one scene gives them one — attached to a real pressure, never manufactured.
4. **Pick threads and shape pacing.** Use `references/PACING.md` to choose the 2–3 threads worth advancing and to vary register so the session has rhythm.
5. **Write the guide** using `references/session-run-guide.md` — its template, inline-first conventions, and module formatting craft.
6. **Run the quality gate** at the end of that reference before finalizing.

Ground every claim in a page you read this session. If a fact isn't in the wiki, mark it a **proposal** and say so — don't quietly canonize it. If two pages conflict, surface a `> [!contradiction]` with both sources rather than silently picking one.

## Voice: concise, direct, and quietly encouraging

The DM reading this is busy and about to perform for hours. Respect their bandwidth:

- **Cut every word that doesn't help them run a beat.** Atmosphere belongs in read-aloud text; DM notes are instructions. Prefer tables and tight bullets over paragraphs.
- **Be direct and devoid of mystery.** State what is true, what the NPC wants, what the roll reveals. The DM should never have to decode your prep — you are their co-DM, not a puzzle.
- **Encourage by removing fear, not by adding pep talk.** A sandbox DM's anxiety is "what if they don't do what I prepped?" Answer it *in the guide*: mark ignored content as resurfacing rather than wasted, give a Surprise procedure, and remind them the menu is theirs to react to, not drive. Confidence comes from "you have what you need and nothing breaks if they wander," delivered in as few words as possible. Encouragement that costs the DM reading time is not encouragement.

Load `ttrpg-writing` for prose and read-aloud standards. Load `sandbox-narrative` for an anti-railroading pass on the finished guide.

## Reference Files

| File | Read when |
|---|---|
| `references/session-run-guide.md` | Building or revising a run guide — the inline-first template, assembly workflow, module formatting craft, and quality gate. |
| `references/STRONG-START.md` | Writing the opening — the five strong-start types, failure modes, and anti-patterns. |
| `references/PACING.md` | Choosing which threads to advance and shaping session rhythm, register variation, and off-screen faction action. |
