import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { parse as parseYaml, stringify as stringifyYaml } from 'yaml';
import fg from 'fast-glob';
import {
  inferType,
  inferSubtype,
  UNIVERSAL_FIELDS,
  TYPE_EXTRA_FIELDS,
  ALLOWED_TYPES_BY_PATH,
} from './path-inference.js';
import { classify, TAG_LIMIT } from './taxonomy.js';
import { relPath } from './vault.js';
import { deriveSlug } from './slug.js';

// ─── Types ──────────────────────────────────────────────────────────────────

export type Severity = 'error' | 'warning' | 'quality';
export const SEVERITIES: readonly Severity[] = ['error', 'warning', 'quality'];

export interface Issue {
  severity: Severity;
  rule: string;
  path: string;
  detail: string;
  fix?: string;
}

export interface LintOptions {
  fix?: boolean;
  fixTags?: boolean;
  since?: string;
  minSeverity?: Severity;
  paths?: string[];
}

export interface LintResult {
  issues: Issue[];
  fixed: Array<{ file: string; changed: string[] }>;
  counts: Record<Severity, number>;
}

export interface Batch {
  rule: string;
  severity: Severity;
  fix: string;
  count: number;
  files: string[];
  detail: string;
  priority: number;
}

interface VaultRecord {
  relpath: string;
  data: Record<string, unknown>;
  body: string;
}

// ─── Constants ──────────────────────────────────────────────────────────────

const SKIP_CONTENT = new Set([
  'index.md',
  'log.md',
  'work-queue.md',
  'discrepancy-log.md',
  'hot.md',
  'review-queue.md',
]);

const SKIP_AS_SOURCE = new Set([
  'index.md',
  'log.md',
  'work-queue.md',
  'discrepancy-log.md',
  'review-queue.md',
]);

const ORPHAN_EXEMPT_PREFIXES = [
  'wiki/system/',
  'wiki/dm/',
  'wiki/sessions/',
  'wiki/entities/characters/pcs/',
];

