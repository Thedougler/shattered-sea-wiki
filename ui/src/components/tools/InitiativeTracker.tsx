import { useCallback, useEffect, useMemo, useRef, useState } from 'preact/hooks';

interface KnownCharacter {
  name: string;
  portrait: string | null;
  subtype: string;
}

interface Combatant {
  id: string;
  name: string;
  initiative: number;
  portrait: string | null;
  conditions: string[];
  isNpc: boolean;
}

interface Props {
  knownCharacters: KnownCharacter[];
}

const CONDITION_LIST = [
  'Blinded', 'Charmed', 'Deafened', 'Frightened', 'Grappled',
  'Incapacitated', 'Invisible', 'Paralyzed', 'Petrified', 'Poisoned',
  'Prone', 'Restrained', 'Stunned', 'Unconscious', 'Concentrating',
];

const COLORS = [
  '#d4a64e', '#5b8fd9', '#4ead7a', '#d4564e', '#8b6fc0',
  '#c07a4b', '#e07bab', '#5bc0de', '#a3be8c', '#ebcb8b',
];

function hashColor(name: string): string {
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = ((hash << 5) - hash + name.charCodeAt(i)) | 0;
  return COLORS[Math.abs(hash) % COLORS.length];
}

function initials(name: string): string {
  return name
    .split(/[\s-]+/)
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() ?? '')
    .join('');
}

let idCounter = 0;
function nextId(): string {
  return `c-${++idCounter}-${Math.random().toString(36).slice(2, 6)}`;
}

