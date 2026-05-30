import threading
from dataclasses import dataclass

import mlx.core as mx
from parakeet_mlx import from_pretrained


@dataclass
class ASRResult:
    text: str = ''
    finalized_text: str = ''
    draft_text: str = ''


class ASRService:
    MODEL_ID = 'mlx-community/parakeet-tdt-0.6b-v3'

    def __init__(self):
        self.model = None
        self._running = False
        self._streamer = None
        self._ctx = None
        self._pending: list = []
        self._lock = threading.Lock()
        self.latest_result = ASRResult()

    def init(self):
        self.model = from_pretrained(self.MODEL_ID)

    @property
    def sample_rate(self) -> int:
        return self.model.preprocessor_config.sample_rate

    def start_streaming(self):
        self._running = True
        with self._lock:
            self._pending = []
        self.latest_result = ASRResult()
        self._ctx = self.model.transcribe_stream(
            context_size=(256, 256),
            depth=2,
            keep_original_attention=False,
        )
        self._streamer = self._ctx.__enter__()

    def feed_audio(self, chunk):
        if self._running:
            with self._lock:
                self._pending.append(chunk)

    def process_pending(self):
        if not self._running or not self._streamer:
            return
        with self._lock:
            chunks = self._pending
            self._pending = []
        if not chunks:
            return
        for chunk in chunks:
            self._streamer.add_audio(mx.array(chunk))
        finalized = ' '.join(t.text for t in self._streamer.finalized_tokens)
        draft = ' '.join(t.text for t in self._streamer.draft_tokens)
        self.latest_result = ASRResult(
            text=self._streamer.result.text,
            finalized_text=finalized,
            draft_text=draft,
        )

    def stop_streaming(self) -> ASRResult:
        self._running = False
        with self._lock:
            self._pending = []
        self._streamer = None
        self._ctx = None
        return self.latest_result