const STUB_SUMMARY = 'Stub — no summary yet.';
const KEBAB_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const FENCE_RE = /```.*?```/gs;
const INLINE_CODE_RE = /`[^`\n]*`/g;

const ASSET_EXTS = new Set([
  '.webp', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp', '.pdf',
  '.mp3', '.m4a', '.aac', '.flac', '.mp4', '.m4v', '.mov', '.webm', '.wav', '.ogg',
  '.json', '.canvas', '.excalidraw',
]);

const STATUS_CANONICAL: Record<string, string> = {
  deceased: 'dead',
  presumed_dead: 'dead',
  open: 'active',
};

const DEAD_STATUSES = new Set(['dead', 'deceased', 'destroyed', 'presumed_dead']);

const XREF_ROLE_FIELDS: Record<string, string> = {
  captain: 'captains',
  current_holder: 'holds',
  owner: 'owns',
};

const SINGLETON_WHITELIST = new Set([
  'cr', 'aliases', 'region', 'species', 'pronouns', 'portrait',
  'ship_class', 'hull_points', 'crew_capacity', 'speed', 'captain',
  'current_holder', 'parent_location', 'narrative_island',
  'session_number', 'session_date', 'alignment', 'ac', 'hp', 'size',
  'challenge_rating', 'damage_resistances', 'damage_immunities',
  'condition_immunities', 'senses', 'languages', 'environment',
  'rarity', 'attunement', 'item_type', 'weight', 'cost',
  'faction', 'domain', 'pantheon', 'population', 'government',
  'defenses', 'trade_goods', 'climate',
]);

// ─── Value validators ───────────────────────────────────────────────────────

type Validator = (value: unknown) => string | null;

const VALUE_VALIDATORS: Record<string, Validator> = {
  campaign: (v) =>
    v === 'shattered-sea' ? null : "must be 'shattered-sea'",
  audience: (v) =>
    typeof v === 'string' && ['agent', 'dm', 'players'].includes(v)
      ? null
      : "must be 'agent', 'dm', or 'players'",
  publish: (v) => (typeof v === 'boolean' ? null : 'must be a boolean'),
  status: (v) =>
    typeof v === 'string' && v.length > 0 ? null : 'must be a non-empty string',
  summary: (v) =>
    typeof v === 'string' && v.length > 0 ? null : 'must be a non-empty string',
  created: (v) =>
    typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v)
      ? null
      : 'must be YYYY-MM-DD format',
  updated: (v) =>
    typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v)
      ? null
      : 'must be YYYY-MM-DD format',
  confidence_level: (v) =>
    typeof v === 'string' &&
    ['observed', 'confirmed', 'inferred', 'low', 'medium', 'high'].includes(v)
      ? null
      : 'must be observed, confirmed, inferred, low, medium, or high',
  lifecycle: (v) =>
    typeof v === 'string' && ['dormant', 'active', 'resolved'].includes(v)
      ? null
      : 'must be dormant, active, or resolved',
  token_profile: (v) =>
    typeof v === 'string' &&
    ['on-demand', 'always-read', 'quick-ref', 'map'].includes(v)
      ? null
      : 'must be on-demand, always-read, quick-ref, or map',
  session_number: (v) =>
    typeof v === 'number' && Number.isInteger(v) ? null : 'must be an integer',
  portable: (v) => (typeof v === 'boolean' ? null : 'must be a boolean'),
  tags: (v) => (Array.isArray(v) ? null : 'must be an array'),
  sources: (v) => (Array.isArray(v) ? null : 'must be an array'),
  entry_points: (v) => (Array.isArray(v) ? null : 'must be an array'),
  contains_situations: (v) => (Array.isArray(v) ? null : 'must be an array'),
  mandatory_for: (v) => (Array.isArray(v) ? null : 'must be an array'),
};

// ─── Rule priorities (for --top batching) ───────────────────────────────────

const RULE_PRIORITY: Record<string, number> = {
  'broken-wikilink': 1,
  'missing-frontmatter': 1,
  'unparseable-frontmatter': 1,
  'naming-convention': 2,
  'invalid-value': 2,
  'duplicate-slug': 2,
  'type-path-mismatch': 3,
  'lifecycle-folder-mismatch': 3,
  'dead-entity-ref': 4,
  'island-situation-mismatch': 4,
  'status-drift': 4,
  'missing-required-field': 5,
  'relationships-in-frontmatter': 6,
  'tag-deprecated': 7,
  'tag-alias': 7,
  'tag-over-limit': 7,
  'tag-unknown': 8,
  'tag-variant': 8,
  'summary-stale': 9,
  'parent-gap': 9,
  'orphan': 10,
  'deadend': 10,
  'bare-wikilink': 11,
  'singleton-property': 12,
};

const DECISION_RULES = new Set([
  'missing-frontmatter',
  'unparseable-frontmatter',
  'broken-wikilink',
  'naming-convention',
  'duplicate-slug',
  'invalid-value',
  'type-path-mismatch',
  'lifecycle-folder-mismatch',
  'dead-entity-ref',
  'island-situation-mismatch',
]);

const BACKLOG_HINT: Record<string, string> = {
  'missing-required-field': 'run `sea lint --fix`',
  'relationships-in-frontmatter': 'weave into body prose, then delete the field',
  'bare-wikilink': 'add display aliases',
  orphan: 'link from a natural parent',
  'summary-stale': 'write a concrete summary',
  deadend: 'add wikilinks to related pages',
  'tag-deprecated':
    'read the file; remove deprecated tag and choose canonical replacements',
  'tag-alias':
    'read the file; replace alias with canonical form shown in the fix message',
  'tag-unknown':
    'read the file; replace with canonical tags or propose adding to taxonomy',
  'tag-over-limit': 'read the file; trim to ≤5 canonical tags',
  'tag-variant': 'consolidate plural/singular tag variants',
  'singleton-property': 'verify not a typo, or add to schema',
  'status-drift': 'use the canonical status value',
  'parent-gap': 'add wikilink in the parent page',
};

// ─── Helpers ────────────────────────────────────────────────────────────────

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

function slugOf(p: string): string {
  return path.basename(p, '.md');
}

function isAsset(target: string): boolean {
  return ASSET_EXTS.has(path.extname(target).toLowerCase());
}

function isOrphanExempt(rp: string): boolean {
  return ORPHAN_EXEMPT_PREFIXES.some((pfx) => rp.startsWith(pfx));
}

function splitDoc(text: string): { fm: string; body: string; had: boolean } {
  const lines = text.split('\n');
  if (!lines.length || lines[0].trim() !== '---') {
    return { fm: '', body: text, had: false };
  }
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === '---') {
      return {
        fm: lines.slice(1, i).join('\n'),
        body: lines.slice(i + 1).join('\n'),
        had: true,
      };
    }
  }
  return { fm: '', body: text, had: false };
}

function loadFrontmatter(fmText: string): Record<string, unknown> {
  if (!fmText.trim()) return {};
  const data = parseYaml(fmText);
  return (data as Record<string, unknown>) ?? {};
}

function scannable(body: string): string {
  return body
    .replace(FENCE_RE, '')
    .replace(INLINE_CODE_RE, '')
    .replace(/\\\|/g, '|');
}

function* wikilinkTargets(
  text: string,
): Generator<{ target: string; hasAlias: boolean; isEmbed: boolean }> {
  const re = /(!?)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    const isEmbed = Boolean(m[1]);
    let target = path.basename(m[2].trim());
    if (target.endsWith('.md')) target = target.slice(0, -3);
    yield { target, hasAlias: Boolean(m[3]), isEmbed };
  }
}

function requiredFields(rp: string): readonly string[] {
  const t = inferType(rp);
  const extra = TYPE_EXTRA_FIELDS[t] ?? [];
  return [...UNIVERSAL_FIELDS, ...extra];
}

function fieldDefaults(rp: string): Record<string, unknown> {
  return {
    type: inferType(rp),
    subtype: inferSubtype(rp),
    campaign: 'shattered-sea',
    status: 'unknown',
    audience: 'dm',
    publish: false,
    summary: STUB_SUMMARY,
    created: today(),
    updated: today(),
    tags: [],
    sources: ['Unknown'],
    confidence_level: 'medium',
    relationships: [],
    lifecycle: 'dormant',
    narrative_island: 'none',
    portable: false,
    entry_points: [],
    contains_situations: [],
    session_number: 0,
    session_date: 'unknown',
    system_role: 'unknown',
    token_profile: 'on-demand',
    mandatory_for: [],
    update_trigger: '',
  };
}

function getSummary(data: Record<string, unknown>): string {
  const raw = data.summary;
  if (typeof raw !== 'string') return '';
  return raw;
}

function extractSlug(value: unknown): string | null {
  const s = String(value ?? '');
  const re = /\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]/;
  const m = re.exec(s);
  if (!m) return null;
  let target = path.basename(m[1].trim());
  if (target.endsWith('.md')) target = target.slice(0, -3);
  return target.toLowerCase();
}

function relationshipEntries(
  node: unknown,
): Array<{ target: string; note: string }> {
  const entries: Array<{ target: string; note: string }> = [];
  if (node == null) return entries;
  const items = Array.isArray(node) ? node : [node];
  for (const item of items) {
    if (typeof item === 'object' && item !== null && !Array.isArray(item)) {
      const obj = item as Record<string, unknown>;
      const targetRaw = String(obj.target ?? '');
      const note = String(obj.relation ?? '').trim();
      for (const { target } of wikilinkTargets(targetRaw)) {
        entries.push({ target, note });
      }
    } else {
      const text = String(item);
      const targets = [...wikilinkTargets(text)].map((t) => t.target);
      const note = text
        .replace(/(!?)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]/g, '')
        .replace(/^[\s—\-:|]+|[\s—\-:|]+$/g, '');
      for (const t of targets) {
        entries.push({ target: t, note });
      }
    }
  }
  return entries;
}

// ─── Per-file checks ────────────────────────────────────────────────────────

function validateValues(
  rp: string,
  data: Record<string, unknown>,
): Issue[] {
  const issues: Issue[] = [];
  for (const [field, validator] of Object.entries(VALUE_VALIDATORS)) {
    if (!(field in data)) continue;
    const msg = validator(data[field]);
    if (msg) {
      issues.push({
        severity: 'error',
        rule: 'invalid-value',
        path: rp,
        detail: `${field}: ${msg}`,
      });
    }
  }
  return issues;
}

export function checkFile(
  rp: string,
  data: Record<string, unknown>,
  body: string,
): Issue[] {
  const issues: Issue[] = [];

  issues.push(...validateValues(rp, data));

  for (const field of requiredFields(rp)) {
    if (!(field in data)) {
      issues.push({
        severity: 'warning',
        rule: 'missing-required-field',
        path: rp,
        detail: field,
        fix: `run sea lint --fix ${rp}`,
      });
    }
  }

  const expectedType = inferType(rp);
  const actualType = String(data.type ?? '').trim();
  const allowedTypes = ALLOWED_TYPES_BY_PATH.find(([prefix]) =>
    rp.startsWith(prefix),
  );
  const typeOk =
    !actualType ||
    expectedType === 'unknown' ||
    expectedType === 'governance' ||
    (allowedTypes ? allowedTypes[1].has(actualType) : actualType === expectedType);
  if (!typeOk) {
    issues.push({
      severity: 'warning',
      rule: 'type-path-mismatch',
      path: rp,
      detail: `type: '${actualType}' but path implies '${expectedType}'`,
    });
  }

  const summary = getSummary(data);
  if (!summary || summary === STUB_SUMMARY) {
    issues.push({
      severity: 'quality',
      rule: 'summary-stale',
      path: rp,
      detail: 'summary missing or still the stub default — write a concrete one',
    });
  }

  const rels = relationshipEntries(data.relationships);
  if (rels.length) {
    const bodyLinks = new Set<string>();
    for (const { target } of wikilinkTargets(scannable(body))) {
      if (!isAsset(target)) bodyLinks.add(target.toLowerCase());
    }
    const parts = rels.map(({ target, note }) => {
      const where = bodyLinks.has(target.toLowerCase()) ? 'in body' : 'NOT in body';
      const noteBit = note ? ` — ${note}` : '';
      return `[[${target}]] (${where})${noteBit}`;
    });
    issues.push({
      severity: 'warning',
      rule: 'relationships-in-frontmatter',
      path: rp,
      detail: `${rels.length} relationship(s) to migrate: ${parts.join('; ')}`,
      fix: 'weave each into the prose with a wikilink (carry the note), then delete the relationships field',
    });
  }

  if (rp.startsWith('wiki/situations/')) {
    const parts = rp.split('/');
    const folder = parts.length > 3 ? parts[2] : '';
    const lifecycle = String(data.lifecycle ?? '').trim();
    if (
      ['active', 'dormant', 'resolved'].includes(folder) &&
      lifecycle &&
      lifecycle !== folder
    ) {
      issues.push({
        severity: 'warning',
        rule: 'lifecycle-folder-mismatch',
        path: rp,
        detail: `lifecycle: '${lifecycle}' but file is in situations/${folder}/`,
        fix: `set lifecycle to '${folder}' or move the file`,
      });
    }
  }

  return issues;
}

function checkNaming(rp: string): Issue | null {
  const name = slugOf(rp);
  if (!KEBAB_RE.test(name)) {
    return {
      severity: 'error',
      rule: 'naming-convention',
      path: rp,
      detail: `filename '${name}' is not kebab-case`,
      fix: 'rename to kebab-case and update inbound wikilinks',
    };
  }
  return null;
}

// ─── Cross-file checks ─────────────────────────────────────────────────────

function crossFileChecks(
  records: VaultRecord[],
  slugToPaths: Map<string, string[]>,
): Issue[] {
  const issues: Issue[] = [];
  const lowerIndex = new Map<string, string[]>();
  for (const [slug, paths] of slugToPaths) {
    const low = slug.toLowerCase();
    const existing = lowerIndex.get(low) ?? [];
    existing.push(...paths);
    lowerIndex.set(low, existing);
  }

  for (const [low, paths] of lowerIndex) {
    if (low === 'index') continue;
    if (paths.length > 1) {
      const sorted = [...paths].sort();
      for (const p of paths) {
        const rest = sorted.filter((o) => o !== p);
        issues.push({
          severity: 'error',
          rule: 'duplicate-slug',
          path: p,
          detail: `slug also used by: ${rest.join(', ')} — wikilinks to it are ambiguous`,
          fix: 'rename one file to a distinct slug and update its inbound links',
        });
      }
    }
  }

  const inbound = new Map<string, Set<string>>();
  for (const { relpath } of records) inbound.set(relpath, new Set());

  const hasOutgoing = new Set<string>();

  for (const { relpath, body } of records) {
    if (SKIP_AS_SOURCE.has(path.basename(relpath))) continue;
    const scan = scannable(body);
    const seenBroken = new Set<string>();
    let fileHasLinks = false;

    for (const { target, hasAlias, isEmbed } of wikilinkTargets(scan)) {
      if (isAsset(target)) continue;
      fileHasLinks = true;
      const matches = lowerIndex.get(target.toLowerCase());
      if (matches) {
        for (const tgtPath of matches) {
          if (tgtPath !== relpath) {
            inbound.get(tgtPath)?.add(relpath);
          }
        }
        if (!hasAlias && !isEmbed) {
          issues.push({
            severity: 'quality',
            rule: 'bare-wikilink',
            path: relpath,
            detail: `[[${target}]] has no display alias`,
            fix: `alias it: [[${target}|Display Name]]`,
          });
        }
      } else {
        if (!seenBroken.has(target)) {
          seenBroken.add(target);
          issues.push({
            severity: 'error',
            rule: 'broken-wikilink',
            path: relpath,
            detail: `[[${target}]] resolves to no page`,
            fix: `create a stub for '${target}' or fix the link`,
          });
        }
      }
    }
    if (fileHasLinks) hasOutgoing.add(relpath);
  }

  for (const { relpath } of records) {
    if (SKIP_CONTENT.has(path.basename(relpath))) continue;
    if (isOrphanExempt(relpath)) continue;
    if (SKIP_AS_SOURCE.has(path.basename(relpath))) continue;
    if (!hasOutgoing.has(relpath)) {
      issues.push({
        severity: 'quality',
        rule: 'deadend',
        path: relpath,
        detail: 'no outgoing wikilinks',
        fix: 'add wikilinks to related pages',
      });
    }
  }

  for (const { relpath } of records) {
    if (SKIP_CONTENT.has(path.basename(relpath))) continue;
    if (isOrphanExempt(relpath)) continue;
    const inboundSet = inbound.get(relpath);
    if (!inboundSet || inboundSet.size === 0) {
      issues.push({
        severity: 'quality',
        rule: 'orphan',
        path: relpath,
        detail: 'no other page links here',
        fix: 'link it from a natural parent page',
      });
    }
  }

  return issues;
}

// ─── Vault-wide checks ─────────────────────────────────────────────────────

function checkTags(records: VaultRecord[]): Issue[] {
  const issues: Issue[] = [];
  const fixSuffix = 'read this file and select canonical tags from wiki/system/taxonomy.md';

  for (const { relpath, data } of records) {
    if (SKIP_CONTENT.has(path.basename(relpath))) continue;
    const tags = data.tags;
    if (!Array.isArray(tags)) continue;

    const contentTags: string[] = [];
    for (const raw of tags) {
      const tag = String(raw).trim();
      if (!tag) continue;
      const [category, canonical] = classify(tag);

      if (category === 'canonical') {
        contentTags.push(tag);
      } else if (category === 'alias') {
        contentTags.push(tag);
        issues.push({
          severity: 'warning',
          rule: 'tag-alias',
          path: relpath,
          detail: `'${tag}' is an alias — canonical form is '${canonical}'`,
          fix: `replace with '${canonical}'; then ${fixSuffix}`,
        });
      } else if (category === 'deprecated-fm') {
        contentTags.push(tag);
        issues.push({
          severity: 'warning',
          rule: 'tag-deprecated',
          path: relpath,
          detail: `'${tag}' duplicates a frontmatter field — remove it`,
          fix: fixSuffix,
        });
      } else if (category === 'deprecated-entity') {
        contentTags.push(tag);
        issues.push({
          severity: 'warning',
          rule: 'tag-deprecated',
          path: relpath,
          detail: `'${tag}' is an entity name — use a wikilink in the body instead`,
          fix: `add wikilink to [[${tag}]] in body; ${fixSuffix}`,
        });
      } else if (category === 'deprecated-source') {
        contentTags.push(tag);
        issues.push({
          severity: 'warning',
          rule: 'tag-deprecated',
          path: relpath,
          detail: `'${tag}' is a source citation — move to sources: frontmatter field`,
          fix: `move to sources: field; ${fixSuffix}`,
        });
      } else if (category === 'deprecated-system') {
        contentTags.push(tag);
        issues.push({
          severity: 'warning',
          rule: 'tag-deprecated',
          path: relpath,
          detail: `'${tag}' is a system/process tag — remove it`,
          fix: fixSuffix,
        });
      } else if (category === 'unknown') {
        contentTags.push(tag);
        issues.push({
          severity: 'quality',
          rule: 'tag-unknown',
          path: relpath,
          detail: `'${tag}' not in controlled vocabulary`,
          fix: `${fixSuffix}, or propose adding '${tag}' if it covers 5+ files across 3+ entity types`,
        });
      }
    }

    if (contentTags.length > TAG_LIMIT) {
      issues.push({
        severity: 'warning',
        rule: 'tag-over-limit',
        path: relpath,
        detail: `${contentTags.length} content tags (limit ${TAG_LIMIT}): ${contentTags.join(', ')}`,
        fix: fixSuffix,
      });
    }
  }

  return issues;
}

function checkTagVariants(records: VaultRecord[]): Issue[] {
  const tagCounter = new Map<string, number>();
  const tagFiles = new Map<string, string[]>();

  for (const { relpath, data } of records) {
    const tags = data.tags;
    if (!Array.isArray(tags)) continue;
    for (const raw of tags) {
      const t = String(raw).trim().toLowerCase();
      if (!t) continue;
      tagCounter.set(t, (tagCounter.get(t) ?? 0) + 1);
      const files = tagFiles.get(t) ?? [];
      files.push(relpath);
      tagFiles.set(t, files);
    }
  }

  const issues: Issue[] = [];
  const seen = new Set<string>();

  for (const tag of [...tagCounter.keys()].sort()) {
    if (seen.has(tag)) continue;
    const variants: string[] = [];
    if (tag.endsWith('s') && tagCounter.has(tag.slice(0, -1))) {
      variants.push(tag.slice(0, -1));
    }
    if (tagCounter.has(tag + 's')) {
      variants.push(tag + 's');
    }
    for (const variant of variants) {
      if (seen.has(variant)) continue;
      const tagCount = tagCounter.get(tag)!;
      const varCount = tagCounter.get(variant)!;
      const [lesser, greater] =
        tagCount < varCount ? [tag, variant] : [variant, tag];
      seen.add(lesser);
      const files = tagFiles.get(lesser) ?? [];
      for (const f of files.slice(0, 3)) {
        issues.push({
          severity: 'quality',
          rule: 'tag-variant',
          path: f,
          detail: `tag '${lesser}' may be a variant of '${greater}' (${tagCounter.get(greater)} uses)`,
          fix: `consolidate to '${greater}'`,
        });
      }
    }
  }

  return issues;
}

function checkSingletonProperties(
  records: VaultRecord[],
  schemaProps: Set<string>,
): Issue[] {
  const propCounter = new Map<string, number>();
  const propFiles = new Map<string, string>();

  for (const { relpath, data } of records) {
    for (const key of Object.keys(data)) {
      propCounter.set(key, (propCounter.get(key) ?? 0) + 1);
      propFiles.set(key, relpath);
    }
  }

  const known = new Set([...schemaProps, ...SINGLETON_WHITELIST]);
  const issues: Issue[] = [];

  for (const [prop, count] of propCounter) {
    if (count === 1 && !known.has(prop)) {
      issues.push({
        severity: 'quality',
        rule: 'singleton-property',
        path: propFiles.get(prop)!,
        detail: `property '${prop}' appears only in this file and is not in the schema`,
        fix: 'verify this isn\'t a typo, or add it to the schema if intentional',
      });
    }
  }

  return issues;
}

function checkLoreConsistency(
  records: VaultRecord[],
  slugToPaths: Map<string, string[]>,
): Issue[] {
  const issues: Issue[] = [];
  const slugToFirst = new Map<string, string>();
  for (const [slug, paths] of slugToPaths) {
    slugToFirst.set(slug.toLowerCase(), paths[0]);
  }

  const dataByPath = new Map<string, Record<string, unknown>>();
  const bodyByPath = new Map<string, string>();
  for (const { relpath, data, body } of records) {
    dataByPath.set(relpath, data);
    bodyByPath.set(relpath, body);
  }

  const entityStatus = new Map<string, string>();
  for (const { relpath, data } of records) {
    const status = String(data.status ?? '').trim().toLowerCase();
    if (status) entityStatus.set(slugOf(relpath).toLowerCase(), status);
  }

  for (const { relpath, data } of records) {
    // Dead-entity references
    for (const [field] of Object.entries(XREF_ROLE_FIELDS)) {
      const val = data[field];
      if (!val) continue;
      const targetSlug = extractSlug(val);
      if (!targetSlug) continue;
      const targetStatus = entityStatus.get(targetSlug) ?? '';
      if (DEAD_STATUSES.has(targetStatus)) {
        issues.push({
          severity: 'warning',
          rule: 'dead-entity-ref',
          path: relpath,
          detail: `${field}: [[${targetSlug}]] is ${targetStatus}`,
          fix: `update ${field} or mark this file's status accordingly`,
        });
      }
    }

    // Parent-location bidirectionality
    const parentVal = data.parent_location;
    if (parentVal) {
      const parentSlug = extractSlug(parentVal);
      if (parentSlug) {
        const parentPath = slugToFirst.get(parentSlug);
        if (parentPath) {
          const parentBody = bodyByPath.get(parentPath) ?? '';
          const childSlug = slugOf(relpath).toLowerCase();
          if (!parentBody.toLowerCase().includes(childSlug)) {
            issues.push({
              severity: 'quality',
              rule: 'parent-gap',
              path: relpath,
              detail: `parent_location [[${parentSlug}]] doesn't mention this page`,
              fix: `add a wikilink to [[${childSlug}]] in ${parentPath}`,
            });
          }
        }
      }
    }

    // contains_situations ↔ narrative_island consistency
    const cs = data.contains_situations;
    if (Array.isArray(cs)) {
      const islandSlug = slugOf(relpath).toLowerCase();
      for (const sit of cs) {
        const sitSlug = extractSlug(String(sit));
        if (!sitSlug) continue;
        const sitPath = slugToFirst.get(sitSlug);
        if (!sitPath) continue;
        const sitData = dataByPath.get(sitPath) ?? {};
        const sitNi = String(sitData.narrative_island ?? '')
          .trim()
          .toLowerCase();
        if (sitNi && sitNi !== 'none' && !sitNi.includes(islandSlug)) {
          issues.push({
            severity: 'warning',
            rule: 'island-situation-mismatch',
            path: sitPath,
            detail: `narrative_island='${sitNi}' but listed in ${relpath}`,
            fix: `set narrative_island to match '${islandSlug}'`,
          });
        } else if (!sitNi || sitNi === 'none') {
          issues.push({
            severity: 'warning',
            rule: 'island-situation-mismatch',
            path: sitPath,
            detail: `narrative_island is unset but listed in ${relpath}`,
            fix: `set narrative_island to '${islandSlug}'`,
          });
        }
      }
    }

    // Status vocabulary drift
    const status = String(data.status ?? '').trim().toLowerCase();
    if (status in STATUS_CANONICAL) {
      const canonical = STATUS_CANONICAL[status];
      issues.push({
        severity: 'warning',
        rule: 'status-drift',
        path: relpath,
        detail: `status '${status}' — use '${canonical}' for consistency`,
        fix: `set status to '${canonical}'`,
      });
    }
  }

  return issues;
}

