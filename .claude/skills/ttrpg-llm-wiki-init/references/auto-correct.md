# Auto-Correct Protocol

Structural problems are fixed immediately and committed — never ask for confirmation. This is
safe because every fix is reversible in git and none of them invents canon.

| Violation | Auto-correction |
|---|---|
| File in wrong path | Move to correct path; update inbound wikilinks; commit |
| Missing frontmatter field | Handled by the hook (`fix_frontmatter.py`) |
| Broken wikilink | Create stub at correct path; add to index; commit |
| Naming-convention violation | Rename to kebab-case; update inbound wikilinks; commit |
| Missing bidirectional relationship | Add the reciprocal link to the target file; commit |
| Orphaned file | Add to index; link from a natural parent; commit |
| Situation/island in wrong lifecycle folder | Move; update `lifecycle`/`status`; update links; commit |
| Stub `summary` still default text | `FLAG: summary-stale — {file}` — do **not** guess content |

## Escalation

**Escalate to the DM only for:**
- A genuine contradiction between two established facts → append to `wiki/discrepancy-log.md`,
  leave both traces visible
- Ambiguous entity identity (two pages may describe the same thing)

Everything else: fix and move on.

## Commit Message Format

```
fix: {correction-type} — {file} — {description}
ingest: {source} — {outputs}
curation: {file} — {what changed}
```
