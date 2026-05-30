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
    spatial_fingerprint: np.ndarray | None = None
    spatial_m2: np.ndarray | None = None
    spatial_sample_count: int = 0

    @property
    def spatial_consistency(self) -> float | None:
        if self.spatial_sample_count < 2 or self.spatial_m2 is None:
            return None
        variance = self.spatial_m2 / self.spatial_sample_count
        return float(np.exp(-10.0 * np.mean(variance)))

    def to_dict(self) -> dict:
        d = {
            'character': self.character,
            'player': self.player,
            'embedding': base64.b64encode(self.embedding.tobytes()).decode(),
            'embedding_shape': list(self.embedding.shape),
            'embedding_dtype': str(self.embedding.dtype),
            'sample_count': self.sample_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'spatial_sample_count': self.spatial_sample_count,
        }
        if self.spatial_fingerprint is not None:
            d['spatial_fingerprint'] = self.spatial_fingerprint.tolist()
        else:
            d['spatial_fingerprint'] = None
        if self.spatial_m2 is not None:
            d['spatial_m2'] = self.spatial_m2.tolist()
        else:
            d['spatial_m2'] = None
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'VoiceProfile':
        raw = base64.b64decode(d['embedding'])
        dtype = np.dtype(d.get('embedding_dtype', 'float32'))
        shape = tuple(d.get('embedding_shape', [-1]))
        embedding = np.frombuffer(raw, dtype=dtype).reshape(shape)

        fp_raw = d.get('spatial_fingerprint')
        m2_raw = d.get('spatial_m2')
        spatial_n = d.get('spatial_sample_count', 0)

        if fp_raw is not None:
            spatial_fp = np.array(fp_raw, dtype=np.float64)
            spatial_m2 = np.array(m2_raw, dtype=np.float64) if m2_raw is not None else None
        elif d.get('spatial_signature') is not None:
            sig = d['spatial_signature']
            rest = (1.0 - sig) / 2.0
            spatial_fp = np.array([sig, rest, rest], dtype=np.float64)
            spatial_m2 = None
        else:
            spatial_fp = None
            spatial_m2 = None

        return cls(
            character=d['character'],
            player=d['player'],
            embedding=embedding,
            sample_count=d.get('sample_count', 1),
            created_at=d.get('created_at', 0),
            updated_at=d.get('updated_at', 0),
            spatial_fingerprint=spatial_fp,
            spatial_m2=spatial_m2,
            spatial_sample_count=spatial_n,
        )

    def update_spatial(self, new_fingerprint: np.ndarray):
        fp = np.asarray(new_fingerprint, dtype=np.float64)
        self.spatial_sample_count += 1
        n = self.spatial_sample_count
        if n == 1:
            self.spatial_fingerprint = fp.copy()
            self.spatial_m2 = np.zeros_like(fp)
        else:
            delta = fp - self.spatial_fingerprint
            self.spatial_fingerprint = self.spatial_fingerprint + delta / n
            delta2 = fp - self.spatial_fingerprint
            self.spatial_m2 = self.spatial_m2 + delta * delta2


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
