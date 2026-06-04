import { z } from 'zod';

export const wikiEntrySchema = z
  .object({
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
  })
  .passthrough();

/**
 * Build the wiki entry schema using a caller-provided Zod instance.
 * Astro's content collections require schemas built from `astro/zod`
 * for JSON schema generation. Call this with `z` from `astro/zod`.
 */
export function buildWikiEntrySchema(zod: typeof z) {
  return zod
    .object({
      type: zod.string(),
      subtype: zod.string().optional(),
      campaign: zod.string().default('shattered-sea'),
      status: zod.string().default('unknown'),
      audience: zod.string().default('dm'),
      publish: zod.boolean().default(false),
      summary: zod.string().default(''),
      created: zod.coerce.date().optional(),
      updated: zod.coerce.date().optional(),
      tags: zod.array(zod.string()).default([]),
      sources: zod.array(zod.string()).default([]),
      confidence_level: zod.string().optional(),
      title: zod.string().optional(),

      aliases: zod.array(zod.string()).default([]),
      species: zod.string().optional(),
      pronouns: zod.string().optional(),
      banner: zod.string().optional(),
      portrait: zod.string().optional(),
      item_type: zod.string().optional(),
      rarity: zod.string().optional(),
      attunement: zod.boolean().optional(),
      homebrew: zod.boolean().optional(),
      current_holder: zod.string().optional(),
      cr: zod.union([zod.number(), zod.string()]).optional(),
      creature_type: zod.string().optional(),

      session_number: zod.number().optional(),
      session_date: zod.coerce.date().or(zod.string()).optional(),
      beat_number: zod.number().optional(),

      lifecycle: zod.string().nullable().optional(),
      narrative_island: zod.string().nullable().optional(),
      contains_situations: zod.array(zod.string()).default([]),

      category: zod.string().optional(),
      visibility: zod.string().optional(),
      region: zod.string().optional(),
      parent_location: zod.string().optional(),
    })
    .passthrough();
}