// ─── Auto-fix ───────────────────────────────────────────────────────────────

function standardize(
  rp: string,
  data: Record<string, unknown>,
): { data: Record<string, unknown>; changed: string[] } {
  const changed: string[] = [];
  const defaults = fieldDefaults(rp);

  // Strip junk fields
  for (const f of ['title', 'cssclasses']) {
    if (f in data) {
      delete data[f];
      changed.push(`-${f}`);
    }
  }

  // Strip null-valued fields
  const nullKeys = Object.keys(data).filter((k) => data[k] === null);
  for (const k of nullKeys) delete data[k];
  if (nullKeys.length) changed.push('-nulls');

  // sources: ["Unknown"] → []
  if (
    Array.isArray(data.sources) &&
    data.sources.length === 1 &&
    data.sources[0] === 'Unknown'
  ) {
    data.sources = [];
    changed.push('sources(clean)');
  }

  // aliases: [] → strip
  if (Array.isArray(data.aliases) && data.aliases.length === 0) {
    delete data.aliases;
    changed.push('-aliases');
  }

  // Drop empty relationships: []
  if (Array.isArray(data.relationships) && data.relationships.length === 0) {
    delete data.relationships;
    changed.push('-relationships');
  }

  // Status-drift: mechanical synonym replacement
  if (
    typeof data.status === 'string' &&
    data.status.trim().toLowerCase() in STATUS_CANONICAL
  ) {
    data.status = STATUS_CANONICAL[data.status.trim().toLowerCase()];
    changed.push('status');
  }

  // Lifecycle-folder sync
  if (rp.startsWith('wiki/situations/')) {
    const parts = rp.split('/');
    if (parts.length > 3) {
      const folder = parts[2];
      const lifecycle = String(data.lifecycle ?? '').trim();
      if (
        ['active', 'dormant', 'resolved'].includes(folder) &&
        lifecycle &&
        lifecycle !== folder
      ) {
        data.lifecycle = folder;
        changed.push('lifecycle');
      }
    }
  }

  // Add missing required fields
  for (const field of requiredFields(rp)) {
    if (!(field in data)) {
      data[field] = defaults[field];
      changed.push(field);
    }
  }

  // Coerce known booleans
  for (const field of ['publish', 'portable']) {
    if (field in data && typeof data[field] === 'string') {
      const v = (data[field] as string).trim().toLowerCase();
      if (v === 'true' || v === 'false') {
        data[field] = v === 'true';
        changed.push(field);
      }
    }
  }

  // Canonical key order
  const order = requiredFields(rp).filter((f) => f in data) as string[];
  for (const k of Object.keys(data)) {
    if (!order.includes(k)) order.push(k);
  }
  const reordered = Object.keys(data);
  const needsReorder = reordered.some((k, i) => k !== order[i]);
  if (needsReorder && !changed.includes('(reorder)')) {
    changed.push('(reorder)');
  }
  const newData: Record<string, unknown> = {};
  for (const k of order) {
    if (k in data) newData[k] = data[k];
  }

  return { data: newData, changed };
}

