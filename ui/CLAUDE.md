# CLAUDE.md — Shattered Sea Wiki UI

Astro 6 static site that renders the `wiki/` Obsidian vault as a browsable web UI.

## Stack

Astro 6.4 | Tailwind 4 | Preact islands | Pagefind search | pnpm

## Key Facts

- Part of a pnpm workspace rooted at `../`. Shared code lives in `@shattered-sea/lib` (`../packages/lib/`).
- All vault utilities (slugs, frontmatter, wikilinks, backlinks, asset map, schema) come from `@shattered-sea/lib`. Do not recreate local copies.
- Remark plugins (`src/plugins/`) stay here — they are UI-specific MDAST tree manipulation. They import shared data/regex from the lib.
- Content collection schema in `src/content.config.ts` imports `wikiEntrySchema` from the lib. The lib uses standalone `zod` (not `astro/zod`), which causes a non-blocking JSON schema generation warning during build. Validation works fine.
- `astro.config.mjs` builds `assetMap` and `slugSet` at config time and passes them to remark plugins.
- The content loader reads from `../wiki` (relative to this directory).

## Commands

- `pnpm dev` — dev server on `:4321`
- `pnpm build` — static build + Pagefind indexing to `dist/`
- `pnpm preview` — preview the built site

## Build Verification

A successful build produces 837+ pages and indexes 826+ with Pagefind. If page count drops significantly, something broke in the content collection or slug derivation.

## Filter Name

The pnpm filter name is `shattered-sea-wiki-ui` (from `package.json` `name` field), not `ui`.
Use `pnpm --filter shattered-sea-wiki-ui <command>` from the workspace root.

## Conventions

- Dark theme by default (DM tool used at the table). Colors use CSS custom properties (`--color-*`).
- Entity index pages live at `src/pages/<type>/index.astro`. Each filters the wiki collection by type/subtype.
- The catch-all renderer at `src/pages/wiki/[...slug].astro` handles all individual wiki pages.
- Preact islands only for genuinely interactive features (search dialog). Default to Astro components.
