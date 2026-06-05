# LLM-Wiki Infrastructure — Optimization Backlog

From the 2026-06-03 comprehensive infrastructure audit. The first wave of high-confidence fixes
shipped in `e4edfc0`, `e61eeff`, `23d5d0f`. This file tracks the follow-up wave and the items
deliberately deferred.

## Done (second wave, 2026-06-03)

- **Skill-registry refresh** (`e14295b`) — removed 21 stale entries for deleted/merged skills,
  added every real skill, fixed all cross-references. Now matches the live 37-skill set.
- **Bloat trims** (`4f99124`) — ttrpg-wiki-lint 554→229, session-ingest 469→235,
  continuous-self-improvement 408→106; procedural detail moved to `references/` (progressive
  disclosure), content preserved. *skill-creator left untouched by request.*
- **Skill frontmatter fixes** (`4f99124`) — `version` nested under `metadata` (init, wiki-lint,
  wiki-query); fixed a YAML regression where inline `Triggers on:` colons broke plain-scalar
  parsing in obsidian-cli / obsidian-json-canvas / tdd (converted to folded block style).
- **prep-ship** duplicate stub line removed (covered by prep-family-standards).
- **Tag-taxonomy drift guard** (`8662187`) — new `check_taxonomy_sync.py` + full tests
  (scripts coverage 85%), wired into the catalog and the "add a tag" checklist. Eliminates the
  silent-drift risk between `tag_taxonomy.py` and `taxonomy.md`.
- **soultrace** skill removed (was untracked).

## Deferred — evaluated, intentionally not built yet

These were assessed against value / effort / risk and the 80%-coverage gate on `.claude/scripts`.
Each has a reason it's parked rather than done.

- **Loop-orchestration scripts** (`world_update.py`, `daily_update.py`, `session_ingest.py
  --resume`, `csi_loop.py`). *Deferred — design-only.* These orchestrate LLM-judgment workflows
  (interpretation, canon writes, cross-linking) that a deterministic script can't perform; a
  script could only sequence steps and roll dice. The deterministic chunks are already one-liners
  over existing tools (`sea lint`, `regen_index.py`, `sea health`,
  `check_ingest.py`). Build one only when a *concrete, repeated* bookkeeping pain appears that a
  harness would remove — and budget for ≥80% test coverage of the subprocess orchestration.
- **Judgment-heavy hooks** (auto-create stubs for unresolved wikilinks; auto-add reciprocal
  backlinks). *Deferred — needs design.* Auto-stubbing risks spawning pages from typos;
  auto-backlinking risks rewriting prose at the wrong insertion point. The current warn-and-let-
  the-agent-fix behavior is safer. Worth doing only with a careful, idempotent, well-tested design.
- **Test-file consolidation** (`test_check_ingest.py`→`_ext`).
  *Deferred — low value.* Tests aren't loaded into agent context,
  so this doesn't serve the context-budget goal; merging risks dropping a unique case and
  perturbing the coverage number for no functional gain. (`test_wiki_health_snapshot*.py` removed
  — health snapshot migrated to TS CLI as `sea health`.)
- **Permission tightening** (replace the blanket `Bash(python3 .../scripts/*)` allow with an
  explicit per-script allowlist; narrow directory-level `git add`). *Deferred — friction > benefit.*
  In a solo content repo these are the agent's own stdlib tools; an allowlist would prompt on every
  new script for negligible security gain.

## Loose ends (no action needed)

- `prep-hb-item` and `prep-location` keep a short stub/filing line with content-type-specific
  context; the shared pointer already covers the general convention. Fine as-is.
- `player-view-dev` and `session-recap` carry `disable-model-invocation` (intentional manual-only
  skills). `quick_validate.py`'s allowlist doesn't know that key — validator limitation, not a bug.
