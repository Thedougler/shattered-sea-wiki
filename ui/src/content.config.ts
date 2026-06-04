import { defineCollection } from 'astro:content';
import { buildWikiEntrySchema } from '@shattered-sea/lib';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const wiki = defineCollection({
  loader: glob({ base: '../wiki', pattern: '**/*.md' }),
  schema: buildWikiEntrySchema(z),
});

export const collections = { wiki };
