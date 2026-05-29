# qmd Querying Reference — Shattered Sea

Read this when a plain `qmd query "..."` underperforms and you need to craft a sharper
query, or when you need the collection/path map. For everyday lookups the single-line
form in SKILL.md is enough — start there.

## Collections

| Collection | Root | Authority | Use |
|---|---|---|---|
| `shattered_sea_wiki` | `wiki/` | Canonical, compiled | Default — search here first for any in-world fact |
| `shattered_sea_raw` | `.raw/` | Draft, unprocessed | Escalation only, when the wiki page is missing/incomplete |

`Inbox/` is **not** indexed — it holds sources awaiting ingestion, not canon. Don't expect
qmd to find Inbox material; if you need it, read it directly.

qmd returns paths as `qmd://<collection>/<relative-path>`. To open the file, strip the
prefix and Read the real path (e.g. `qmd://shattered_sea_wiki/entities/places/x.md` →
`wiki/entities/places/x.md`). Reading directly gives you full content, line numbers, and the
page's wikilinks for the completeness pass.

## The three query types

`qmd query` accepts a single auto-expanding line (recommended default) **or** a multi-line
document where each line is typed `lex:`, `vec:`, or `hyde:`. Don't mix `expand:` with typed
lines — it's one or the other.

| Type | Method | Give it | Best for |
|---|---|---|---|
| `lex` | BM25 keywords | 2–5 exact terms, no filler | Names, slugs, distinctive jargon, stat-block terms |
| `vec` | Vector similarity | A full natural-language question | Conceptual / thematic recall when you don't know the vocabulary |
| `hyde` | Vector on a hypothetical answer | 50–100 words of what the answer *would* look like | Hard questions where you can describe the answer better than ask it |

The first query in a document gets 2× weight in fusion — lead with your best guess.

## Writing each type

**lex** — keyword precision:
- 2–5 terms, drop articles and filler.
- Exact phrase: quote it — `"sending stone"`.
- Exclude a term: minus prefix — `umberlee -storm` (lex only; not valid in vec/hyde).
- Prefix match is automatic: `perr` matches "Perrin".

**vec** — semantic question:
- Write the actual question in full: `"how is the Uncertainty being repaired in Calveno"`.
- Include context that disambiguates: name the place, faction, or PC involved.

**hyde** — hypothetical document:
- Write a short paragraph in the *vocabulary you expect in the result*, as if it were the
  answer. The retriever matches your fake answer against real pages.

## Combining for hard questions

| Situation | Approach |
|---|---|
| You know the exact term | `lex` only (or just `qmd search`) |
| You don't know the vocabulary | single-line `qmd query "..."` (auto-expand) or `vec` |
| You want best recall | `lex` + `vec` together |
| Complex / multi-faceted topic | `lex` + `vec` + `hyde` |
| Ambiguous term (e.g. "passage") | add an `intent:` line |

Multi-line example:

```bash
qmd query $'lex: Nona Black-Jaw favor\nvec: what does Nona want from Perrin in return for the sending stone' \
  -c shattered_sea_wiki --json | jq -r '.[] | "[\(.score)] \(.file)\n\(.snippet)\n"'
```

## intent — disambiguation

`intent:` does not search on its own; it steers expansion, reranking, and snippet selection
when a term is ambiguous in this world. Example: "the Passage" is a faction here, not a
hallway — `intent: the smuggling faction led by Nona` keeps results on-target.

```bash
qmd query $'intent: the smuggling faction, not a corridor\nlex: passage' -c shattered_sea_wiki
```

## Output hygiene

`--json` returns objects with `docid`, `score`, `file`, `title`, `context`, `snippet`. The
`context` field repeats the collection description on every result and is pure noise for you
— always project it away:

```bash
qmd query "..." -c shattered_sea_wiki --json | jq -r '.[] | "[\(.score)] \(.file)\n\(.snippet)\n"'
```

Or keep structured fields without the noise: `jq 'map(del(.context))'`.

## Maintenance commands (rarely needed by hand — the hook handles it)

| Command | Effect |
|---|---|
| `qmd status` | Index health, collection counts, staleness |
| `qmd update` | Re-index changed files (fast; lex/get freshness) |
| `qmd embed` | Regenerate vector embeddings (slow; semantic freshness) |
| `qmd get qmd://<collection>/<path>` | Fetch one indexed doc (prefer Reading the real file) |
