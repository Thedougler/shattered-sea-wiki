import queue
import threading
from dataclasses import dataclass, field

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
        self._audio_queue: queue.Queue = queue.Queue()
        self._thread: threading.Thread | None = None
        self._running = False
        self.latest_result = ASRResult()

    def init(self):
        self.model = from_pretrained(self.MODEL_ID)

    @property
    def sample_rate(self) -> int:
        return self.model.preprocessor_config.sample_rate

    def start_streaming(self, on_result=None):
        self._running = True
        self._audio_queue = queue.Queue()
        self.latest_result = ASRResult()
        self._thread = threading.Thread(
            target=self._stream_worker,
            args=(on_result,),
            daemon=True,
        )
        self._thread.start()

    def feed_audio(self, chunk):
        if self._running:
            self._audio_queue.put(chunk)

    def stop_streaming(self) -> ASRResult:
        self._running = False
        self._audio_queue.put(None)
        if self._thread:
            self._thread.join(timeout=10)
            self._thread = None
        return self.latest_result

    def _stream_worker(self, on_result):
        with self.model.transcribe_stream(
            context_size=(256, 256),
            depth=2,
            keep_original_attention=False,
        ) as streamer:
            while self._running:
                try:
                    chunk = self._audio_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                if chunk is None:
                    break
                streamer.add_audio(chunk)
                finalized = ' '.join(t.text for t in streamer.finalized_tokens)
                draft = ' '.join(t.text for t in streamer.draft_tokens)
                result = ASRResult(
                    text=streamer.result.text,
                    finalized_text=finalized,
                    draft_text=draft,
                )
                self.latest_result = result
                if on_result:
                    on_result(result)
