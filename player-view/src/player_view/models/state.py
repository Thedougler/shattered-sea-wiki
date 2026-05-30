from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    speaker: str
    text: str
    timestamp: float = 0.0


@dataclass
class SessionState:
    messages: list[ChatMessage] = field(default_factory=list)
    is_recording: bool = False
    session_length_s: float = 0.0
    chunk_count: int = 0
    speaker_count: int = 0
    status: str = 'idle'


@dataclass
class SlideshowState:
    images: list[str] = field(default_factory=list)
    current_index: int = 0
    interval_s: float = 10.0
