import { describe, expect, it } from 'vitest';
import {
  CANONICAL,
  ALIASES,
  DEPRECATED_FRONTMATTER,
  classify,
} from '../src/taxonomy.js';

describe('CANONICAL', () => {
  it('contains expected faction tags', () => {
    expect(CANONICAL.has('dravosi')).toBe(true);
    expect(CANONICAL.has('tessarine')).toBe(true);
  });

  it('contains expected workflow tags', () => {
    expect(CANONICAL.has('dm-prep')).toBe(true);
    expect(CANONICAL.has('encounter-ready')).toBe(true);
  });
});

describe('classify', () => {
  it('recognizes canonical tags', () => {
    expect(classify('maritime')).toEqual(['canonical', 'maritime']);
  });

  it('resolves aliases', () => {
    expect(classify('crown')).toEqual(['alias', 'dravosi']);
    expect(classify('dm-notes')).toEqual(['alias', 'dm-prep']);
  });

  it('flags deprecated frontmatter tags', () => {
    expect(classify('npc')).toEqual(['deprecated-fm', null]);
    expect(classify('faction')).toEqual(['deprecated-fm', null]);
  });

  it('flags deprecated entity name tags', () => {
    expect(classify('perrin')).toEqual(['deprecated-entity', null]);
    expect(classify('calveno')).toEqual(['deprecated-entity', null]);
  });

  it('flags deprecated source tags', () => {
    expect(classify('xmm')).toEqual(['deprecated-source', null]);
  });

  it('flags deprecated system tags', () => {
    expect(classify('work-queue')).toEqual(['deprecated-system', null]);
  });

  it('passes through visibility tags', () => {
    expect(classify('visibility/hidden')).toEqual(['visibility', null]);
  });

  it('returns unknown for unrecognized tags', () => {
    expect(classify('completely-novel')).toEqual(['unknown', null]);
  });
});
