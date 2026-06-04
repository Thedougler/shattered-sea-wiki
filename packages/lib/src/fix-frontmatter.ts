import fs from 'node:fs';
import { parseFields, type SplitResult, splitFrontmatter } from './frontmatter.js';
import { inferSubtype, inferType, TYPE_EXTRA_FIELDS, UNIVERSAL_FIELDS } from './path-inference.js';
import { relPath } from './vault.js';

const STUB_SUMMARY = 'Stub — no summary yet.';

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

function defaultValue(field: string, relpath: string): string {
  const t = inferType(relpath);
  const st = inferSubtype(relpath);
  const defaults: Record<string, string> = {
    type: t,
    subtype: st,
    campaign: 'shattered-sea',
    status: 'unknown',
    audience: 'dm',
    publish: 'false',
    summary: `"${STUB_SUMMARY}"`,
    created: today(),
    updated: today(),
    tags: '[]',
    sources: '["Unknown"]',
    confidence_level: 'medium',
    lifecycle: 'dormant',
    narrative_island: 'null',
    portable: 'false',
    entry_points: '[]',
    contains_situations: '[]',
    session_number: '0',
    session_date: '"unknown"',
    system_role: '"unknown"',
    token_profile: 'on-demand',
    mandatory_for: '[]',
    update_trigger: '""',
  };
  return defaults[field] ?? '""';
}

function requiredFields(relpath: string): readonly string[] {
  const t = inferType(relpath);
  const extra = TYPE_EXTRA_FIELDS[t] ?? [];
  return [...UNIVERSAL_FIELDS, ...extra];
}

export interface FixResult {
  changed: string[];
  summaryStale: boolean;
}

export function fixFrontmatter(filePath: string, repoRoot: string): FixResult {
  const rp = relPath(filePath, repoRoot);
  const text = fs.readFileSync(filePath, 'utf-8');
  const { frontmatterLines, body, hadFrontmatter }: SplitResult = splitFrontmatter(text);

  const fields = hadFrontmatter ? parseFields(frontmatterLines) : {};
  const newLines = [...frontmatterLines];
  const changed: string[] = [];

  for (const field of requiredFields(rp)) {
    if (!(field in fields)) {
      const val = defaultValue(field, rp);
      newLines.push(`${field}: ${val}`);
      fields[field] = val;
      changed.push(field);
    }
  }

  let stamped = false;
  for (let i = 0; i < newLines.length; i++) {
    if (newLines[i].startsWith('updated:')) {
      const want = `updated: ${today()}`;
      if (newLines[i].trim() !== want) {
        newLines[i] = want;
        if (!changed.includes('updated')) changed.push('updated');
      }
      stamped = true;
      break;
    }
  }
  if (!stamped) {
    newLines.push(`updated: ${today()}`);
    changed.push('updated');
  }

  const summary = (fields.summary ?? '').replace(/^["']|["']$/g, '');
  const summaryStale = !summary || summary === STUB_SUMMARY;

  if (!changed.length && hadFrontmatter) {
    return { changed, summaryStale };
  }

  const rebuilt = '---\n' + newLines.join('\n') + '\n---\n';
  let newText: string;
  if (hadFrontmatter) {
    newText = body.startsWith('\n') ? rebuilt + body : rebuilt + '\n' + body;
  } else {
    newText = text.trim() ? rebuilt + '\n' + text : rebuilt;
  }

  fs.writeFileSync(filePath, newText, 'utf-8');
  return { changed, summaryStale };
}
