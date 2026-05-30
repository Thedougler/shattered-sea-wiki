from dataclasses import dataclass

import numpy as np


@dataclass
class SpatialAnalysis:
    dm_energy: float
    player_energy: float
    dm_ratio: float
    fingerprint: np.ndarray
    best_channel_audio: np.ndarray
    dm_channel_audio: np.ndarray
    player_channel_audio: np.ndarray
    is_speech: bool


class SpatialAnalyzer:
    def __init__(
        self,
        dm_channels: list[int] | None = None,
        player_channels: list[int] | None = None,
        silence_db: float = -50.0,
    ):
        self.dm_channels = dm_channels or [0]
        self.player_channels = player_channels or [1, 2]
        self._silence_threshold = 10 ** (silence_db / 20)

    def analyze(self, chunk: np.ndarray) -> SpatialAnalysis:
        n_channels = chunk.shape[1]
        channel_rms = np.array(
            [float(np.sqrt(np.mean(chunk[:, ch] ** 2))) for ch in range(n_channels)]
        )
        total_rms = channel_rms.sum()
        if total_rms < 1e-10:
            fingerprint = np.full(n_channels, 1.0 / n_channels)
        else:
            fingerprint = channel_rms / total_rms

        dm_audio = np.mean(chunk[:, self.dm_channels], axis=1)
        player_audio = np.mean(chunk[:, self.player_channels], axis=1)

        dm_rms = float(np.sqrt(np.mean(dm_audio**2)))
        player_rms = float(np.sqrt(np.mean(player_audio**2)))

        dm_ratio = dm_rms / (dm_rms + player_rms + 1e-10)
        is_speech = max(dm_rms, player_rms) > self._silence_threshold

        if dm_rms >= player_rms:
            best = dm_audio
        else:
            best = player_audio

        return SpatialAnalysis(
            dm_energy=dm_rms,
            player_energy=player_rms,
            dm_ratio=dm_ratio,
            fingerprint=fingerprint,
            best_channel_audio=best,
            dm_channel_audio=dm_audio,
            player_channel_audio=player_audio,
            is_speech=is_speech,
        )