function fixSafeTags(data: Record<string, unknown>): string[] {
  const tags = data.tags;
  if (!Array.isArray(tags)) return [];

  const newTags: string[] = [];
  const changes: string[] = [];
  const seen = new Set<string>();

  for (const raw of tags) {
    const tag = String(raw).trim();
    if (!tag) continue;
    const [category, canonical] = classify(tag);

    if (category === 'alias' && canonical) {
      if (!seen.has(canonical.toLowerCase())) {
        newTags.push(canonical);
        seen.add(canonical.toLowerCase());
        if (canonical !== tag) changes.push(`tag:${tag}->${canonical}`);
      } else {
        changes.push(`tag:-${tag}(dup)`);
      }
    } else if (category === 'deprecated-fm' || category === 'deprecated-system') {
      changes.push(`tag:-${tag}`);
    } else if (category === 'canonical') {
      if (!seen.has(tag.toLowerCase())) {
        newTags.push(tag);
        seen.add(tag.toLowerCase());
      }
    } else {
      if (!seen.has(tag.toLowerCase())) {
        newTags.push(tag);
        seen.add(tag.toLowerCase());
      }
    }
  }

  if (changes.length) {
    data.tags = newTags;
  }

  return changes;
}

export function applyFix(
  filePath: string,
  repoRoot: string,
  fixTags = false,
): string[] {
  const rp = relPath(filePath, repoRoot);
  const text = fs.readFileSync(filePath, 'utf-8');
  const { fm, body, had } = splitDoc(text);

  const parsed = had ? loadFrontmatter(fm) : {};
  const { data: newData, changed } = standardize(rp, { ...parsed });
  if (fixTags) changed.push(...fixSafeTags(newData));

  const newFm = stringifyYaml(newData, { lineWidth: 0 }).trimEnd();
  const rebuilt = `---\n${newFm}\n---\n${body}`;

  if (rebuilt === text) return [];
  fs.writeFileSync(filePath, rebuilt, 'utf-8');
  return changed.length ? changed : ['(reformat)'];
}

