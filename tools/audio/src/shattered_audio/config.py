"""Configuration management for shattered-audio."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Config:
    vault_path: Path = Path(".")
    whisper_model: str = "mlx-community/whisper-large-v3-mlx"
    device: str = "mps"
    speaker_map: dict[str, str] = field(default_factory=dict)

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
                    device=data.get("device", cls.device),
                    speaker_map=data.get("speaker_map", {}),
                )
        return cls()
