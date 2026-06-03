export { deriveSlug, slugify, titleCase } from './slug.js';
export { resolveVaultRoot, iterWikiFiles, relPath } from './vault.js';
export {
  inferType,
  inferSubtype,
  UNIVERSAL_FIELDS,
  TYPE_EXTRA_FIELDS,
  ALLOWED_TYPES_BY_PATH,
} from './path-inference.js';
export {
  splitFrontmatter,
  parseFields,
  getSummary,
  firstH1,
  type SplitResult,
} from './frontmatter.js';
export { wikiEntrySchema } from './schema.js';
export {
  parseWikilinks,
  resolveWikilink,
  escapeHtml,
  escapeAttr,
  type Wikilink,
} from './wikilinks.js';
export {
  buildSlugSet,
  buildBacklinks,
  type BacklinkEntry,
} from './wiki-graph.js';
export { buildAssetMap } from './asset-map.js';
export {
  CANONICAL,
  ALIASES,
  DEPRECATED_FRONTMATTER,
  DEPRECATED_ENTITY_NAMES,
  DEPRECATED_SOURCE,
  DEPRECATED_SYSTEM,
  TAG_LIMIT,
  classify,
  type TagCategory,
} from './taxonomy.js';
export { generateIndex, generateIndexFile } from './index-gen.js';
export { fixFrontmatter, type FixResult } from './fix-frontmatter.js';
