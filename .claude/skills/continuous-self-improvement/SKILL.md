---
name: continuous-self-improvement
description: >
  Use when running scheduled/autonomous wiki infrastructure improvement. Triggers
  on: "improve the wiki", "optimize the wiki", "self-improve", "kaizen",
  "continuous improvement", "daily improvement", scheduled routine invocations
  targeting wiki infrastructure quality. NOT for content creation, session prep,
  or ingest — those have dedicated skills. This skill targets the machinery
  (scripts, hooks, lint rules, skills, CLAUDE.md, settings) not the content.
---

# Continuous Self-Improvement

One run. One problem. Measured before and after. Enforced with code.

---

## Core Discipline

Every run follows the same loop:

```
MEASURE → IDENTIFY → FIX → ENFORCE → VERIFY → LOG
```

**You must complete all six steps, in order.** Skipping any step — especially
MEASURE or VERIFY — invalidates the run. A fix without measurement is a guess.
A fix without enforcement will regress.

| # | Step | In one line |
|---|---|---|
| 1 | **MEASURE** | Take a `sea health` baseline before touching anything. If you can't measure it, building the measurement IS this run's fix. |
| 2 | **IDENTIFY** | Pick the single highest-impact issue from the snapshot + transcript mining, ranked by the priority stack (P0 user frustration → P8 skill bloat). One problem per run. |
| 3 | **FIX** | TDD a surgical fix (≤3 files) pushed as far down the enforcement stack as it goes — deny rule > hook > lint rule > skill edit. Docs alone are not a fix. |
| 4 | **ENFORCE** | Add the mechanism that prevents regression: a test, a lint rule that fires on known-bad input, a registered hook. No enforcement → it regresses. |
| 5 | **VERIFY** | Take a second snapshot and `--diff`. At least one metric must improve with no unjustified regression, or revert. |
| 6 | **LOG** | Commit `feat: CSI — {change} ({metric}: {before} → {after})`. On failure, commit nothing but log issue/attempt/result/next. |

**Each step has detailed sub-procedures, tables, examples, and edge cases.**
Before executing the loop, read
[references/loop-steps.md](references/loop-steps.md) — it is the operating
manual for all six steps (snapshot metric catalog, transcript-mining queries,
the full priority stack, the enforcement-layer table, SKILL.md-edit validity
rules, the VERIFY acceptance matrix, and the LOG formats).

---

## Reference Files

| File | Read it when |
|---|---|
| [references/loop-steps.md](references/loop-steps.md) | Executing any step of the loop — full per-step procedures, metric tables, priority stack, enforcement stack, verification matrix, and commit/log formats. |

---

## Red Flags — STOP and Reconsider

| You're about to... | Instead... |
|---|---|
| Fix two things in one run | Pick one. Log the other for tomorrow. |
| Skip the before-snapshot | Stop. Measure first. Always. |
| Add a CLAUDE.md note as your "fix" | Find the code enforcement. Docs aren't fixes. |
| "Improve" something you can't measure | Pick a measurable problem. |
| Manually fix 50 files | Write a script or lint rule that fixes them. |
| Skip verification because "it obviously works" | Take the snapshot. Obvious is wrong often enough. |
| Extend scope because you "found something else" | Log it. Fix it tomorrow. |
| Fix a content problem (lore, prose, missing info) | That's not infrastructure. Use the appropriate content skill. |
| Edit a SKILL.md "because it reads better" | That's curation. You need transcript/log evidence of waste. |
| Skip transcript mining because "the snapshot is enough" | The snapshot is blind to workflow waste. Search transcripts. |
| Rewrite a whole skill as your CSI fix | One surgical edit per run. Rewrites are a dedicated session. |

---

## What This Skill Does NOT Do

- **Content creation or curation** — use `daily-update`, `ttrpg-writing`, or
  domain prep skills
- **Ingest** — use `ttrpg-wiki-ingest`
- **Full vault audit** — use `ttrpg-llm-wiki-init` Full Audit Mode
- **Lint the vault** — use `ttrpg-wiki-lint` (but this skill may ADD lint rules)

This skill improves the **machinery** — the scripts, hooks, rules, and skills
that other skills depend on.

---

## Bootstrapping: First Runs

On early runs, the measurement infrastructure itself may be incomplete. The
priority stack handles this: "Can't measure something that matters?" is priority
#1. Expected early-run targets:

1. Ensure `sea health` works (if CLI not built)
2. Add tests for existing scripts that lack them
3. Extend the snapshot with metrics the current lint doesn't capture
4. Add lint rules for the largest uncovered issue categories

Once the measurement baseline stabilizes (3+ snapshots with no new metrics
needed), the skill shifts to its steady state: identify → fix → enforce →
verify from the numbers.

The snapshot schema itself may need extending as the wiki matures. Adding a
new metric to the snapshot script is a valid CSI fix — it goes through the same
cycle (measure current coverage gaps → add the metric → test → verify the new
metric populates). Don't add metrics speculatively; add them when you identify
a real problem you can't currently quantify.
