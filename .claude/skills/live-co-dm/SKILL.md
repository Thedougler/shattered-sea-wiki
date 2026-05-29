---
name: live-co-dm
description: >
  Real-time co-DM for the Shattered Sea campaign while a session is actively being
  played. Invoke for: "co-DM the session", "live DM help", "I'm running right now",
  "mid-session", "improv help", "the players just...", "what happens next", "they
  went off-book", "I need an NPC/name/twist right now", "/live-dm", "/co-dm". ALSO
  the home of the DM's voice tools — invoke for "save a voice profile", "set up a
  character voice", "improve/correct/optimize a voice profile", "start transcribing
  the session", "record the session", "finalize the transcript". In live mode it reads
  the most recent session transcript plus minimal world state and replies FAST and
  CONCISE, then waits — skipping wiki startup, init, lint, index regen, and routine
  maintenance so the whole context serves the moment. Bundled scripts do voice
  profiling (browser teleprompter, self-correcting from finalized transcripts) and
  continuous 4h+ transcription with accurate, overlap-aware speaker separation.
---

> Cross-cutting rules (reading order, sandbox constraints, PC-connection requirement,
> frontmatter, auto-correct) live in `wiki/system/doctrine.md`. **In live mode you
> deliberately skip most of them** — see below. Grounding/agency non-negotiables are
> shared with `.claude/skills/prep-session/references/co-dm.md`.

This skill has two distinct users:

- **The agent (you), live at the table** — give the DM fast, concise improv help.
- **The human DM, with the bundled scripts** — capture voice profiles and transcribe
  the session. You do not run these for them; you point them to the reference docs.

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

If the DM asks about voices or transcription, route them to the right doc and the
right command. These need the one-time setup in `references/setup.md` (Python venv +
`requirements.txt`, Hugging Face token, pyannote license acceptance, mic permission).

| The DM wants to… | Point them to | Command |
|---|---|---|
| Save / improve a character's voice profile | `references/voice-profiler.md` | `voice_profiler.py --name "Grigori" --player "Dave"` |
| Transcribe a live session (4h+) | `references/transcription.md` | `transcribe_session.py --session 4 --speakers 5` |
| Produce the canonical transcript | `references/transcription.md` | `finalize_session.py --session 4 --speakers 5` |

**Why two passes:** the live run gives a provisional transcript during play; the
finalize pass re-diarizes the *whole* recording at once with the known speaker count
— the big accuracy lever for the campaign's heavy crosstalk (5 players, many voices).
Profiles are one per **character voice**; the `player` field groups the several voices
one person performs so they can be told apart.

**Self-correcting profiles:** saving a profile also harvests that character's lines from
corrected, finalized transcripts (whose `.live` audio still exists), folding the real
in-character audio into the teleprompter anchor. Overlap/low-confidence lines are skipped
and outliers rejected, so correction only sharpens. The loop: correct a session transcript
→ re-save that character's profile → it absorbs the fixes for next time. Details in
`references/voice-profiler.md`.

---

## Bundled scripts (reference)

| Script | Role | Tested |
|---|---|---|
| `latest_session_context.py` | Fast mid-session context bundle | yes |
| `transcribe_session.py` (`run_loop.py`) | Continuous live capture loop | core: yes |
| `finalize_session.py` (`finalize.py`) | Offline canonical re-pass | core: yes |
| `voice_profiler.py` (`profiler_core.py`) | Teleprompter + enrollment + correction | core: yes |
| `profile_harvest.py` / `profile_enhance.py` / `transcript_parse.py` | Harvest + fold corrected audio into profiles | yes |
| `vecmath / attribute / speaker_id / render / silence_chunker / profiles / session_paths / transcript_writer / pipeline / audio_file` | Pure logic | yes |
| `adapters.py` | Thin Parakeet/pyannote/sounddevice/NiceGUI wrappers | manual + opt-in ML |

Run the unit suite (no ML stack needed):
```bash
cd .claude/skills/live-co-dm/scripts && python3 -m unittest discover -s . -p 'test_*.py'
```
