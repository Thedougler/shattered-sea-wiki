import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { wikiEntrySchema } from '@shattered-sea/lib';

const wiki = defineCollection({
  loader: glob({ base: '../wiki', pattern: '**/*.md' }),
  schema: wikiEntrySchema,
});

export const collections = { wiki };
