"""Configuration management for shattered-audio."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


PROFILES_DIR = Path.home() / ".config" / "shattered-audio" / "profiles"


@dataclass
class Config:
    vault_path: Path = Path(".")
    whisper_model: str = "mlx-community/whisper-large-v3-mlx"
    whisper_model_fast: str = "mlx-community/whisper-medium-mlx"
    device: str = "mps"
    speaker_map: dict[str, str] = field(default_factory=dict)
    mic_names: list[str] = field(default_factory=list)
    channel_priors: dict[str, str] = field(default_factory=dict)
    channel_boost: float = 0.15
    speaker_threshold: float = 0.7
    profiles_dir: Path = PROFILES_DIR
    chunk_target_minutes: int = 15
    chunk_silence_gap: float = 2.0
    inbox_path: Path = Path("Inbox")

    @classmethod
    def load(cls, path: Path | None = None) -> Config:
        candidates = [
            path,
            Path("config.yaml"),
            Path.home() / ".config" / "shattered-audio" / "config.yaml",
        ]
        for candidate in candidates:
            if candidate and candidate.exists():
                with open(candidate) as f:
                    data = yaml.safe_load(f) or {}
                return cls(
                    vault_path=Path(data.get("vault_path", ".")),
                    whisper_model=data.get("whisper_model", cls.whisper_model),
                    whisper_model_fast=data.get("whisper_model_fast", cls.whisper_model_fast),
                    device=data.get("device", cls.device),
                    speaker_map=data.get("speaker_map", {}),
                    mic_names=data.get("mic_names", []),
                    channel_priors=data.get("channel_priors", {}),
                    channel_boost=data.get("channel_boost", cls.channel_boost),
                    speaker_threshold=data.get("speaker_threshold", cls.speaker_threshold),
                    profiles_dir=Path(data.get("profiles_dir", cls.profiles_dir)),
                    chunk_target_minutes=data.get("chunk_target_minutes", cls.chunk_target_minutes),
                    chunk_silence_gap=data.get("chunk_silence_gap", cls.chunk_silence_gap),
                    inbox_path=Path(data.get("inbox_path", cls.inbox_path)),
                )
        return cls()
