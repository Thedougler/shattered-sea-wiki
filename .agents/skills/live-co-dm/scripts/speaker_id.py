#!/usr/bin/env python3
"""Pure speaker-identification policy.

Given a speaker embedding, decide which enrolled *character voice* it is — or, if
none matches, assign a stable ``Unknown-N`` label by clustering against previously
seen unknown voices. Confidence is exposed through the top-1/top-2 cosine margin
so the renderer can flag shaky attributions with ``(?)`` instead of silently
guessing — important when five players talk over each other doing many voices.

No numpy: embeddings are plain float lists (see ``vecmath``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import vecmath
from profiles import VoiceProfile


@dataclass(frozen=True)
class Identification:
    name: str
    player: str
    score: float
    margin: float
    confident: bool
    is_unknown: bool


@dataclass
class SpeakerIdentifier:
    """Match embeddings to profiles; cluster the rest into stable Unknown-N labels.

    ``threshold`` is the minimum cosine similarity to accept a known profile (and
    to fold a new embedding into an existing unknown cluster). ``margin`` is the
    minimum top-1 minus top-2 gap required to call a known match *confident*.
    """

    profiles: list[VoiceProfile]
    threshold: float = 0.5
    margin: float = 0.1
    _unknowns: list[list[float]] = field(default_factory=list, init=False)

    def identify(self, embedding: list[float]) -> Identification:
        scored = sorted(
            (
                (vecmath.cosine_similarity(embedding, p.embedding), p)
                for p in self.profiles
            ),
            key=lambda t: t[0],
            reverse=True,
        )
        if scored and scored[0][0] >= self.threshold:
            top_score, top = scored[0]
            second = scored[1][0] if len(scored) > 1 else 0.0
            gap = top_score - second
            return Identification(
                name=top.name,
                player=top.player,
                score=top_score,
                margin=gap,
                confident=gap >= self.margin,
                is_unknown=False,
            )
        return self._assign_unknown(embedding)

    def _assign_unknown(self, embedding: list[float]) -> Identification:
        best_idx, best_score = -1, -1.0
        for idx, centroid in enumerate(self._unknowns):
            score = vecmath.cosine_similarity(embedding, centroid)
            if score > best_score:
                best_idx, best_score = idx, score
        if best_idx >= 0 and best_score >= self.threshold:
            label = best_idx + 1
            score = best_score
        else:
            self._unknowns.append(list(embedding))
            label = len(self._unknowns)
            score = 1.0
        return Identification(
            name=f"Unknown-{label}",
            player="",
            score=score,
            margin=0.0,
            confident=False,
            is_unknown=True,
        )