// ─── Batch / output helpers ─────────────────────────────────────────────────

export function batchIssues(issues: Issue[]): Batch[] {
  const groups = new Map<string, Issue[]>();
  for (const i of issues) {
    const key = `${i.rule}\0${i.fix ?? ''}`;
    const group = groups.get(key) ?? [];
    group.push(i);
    groups.set(key, group);
  }

  const batches: Batch[] = [];
  for (const [, items] of groups) {
    const sev = items.reduce(
      (best, i) =>
        SEVERITIES.indexOf(i.severity) < SEVERITIES.indexOf(best)
          ? i.severity
          : best,
      'quality' as Severity,
    );
    const files = [...new Set(items.map((i) => i.path))].sort();
    batches.push({
      rule: items[0].rule,
      severity: sev,
      fix: items[0].fix ?? '',
      count: items.length,
      files,
      detail:
        items.length === 1 ? items[0].detail : `${items.length} instances`,
      priority: RULE_PRIORITY[items[0].rule] ?? 50,
    });
  }

  batches.sort((a, b) => a.priority - b.priority || b.count - a.count);
  return batches;
}

export function formatTopActions(issues: Issue[], n: number): string {
  const batches = batchIssues(issues);
  const lines = [
    `TOP ${Math.min(n, batches.length)} ACTIONS (of ${batches.length} distinct issue types)`,
  ];
  for (let i = 0; i < Math.min(n, batches.length); i++) {
    const b = batches[i];
    const fixPart = b.fix ? `  →  ${b.fix}` : '';
    if (b.count === 1) {
      lines.push(
        `  ${i + 1}. [${b.severity}] ${b.rule}  ${b.files[0]}  ${b.detail}${fixPart}`,
      );
    } else {
      const sample = b.files.slice(0, 3).join(', ');
      const more = b.count > 3 ? ` +${b.count - 3} more` : '';
      lines.push(
        `  ${i + 1}. [${b.severity}] ${b.rule} × ${b.count}  (${sample}${more})${fixPart}`,
      );
    }
  }
  return lines.join('\n');
}

