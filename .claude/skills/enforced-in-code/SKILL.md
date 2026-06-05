---
name: enforced-in-code
description: Use when a recurring problem is identified — agent keeps making the same mistake, a convention is violated repeatedly, or the user says "this keeps happening." Also use when evaluating whether a fix belongs in a hook, script, rule, CLAUDE.md, or skill. Triggers on phrases like "enforce", "automate this check", "stop doing X", "this keeps happening", "permanent fix", "make this automatic."
---

# Enforced in Code

## Overview

Fix recurring problems once, permanently, at the lowest-context layer that can catch them. Every token spent reminding an agent of a rule is wasted if a script can enforce it silently. Every hook that fires is wasted if a permission can block the action outright.

**Core principle:** Push enforcement down the stack. The best fix is one the agent never sees.

## Decision Flowchart

```dot
digraph enforce {
  rankdir=TB;
  node [shape=diamond];

  Q1 [label="Can the violation be\ndetected mechanically?\n(regex, file check, schema)"];
  Q2 [label="Should it BLOCK\nor CORRECT?"];
  Q3 [label="Is it file/path-scoped\nor universal?"];
  Q4 [label="Does the agent need\nto understand WHY?"];

  node [shape=box];
  PERMISSION [label="settings.json\npermissions.deny"];
  PRE_HOOK [label="PreToolUse hook\n(exit 2 to block)"];
  POST_HOOK [label="PostToolUse hook\n(auto-fix silently)"];
  LINT [label="sea lint rule\n(batch catch + --fix)"];
  RULE [label=".claude/rules/*.md\n(path-scoped guidance)"];
  CLAUDEMD [label="CLAUDE.md\n(universal guidance)"];
  SKILL [label="Skill guidance\n(last resort)"];

  Q1 -> Q2 [label="yes"];
  Q1 -> Q3 [label="no — judgment call"];
  Q2 -> PERMISSION [label="block — and it's\na tool pattern"];
  Q2 -> PRE_HOOK [label="block — needs\ncustom logic"];
  Q2 -> POST_HOOK [label="correct"];
  Q2 -> LINT [label="correct — but too\nslow for every edit"];
  Q3 -> RULE [label="scoped to\nspecific paths"];
  Q3 -> Q4 [label="universal"];
  Q4 -> CLAUDEMD [label="no — just do it"];
  Q4 -> SKILL [label="yes — needs\nprocedure/checklist"];
}
```

## Enforcement Stack (strongest to weakest)

| Layer | Mechanism | Token cost | Agent sees it? | When to use |
|---|---|---|---|---|
| 1 | `permissions.deny` | 0 | No | Block a tool pattern outright (e.g., `Bash(rm -rf *)`) |
| 2 | PreToolUse hook | ~0 (runs silently) | Only on block | Custom blocking logic (e.g., reject .env edits) |
| 3 | PostToolUse hook | ~0 (runs silently) | Only on warning | Auto-fix after every write (e.g., frontmatter, formatting) |
| 4 | `sea lint` rule | 0 until run | On explicit run | Batch detection, cross-file checks, things too slow for hooks |
| 5 | `.claude/rules/*.md` | ~0 until path match | Yes, on file access | Path-scoped guidance (loads only for matching files) |
| 6 | `CLAUDE.md` | Always loaded | Yes, every turn | Universal behavioral guidance |
| 7 | Memory | First 200 lines | Yes, at session start | Cross-session facts the agent should know |
| 8 | Skill | On-demand | Yes, when invoked | Procedures, checklists, complex workflows |

**Always start at layer 1 and work down.** Only reach for guidance (layers 5-8) when the problem requires judgment.

## Implementation Patterns

### Adding a permission deny

In `.claude/settings.json` under `permissions.deny`:
```json
"deny": ["Bash(rm -rf *)", "Bash(git push --force *)"]
```

### Adding a PreToolUse hook (blocking)

