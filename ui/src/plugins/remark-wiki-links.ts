import { visit } from 'unist-util-visit';
import type { Plugin } from 'unified';

interface WikiLinkOptions {
  slugSet: Set<string>;
}

export const remarkWikiLinks: Plugin<[WikiLinkOptions]> = (options) => {
  const { slugSet } = options;
  const wikiLinkRegex = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;

  return (tree: any) => {
    visit(tree, 'text', (node: any, index: number | undefined, parent: any) => {
      if (!parent || index === undefined) return;
      if (parent.type === 'link') return;

      const text: string = node.value;
      if (!text.includes('[[')) return;

      const parts: any[] = [];
      let lastIndex = 0;

      for (const match of text.matchAll(wikiLinkRegex)) {
        const fullMatch = match[0];
        const slug = match[1].toLowerCase().replace(/\s+/g, '-');
        const display = match[2] || titleCase(match[1]);
        const matchIndex = match.index!;

        if (matchIndex > lastIndex) {
          parts.push({ type: 'text', value: text.slice(lastIndex, matchIndex) });
        }

        const exists = slugSet.has(slug);
        const cls = exists ? 'wiki-link' : 'wiki-link wiki-link--broken';
        parts.push({
          type: 'html',
          value: `<a href="/wiki/${escapeAttr(slug)}" class="${cls}" data-exists="${exists}">${escapeHtml(display)}</a>`,
        });

        lastIndex = matchIndex + fullMatch.length;
      }

      if (parts.length === 0) return;

      if (lastIndex < text.length) {
        parts.push({ type: 'text', value: text.slice(lastIndex) });
      }

      parent.children.splice(index, 1, ...parts);
    });
  };
};

function titleCase(s: string): string {
  return s
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function escapeAttr(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
