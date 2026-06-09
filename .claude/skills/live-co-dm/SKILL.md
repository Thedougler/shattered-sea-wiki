---
name: live-co-dm
description: >
  Real-time co-DM for the Shattered Sea campaign while a session is actively being
  played. Invoke for: "co-DM the session", "live DM help", "improv help", "/co-dm".
  ALSO home of the DM's voice tools ("set up a character voice"). For "record the
  session" use record-session-audio; for "transcribe the session" use
  transcribe-session-audio. In live mode replies FAST and CONCISE, skipping wiki
  startup/init/lint/index/maintenance so the whole context serves the moment.
  Full trigger list in the skill body.
---

# Live Co-DM

## When to use

Full trigger set: "co-DM the session", "live DM help", "I'm running right now", "mid-session", "improv help", "the players just...", "what happens next", "they went off-book", "I need an NPC/name/twist right now", "/live-dm", "/co-dm". ALSO the home of the DM's voice tools — invoke for "set up a character voice", "improve/correct/optimize a voice profile". For "record the session" use the record-session-audio skill; for "transcribe the session" / "save a voice profile" use the transcribe-session-audio skill.

> Sandbox rules (PC boundary, NPC agency, pressures not plots) are in CLAUDE.md.
> **In live mode you deliberately skip most operational rules** — see below.
> Grounding/agency non-negotiables are shared with
> `.claude/skills/prep-session/references/co-dm.md`.

This skill has two distinct users:

- **The agent (you), live at the table** — give the DM fast, concise improv help.
- **The human DM, with the voice/transcription tools** — these now live in dedicated
  skills backed by the `tools/audio` (`shattered-audio`) engine: **record-session-audio**
  (capture) and **transcribe-session-audio** (transcript + voice profiles). Point the
  DM there; don't run a 4h recording mid-improv.

---

## Mode A — Live co-DM (your primary job)

You are assisting a DM **mid-session**. Latency and concision beat completeness.

### Startup (do exactly this — and nothing else)
1. Run the fast context loader — this is your ONLY required read:
   ```bash
   python3 .claude/skills/live-co-dm/scripts/latest_session_context.py --wiki wiki --tail 80
   ```
   It returns: the tail of the live transcript (what just happened at the table),
   current world state from `hot.md` (faction clocks, live threads), and a pointer
   to the previous session note.
2. **SKIP** `ttrpg-llm-wiki-init`, `ttrpg-wiki-lint`, index regen, frontmatter passes,
   full audits, and every other maintenance/startup task. Do not read the full vault.
   You are on the clock — the players are waiting.

### During play
- **Answer in seconds, not paragraphs.** A name, three bullet options, one stat line,
  a yes/and. The DM is reading you aloud-adjacent — be table-ready.
- The live transcript at `wiki/sessions/.live/session-NN/live_transcript.md` is your
  memory of the current scene. Re-read its tail when the DM asks "what just happened".
- Need one specific established fact (an NPC's secret, a location detail)? Use
  `ttrpg-wiki-query` for that single lookup — don't bulk-load.
- Surface faction-clock pressure from `hot.md` when it's relevant ("Knighton's ships
  are still inbound — want them to crest the horizon now?"), but never fire a trigger
  without offering it as a choice.
- **Preserve agency.** Offer options and consequences; never narrate PC choices,
  thoughts, or feelings. Flag invented detail as a proposal, not canon.
- **Defer all canon writes.** No session recap, ingest, cross-linking, or page edits
  mid-session. The live transcript is gitignored scratch; it gets promoted to canon
  *after* the game via `ttrpg-wiki-ingest` (transcript-ingest path).

When you need the deeper grounding/agency contract, read `references/co-dm-behavior.md`.

---

## Mode B — The DM's voice tools (you point, you don't run)

Recording and transcription now live in two dedicated skills, both backed by the
`tools/audio` (`shattered-audio`) engine. Route the DM there:

| The DM wants to… | Skill | Entry point |
|---|---|---|
| Record the session (multi-mic, 4h+) | **record-session-audio** | `.claude/skills/record-session-audio/scripts/record.sh --session N` |
| Transcribe a recording → speaker CSVs | **transcribe-session-audio** | `.claude/skills/transcribe-session-audio/scripts/transcribe.sh --session N` |
| Save / refresh a voice profile | **transcribe-session-audio** | `transcribe.sh --session N --save-profile "Name" --from-mic micKK` |
| Enroll a character voice (persona) | **transcribe-session-audio** | `transcribe.sh --session N --save-profile "Grigori" --from-mic micKK --actor Nick` |

**Why per-mic capture:** each person records to their own isolated track, so the mic a
voice came from is a strong speaker prior — the big accuracy lever for the campaign's
heavy crosstalk. Voice profiles (actor → character-voice personas) refine that further
and are auto-loaded on every transcribe.

**Self-correcting profiles:** the [[session-ingest]] skill emits a `speaker-map.md`;
`shattered-audio retrain --speaker-map ...` folds those corrections back into the
profiles, so accuracy improves every session.

---

## Bundled scripts (this skill only)

| Script | Role | Tested |
|---|---|---|
| `latest_session_context.py` | Fast mid-session context bundle | yes |

The recording/transcription engine lives in `tools/audio` (`shattered-audio`). Run its
test suite with:
```bash
cd tools/audio && .venv/bin/python -m pytest
```
