import { describe, expect, it } from 'vitest';
import { inferType, inferSubtype } from '../src/path-inference.js';

describe('inferType', () => {
  it('infers entity type from entities path', () => {
    expect(inferType('wiki/entities/characters/npcs/voss.md')).toBe('entity');
  });

  it('infers situation type', () => {
    expect(inferType('wiki/situations/active/the-blockade.md')).toBe('situation');
  });

  it('infers narrative-island type', () => {
    expect(inferType('wiki/narrative-islands/calveno-raid.md')).toBe('narrative-island');
  });

  it('infers session type', () => {
    expect(inferType('wiki/sessions/session-04-day-1.md')).toBe('session');
  });

  it('infers system type', () => {
    expect(inferType('wiki/system/task-routing.md')).toBe('system');
  });

  it('infers lore type', () => {
    expect(inferType('wiki/lore/species/aarakocra.md')).toBe('lore');
  });

  it('infers rules type', () => {
    expect(inferType('wiki/rules/core/resting.md')).toBe('rules');
  });

  it('infers dm-intelligence type', () => {
    expect(inferType('wiki/dm/player-interests.md')).toBe('dm-intelligence');
  });

  it('infers raw type', () => {
    expect(inferType('.raw/sessions/s04/s04-raw.md')).toBe('raw');
  });

  it('returns governance for root-level files', () => {
    expect(inferType('hot.md')).toBe('governance');
  });

  it('returns unknown for unmatched paths', () => {
    expect(inferType('somewhere/else/thing.md')).toBe('unknown');
  });
});

describe('inferSubtype', () => {
  it('infers npc subtype', () => {
    expect(inferSubtype('wiki/entities/characters/npcs/voss.md')).toBe('npc');
  });

  it('infers pc subtype', () => {
    expect(inferSubtype('wiki/entities/characters/pcs/perrin.md')).toBe('pc');
  });

  it('infers crew subtype', () => {
    expect(inferSubtype('wiki/entities/characters/crew/thunk.md')).toBe('crew');
  });

  it('infers settlement subtype', () => {
    expect(inferSubtype('wiki/entities/places/settlements/warren.md')).toBe('settlement');
  });

  it('infers faction subtype', () => {
    expect(inferSubtype('wiki/entities/factions/salt-covenant.md')).toBe('faction');
  });

  it('infers vehicle subtype', () => {
    expect(inferSubtype('wiki/entities/vehicles/fernen.md')).toBe('vehicle');
  });

  it('infers active-situation subtype', () => {
    expect(inferSubtype('wiki/situations/active/blockade.md')).toBe('active-situation');
  });

  it('infers session-note subtype', () => {
    expect(inferSubtype('wiki/sessions/session-04-day-1.md')).toBe('session-note');
  });

  it('infers raw-session subtype for legacy flat session files', () => {
    expect(inferSubtype('.raw/sessions/s04/s04-raw.md')).toBe('raw-session');
  });

  it('infers raw-session-audio subtype', () => {
    expect(inferSubtype('.raw/sessions/session-04/audio/part01.wav')).toBe('raw-session-audio');
  });

  it('infers raw-session-transcript subtype', () => {
    expect(inferSubtype('.raw/sessions/session-04/transcripts/part01.csv')).toBe(
      'raw-session-transcript',
    );
  });

  it('infers raw-session-ingest subtype', () => {
    expect(inferSubtype('.raw/sessions/session-04/ingest/cleaned.md')).toBe('raw-session-ingest');
  });

  it('infers raw-session-note subtype', () => {
    expect(inferSubtype('.raw/sessions/session-04/notes/dm-notes.md')).toBe('raw-session-note');
  });

  it('infers raw-session-export subtype', () => {
    expect(inferSubtype('.raw/sessions/session-04/exports/recap.md')).toBe('raw-session-export');
  });

  it('infers session-manifest subtype for source-manifest.md in the session dir', () => {
    expect(inferSubtype('.raw/sessions/session-04/source-manifest.md')).toBe('session-manifest');
  });

  it('returns raw-session-audio (not session-manifest) for source-manifest.md nested under audio/', () => {
    expect(inferSubtype('.raw/sessions/session-04/audio/source-manifest.md')).toBe(
      'raw-session-audio',
    );
  });

  it('falls back to raw-session for other files in the session dir', () => {
    expect(inferSubtype('.raw/sessions/session-04/random.md')).toBe('raw-session');
  });

  it('returns unknown for unmatched paths', () => {
    expect(inferSubtype('somewhere/else.md')).toBe('unknown');
  });
});
