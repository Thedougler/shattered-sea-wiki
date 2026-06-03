import { visit } from 'unist-util-visit';
import type { Plugin } from 'unified';

const CALLOUT_LABELS: Record<string, string> = {
  dm: 'DM Note',
  'read-aloud': 'Read Aloud',
  secret: 'Secret',
  mechanic: 'Mechanic',
  warning: 'Warning',
  appearance: 'Appearance',
  check: 'Skill Check',
  stub: 'Stub',
  info: 'Info',
  tip: 'Tip',
  note: 'Note',
};

export const remarkObsidianCallouts: Plugin = () => {
  return (tree: any) => {
    visit(tree, 'blockquote', (node: any, index: number | undefined, parent: any) => {
      if (!node.children?.length || index === undefined) return;

      const firstChild = node.children[0];
      if (firstChild.type !== 'paragraph' || !firstChild.children?.length) return;

      const firstText = firstChild.children[0];
      if (firstText.type !== 'text') return;

      const match = firstText.value.match(/^\[!(\w[\w-]*)\][^\S\n]*(.*)?$/m);
      if (!match) return;

      const calloutType = match[1].toLowerCase();
      const customTitle = match[2]?.trim();
      const label = customTitle || CALLOUT_LABELS[calloutType] || titleCase(calloutType);

      const remainingText = firstText.value.replace(/^\[!(\w[\w-]*)\][^\S\n]*(.*)?\n?/, '');
      const contentChildren: any[] = [];

      if (remainingText.trim()) {
        contentChildren.push({
          type: 'paragraph',
          children: [{ type: 'text', value: remainingText.trim() }],
        });
      }

      if (firstChild.children.length > 1) {
        contentChildren.push({
          type: 'paragraph',
          children: firstChild.children.slice(1),
        });
      }

      contentChildren.push(...node.children.slice(1));

      const html = {
        type: 'html',
        value: `<div class="callout callout--${calloutType}" data-callout="${calloutType}"><div class="callout-title">${escapeHtml(label)}</div><div class="callout-content">`,
      };

      const htmlClose = {
        type: 'html',
        value: '</div></div>',
      };

      parent.children.splice(index, 1, html, ...contentChildren, htmlClose);
    });
  };
};

function titleCase(s: string): string {
  return s.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
