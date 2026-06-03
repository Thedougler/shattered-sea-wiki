import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { buildWikiEntrySchema } from '@shattered-sea/lib';

const wiki = defineCollection({
  loader: glob({ base: '../wiki', pattern: '**/*.md' }),
  schema: buildWikiEntrySchema(z),
});

export const collections = { wiki };
