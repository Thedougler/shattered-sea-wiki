export { buildAssetMap } from './asset-map.js';
export { type FixResult, fixFrontmatter } from './fix-frontmatter.js';
export {
  detectDrift,
  type DriftEntry,
  getField,
  getFields,
  setField,
  type SetFieldResult,
  syncField,
} from './frontmatter-ops.js';
export {
  firstH1,
  getSummary,
  parseFields,
  type SplitResult,
  splitFrontmatter,
} from './frontmatter.js';
export { generateIndex, generateIndexFile } from './index-gen.js';
export {
  ALLOWED_TYPES_BY_PATH,
  inferSubtype,
  inferType,
  TYPE_EXTRA_FIELDS,
  UNIVERSAL_FIELDS,
} from './path-inference.js';
export { buildWikiEntrySchema, wikiEntrySchema } from './schema.js';
export { deriveSlug, slugify, titleCase } from './slug.js';
export {
  ALIASES,
  CANONICAL,
  classify,
  DEPRECATED_ENTITY_NAMES,
  DEPRECATED_FRONTMATTER,
  DEPRECATED_SOURCE,
  DEPRECATED_SYSTEM,
  TAG_LIMIT,
  type TagCategory,
} from './taxonomy.js';
export { iterWikiFiles, relPath, resolveVaultRoot } from './vault.js';
export {
  type BacklinkEntry,
  buildBacklinks,
  buildSlugSet,
} from './wiki-graph.js';
export {
  escapeAttr,
  escapeHtml,
  parseWikilinks,
  resolveWikilink,
  type Wikilink,
} from './wikilinks.js';
export {
  applyFix,
  type Batch,
  batchIssues,
  checkFile,
  diffSnapshots,
  filesChangedSince,
  formatTopActions,
  type Issue,
  lint,
  type LintOptions,
  type LintResult,
  type Severity,
  SEVERITIES,
  writeReport,
} from './lint.js';
export {
  countHooks,
  countPendingIngest,
  countScriptTests,
  countWikiFiles,
  diffHealthSnapshots,
  formatDiff,
  formatHistory,
  type HealthSnapshot,
  type InfraInventory,
  inventoryInfrastructure,
  loadSnapshots,
  parseDailyLog,
  runLint,
  saveSnapshot,
  type SnapshotDelta,
  takeSnapshot,
} from './health.js';
