import fs from 'node:fs';
import { parseFields, splitFrontmatter } from './frontmatter.js';
import { inferSubtype, inferType } from './path-inference.js';
import { relPath } from './vault.js';

export interface SetFieldResult {
  file: string;
  field: string;
  changed: boolean;
  oldValue: string | null;
  newValue: string;
}

export interface DriftEntry {
  file: string;
  field: string;
  actual: string;
  expected: string;
}

export function getField(filePath: string, field: string): string | null {
  const text = fs.readFileSync(filePath, 'utf-8');
  const { frontmatterLines, hadFrontmatter } = splitFrontmatter(text);
  if (!hadFrontmatter) return null;
  const fields = parseFields(frontmatterLines);
  return fields[field] ?? null;
}

export function getFields(filePath: string): Record<string, string> {
  const text = fs.readFileSync(filePath, 'utf-8');
  const { frontmatterLines, hadFrontmatter } = splitFrontmatter(text);
  if (!hadFrontmatter) return {};
  return parseFields(frontmatterLines);
}

export function setField(filePath: string, field: string, value: string): SetFieldResult {
  const text = fs.readFileSync(filePath, 'utf-8');
  const { frontmatterLines, body, hadFrontmatter } = splitFrontmatter(text);

  if (!hadFrontmatter) {
    return { file: filePath, field, changed: false, oldValue: null, newValue: value };
  }

  const fields = parseFields(frontmatterLines);
  const oldValue = fields[field] ?? null;
  const oldRaw = oldValue?.replace(/^["']|["']$/g, '') ?? null;
  const newRaw = value.replace(/^["']|["']$/g, '');

  if (oldRaw === newRaw) {
    return { file: filePath, field, changed: false, oldValue: oldRaw, newValue: newRaw };
  }

  const newLines = [...frontmatterLines];
  let replaced = false;

  for (let i = 0; i < newLines.length; i++) {
    const m = newLines[i].match(/^([A-Za-z0-9_]+):/);
    if (m && m[1] === field) {
      newLines[i] = `${field}: ${value}`;
      replaced = true;
      break;
    }
  }

  if (!replaced) {
    newLines.push(`${field}: ${value}`);
  }

  const rebuilt = '---\n' + newLines.join('\n') + '\n---\n';
  const newText = body.startsWith('\n') ? rebuilt + body : rebuilt + '\n' + body;
  fs.writeFileSync(filePath, newText, 'utf-8');

  return { file: filePath, field, changed: true, oldValue: oldRaw, newValue: newRaw };
}

export function detectDrift(
  filePath: string,
  repoRoot: string,
  checkFields: ('type' | 'subtype')[],
): DriftEntry[] {
  const rp = relPath(filePath, repoRoot);
  const text = fs.readFileSync(filePath, 'utf-8');
  const { frontmatterLines, hadFrontmatter } = splitFrontmatter(text);
  if (!hadFrontmatter) return [];

  const fields = parseFields(frontmatterLines);
  const results: DriftEntry[] = [];

  for (const f of checkFields) {
    const actual = (fields[f] ?? '').replace(/^["']|["']$/g, '');
    const expected = f === 'type' ? inferType(rp) : inferSubtype(rp);
    if (actual && actual !== expected && actual !== 'unknown') {
      results.push({ file: rp, field: f, actual, expected });
    }
  }

  return results;
}

export function syncField(
  filePath: string,
  repoRoot: string,
  field: 'type' | 'subtype',
): SetFieldResult {
  const rp = relPath(filePath, repoRoot);
  const expected = field === 'type' ? inferType(rp) : inferSubtype(rp);
  return setField(filePath, field, expected);
}
