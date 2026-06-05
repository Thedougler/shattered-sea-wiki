import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import tailwindcss from '@tailwindcss/vite';
import preact from '@astrojs/preact';
import node from '@astrojs/node';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import { remarkObsidianCallouts } from './src/plugins/remark-obsidian-callouts';
import { remarkObsidianEmbeds } from './src/plugins/remark-obsidian-embeds';
import { remarkWikiLinks } from './src/plugins/remark-wiki-links';
import path from 'node:path';
import { buildAssetMap, buildSlugSet } from '@shattered-sea/lib';

const wikiDir = path.resolve(import.meta.dirname, '../wiki');
const assetsDir = path.join(wikiDir, 'assets');

const [assetMap, slugSet] = await Promise.all([
  buildAssetMap(assetsDir),
  buildSlugSet(wikiDir),
]);

export default defineConfig({
  site: 'http://localhost:4321',
  adapter: node({ mode: 'standalone' }),
  integrations: [preact()],
  vite: {
    plugins: [tailwindcss()],
    envDir: path.resolve(import.meta.dirname, '..'),
  },
  markdown: {
    processor: unified({
      remarkPlugins: [
        remarkObsidianCallouts,
        [remarkObsidianEmbeds, { assetMap }],
        [remarkWikiLinks, { slugSet }],
      ],
      rehypePlugins: [
        rehypeSlug,
        [rehypeAutolinkHeadings, { behavior: 'append' }],
      ],
    }),
    syntaxHighlight: 'shiki',
    shikiConfig: {
      theme: 'github-dark-default',
    },
  },
});