export function writeReport(
  vaultDir: string,
  issues: Issue[],
  counts: Record<Severity, number>,
): string {
  const reportPath = path.join(vaultDir, 'dm', 'review-queue.md');
  fs.mkdirSync(path.dirname(reportPath), { recursive: true });

  const decisions = issues
    .filter((i) => DECISION_RULES.has(i.rule))
    .sort((a, b) => {
      const si = SEVERITIES.indexOf(a.severity) - SEVERITIES.indexOf(b.severity);
      if (si !== 0) return si;
      const ri = a.rule.localeCompare(b.rule);
      if (ri !== 0) return ri;
      return a.path.localeCompare(b.path);
    });

  const backlog = new Map<string, number>();
  for (const i of issues) {
    if (!DECISION_RULES.has(i.rule)) {
      backlog.set(i.rule, (backlog.get(i.rule) ?? 0) + 1);
    }
  }

  const d = today();
  const lines = [
    '---',
    'type: dm-intelligence',
    'subtype: review-queue',
    'campaign: shattered-sea',
    'status: active',
    'audience: agent',
    'publish: false',
    `summary: "Generated by sea lint on ${d}. ${decisions.length} items need a DM decision. Regenerated each run; do not hand-edit — fix the underlying file instead."`,
    `created: ${d}`,
    `updated: ${d}`,
    'tags: [system, lint, review]',
    'sources: []',
    '---',
    '',
    '# Wiki Review Queue',
    '',
    `Generated ${d}. **${decisions.length} items need a decision** (${counts.error} errors · ${counts.warning} warnings · ${counts.quality} quality total).`,
    '',
    'This file is regenerated by `sea lint --report` and shrinks as issues are resolved — don\'t hand-edit it; fix the file it points to. Identity and lore-contradiction calls live in `wiki/discrepancy-log.md`.',
    '',
    '## Decisions needed',
    '',
  ];

  if (decisions.length) {
    for (const i of decisions) {
      const fixpart = i.fix ? ` — _fix:_ ${i.fix}` : '';
      lines.push(
        `- [${i.severity}] \`${i.path}\` **${i.rule}** — ${i.detail}${fixpart}`,
      );
    }
  } else {
    lines.push(
      '_None — every detectable structural issue is resolved._',
    );
  }

  lines.push('', '## Backlog (mechanical / content)', '');
  if (backlog.size) {
    const sorted = [...backlog.entries()].sort((a, b) => b[1] - a[1]);
    for (const [rule, n] of sorted) {
      const hint = BACKLOG_HINT[rule] ?? '';
      lines.push(`- **${rule}**: ${n}${hint ? ` — ${hint}` : ''}`);
    }
  } else {
    lines.push('_Clear._');
  }

  fs.writeFileSync(reportPath, lines.join('\n').trimEnd() + '\n', 'utf-8');
  return reportPath;
}

