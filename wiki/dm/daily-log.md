---
type: system
subtype: log
campaign: shattered-sea
status: active
audience: agent
publish: false
summary: Log of autonomous daily wiki maintenance runs.
created: 2026-05-30
updated: 2026-05-31
tags: []
sources: []
---

# Daily Update Log

## 2026-05-31

- **Lint:** Warnings 111→94 (17 resolved); Quality 1373→316 (1057 resolved)
  - Status-drift: 4 fixed (deceased→dead ×3, open→active ×1); barnaby-rook `presumed_dead` deferred — lore-accurate, not confirmed dead
  - Dead-entity-ref: removed `captain:` from Heft, Loud Argument, The Narrow (all `status: lost`, captain info in body)
  - Island-situation-mismatch: 10 resolved — `narrative_island` set on 8 child narrative islands (→calveno-sandbox-run-guide); calveno-beffa-grung-raid→calveno-raid-signs; removed redundant transitive link from sandbox-run-guide
  - Parent-gap: 8 resolved — 4 Midchain children, 2 Shattered Sea children, Anchor & Line (Tidefall), Taufa Fifita & Sons (Kalowe)
  - Singleton-property: removed junk `name:` from otar-the-foul frontmatter
  - Markdown: 813 files — trailing newlines, blanks-around-headings/lists fixed by markdownlint-cli2
  - Type-path-mismatch: 93 deferred — creatures schema gap (path infers `entity`, files correctly typed `monster`/`index`); requires wiki_common.py update

## 2026-05-30

- **Init:** OK — vault healthy, no active work queue, no structural issues
- **Ingest:** 6 sources processed (giant-centipede, giant-constrictor-snake, giant-crab, giant-crocodile, giant-eagle, giant-frog) | 295 remaining in queue
- **Lint:** 26 files auto-fixed (frontmatter reorder, MD022/MD032/MD058) | 1065 errors deferred to review queue
- **Cross-link:** 7 links added across 7 pages — giant-shark orphan resolved (tail.md, galewall.md); giant-crocodile linked from dreth.md, midchain.md; giant-frog linked from dreth.md, orak.md, veth.md; giant-centipede linked from sorn.md
- **Index:** regenerated
- **Errors:** none