export default function InitiativeTracker({ knownCharacters }: Props) {
  const [combatants, setCombatants] = useState<Combatant[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [round, setRound] = useState(1);
  const [inCombat, setInCombat] = useState(false);

  // Add form state
  const [addName, setAddName] = useState('');
  const [addInit, setAddInit] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedSuggestion, setSelectedSuggestion] = useState(0);
  const nameInputRef = useRef<HTMLInputElement>(null);
  const initInputRef = useRef<HTMLInputElement>(null);

  // Condition popover
  const [conditionTarget, setConditionTarget] = useState<string | null>(null);

  const sorted = useMemo(
    () => [...combatants].sort((a, b) => b.initiative - a.initiative),
    [combatants],
  );

  const suggestions = useMemo(() => {
    if (!addName.trim()) return [];
    const q = addName.toLowerCase();
    return knownCharacters
      .filter(
        (c) =>
          c.name.toLowerCase().includes(q) &&
          !combatants.some((x) => x.name.toLowerCase() === c.name.toLowerCase()),
      )
      .slice(0, 6);
  }, [addName, knownCharacters, combatants]);

  const addCombatant = useCallback(
    (name: string, init: number, portrait: string | null, isNpc: boolean) => {
      setCombatants((prev) => [
        ...prev,
        {
          id: nextId(),
          name,
          initiative: init,
          portrait,
          conditions: [],
          isNpc,
        },
      ]);
    },
    [],
  );

  const handleAdd = useCallback(() => {
    const name = addName.trim();
    const init = parseInt(addInit) || 0;
    if (!name) return;

    const known = knownCharacters.find((c) => c.name.toLowerCase() === name.toLowerCase());
    addCombatant(
      known?.name ?? name,
      init,
      known?.portrait ?? null,
      known?.subtype !== 'pc',
    );
    setAddName('');
    setAddInit('');
    setShowSuggestions(false);
    nameInputRef.current?.focus();
  }, [addName, addInit, knownCharacters, addCombatant]);

  const selectSuggestion = useCallback(
    (char: KnownCharacter) => {
      setAddName(char.name);
      setShowSuggestions(false);
      initInputRef.current?.focus();
    },
    [],
  );

  const removeCombatant = useCallback(
    (id: string) => {
      setCombatants((prev) => {
        const next = prev.filter((c) => c.id !== id);
        setCurrentIndex((ci) => {
          const newSorted = [...next].sort((a, b) => b.initiative - a.initiative);
          if (ci >= newSorted.length) return 0;
          return ci;
        });
        return next;
      });
    },
    [],
  );

  const nextTurn = useCallback(() => {
    if (sorted.length === 0) return;
    if (!inCombat) {
      setInCombat(true);
      setCurrentIndex(0);
      setRound(1);
      return;
    }
    setCurrentIndex((prev) => {
      const next = prev + 1;
      if (next >= sorted.length) {
        setRound((r) => r + 1);
        return 0;
      }
      return next;
    });
  }, [sorted.length, inCombat]);

  const prevTurn = useCallback(() => {
    if (sorted.length === 0 || !inCombat) return;
    setCurrentIndex((prev) => {
      if (prev === 0) {
        setRound((r) => Math.max(1, r - 1));
        return sorted.length - 1;
      }
      return prev - 1;
    });
  }, [sorted.length, inCombat]);

  const resetCombat = useCallback(() => {
    setInCombat(false);
    setCurrentIndex(0);
    setRound(1);
  }, []);

  const clearAll = useCallback(() => {
    setCombatants([]);
    resetCombat();
  }, [resetCombat]);

  const toggleCondition = useCallback((id: string, condition: string) => {
    setCombatants((prev) =>
      prev.map((c) => {
        if (c.id !== id) return c;
        const has = c.conditions.includes(condition);
        return {
          ...c,
          conditions: has
            ? c.conditions.filter((x) => x !== condition)
            : [...c.conditions, condition],
        };
      }),
    );
  }, []);

  const updateInitiative = useCallback((id: string, newInit: number) => {
    setCombatants((prev) => prev.map((c) => (c.id === id ? { ...c, initiative: newInit } : c)));
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement
      )
        return;
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        nextTurn();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prevTurn();
      }
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [nextTurn, prevTurn]);

  return (
    <div class="initiative-tracker">
      {/* Header */}
      <div class="it-header">
        <div class="it-header-left">
          <h1 class="it-title">Initiative</h1>
          {inCombat && (
            <span class="it-round">Round {round}</span>
          )}
        </div>
        <div class="it-header-right">
          <button class="it-btn it-btn-secondary" onClick={clearAll}>
            Clear
          </button>
          {inCombat && (
            <button class="it-btn it-btn-secondary" onClick={resetCombat}>
              End Combat
            </button>
          )}
        </div>
      </div>

      {/* Add combatant form */}
      <div class="it-add-form">
        <div class="it-add-name-wrap">
          <input
            ref={nameInputRef}
            type="text"
            placeholder="Name"
            value={addName}
            onInput={(e) => {
              setAddName((e.target as HTMLInputElement).value);
              setShowSuggestions(true);
              setSelectedSuggestion(0);
            }}
            onFocus={() => setShowSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
            onKeyDown={(e) => {
              if (e.key === 'ArrowDown' && suggestions.length > 0) {
                e.preventDefault();
                setSelectedSuggestion((s) => Math.min(s + 1, suggestions.length - 1));
              } else if (e.key === 'ArrowUp' && suggestions.length > 0) {
                e.preventDefault();
                setSelectedSuggestion((s) => Math.max(s - 1, 0));
              } else if (e.key === 'Enter' && suggestions.length > 0 && showSuggestions) {
                e.preventDefault();
                selectSuggestion(suggestions[selectedSuggestion]);
              } else if (e.key === 'Tab' && !e.shiftKey) {
                setShowSuggestions(false);
              }
            }}
            class="it-input it-input-name"
          />
          {showSuggestions && suggestions.length > 0 && (
            <div class="it-suggestions">
              {suggestions.map((s, i) => (
                <button
                  key={s.name}
                  class={`it-suggestion ${i === selectedSuggestion ? 'it-suggestion-active' : ''}`}
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={() => selectSuggestion(s)}
                >
                  {s.portrait ? (
                    <img src={s.portrait} alt="" class="it-suggestion-portrait" />
                  ) : (
                    <span
                      class="it-suggestion-initials"
                      style={{ background: hashColor(s.name) }}
                    >
                      {initials(s.name)}
                    </span>
                  )}
                  <span class="it-suggestion-name">{s.name}</span>
                  <span class="it-suggestion-type">{s.subtype}</span>
                </button>
              ))}
            </div>
          )}
        </div>
        <input
          ref={initInputRef}
          type="number"
          placeholder="Init"
          value={addInit}
          onInput={(e) => setAddInit((e.target as HTMLInputElement).value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') handleAdd();
          }}
          class="it-input it-input-init"
        />
        <button class="it-btn it-btn-add" onClick={handleAdd}>
          Add
        </button>
      </div>

      {/* Turn controls */}
      {sorted.length > 0 && (
        <div class="it-controls">
          <button
            class="it-btn it-btn-turn it-btn-prev"
            onClick={prevTurn}
            disabled={!inCombat}
          >
            Prev
          </button>
          <button class="it-btn it-btn-turn it-btn-next" onClick={nextTurn}>
            {inCombat ? 'Next Turn' : 'Start Combat'}
          </button>
        </div>
      )}

      {/* Initiative list */}
      <div class="it-list">
        {sorted.map((c, i) => {
          const isCurrent = inCombat && i === currentIndex;
          const isOnDeck = inCombat && i === (currentIndex + 1) % sorted.length && sorted.length > 1;
          return (
            <div
              key={c.id}
              class={[
                'it-combatant',
                isCurrent && 'it-current',
                isOnDeck && 'it-on-deck',
              ]
                .filter(Boolean)
                .join(' ')}
            >
              {/* Turn indicator */}
              <div class="it-turn-indicator">
                {isCurrent && <span class="it-arrow it-arrow-current" />}
                {isOnDeck && <span class="it-arrow it-arrow-deck" />}
              </div>

              {/* Portrait */}
              <div class="it-portrait-wrap">
                {c.portrait ? (
                  <img src={c.portrait} alt={c.name} class="it-portrait" />
                ) : (
                  <div class="it-portrait-fallback" style={{ background: hashColor(c.name) }}>
                    {initials(c.name)}
                  </div>
                )}
              </div>

              {/* Info */}
              <div class="it-info">
                <div class="it-name-row">
                  <span class="it-name">{c.name}</span>
                  {isCurrent && <span class="it-label-current">CURRENT</span>}
                  {isOnDeck && <span class="it-label-deck">ON DECK</span>}
                </div>

                {/* Conditions */}
                {c.conditions.length > 0 && (
                  <div class="it-conditions">
                    {c.conditions.map((cond) => (
                      <span
                        key={cond}
                        class="it-condition"
                        onClick={() => toggleCondition(c.id, cond)}
                        title="Click to remove"
                      >
                        {cond}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Initiative value */}
              <div class="it-init-col">
                <input
                  type="number"
                  value={c.initiative}
                  class="it-init-value"
                  onInput={(e) => {
                    const val = parseInt((e.target as HTMLInputElement).value);
                    if (!isNaN(val)) updateInitiative(c.id, val);
                  }}
                  title="Initiative"
                />
              </div>

              {/* Actions */}
              <div class="it-actions">
                <button
                  class="it-btn-icon"
                  title="Conditions"
                  onClick={() =>
                    setConditionTarget(conditionTarget === c.id ? null : c.id)
                  }
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" />
                    <path d="M12 8v4M12 16h.01" />
                  </svg>
                </button>
                <button
                  class="it-btn-icon it-btn-remove"
                  title="Remove"
                  onClick={() => removeCombatant(c.id)}
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 6L6 18M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Condition popover */}
              {conditionTarget === c.id && (
                <div class="it-condition-popover">
                  {CONDITION_LIST.map((cond) => (
                    <label key={cond} class="it-condition-option">
                      <input
                        type="checkbox"
                        checked={c.conditions.includes(cond)}
                        onChange={() => toggleCondition(c.id, cond)}
                      />
                      <span>{cond}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          );
        })}

        {sorted.length === 0 && (
          <div class="it-empty">
            Add combatants above to begin tracking initiative.
          </div>
        )}
      </div>

      {/* Keyboard hint */}
      <div class="it-footer">
        <span>
          <kbd>Space</kbd> / <kbd>&#8594;</kbd> Next turn
        </span>
        <span>
          <kbd>&#8592;</kbd> Previous turn
        </span>
      </div>
    </div>
  );
}
