import type { Plugin } from 'unified';
import { visit } from 'unist-util-visit';

export const remarkObsidianHighlights: Plugin = () => {
  return (tree: any) => {
    visit(tree, 'text', (node: any, index: number | undefined, parent: any) => {
      if (!parent || index === undefined) return;
      if (!node.value.includes('==')) return;

      const parts = node.value.split(/(==(?:[^=]|=[^=])+==)/);
      if (parts.length === 1) return;

      const newChildren: any[] = [];
      for (const part of parts) {
        const m = part.match(/^==([\s\S]+)==$/);
        if (m) {
          newChildren.push({
            type: 'html',
            value: `<mark>${escapeHtml(m[1])}</mark>`,
          });
        } else if (part) {
          newChildren.push({ type: 'text', value: part });
        }
      }

      parent.children.splice(index, 1, ...newChildren);
    });
  };
};

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
