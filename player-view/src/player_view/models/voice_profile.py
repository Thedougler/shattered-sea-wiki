import base64
import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np


@dataclass
class VoiceProfile:
    character: str
    player: str
    embedding: np.ndarray
    sample_count: int = 1
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    spatial_signature: float | None = None
    spatial_sample_count: int = 0

    def to_dict(self) -> dict:
        return {
            'character': self.character,
            'player': self.player,
            'embedding': base64.b64encode(self.embedding.tobytes()).decode(),
            'embedding_shape': list(self.embedding.shape),
            'embedding_dtype': str(self.embedding.dtype),
            'sample_count': self.sample_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'spatial_signature': self.spatial_signature,
            'spatial_sample_count': self.spatial_sample_count,
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'VoiceProfile':
        raw = base64.b64decode(d['embedding'])
        dtype = np.dtype(d.get('embedding_dtype', 'float32'))
        shape = tuple(d.get('embedding_shape', [-1]))
        embedding = np.frombuffer(raw, dtype=dtype).reshape(shape)
        return cls(
            character=d['character'],
            player=d['player'],
            embedding=embedding,
            sample_count=d.get('sample_count', 1),
            created_at=d.get('created_at', 0),
            updated_at=d.get('updated_at', 0),
            spatial_signature=d.get('spatial_signature'),
            spatial_sample_count=d.get('spatial_sample_count', 0),
        )

    def update_spatial(self, new_ratio: float):
        if self.spatial_signature is None:
            self.spatial_signature = new_ratio
            self.spatial_sample_count = 1
        else:
            n = self.spatial_sample_count
            self.spatial_signature = (self.spatial_signature * n + new_ratio) / (n + 1)
            self.spatial_sample_count = n + 1


class ProfileStore:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path_for(self, character: str) -> Path:
        safe = character.lower().replace(' ', '_')
        return self.directory / f'{safe}.json'

    def save(self, profile: VoiceProfile):
        profile.updated_at = time.time()
        path = self._path_for(profile.character)
        path.write_text(json.dumps(profile.to_dict(), indent=2))

    def load(self, character: str) -> VoiceProfile | None:
        path = self._path_for(character)
        if not path.exists():
            return None
        return VoiceProfile.from_dict(json.loads(path.read_text()))

    def load_all(self) -> list[VoiceProfile]:
        profiles = []
        for path in self.directory.glob('*.json'):
            try:
                profiles.append(VoiceProfile.from_dict(json.loads(path.read_text())))
            except (json.JSONDecodeError, KeyError):
                continue
        return profiles

    def delete(self, character: str) -> bool:
        path = self._path_for(character)
        if path.exists():
            path.unlink()
            return True
        return False

    def update_embedding(self, character: str, new_embedding: np.ndarray):
        profile = self.load(character)
        if profile is None:
            raise ValueError(f'No profile for {character}')
        n = profile.sample_count
        profile.embedding = (profile.embedding * n + new_embedding) / (n + 1)
        profile.sample_count = n + 1
        self.save(profile)