export function diffSnapshots(
  currentIssues: Issue[],
  prevPath: string,
): string {
  const prev = JSON.parse(fs.readFileSync(prevPath, 'utf-8'));
  const prevCounts: Record<string, number> = prev.summary ?? {};
  const curCounts: Record<string, number> = {};
  for (const s of SEVERITIES) {
    curCounts[s] = currentIssues.filter((i) => i.severity === s).length;
  }

  const prevByRule = new Map<string, number>();
  for (const i of prev.issues ?? []) {
    prevByRule.set(i.rule, (prevByRule.get(i.rule) ?? 0) + 1);
  }
  const curByRule = new Map<string, number>();
  for (const i of currentIssues) {
    curByRule.set(i.rule, (curByRule.get(i.rule) ?? 0) + 1);
  }

  const allRules = [
    ...new Set([...prevByRule.keys(), ...curByRule.keys()]),
  ].sort();

  const lines = ['DIFF vs previous snapshot:'];
  for (const sev of SEVERITIES) {
    const p = prevCounts[sev] ?? 0;
    const c = curCounts[sev] ?? 0;
    const delta = c - p;
    const arrow = delta === 0 ? '→' : delta > 0 ? '↑' : '↓';
    lines.push(`  ${sev}: ${p} ${arrow} ${c} (${delta >= 0 ? '+' : ''}${delta})`);
  }

  const changedRules: Array<[string, number, number]> = [];
  for (const rule of allRules) {
    const p = prevByRule.get(rule) ?? 0;
    const c = curByRule.get(rule) ?? 0;
    if (p !== c) changedRules.push([rule, p, c]);
  }

  if (changedRules.length) {
    lines.push('', '  Changed rules:');
    changedRules.sort((a, b) => a[1] - a[2] - (b[1] - b[2]));
    for (const [rule, p, c] of changedRules) {
      const delta = c - p;
      const marker = delta < 0 ? 'IMPROVED' : 'REGRESSED';
      lines.push(
        `    ${rule}: ${p} → ${c} (${delta >= 0 ? '+' : ''}${delta}) ${marker}`,
      );
    }
  }

  const prevFiles = new Set(
    ((prev.issues ?? []) as Array<{ path: string }>).map((i) => i.path),
  );
  const newFiles = [
    ...new Set(currentIssues.map((i) => i.path).filter((p) => !prevFiles.has(p))),
  ].sort();
  if (newFiles.length) {
    lines.push(`\n  New files with issues: ${newFiles.length}`);
    for (const f of newFiles.slice(0, 5)) lines.push(`    ${f}`);
    if (newFiles.length > 5) lines.push(`    ... +${newFiles.length - 5} more`);
  }

  return lines.join('\n');
}

// ─── Git helpers ────────────────────────────────────────────────────────────

