import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import tailwindcss from '@tailwindcss/vite';
import preact from '@astrojs/preact';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import { remarkObsidianCallouts } from './src/plugins/remark-obsidian-callouts';
import { remarkObsidianEmbeds } from './src/plugins/remark-obsidian-embeds';
import { remarkWikiLinks } from './src/plugins/remark-wiki-links';
import { buildAssetMap } from './src/lib/asset-map';
import { buildSlugSet } from './src/lib/wiki-graph';

const [assetMap, slugSet] = await Promise.all([
  buildAssetMap(),
  buildSlugSet(),
]);

export default defineConfig({
  site: 'http://localhost:4321',
  integrations: [preact()],
  vite: {
    plugins: [tailwindcss()],
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
