---
globs: wiki/**/*.md
---

# Wiki Write Rules

These rules apply to every Write or Edit targeting a file under `wiki/`.

## Sandbox Rules

- **PC Boundary.** Never write what a PC decides, chooses, intends, feels, thinks, or wants.
- **NPC Agency.** NPC goals predate the party. NPCs pursue their goals independently.
- **Pressures, Not Plots.** Frame content as pressures and possibilities, never scripted outcomes.
- **PC-Connection Requirement.** Every element must pull on at least one PC's internal tensions.

## Self-Healing Protocol

PostToolUse hooks fire after every edit. You must close the loop:

1. If `validate-frontmatter.sh` prints `FLAG: summary is default` — write a concrete summary
   in the same edit pass. Do not commit with a placeholder summary.
2. If `check-wikilinks.sh` prints `Unresolved wikilinks` — either fix the link target spelling
   or create a stub file for the missing entity before committing.
3. Never suppress, ignore, or work around hook output. The hooks are the source of truth for
   mechanical correctness.

## Commit Discipline

- Commit wiki changes with an appropriate prefix (`fix:`, `ingest:`, `curation:`, `prep:`).
- Stage with `git add wiki/…` — never `git add .` or `git add -A`.
- One logical commit per coherent unit of work. Do not batch unrelated changes.
- Do not commit files with unresolved hook warnings.
