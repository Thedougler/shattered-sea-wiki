export interface SplitResult {
  frontmatterLines: string[];
  body: string;
  hadFrontmatter: boolean;
}

export function splitFrontmatter(text: string): SplitResult {
  const lines = text.split('\n');
  if (!lines.length || lines[0].trim() !== '---') {
    return { frontmatterLines: [], body: text, hadFrontmatter: false };
  }
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === '---') {
      return {
        frontmatterLines: lines.slice(1, i),
        body: lines.slice(i + 1).join('\n'),
        hadFrontmatter: true,
      };
    }
  }
  return { frontmatterLines: [], body: text, hadFrontmatter: false };
}

export function parseFields(fmLines: string[]): Record<string, string> {
  const fields: Record<string, string> = {};
  for (const line of fmLines) {
    const m = line.match(/^([A-Za-z0-9_]+):(.*)$/);
    if (m) {
      fields[m[1]] = m[2].trim();
    }
  }
  return fields;
}

export function getSummary(fields: Record<string, string>): string {
  const raw = fields.summary ?? '';
  return raw.replace(/^["']|["']$/g, '');
}

export function firstH1(body: string): string | null {
  for (const line of body.split('\n')) {
    const m = line.match(/^#\s+(.+?)\s*$/);
    if (m) {
      return m[1].replace(/\s+[—-]\s+Stub\s*$/, '').trim();
    }
  }
  return null;
}
