import type { Plugin } from 'unified';
import { visit } from 'unist-util-visit';

export const remarkObsidianColumns: Plugin = () => {
  return (tree: any) => {
    visit(tree, 'code', (node: any, index: number | undefined, parent: any) => {
      if (!parent || index === undefined) return;
      if (node.lang !== 'columns') return;

      const raw: string = node.value;
      const idLine = raw.match(/^id:\s*\S+\n?/m);
      const content = idLine ? raw.replace(idLine[0], '') : raw;
      const columns = content
        .split(/^===$/m)
        .map((col) => col.trim())
        .filter(Boolean);

      if (columns.length === 0) return;

      const colHtml = columns
        .map((col) => `<div class="obsidian-column">${mdToHtml(col)}</div>`)
        .join('\n');

      parent.children[index] = {
        type: 'html',
        value: `<div class="obsidian-columns" style="--col-count: ${columns.length}">${colHtml}</div>`,
      };
    });
  };
};

function mdToHtml(md: string): string {
  return md
    .split('\n\n')
    .map((block) => {
      block = block.trim();
      if (!block) return '';

      const hMatch = block.match(/^(#{1,4})\s+(.+)$/m);
      if (hMatch) {
        const level = hMatch[1].length;
        return `<h${level}>${esc(hMatch[2])}</h${level}>`;
      }

      if (block.startsWith('|')) {
        return renderTable(block);
      }

      const lines = block.split('\n');
      const isList = lines.every((l) => /^[-*]\s/.test(l));
      if (isList) {
        const items = lines.map((l) => `<li>${inlineMd(l.replace(/^[-*]\s+/, ''))}</li>`).join('');
        return `<ul>${items}</ul>`;
      }

      return `<p>${inlineMd(block.replace(/\n/g, ' '))}</p>`;
    })
    .join('\n');
}

function renderTable(block: string): string {
  const rows = block.split('\n').filter((r) => r.trim());
  if (rows.length < 2) return `<p>${esc(block)}</p>`;

  const parseRow = (r: string) =>
    r
      .split('|')
      .slice(1, -1)
      .map((c) => c.trim());

  const isSep = (r: string) => /^\|[\s-:|]+\|$/.test(r);

  const headerRow = parseRow(rows[0]);
  const sepIdx = rows.findIndex((r) => isSep(r));

  let html = '<table>';

  if (sepIdx === 1) {
    html +=
      '<thead><tr>' + headerRow.map((c) => `<th>${inlineMd(c)}</th>`).join('') + '</tr></thead>';
    html += '<tbody>';
    for (let i = sepIdx + 1; i < rows.length; i++) {
      const cells = parseRow(rows[i]);
      html += '<tr>' + cells.map((c) => `<td>${inlineMd(c)}</td>`).join('') + '</tr>';
    }
    html += '</tbody>';
  } else {
    html += '<tbody>';
    for (const row of rows) {
      if (isSep(row)) continue;
      const cells = parseRow(row);
      html += '<tr>' + cells.map((c) => `<td>${inlineMd(c)}</td>`).join('') + '</tr>';
    }
    html += '</tbody>';
  }

  html += '</table>';
  return html;
}

function inlineMd(s: string): string {
  let out = esc(s);
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
  out = out.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '<a class="wiki-link" href="/wiki/$1/">$2</a>');
  out = out.replace(/\[\[([^\]]+)\]\]/g, '<a class="wiki-link" href="/wiki/$1/">$1</a>');
  return out;
}

function esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
