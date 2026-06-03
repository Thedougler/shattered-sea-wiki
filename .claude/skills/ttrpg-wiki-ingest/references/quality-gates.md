# Quality Gates

Run these before finalizing an ingest task.

## Canon Gates

- Every durable claim has a source path.
- Uncertain source text remains marked uncertain.
- Player speculation is not written as fact.
- Existing wiki canon is not overwritten without evidence.
- Contradictions are logged, not silently resolved.
- Secrets are not placed on player-facing pages.

## Wiki Structure Gates

- Required frontmatter fields are present on touched wiki files.
- `updated` is today's date on touched wiki files.
- `summary` answers "what is this?" in two sentences or fewer.
- New wikilinks resolve or have stubs.
- Reciprocal links exist where the relationship is durable.
- `wiki/index.md` reflects created, moved, or newly meaningful files.
- `wiki/hot.md` changed only if current world state changed.

## Prose Gates

Apply `ttrpg-writing`:

- DM-facing pages are terse, scannable reference.
- Player-facing text contains no DM secrets.
- No false mystery around plain facts.
- No invented stakes, motives, or emotions.
- No decorative summaries that repeat the source without making wiki state clearer.

For source-derived text, match the source's authority and tone. Do not "improve" blunt
notes into theatrical prose.

## Technical Checks

Run:

```bash
git diff --check
python3 .claude/scripts/check_ingest.py   # the source just ingested should be gone from the output
```

If this skill package was edited, also run:

```bash
python3 .claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/ttrpg-wiki-ingest
```

If `quick_validate.py` is unavailable or incompatible, validate manually:

- `SKILL.md` exists.
- YAML frontmatter parses.
- `name` and `description` exist.
- referenced files exist.
- helper scripts run with `--help`.

## Final Response Gate

Report only:

- Source processed and archived to `.raw/<type>/`.
- Files created/updated.
- Flags requiring DM action.
- Verification commands run or skipped.

Do not paste large rewritten wiki content into chat. The files are the artifact.
