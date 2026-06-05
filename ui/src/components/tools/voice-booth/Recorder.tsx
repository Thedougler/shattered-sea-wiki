import { useCallback, useEffect, useRef, useState } from 'preact/hooks';

interface Props {
  onRecordingComplete: (blob: Blob, durationSec: number) => void;
  onDurationUpdate: (seconds: number) => void;
  isActive: boolean;
}

function getSupportedMimeType(): string {
  const types = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/mp4',
    'audio/ogg;codecs=opus',
  ];
  for (const t of types) {
    if (MediaRecorder.isTypeSupported(t)) return t;
  }
  return '';
}

function extensionForMime(mime: string): string {
  if (mime.includes('webm')) return 'webm';
  if (mime.includes('mp4')) return 'mp4';
  if (mime.includes('ogg')) return 'ogg';
  return 'webm';
}

export { extensionForMime, getSupportedMimeType };

export default function Recorder({ onRecordingComplete, onDurationUpdate, isActive }: Props) {
  const [recording, setRecording] = useState(false);
  const [permissionDenied, setPermissionDenied] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [level, setLevel] = useState(0);

  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);
  const stream = useRef<MediaStream | null>(null);
  const analyser = useRef<AnalyserNode | null>(null);
  const animFrame = useRef<number>(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startTime = useRef(0);
  const mimeType = useRef('');

  const cleanup = useCallback(() => {
    if (animFrame.current) cancelAnimationFrame(animFrame.current);
    if (timerRef.current) clearInterval(timerRef.current);
    if (stream.current) {
      stream.current.getTracks().forEach((t) => t.stop());
      stream.current = null;
    }
    analyser.current = null;
    mediaRecorder.current = null;
  }, []);

  useEffect(() => () => cleanup(), [cleanup]);

  const updateLevel = useCallback(() => {
    if (!analyser.current) return;
    const data = new Uint8Array(analyser.current.fftSize);
    analyser.current.getByteTimeDomainData(data);
    let sum = 0;
    for (let i = 0; i < data.length; i++) {
      const v = (data[i] - 128) / 128;
      sum += v * v;
    }
    setLevel(Math.min(1, Math.sqrt(sum / data.length) * 3));
    animFrame.current = requestAnimationFrame(updateLevel);
  }, []);

  const startRecording = useCallback(async () => {
    try {
      const s = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.current = s;
      setPermissionDenied(false);

      const ctx = new AudioContext();
      const source = ctx.createMediaStreamSource(s);
      const an = ctx.createAnalyser();
      an.fftSize = 256;
      source.connect(an);
      analyser.current = an;

      mimeType.current = getSupportedMimeType();
      const recorder = new MediaRecorder(s, mimeType.current ? { mimeType: mimeType.current } : {});
      chunks.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.current.push(e.data);
      };
      recorder.onstop = () => {
        const blob = new Blob(chunks.current, { type: mimeType.current || 'audio/webm' });
        const duration = (Date.now() - startTime.current) / 1000;
        onRecordingComplete(blob, duration);
        cleanup();
      };

      mediaRecorder.current = recorder;
      recorder.start(250);
      startTime.current = Date.now();
      setRecording(true);
      setElapsed(0);

      timerRef.current = setInterval(() => {
        const sec = (Date.now() - startTime.current) / 1000;
        setElapsed(sec);
        onDurationUpdate(sec);
      }, 250);

      updateLevel();
    } catch {
      setPermissionDenied(true);
    }
  }, [onRecordingComplete, onDurationUpdate, updateLevel, cleanup]);

  const stopRecording = useCallback(() => {
    if (mediaRecorder.current && mediaRecorder.current.state !== 'inactive') {
      mediaRecorder.current.stop();
    }
    setRecording(false);
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const formatTime = (sec: number) => {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  if (!isActive) return null;

  return (
    <div class="vb-recorder">
      {permissionDenied && (
        <div class="vb-recorder__error">
          Microphone access denied. Please allow microphone access and try again.
        </div>
      )}

      <div class="vb-recorder__controls">
        {!recording ? (
          <button class="vb-recorder__btn vb-recorder__btn--start" onClick={startRecording}>
            <span class="vb-recorder__btn-icon">●</span> Record
          </button>
        ) : (
          <button class="vb-recorder__btn vb-recorder__btn--stop" onClick={stopRecording}>
            <span class="vb-recorder__btn-icon">■</span> Done
          </button>
        )}

        <div class="vb-recorder__timer">{formatTime(elapsed)}</div>
      </div>

      {recording && (
        <div class="vb-recorder__meter">
          <div class="vb-recorder__meter-fill" style={{ width: `${level * 100}%` }} />
        </div>
      )}
    </div>
  );
}