Create `.claude/hooks/<name>.sh`. Core pattern:
```bash
#!/usr/bin/env bash
set -euo pipefail
FILE=$(python3 -c "
import os, json
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}') or '{}'
try: print(json.loads(raw).get('file_path', ''))
except: print('')
" 2>/dev/null || true)

# Guard: only check relevant files
[[ "$FILE" == *.md ]] || exit 0
[[ "$FILE" == */wiki/* ]] || exit 0

# Check condition — exit 2 to block, 0 to allow
if some_check_fails "$FILE"; then
  echo "BLOCKED: reason"
  exit 2
fi
exit 0
```

Register in `.claude/settings.json`:
```json
"PreToolUse": [{"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "bash .claude/hooks/<name>.sh"}]}]
```

### Adding a PostToolUse hook (corrective)

Same shell pattern, but always `exit 0`. Fix the file in-place or emit a warning to stderr. The agent sees stderr output as tool feedback.

### Adding a sea lint rule

Add a check function in `packages/lib/src/lint.ts`. Register it in the main `lint()` function's check loop. Use `--fix` for auto-correctable variants.

### Adding a path-scoped rule

Create `.claude/rules/<name>.md`:
```markdown
---
paths: ["wiki/entities/characters/**"]
---
NPC files must use terse DM-reference prose, not fiction. Every sentence should give the DM an actionable fact.
```

Rules without `paths:` load at session start (same cost as CLAUDE.md). Rules with `paths:` load only when the agent reads a matching file — zero cost otherwise.

## Worked Example

**Problem:** "Agents keep writing YAML block scalars in frontmatter summaries."

1. Mechanical? **Yes** — regex can detect `>-` or `|` after `summary:`.
2. Block or correct? **Correct** — the content is fine, just the format.
3. Hook or lint? **Hook** — fast enough for every edit, single-file check.
4. **Solution:** Add normalization to `fix_frontmatter.py` (already runs on every PostToolUse write). Zero new infrastructure.

**Problem:** "NPC prose reads like fiction instead of DM reference."

1. Mechanical? **Partially** — regex can flag obvious patterns (emotional framing, atmospheric openers). But prose quality is a judgment call.
2. **Solution:** Two layers:
   - **Layer 4:** Add a prose-style check to `packages/lib/src/lint.ts` for the mechanical patterns.
   - **Layer 5:** Add `.claude/rules/npc-prose.md` scoped to `wiki/entities/characters/**` for the judgment guidance.

## When Automation Isn't Possible

Some problems can't be fully automated — they require judgment, context, or LLM-level understanding. When you hit the bottom of the mechanical stack, **maximize the automated portion** before falling through to guidance:

1. **Split the problem.** Separate mechanical symptoms from judgment calls. Automate the mechanical part (hook/lint), guide the rest (rule/CLAUDE.md).
2. **Pick the cheapest guidance layer.** Path-scoped rules (Layer 5) cost nothing outside their scope. CLAUDE.md (Layer 6) costs every turn. Skills (Layer 8) cost only when invoked. Don't load guidance universally if it only applies to one file type.
3. **Make the guidance actionable.** A rule that says "write better prose" is noise. A rule with a bad/good example pair and a concrete checklist changes behavior.

If a problem truly can't be addressed in code at all — say, a creative direction preference with no mechanical signal — document it at the cheapest layer that reaches the agent when it matters.

## When NOT to Automate

- **One-off problems** — if it happened once, fix it once. Don't build infrastructure.
- **Rapidly evolving standards** — if the rule is still being figured out, use CLAUDE.md or a skill until it stabilizes, then push it down the stack.
- **Cross-file semantic checks** — if the check requires understanding relationships across many files, it belongs in `sea lint` (batch), not a hook (per-file).

## Red Flags

If you catch yourself doing any of these, stop and push the fix down the stack:

| You're about to... | Instead... |
|---|---|
| Add a reminder to a skill | Add a hook or lint rule |
| Write "remember to X" in CLAUDE.md | Check if a PostToolUse hook can do X automatically |
| Manually fix the same formatting issue twice | Add it to `fix_frontmatter.py` or a PostToolUse hook |
| Tell the agent to "always check Y" | Make a hook that checks Y |
| Add a rule that could be a regex | Add it to `sea lint` with `--fix` |