export function filesChangedSince(ref: string, repoRoot: string): string[] {
  let gitRef = ref;
  try {
    execSync(`git rev-parse --verify ${ref}`, {
      cwd: repoRoot,
      stdio: 'pipe',
    });
  } catch {
    try {
      const result = execSync(
        `git rev-list -1 --before="${ref}" HEAD`,
        { cwd: repoRoot, encoding: 'utf-8', stdio: 'pipe' },
      );
      gitRef = result.trim() || 'HEAD~50';
    } catch {
      gitRef = 'HEAD~50';
    }
  }

  let changed = new Set<string>();
  try {
    const diff = execSync(`git diff --name-only ${gitRef} -- wiki/`, {
      cwd: repoRoot,
      encoding: 'utf-8',
      stdio: 'pipe',
    });
    for (const line of diff.split('\n')) {
      if (line.trim()) changed.add(line.trim());
    }
  } catch {
    /* empty */
  }

  try {
    const untracked = execSync(
      'git ls-files --others --exclude-standard wiki/',
      { cwd: repoRoot, encoding: 'utf-8', stdio: 'pipe' },
    );
    for (const line of untracked.split('\n')) {
      if (line.trim()) changed.add(line.trim());
    }
  } catch {
    /* empty */
  }

  return [...changed].filter((f) => f.endsWith('.md')).sort();
}

// ─── Gather records ─────────────────────────────────────────────────────────

function gatherRecords(vaultDir: string, repoRoot: string): {
  records: VaultRecord[];
  parseErrors: Issue[];
} {
  const files = fg.sync('**/*.md', { cwd: vaultDir }).sort();
  const records: VaultRecord[] = [];
  const parseErrors: Issue[] = [];

  for (const file of files) {
    const rp = `wiki/${file}`;
    const abs = path.join(vaultDir, file);
    let text: string;
    try {
      text = fs.readFileSync(abs, 'utf-8');
    } catch {
      continue;
    }

    const { fm, body, had } = splitDoc(text);
    if (!had) {
      parseErrors.push({
        severity: 'error',
        rule: 'missing-frontmatter',
        path: rp,
        detail: 'no frontmatter block',
      });
      records.push({ relpath: rp, data: {}, body });
      continue;
    }

    try {
      const data = loadFrontmatter(fm);
      records.push({ relpath: rp, data, body });
    } catch (err) {
      parseErrors.push({
        severity: 'error',
        rule: 'unparseable-frontmatter',
        path: rp,
        detail: String(err).split('\n')[0],
      });
      records.push({ relpath: rp, data: {}, body });
    }
  }

  return { records, parseErrors };
}

// ─── Main lint function ─────────────────────────────────────────────────────

function inScope(rp: string, scope: string[] | null): boolean {
  if (!scope) return true;
  return scope.some(
    (s) => rp === s || rp.startsWith(s.replace(/\/$/, '') + '/'),
  );
}

function resolveScope(
  paths: string[] | undefined,
  repoRoot: string,
): string[] | null {
  if (!paths || paths.length === 0) return null;
  return paths.map((p) => relPath(path.resolve(p), repoRoot));
}

export function lint(
  vaultDir: string,
  repoRoot: string,
  options: LintOptions = {},
): LintResult {
  const fixTags = options.fixTags ?? false;
  const doFix = options.fix || fixTags;

  let scope = resolveScope(options.paths, repoRoot);

  if (options.since) {
    const sinceFiles = filesChangedSince(options.since, repoRoot);
    if (scope) {
      const sinceSet = new Set(sinceFiles);
      scope = scope.filter((s) => sinceSet.has(s));
    } else {
      scope = sinceFiles;
    }
    if (scope.length === 0) {
      return {
        issues: [],
        fixed: [],
        counts: { error: 0, warning: 0, quality: 0 },
      };
    }
  }

  // Auto-fix pass
  const fixed: Array<{ file: string; changed: string[] }> = [];
  if (doFix) {
    const files = fg.sync('**/*.md', { cwd: vaultDir }).sort();
    for (const file of files) {
      const rp = `wiki/${file}`;
      if (!inScope(rp, scope)) continue;
      if (SKIP_CONTENT.has(path.basename(rp))) continue;
      const abs = path.join(vaultDir, file);
      try {
        const changed = applyFix(abs, repoRoot, fixTags);
        if (changed.length) fixed.push({ file: rp, changed });
      } catch {
        /* skip errors during fix */
      }
    }
  }

  // Report pass
  const { records, parseErrors } = gatherRecords(vaultDir, repoRoot);
  const slugToPaths = new Map<string, string[]>();
  for (const { relpath } of records) {
    const slug = slugOf(relpath);
    const existing = slugToPaths.get(slug) ?? [];
    existing.push(relpath);
    slugToPaths.set(slug, existing);
  }

  const allIssues: Issue[] = [...parseErrors];

  // Per-file checks
  for (const { relpath, data, body } of records) {
    if (!SKIP_CONTENT.has(path.basename(relpath))) {
      allIssues.push(...checkFile(relpath, data, body));
      const naming = checkNaming(relpath);
      if (naming) allIssues.push(naming);
    }
  }

  // Cross-file checks
  allIssues.push(...crossFileChecks(records, slugToPaths));

  // Vault-wide checks
  allIssues.push(...checkTags(records));
  allIssues.push(...checkTagVariants(records));

  const schemaProps = new Set([
    ...Object.keys(VALUE_VALIDATORS),
    'type', 'subtype', 'campaign', 'status', 'audience', 'publish',
    'summary', 'created', 'updated', 'tags', 'sources',
    'confidence_level', 'lifecycle', 'narrative_island', 'portable',
    'entry_points', 'contains_situations', 'session_number', 'session_date',
    'system_role', 'token_profile', 'mandatory_for', 'update_trigger',
    'mortis', 'reveal_status', 'rooms', 'cr_range', 'topology',
    'plane_type', 'canonical_location', 'owner', 'timeline_position',
  ]);
  allIssues.push(...checkSingletonProperties(records, schemaProps));
  allIssues.push(...checkLoreConsistency(records, slugToPaths));

  // Scope + severity filter
  const minIdx = SEVERITIES.indexOf(options.minSeverity ?? 'quality');
  const issues = allIssues.filter(
    (i) =>
      inScope(i.path, scope) &&
      SEVERITIES.indexOf(i.severity) <= minIdx,
  );

  const counts: Record<Severity, number> = { error: 0, warning: 0, quality: 0 };
  for (const i of allIssues) {
    if (inScope(i.path, scope)) {
      counts[i.severity]++;
    }
  }

  return { issues, fixed, counts };
}
