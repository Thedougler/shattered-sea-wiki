export const CANONICAL: ReadonlySet<string> = new Set([
  // faction
  'dravosi', 'tessarine', 'passage', 'waveservants', 'sunken-crown',
  'drowned-maw', 'fisk-fleet', 'five-blades',
  // theme/domain
  'umberlee', 'undead', 'antheri', 'rattkin', 'grung', 'moucheron',
  // narrative
  'maritime', 'mystery', 'salvage',
  // content type
  'homebrew', 'late-game',
  // prep/workflow
  'needs-detail', 'encounter-ready', 'read-aloud', 'player-resource',
  'dm-prep', 'recurring', 'combat',
]);

export const ALIASES: ReadonlyMap<string, string> = new Map([
  ['dravosi-crown', 'dravosi'],
  ['crown', 'dravosi'],
  ['tessarine-concordat', 'tessarine'],
  ['the-passage', 'passage'],
  ['maw', 'drowned-maw'],
  ['waveservant', 'waveservants'],
  ['fisks-fleet', 'fisk-fleet'],
  ['homebrew', 'homebrew'],
  ['late_game', 'late-game'],
  ['dm-craft', 'dm-prep'],
  ['dm-notes', 'dm-prep'],
  ['dm-reference', 'dm-prep'],
  ['prep', 'dm-prep'],
  ['player-facing', 'player-resource'],
  ['primer', 'player-resource'],
  ['lich', 'undead'],
  ['antheri-adjacent', 'antheri'],
]);

export const DEPRECATED_FRONTMATTER: ReadonlySet<string> = new Set([
  'situation', 'session', 'rules', 'lore', 'system', 'index',
  'narrative-island', 'reference', 'entity', 'item', 'place', 'npc',
  'creature', 'subclass', 'scene', 'faction', 'ship', 'vehicle', 'species',
  'deity', 'thread', 'run-guide', 'equipment', 'encounter', 'conflict',
  'obligation', 'question', 'secret', 'pursuit', 'event', 'active',
  'dormant', 'resolved', 'dead', 'destroyed', 'dm-only', 'players',
]);

export const DEPRECATED_ENTITY_NAMES: ReadonlySet<string> = new Set([
  'perrin', 'delmar', 'jean-claude', 'crissdalynn', 'nona', 'grigori',
  'kyzil', 'hollowell', 'calveno', 'warren', 'port-tidefall', 'kalowe',
  'midchain', 'crown-islands', 'verdant-teeth', 'calders-tooth',
  'fort-crestwall', 'cape-solitude', 'aruhe', 'takowan', 'surety',
  'saltwright',
]);

export const DEPRECATED_SOURCE: ReadonlySet<string> = new Set([
  'bestiary', 'xmm', 'xphb', 'phb', 'dmg',
]);

export const DEPRECATED_SYSTEM: ReadonlySet<string> = new Set([
  'current-state', 'work-queue', 'lint', 'review', 'log', 'discrepancy',
]);

export const TAG_LIMIT = 5;

export type TagCategory =
  | 'canonical'
  | 'alias'
  | 'deprecated-fm'
  | 'deprecated-entity'
  | 'deprecated-source'
  | 'deprecated-system'
  | 'unknown'
  | 'visibility';

export function classify(tag: string): [TagCategory, string | null] {
  if (tag.startsWith('visibility/')) {
    return ['visibility', null];
  }

  const t = tag.toLowerCase();

  const canonicalLower = new Set([...CANONICAL].map((c) => c.toLowerCase()));
  if (canonicalLower.has(t)) return ['canonical', tag];

  if (ALIASES.has(t)) return ['alias', ALIASES.get(t)!];

  if (DEPRECATED_FRONTMATTER.has(t)) return ['deprecated-fm', null];
  if (DEPRECATED_ENTITY_NAMES.has(t)) return ['deprecated-entity', null];
  if (DEPRECATED_SOURCE.has(t)) return ['deprecated-source', null];
  if (DEPRECATED_SYSTEM.has(t)) return ['deprecated-system', null];

  return ['unknown', null];
}
