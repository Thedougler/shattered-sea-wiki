import os

import numpy as np
import torch
from dotenv import find_dotenv, load_dotenv
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from scipy.spatial.distance import cdist

load_dotenv(find_dotenv(usecwd=True))


class DiarizationService:
    EMBEDDING_MODEL = 'pyannote/embedding'
    SAMPLE_RATE = 16000

    def __init__(self):
        self._embedding_model: PretrainedSpeakerEmbedding | None = None

    def init(self):
        token = os.environ.get('HF_TOKEN')
        self._embedding_model = PretrainedSpeakerEmbedding(
            self.EMBEDDING_MODEL,
            device=torch.device('cpu'),
            token=token,
        )

    def extract_embedding(self, audio: np.ndarray) -> np.ndarray:
        waveform = torch.from_numpy(audio).float().unsqueeze(0).unsqueeze(0)
        embedding = self._embedding_model(waveform)
        return embedding[0]

    def compare(self, emb_a: np.ndarray, emb_b: np.ndarray) -> float:
        dist = cdist(
            emb_a.reshape(1, -1),
            emb_b.reshape(1, -1),
            metric='cosine',
        )[0, 0]
        return 1.0 - dist

    def rank_against(
        self,
        embedding: np.ndarray,
        profiles: list[tuple[str, np.ndarray]],
    ) -> list[tuple[str, float]]:
        results = []
        for name, prof_emb in profiles:
            sim = self.compare(embedding, prof_emb)
            results.append((name, sim))
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def rank_against_with_spatial(
        self,
        embedding: np.ndarray,
        dm_ratio: float,
        profiles: list[tuple[str, np.ndarray, float | None]],
        spatial_weight: float = 0.2,
    ) -> list[tuple[str, float]]:
        results = []
        for name, prof_emb, spatial_sig in profiles:
            cosine_sim = self.compare(embedding, prof_emb)
            if spatial_sig is not None and spatial_weight > 0:
                spatial_sim = 1.0 - abs(spatial_sig - dm_ratio)
                score = (1 - spatial_weight) * cosine_sim + spatial_weight * spatial_sim
            else:
                score = cosine_sim
            results.append((name, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results
