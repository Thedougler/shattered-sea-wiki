# `.claude/scripts/` — Maintenance Script Catalog

Pure-stdlib wiki-maintenance scripts (no venv needed) plus the player-view test entry points.
Run from the repo root. Several scripts back hooks or skills; see each row.

## Wiki maintenance (pure stdlib, no venv)

```bash
python3 .claude/scripts/regen_index.py --write   # regenerate wiki/index.md (also run by regen-index.sh hook)
python3 .claude/scripts/wiki_lint.py              # lint vault (auto-detects Obsidian CLI + markdownlint)
python3 .claude/scripts/wiki_lint.py --obsidian on  # force Obsidian CLI for deeper cross-file checks
python3 .claude/scripts/check_ingest.py           # list source material still pending ingest
python3 .claude/scripts/fix_frontmatter.py <file> # add missing frontmatter fields (run by validate-frontmatter.sh hook)
python3 .claude/scripts/archive_source.py <file>  # git-mv ingested source from Inbox/ to .raw/
python3 .claude/scripts/ingest_packet.py <dir>    # compile context packet for subagent ingest
python3 .claude/scripts/assemble_transcript.py    # assemble transcript chunks into a single file
python3 .claude/scripts/preprocess_pdf.py <file>  # extract text/form fields from PDF source material
python3 .claude/scripts/tag_taxonomy.py           # controlled tag vocabulary (data module; consumed by wiki_lint)
python3 .claude/scripts/check_taxonomy_sync.py    # verify tag_taxonomy.py ↔ wiki/system/taxonomy.md stay in sync
python3 .claude/scripts/wiki_health_snapshot.py   # capture vault health metrics (--save to persist)
markdownlint-cli2 "wiki/**/*.md"                  # markdown formatting (config: .markdownlint-cli2.jsonc)
```

`wiki_common.py` is the shared library (frontmatter parsing, path inference, field defaults) imported
by the others — not run directly.

## Hook-backing scripts

| Script | Hook | What the hook does |
|---|---|---|
| `fix_frontmatter.py` | `validate-frontmatter.sh` (PostToolUse) | Completes frontmatter, stamps `updated:`, flags default summaries |
| `regen_index.py` | `regen-index.sh` (PostToolUse) | Debounced background regen of `wiki/index.md` on any `wiki/` write |

## player-view app

See `player-view/CLAUDE.md` for setup. Quick reference:

```bash
cd player-view
python3.11 -m venv .venv && .venv/bin/pip install -e ".[dev]"  # first-time setup
.venv/bin/python -m player_view.main                            # serves on localhost:8080
```

## Tests

```bash
for t in .claude/scripts/test_*.py; do python3 "$t"; done   # all script tests
cd player-view && .venv/bin/pytest tests/                    # player-view unit tests (no ML stack)
```
