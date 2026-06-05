export interface CharacterInfo {
  name: string;
  slug: string;
  portrait: string | null;
  summary: string;
  subtype: 'pc' | 'npc';
}

export type RecordingMode = 'character' | 'normal';

export type Phase = 'select' | 'character-voice' | 'normal-voice' | 'complete';

export interface ScriptRequest {
  character: string;
  summary: string;
  mode: RecordingMode;
  previousContext?: string;
}

export interface Tier {
  minSeconds: number;
  stars: number;
  title: string;
}

export const TIERS: Tier[] = [
  { minSeconds: 0, stars: 0, title: 'Mic Check' },
  { minSeconds: 10, stars: 1, title: 'First Words' },
  { minSeconds: 30, stars: 2, title: 'Finding the Voice' },
  { minSeconds: 60, stars: 3, title: 'Voice of the Realm' },
  { minSeconds: 120, stars: 4, title: 'Legendary Performance' },
  { minSeconds: 180, stars: 5, title: 'Voice of the Gods' },
];

export function getTier(seconds: number): Tier {
  for (let i = TIERS.length - 1; i >= 0; i--) {
    if (seconds >= TIERS[i].minSeconds) return TIERS[i];
  }
  return TIERS[0];
}

export function getNextTier(seconds: number): Tier | null {
  for (const tier of TIERS) {
    if (seconds < tier.minSeconds) return tier;
  }
  return null;
}
