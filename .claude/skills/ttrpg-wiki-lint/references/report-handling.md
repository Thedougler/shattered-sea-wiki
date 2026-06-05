# Working the report

Fix in this order; commit per logical batch using the conventions in
`.claude/skills/ttrpg-llm-wiki-init/references/auto-correct.md` (`fix: {type} — {file} — {what}`).

## broken-wikilink (error)

A `[[target]]` resolves to no page. When Obsidian CLI is active, this uses Obsidian's
live metadata cache — it catches path-qualified links (`[[wiki/situations/...]]`) and
alias-resolved links that regex-based checking misses. Per `.claude/skills/ttrpg-llm-wiki-init/references/wikilink-standards.md`, the standard
correction is to **create a stub** at the right path with `status: stub` and a
`summary: "Stub — referenced in [[source]]. No page yet."`, then let the hook
complete the frontmatter. If the link is a typo or wrong slug, fix it instead.

## naming-convention (error)

Filename isn't kebab-case. Rename to kebab-case **and update inbound wikilinks**, then
commit. (`git mv` keeps history.)

## invalid-value (error)

A frontmatter value is outside its allowed vocabulary (e.g. `lifecycle: island` when
the schema allows only `dormant`/`active`/`resolved`). Either correct the value or —
if the vault has genuinely outgrown the vocabulary — that's a schema question for the
DM (see *When the rules are wrong*).

## missing-required-field (warning)

Almost always cleared by `--fix`. If it persists, the field's type-inference is off —
check the file is at the right path.

## relationships-in-frontmatter (warning) — the migration

Relationships belong in the **body prose as wikilinks**, not in a frontmatter field.
Each report line lists every relationship, its note, and whether the target is
**already linked in the body**:

- **target already "in body"** — the link exists; just fold the note into a nearby
  sentence so the relationship reads naturally, then delete that entry.
- **target "NOT in body"** — the relationship isn't reflected in the prose at all;
  write a sentence that introduces it with an aliased wikilink, carrying the note's
  substance.

Weaving prose is a writing task — load `ttrpg-writing` for voice. Don't mechanically
dump `Relationships:` as a bullet list; work each one into the lore/DM text where it
belongs. Once every entry for a file is woven in, **delete the `relationships:` field
entirely**. Commit: `curation: {file} — relationships woven into body`.

## dead-entity-ref (warning) — lore consistency

A frontmatter cross-reference field (`captain`, `current_holder`, `owner`) points to
an entity whose status is `dead`, `deceased`, `destroyed`, or `presumed_dead`. The
ship/item page still claims a dead entity fills that role. Either update the field
(new captain, no holder) or mark the parent file's status to reflect the loss.

## island-situation-mismatch (warning) — lore consistency

A narrative island's `contains_situations` lists a situation whose `narrative_island`
field doesn't match (or is unset). Set the situation's `narrative_island` to match
the island that claims it, or remove it from `contains_situations` if the mapping
is wrong.

## status-drift (warning) — lore consistency

A status value has a near-synonym in use elsewhere (`deceased` vs `dead`, `open` vs
`active`). Now **auto-fixed by `--fix`** — synonyms are replaced with the canonical
form. If this still appears in the report, run `--fix` first.

## parent-gap (quality) — lore consistency

A place's `parent_location` field points to a parent page, but the parent's body
prose doesn't mention this child. Add a wikilink to the child in the parent page.

## type-path-mismatch (warning)

`type:` disagrees with the file's location. Usually the value is wrong — set it to
match the path. But a cluster of mismatches means the directory structure has evolved
past what `packages/lib/src/path-inference.ts`'s inference tables know — see below.

## deadend (quality)

No outgoing wikilinks. The page is a terminal node in the graph — it doesn't link to
anything. Add wikilinks to related pages where natural. Some stat blocks and minor
entries are legitimately standalone.

## orphan (quality)

No other page links here (links from the generated `index.md` don't count; links from
hand-curated `hot.md` do). Link it from a natural parent.

## tag-deprecated (warning)

A tag in the deprecated list from `wiki/system/taxonomy.md`. Sub-types identified in
the detail:

- **Frontmatter duplicate** — restates `type`/`subtype`/`status`/`audience`. **Auto-fixed
  by `--fix-tags`** (removed automatically).
- **System tag** — system/process tag like `lint`, `review`. **Auto-fixed by `--fix-tags`.**
- **Entity name** — names an NPC, place, ship, or PC. Requires judgment: add a wikilink
  to that entity in the body, then remove the tag.
- **Source citation** — belongs in `sources:` field. Requires judgment: move it there.

**Fixing (entity/source — not auto-fixed):** Read the file first. Once you know what
the page is about, choose up to 5 canonical replacements from `wiki/system/taxonomy.md`.
Don't just delete the old tag — the page may now have zero tags and deserve real ones.

## tag-alias (warning)

A tag is a known alias for a canonical form (e.g. `maw` → `drowned-maw`, `prep` → `dm-prep`).
Now **auto-fixed by `--fix-tags`** — aliases are replaced with their canonical form.
If this still appears after running `--fix-tags`, the alias map may need updating.

**Manual fixing (if not using --fix-tags):** Read the file. Replace the alias with
its canonical form — but also check whether the canonical tag actually applies.

## tag-unknown (quality)

A tag that isn't in the controlled vocabulary and isn't a known alias or deprecated tag. These are ad-hoc labels accumulated before the taxonomy existed.

**Fixing:** Read the file. Either:

1. Replace with the closest canonical tag from `wiki/system/taxonomy.md` if one fits.
2. If the page doesn't need the tag at all, remove it.
3. If the tag genuinely deserves to be canonical (appears or is needed on 5+ files across 3+ entity types), propose adding it to the taxonomy before applying it.

Never add an unknown tag to more files — only canonicalize or remove.

## tag-over-limit (warning)

More than 5 content tags (visibility tags don't count toward the limit).

**Fixing:** Read the file. Keep the 3–5 tags that are most cross-cutting and useful for DM prep. Prefer faction and theme/domain tags over workflow tags when space is tight. The limit is strict — trim to ≤5.

## tag-variant (quality)

A tag looks like a plural/singular variant of another tag (e.g. `#ship` vs `#ships`).
The less-used variant is flagged. Consolidate to the more common form.

## singleton-property (quality)

A frontmatter property name appears in only one file and isn't in the schema. Likely
a typo or a field that should be consolidated. Verify it's intentional, or fix it.

## bare-wikilink / summary-stale (quality)

Add a display alias (`[[slug|Name]]`); write a concrete summary. Opportunistic.

## md-* (quality, markdownlint)

Markdown formatting issues detected by markdownlint-cli2. Common ones:
`md-blanks-around-headings`, `md-blanks-around-lists`, `md-no-trailing-spaces`.
Config at `.markdownlint-cli2.jsonc` — noisy rules (line-length, table formatting,
multi-H1) are already disabled.
