export interface Wikilink {
  slug: string;
  displayName: string | null;
  raw: string;
  index: number;
}

const WIKILINK_REGEX = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;

export function parseWikilinks(markdown: string): Wikilink[] {
  const results: Wikilink[] = [];
  for (const match of markdown.matchAll(WIKILINK_REGEX)) {
    results.push({
      slug: match[1].toLowerCase().replace(/\s+/g, '-'),
      displayName: match[2] ?? null,
      raw: match[0],
      index: match.index!,
    });
  }
  return results;
}

export function resolveWikilink(slug: string, slugSet: ReadonlySet<string>): boolean {
  return slugSet.has(slug);
}

export function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export function escapeAttr(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}
