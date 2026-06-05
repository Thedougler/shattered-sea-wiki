import { useCallback, useState } from 'preact/hooks';
import type { CharacterInfo, Phase } from './voice-booth/types';
import Teleprompter from './voice-booth/Teleprompter';
import Recorder from './voice-booth/Recorder';
import ScoreBoard from './voice-booth/ScoreBoard';
import { getSupportedMimeType, extensionForMime } from './voice-booth/Recorder';

interface Props {
  pcs: CharacterInfo[];
  npcs: CharacterInfo[];
}

export default function VoiceBooth({ pcs, npcs }: Props) {
  const [phase, setPhase] = useState<Phase>('select');
  const [selected, setSelected] = useState<CharacterInfo | null>(null);
  const [npcSearch, setNpcSearch] = useState('');
  const [showNpcPicker, setShowNpcPicker] = useState(false);
  const [customName, setCustomName] = useState('');
  const [customSummary, setCustomSummary] = useState('');

  const [charBlob, setCharBlob] = useState<Blob | null>(null);
  const [charDuration, setCharDuration] = useState(0);
  const [normalBlob, setNormalBlob] = useState<Blob | null>(null);
  const [normalDuration, setNormalDuration] = useState(0);
  const [liveCharDuration, setLiveCharDuration] = useState(0);
  const [liveNormalDuration, setLiveNormalDuration] = useState(0);

  const selectCharacter = useCallback((c: CharacterInfo) => {
    setSelected(c);
    setPhase('character-voice');
    setShowNpcPicker(false);
  }, []);

  const selectCustom = useCallback(() => {
    if (!customName.trim()) return;
    setSelected({
      name: customName.trim(),
      slug: customName.trim().toLowerCase().replace(/\s+/g, '-'),
      portrait: null,
      summary: customSummary.trim() || 'A mysterious character',
      subtype: 'npc',
    });
    setPhase('character-voice');
    setShowNpcPicker(false);
  }, [customName, customSummary]);

  const handleCharRecording = useCallback((blob: Blob, dur: number) => {
    setCharBlob(blob);
    setCharDuration(dur);
    setPhase('normal-voice');
  }, []);

  const handleNormalRecording = useCallback((blob: Blob, dur: number) => {
    setNormalBlob(blob);
    setNormalDuration(dur);
    setPhase('complete');
  }, []);

  const download = useCallback((blob: Blob, suffix: string) => {
    if (!selected || !blob) return;
    const ext = extensionForMime(getSupportedMimeType());
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${selected.slug}-${suffix}.${ext}`;
    a.click();
    URL.revokeObjectURL(a.href);
  }, [selected]);

  const filteredNpcs = npcSearch
    ? npcs.filter((n) => n.name.toLowerCase().includes(npcSearch.toLowerCase())).slice(0, 12)
    : npcs.slice(0, 12);

  // --- SELECT PHASE ---
  if (phase === 'select') {
    return (
      <div class="vb-container">
        <div class="vb-header">
          <h1 class="vb-title">Voice Booth</h1>
          <p class="vb-subtitle">Record a voice profile for a character. Pick who you're voicing.</p>
        </div>

        <div class="vb-section">
          <h2 class="vb-section-title">Player Characters</h2>
          <div class="vb-cards">
            {pcs.map((pc) => (
              <button key={pc.slug} class="vb-card" onClick={() => selectCharacter(pc)}>
                <div class="vb-card__portrait">
                  {pc.portrait ? (
                    <img src={pc.portrait} alt={pc.name} />
                  ) : (
                    <div class="vb-card__initials">
                      {pc.name.split(/[\s-]+/).slice(0, 2).map((w) => w[0]?.toUpperCase()).join('')}
                    </div>
                  )}
                </div>
                <div class="vb-card__name">{pc.name}</div>
              </button>
            ))}
          </div>
        </div>

        <div class="vb-section">
          <h2 class="vb-section-title">NPC Voice</h2>
          {!showNpcPicker ? (
            <button class="vb-btn vb-btn--secondary" onClick={() => setShowNpcPicker(true)}>
              Record for an NPC
            </button>
          ) : (
            <div class="vb-npc-picker">
              <input
                class="vb-input"
                type="text"
                placeholder="Search NPCs..."
                value={npcSearch}
                onInput={(e) => setNpcSearch((e.target as HTMLInputElement).value)}
                autoFocus
              />
              {filteredNpcs.length > 0 && (
                <div class="vb-npc-list">
                  {filteredNpcs.map((npc) => (
                    <button key={npc.slug} class="vb-npc-item" onClick={() => selectCharacter(npc)}>
                      <span class="vb-npc-item__name">{npc.name}</span>
                      {npc.summary && (
                        <span class="vb-npc-item__summary">{npc.summary.slice(0, 80)}</span>
                      )}
                    </button>
                  ))}
                </div>
              )}
              <div class="vb-custom">
                <h3 class="vb-custom__title">Or create a custom character</h3>
                <input
                  class="vb-input"
                  type="text"
                  placeholder="Character name"
                  value={customName}
                  onInput={(e) => setCustomName((e.target as HTMLInputElement).value)}
                />
                <input
                  class="vb-input"
                  type="text"
                  placeholder="Brief description (species, class, personality...)"
                  value={customSummary}
                  onInput={(e) => setCustomSummary((e.target as HTMLInputElement).value)}
                />
                <button
                  class="vb-btn vb-btn--primary"
                  onClick={selectCustom}
                  disabled={!customName.trim()}
                >
                  Start Recording
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // --- RECORDING PHASES ---
  if (phase === 'character-voice' || phase === 'normal-voice') {
    const isChar = phase === 'character-voice';
    const mode = isChar ? 'character' : 'normal';
    const liveDuration = isChar ? liveCharDuration : liveNormalDuration;
    const setLiveDuration = isChar ? setLiveCharDuration : setLiveNormalDuration;

    return (
      <div class="vb-container">
        <div class="vb-header">
          <h1 class="vb-title">
            {isChar ? `Voice: ${selected!.name}` : 'Your Normal Voice'}
          </h1>
          <p class="vb-subtitle">
            {isChar
              ? 'Read the script in character. Have fun with it — ham it up!'
              : 'Now read this one in your regular voice. Just be yourself.'}
          </p>
        </div>

        <div class="vb-booth">
          <Teleprompter
            character={selected!.name}
            summary={selected!.summary}
            mode={mode}
            isRecording={true}
          />

          <div class="vb-booth__controls">
            <Recorder
              isActive={true}
              onRecordingComplete={isChar ? handleCharRecording : handleNormalRecording}
              onDurationUpdate={setLiveDuration}
            />
            <ScoreBoard
              seconds={liveDuration}
              label={isChar ? 'Character Voice' : 'Normal Voice'}
            />
          </div>
        </div>
      </div>
    );
  }

  // --- COMPLETE PHASE ---
  return (
    <div class="vb-container">
      <div class="vb-header">
        <h1 class="vb-title">Recording Complete!</h1>
        <p class="vb-subtitle">
          Voice profile samples for {selected!.name} are ready to download.
        </p>
      </div>

      <div class="vb-results">
        <div class="vb-result">
          <ScoreBoard seconds={charDuration} label="Character Voice" />
          <button class="vb-btn vb-btn--primary" onClick={() => download(charBlob!, 'character')}>
            Download Character Voice
          </button>
          <button class="vb-btn vb-btn--ghost" onClick={() => {
            setCharBlob(null);
            setCharDuration(0);
            setLiveCharDuration(0);
            setPhase('character-voice');
          }}>
            Re-record
          </button>
        </div>

        <div class="vb-result">
          <ScoreBoard seconds={normalDuration} label="Normal Voice" />
          <button class="vb-btn vb-btn--primary" onClick={() => download(normalBlob!, 'normal')}>
            Download Normal Voice
          </button>
          <button class="vb-btn vb-btn--ghost" onClick={() => {
            setNormalBlob(null);
            setNormalDuration(0);
            setLiveNormalDuration(0);
            setPhase('normal-voice');
          }}>
            Re-record
          </button>
        </div>
      </div>

      <button class="vb-btn vb-btn--secondary vb-start-over" onClick={() => {
        setPhase('select');
        setSelected(null);
        setCharBlob(null);
        setNormalBlob(null);
        setCharDuration(0);
        setNormalDuration(0);
        setLiveCharDuration(0);
        setLiveNormalDuration(0);
      }}>
        Start Over
      </button>
    </div>
  );
}
