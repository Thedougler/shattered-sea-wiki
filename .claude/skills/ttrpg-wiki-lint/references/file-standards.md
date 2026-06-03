# LLM-wiki file standards

Every file in this vault is optimized for two audiences: Obsidian (visual browsing)
and Claude Code (agent context). Linting is the process of transforming files safely
toward that dual-purpose ideal. The script handles the mechanical enforcement; the
agent handles judgment calls the script can't make.

## Frontmatter standards

The `--fix` pass enforces these mechanically. When writing or editing manually,
follow the same conventions so `--fix` is a no-op:

**Field ordering.** Universal fields first in canonical order (`type`, `subtype`,
`campaign`, `status`, `audience`, `publish`, `summary`, `created`, `updated`, `tags`,
`sources`), then type-specific extras, then domain fields. The script reorders on
`--fix`.

**Block-style lists.** `tags`, `sources`, and `aliases` use block style per
Obsidian's preferred format:

```yaml
tags:
  - npc
  - shattered-sea
```

Not flow style (`tags: [npc, shattered-sea]`). The `--fix` script enforces this.
Running `--fix` will convert existing flow-style lists to block style.

**No junk fields.** These waste tokens on every Read and carry no signal:

| Field | Action |
|---|---|
| `title` | Strip — the H1 heading and the filename carry the title. 558 files have this; it's ~2k tokens of pure noise across the vault. |
| `cssclasses` | Strip — only matters to Obsidian's CSS renderer, invisible to the agent. 93 files (`wiki-monster`, `wiki-ship`). |
| `null` values (`field: null`) | Strip or set to a real default. 23 files have `narrative_island: null`. |
| `sources: [Unknown]` | Replace with `sources: []` — "Unknown" is not a source. |
| `aliases: []` | Strip empty alias lists — adds nothing. |

These are safe to remove in `--fix` bulk passes (the script currently handles
`relationships: []` stripping; the others are candidates for future `--fix` scope).
Until then, remove by hand when touching a file.

**Concrete summaries.** Every summary must state a fact the agent can use for
routing. "Stub — no summary yet." fails this. A summary like "Tavern in the Warren
district of Calveno, run by Nona" lets the agent decide whether to read the file
without opening it. Write summaries as if the agent is scanning 500+ of them in
an index.

## Markdown standards

**Aliased wikilinks.** Always alias: `[[bastian-crev|Bastian Crev]]`, not
`[[bastian-crev]]`. Bare links render as slugs in agent context — the alias is how
the entity name reaches the agent without it opening the target file.

**One H1 per file.** The H1 is the page title. Use H2+ for sections. (markdownlint
rule MD025 is disabled because some legacy files violate this, but new content should
comply.)

**Blank lines around headings and lists.** markdownlint enforces this (MD022, MD032).
Missing blank lines cause Obsidian to sometimes merge content into the heading or
misparse list items.

**No trailing whitespace.** Invisible bytes that inflate diffs and token counts.

**Image embeds are for Obsidian, not the agent.** `![[portrait.webp]]` renders
visually in Obsidian but is a dead token for the agent. Keep them for visual
reference but don't rely on them to convey information — the body text must stand
alone.

**Thematic breaks (`---`) in body.** Use sparingly between major sections. They're
three tokens each and 190 files have them. Not wrong, but don't add them reflexively.

## Token efficiency and context engineering

The vault exists so the agent can answer questions and generate content without
reading everything. Every file should be optimized for **selective loading**:

**Frontmatter is the routing layer.** The agent reads frontmatter (via the index,
via `qmd`, via direct file reads) to decide what to load fully. `summary`, `type`,
`status`, `tags`, and `audience` are the fields that drive routing. If these are
wrong or vague, the agent either loads the wrong files or misses the right ones.

**`token_profile`** (system files only) signals how aggressively a file should be
loaded:

| Value | Meaning |
|---|---|
| `always-read` | Load every session (hot.md, doctrine) |
| `quick-ref` | Load the summary; read fully only when task matches |
| `on-demand` | Read only when explicitly needed |
| `map` | Index/generated file — scan, don't read deeply |

**`audience`** gates what the agent surfaces to players:

| Value | Meaning |
|---|---|
| `dm` | DM-only content; never show to players |
| `players` | Safe to surface in player-facing contexts |
| `agent` | System/infrastructure; not campaign content |

**Body density.** Prefer concrete facts over atmospheric prose in DM-reference
pages. A 200-word page with 10 actionable facts is more useful to the agent than a
1000-word page with 2 facts buried in flavor. Save the prose for `read-aloud`
callouts and player-facing content. See `ttrpg-writing` for the two content modes.

**Cross-reference over duplication.** If fact X lives on Entity A's page, don't
restate it on Entity B's page — link to it. Duplication means two places to update
and two places that can drift. Use wikilinks and section embeds (`![[A#Section]]`).

## Agent-driven fixes (what the script can't catch)

When touching files during a lint pass, also check for these by judgment:

**Vague summaries.** The script flags `"Stub — no summary yet."` but can't judge
whether `"An NPC in the campaign"` is useful. It isn't. Rewrite to include the
entity's distinguishing fact: role, location, relationship to a PC, or reason
they matter.

**Redundant body content.** If the frontmatter already carries a field (`captain`,
`parent_location`, `species`) and the body restates the same fact in prose with no
additional context, the prose version wastes tokens. Either enrich the prose version
(add context the field can't carry) or cut it.

**Orphaned callouts.** A `> [!secret]` or `> [!mechanic]` callout whose content
has been revealed in play or superseded by later sessions. These should be converted
to plain text or removed. The script can't know what's been revealed — you can, by
checking session notes.

**Dead content blocks.** Sections like "## Hooks" or "## Rumors" that are empty or
contain only placeholder text like "TBD" or "None yet". Either populate them with
real content or remove the heading entirely. Empty sections waste tokens and mislead
the agent into thinking there's structure where there's none.
