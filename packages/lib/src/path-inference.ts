export const UNIVERSAL_FIELDS = [
  'type',
  'subtype',
  'campaign',
  'status',
  'audience',
  'publish',
  'summary',
  'created',
  'updated',
  'tags',
  'sources',
] as const;

export const TYPE_EXTRA_FIELDS: Record<string, readonly string[]> = {
  entity: ['confidence_level'],
  situation: ['lifecycle', 'narrative_island'],
  'narrative-island': ['portable', 'entry_points', 'contains_situations'],
  session: ['session_number', 'session_date'],
  system: ['system_role', 'token_profile', 'mandatory_for', 'update_trigger'],
};

export const ALLOWED_TYPES_BY_PATH: Array<[string, ReadonlySet<string>]> = [
  ['wiki/entities/creatures/', new Set(['entity', 'monster', 'index'])],
  ['wiki/entities/vehicles/', new Set(['entity', 'index'])],
  ['wiki/dm/', new Set(['dm-intelligence', 'system'])],
];

const TYPE_TABLE: Array<[string, string]> = [
  ['wiki/entities/', 'entity'],
  ['wiki/situations/', 'situation'],
  ['wiki/narrative-islands/', 'narrative-island'],
  ['wiki/sessions/', 'session'],
  ['wiki/system/', 'system'],
  ['wiki/lore/', 'lore'],
  ['wiki/rules/', 'rules'],
  ['wiki/dm/', 'dm-intelligence'],
  ['.raw/', 'raw'],
];

export function inferType(relpath: string): string {
  for (const [prefix, value] of TYPE_TABLE) {
    if (relpath.startsWith(prefix)) return value;
  }
  if (!relpath.includes('/')) return 'governance';
  return 'unknown';
}

const SUBTYPE_TABLE: Array<[string, string]> = [
  ['wiki/entities/characters/pcs/', 'pc'],
  ['wiki/entities/characters/npcs/', 'npc'],
  ['wiki/entities/characters/crew/', 'crew'],
  ['wiki/entities/characters/minor/', 'minor-npc'],
  ['wiki/entities/places/regions/', 'region'],
  ['wiki/entities/places/islands/', 'island-place'],
  ['wiki/entities/places/settlements/', 'settlement'],
  ['wiki/entities/places/buildings/', 'building'],
  ['wiki/entities/places/dungeons/', 'dungeon'],
  ['wiki/entities/places/sites/', 'site'],
  ['wiki/entities/places/planes/', 'plane'],
  ['wiki/entities/places/', 'place'],
  ['wiki/entities/factions/', 'faction'],
  ['wiki/entities/deities/', 'deity'],
  ['wiki/entities/items/', 'item'],
  ['wiki/entities/vehicles/', 'vehicle'],
  ['wiki/situations/active/', 'active-situation'],
  ['wiki/situations/dormant/', 'dormant-situation'],
  ['wiki/situations/resolved/', 'resolved-situation'],
  ['wiki/narrative-islands/', 'narrative-island'],
  ['wiki/lore/species/', 'species'],
  ['wiki/lore/creatures/', 'creature'],
  ['wiki/lore/history/', 'history'],
  ['wiki/lore/geography/', 'geography'],
  ['wiki/lore/cultures/', 'culture'],
  ['wiki/lore/religions/', 'religion'],
  ['wiki/lore/magic/', 'magic'],
  ['wiki/lore/languages/', 'language'],
  ['wiki/lore/', 'lore-page'],
  ['wiki/rules/core/', 'core-rule'],
  ['wiki/rules/subsystems/', 'subsystem'],
  ['wiki/rules/', 'rule'],
  ['wiki/sessions/', 'session-note'],
  ['wiki/system/players/', 'pc-sheet'],
  ['wiki/system/', 'system-file'],
  ['wiki/dm/', 'dm-file'],
  ['.raw/characters/', 'raw-character'],
  ['.raw/homebrew/', 'raw-homebrew'],
  ['.raw/reference/', 'raw-reference'],
  ['.raw/assets/', 'raw-asset'],
];

// Session source packets live under `.raw/sessions/session-NN/` with typed
// subdirs. The session-id segment is variable, so the first segment *after* it
// determines the subtype. Legacy flat files fall through to `raw-session`.
const SESSION_PACKET_SUBTYPES: Record<string, string> = {
  audio: 'raw-session-audio',
  transcripts: 'raw-session-transcript',
  ingest: 'raw-session-ingest',
  notes: 'raw-session-note',
  exports: 'raw-session-export',
};

function inferSessionSubtype(relpath: string): string {
  // relpath starts with '.raw/sessions/'; segments after that are
  // [session-id, next, ...].
  const segments = relpath.slice('.raw/sessions/'.length).split('/');
  if (segments.length >= 2) {
    const next = segments[1];
    if (segments.length === 2 && next === 'source-manifest.md') return 'session-manifest';
    const mapped = SESSION_PACKET_SUBTYPES[next];
    if (mapped) return mapped;
  }
  return 'raw-session';
}

export function inferSubtype(relpath: string): string {
  if (relpath.startsWith('.raw/sessions/')) return inferSessionSubtype(relpath);
  for (const [prefix, value] of SUBTYPE_TABLE) {
    if (relpath.startsWith(prefix)) return value;
  }
  return 'unknown';
}
