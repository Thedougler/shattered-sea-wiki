import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const wiki = defineCollection({
  loader: glob({ base: '../wiki', pattern: '**/*.md' }),
  schema: z.object({
    type: z.string(),
    subtype: z.string().optional(),
    campaign: z.string().default('shattered-sea'),
    status: z.string().default('unknown'),
    audience: z.string().default('dm'),
    publish: z.boolean().default(false),
    summary: z.string().default(''),
    created: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    sources: z.array(z.string()).default([]),
    confidence_level: z.string().optional(),
    title: z.string().optional(),

    // entity-specific
    aliases: z.array(z.string()).default([]),
    species: z.string().optional(),
    pronouns: z.string().optional(),
    banner: z.string().optional(),
    portrait: z.string().optional(),
    item_type: z.string().optional(),
    rarity: z.string().optional(),
    attunement: z.boolean().optional(),
    homebrew: z.boolean().optional(),
    current_holder: z.string().optional(),
    cr: z.union([z.number(), z.string()]).optional(),
    creature_type: z.string().optional(),

    // session-specific
    session_number: z.number().optional(),
    session_date: z.coerce.date().or(z.string()).optional(),
    beat_number: z.number().optional(),

    // situation-specific
    lifecycle: z.string().nullable().optional(),
    narrative_island: z.string().nullable().optional(),
    contains_situations: z.array(z.string()).default([]),

    // place-specific
    category: z.string().optional(),
    visibility: z.string().optional(),
    region: z.string().optional(),
    parent_location: z.string().optional(),
  }).passthrough(),
});

export const collections = { wiki };
