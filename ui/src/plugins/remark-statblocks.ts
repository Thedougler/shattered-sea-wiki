import type { Plugin } from 'unified';
import { visit } from 'unist-util-visit';
import yaml from 'yaml';

export const remarkStatblocks: Plugin = () => {
  return (tree: any) => {
    visit(tree, 'code', (node: any, index: number | undefined, parent: any) => {
      if (!parent || index === undefined) return;
      if (node.lang !== 'statblock') return;

      let data: any;
      try {
        data = yaml.parse(node.value);
      } catch {
        return;
      }

      if (!data || !data.name) return;

      parent.children[index] = {
        type: 'html',
        value: renderStatblock(data),
      };
    });
  };
};

function renderStatblock(d: any): string {
  const parts: string[] = [];
  parts.push('<div class="statblock">');

  parts.push('<div class="statblock__hr statblock__hr--top"></div>');

  parts.push(`<div class="statblock__name">${esc(d.name)}</div>`);

  const meta = [d.size, d.type, d.alignment].filter(Boolean).join(', ');
  if (meta) {
    parts.push(`<div class="statblock__meta">${esc(meta)}</div>`);
  }

  parts.push('<div class="statblock__hr"></div>');

  if (d.ac !== undefined) parts.push(propLine('Armor Class', String(d.ac)));
  if (d.hp !== undefined) {
    const hp = d.hit_dice ? `${d.hp} (${d.hit_dice})` : String(d.hp);
    parts.push(propLine('Hit Points', hp));
  }
  if (d.speed) parts.push(propLine('Speed', d.speed));

  parts.push('<div class="statblock__hr"></div>');

  if (d.stats && Array.isArray(d.stats) && d.stats.length === 6) {
    const labels = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'];
    parts.push('<div class="statblock__abilities">');
    d.stats.forEach((val: number, i: number) => {
      const mod = Math.floor((val - 10) / 2);
      const sign = mod >= 0 ? '+' : '';
      parts.push(
        `<div class="statblock__ability"><span class="statblock__ability-label">${labels[i]}</span><span class="statblock__ability-score">${val} (${sign}${mod})</span></div>`,
      );
    });
    parts.push('</div>');
  }

  parts.push('<div class="statblock__hr"></div>');

  if (d.saves?.length) {
    const saves = d.saves.map((s: any) => {
      const [k, v] = Object.entries(s)[0];
      return `${titleCase(k as string)} ${formatMod(v as number)}`;
    });
    parts.push(propLine('Saving Throws', saves.join(', ')));
  }
  if (d.skillsaves?.length) {
    const skills = d.skillsaves.map((s: any) => {
      const [k, v] = Object.entries(s)[0];
      return `${titleCase(k as string)} ${formatMod(v as number)}`;
    });
    parts.push(propLine('Skills', skills.join(', ')));
  }
  if (d.damage_vulnerabilities)
    parts.push(propLine('Damage Vulnerabilities', d.damage_vulnerabilities));
  if (d.damage_resistances) parts.push(propLine('Damage Resistances', d.damage_resistances));
  if (d.damage_immunities) parts.push(propLine('Damage Immunities', d.damage_immunities));
  if (d.condition_immunities) parts.push(propLine('Condition Immunities', d.condition_immunities));
  if (d.senses) parts.push(propLine('Senses', d.senses));
  if (d.languages) parts.push(propLine('Languages', d.languages));
  if (d.cr !== undefined) {
    const xp = crToXp(String(d.cr));
    const crText = xp ? `${d.cr} (${xp} XP)` : String(d.cr);
    parts.push(propLine('Challenge', crText));
  }

  if (d.spells?.length) {
    parts.push('<div class="statblock__hr"></div>');
    d.spells.forEach((spell: string) => {
      parts.push(`<div class="statblock__spells">${esc(spell)}</div>`);
    });
  }

  if (d.traits?.length) {
    parts.push('<div class="statblock__hr"></div>');
    renderSection(parts, d.traits);
  }

  if (d.actions?.length) {
    parts.push('<div class="statblock__hr"></div>');
    parts.push('<div class="statblock__section-title">Actions</div>');
    renderSection(parts, d.actions);
  }

  if (d.bonus_actions?.length) {
    parts.push('<div class="statblock__hr"></div>');
    parts.push('<div class="statblock__section-title">Bonus Actions</div>');
    renderSection(parts, d.bonus_actions);
  }

  if (d.reactions?.length) {
    parts.push('<div class="statblock__hr"></div>');
    parts.push('<div class="statblock__section-title">Reactions</div>');
    renderSection(parts, d.reactions);
  }

  if (d.legendary_actions?.length) {
    parts.push('<div class="statblock__hr"></div>');
    parts.push('<div class="statblock__section-title">Legendary Actions</div>');
    renderSection(parts, d.legendary_actions);
  }

  parts.push('<div class="statblock__hr statblock__hr--bottom"></div>');
  parts.push('</div>');

  return parts.join('\n');
}

function renderSection(parts: string[], entries: any[]) {
  entries.forEach((e: any) => {
    if (e.name && e.desc) {
      parts.push(
        `<div class="statblock__trait"><span class="statblock__trait-name">${esc(e.name)}.</span> ${esc(e.desc)}</div>`,
      );
    }
  });
}

function propLine(label: string, value: string): string {
  return `<div class="statblock__prop"><span class="statblock__prop-label">${esc(label)}</span> ${esc(value)}</div>`;
}

function formatMod(v: number): string {
  return v >= 0 ? `+${v}` : String(v);
}

function titleCase(s: string): string {
  return s.replace(/\b\w/g, (c) => c.toUpperCase());
}

function crToXp(cr: string): string | null {
  const map: Record<string, string> = {
    '0': '0',
    '1/8': '25',
    '1/4': '50',
    '1/2': '100',
    '1': '200',
    '2': '450',
    '3': '700',
    '4': '1,100',
    '5': '1,800',
    '6': '2,300',
    '7': '2,900',
    '8': '3,900',
    '9': '5,000',
    '10': '5,900',
    '11': '7,200',
    '12': '8,400',
    '13': '10,000',
    '14': '11,500',
    '15': '13,000',
    '16': '15,000',
    '17': '18,000',
    '18': '20,000',
    '19': '22,000',
    '20': '25,000',
    '21': '33,000',
    '22': '41,000',
    '23': '50,000',
    '24': '62,000',
    '25': '75,000',
    '26': '90,000',
    '27': '105,000',
    '28': '120,000',
    '29': '135,000',
    '30': '155,000',
  };
  return map[cr] || null;
}

function esc(s: string): string {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
