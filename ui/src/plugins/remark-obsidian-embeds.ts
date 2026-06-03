import { visit } from 'unist-util-visit';
import type { Plugin } from 'unified';

interface EmbedOptions {
  assetMap: Map<string, string>;
}

export const remarkObsidianEmbeds: Plugin<[EmbedOptions]> = (options) => {
  const { assetMap } = options;

  return (tree: any) => {
    visit(tree, 'paragraph', (node: any, index: number | undefined, parent: any) => {
      if (!parent || index === undefined) return;
      if (node.children.length !== 1 || node.children[0].type !== 'text') return;

      const text: string = node.children[0].value;
      const match = text.match(/^!\[\[([^\]]+)\]\]$/);
      if (!match) return;

      const inner = match[1];
      const pipeIdx = inner.indexOf('|');
      const ref = pipeIdx >= 0 ? inner.slice(0, pipeIdx) : inner;
      const altRaw = pipeIdx >= 0 ? inner.slice(pipeIdx + 1) : '';

      if (!/\.(png|jpg|jpeg|webp|gif|svg)$/i.test(ref)) return;

      let src: string | undefined;
      const filename = ref.split('/').pop()!;

      if (assetMap.has(filename)) {
        src = assetMap.get(filename);
      } else {
        src = `/assets/${filename}`;
      }

      let alt = '';
      let width = '';
      let height = '';

      if (altRaw) {
        const dimMatch = altRaw.match(/^(\d+)(?:x(\d+))?$/);
        if (dimMatch) {
          width = dimMatch[1];
          height = dimMatch[2] || '';
        } else {
          const trailingDim = altRaw.match(/^(.*)\|(\d+)(?:x(\d+))?$/);
          if (trailingDim) {
            alt = trailingDim[1].trim();
            width = trailingDim[2];
            height = trailingDim[3] || '';
          } else {
            alt = altRaw;
          }
        }
      }

      const attrs = [
        `src="${escapeAttr(src!)}"`,
        `alt="${escapeAttr(alt)}"`,
        'class="wiki-image"',
        'loading="lazy"',
      ];
      if (width) attrs.push(`width="${width}"`);
      if (height) attrs.push(`height="${height}"`);

      parent.children[index] = {
        type: 'html',
        value: `<img ${attrs.join(' ')} />`,
      };
    });
  };
};

function escapeAttr(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
