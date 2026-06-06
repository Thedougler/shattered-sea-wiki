import type { Plugin } from 'unified';
import { visit } from 'unist-util-visit';

export const remarkObsidianComments: Plugin = () => {
  return (tree: any) => {
    visit(tree, 'text', (node: any) => {
      if (!node.value.includes('%%')) return;
      node.value = node.value.replace(/%%[\s\S]*?%%/g, '');
    });

    visit(tree, 'html', (node: any) => {
      if (!node.value.includes('%%')) return;
      node.value = node.value.replace(/%%[\s\S]*?%%/g, '');
    });
  };
};
