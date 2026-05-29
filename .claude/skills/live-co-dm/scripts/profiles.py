#!/usr/bin/env python3
"""Voice profiles: one enrolled *character voice* each, JSON-backed.

A profile pairs a speaker embedding (plain float list — no numpy) with the
character ``name`` and the physical ``player`` who performs it. Storing the
embedding as JSON keeps profiles tiny, diffable, and safe to commit, and lets
the identifier run on pure stdlib. The ``player`` field is what lets the
identifier tell apart the several characters one person voices.

Usage:
    store = ProfileStore("/path/to/profiles")
    store.save(VoiceProfile(...))
    profiles = store.load_all()
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class VoiceProfile:
    name: str
    player: str
    embedding: list[float]
    sample_rate: int
    model_id: str
    seconds: float
    created_utc: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "VoiceProfile":
        return cls(
            name=data["name"],
            player=data["player"],
            embedding=[float(x) for x in data["embedding"]],
            sample_rate=int(data["sample_rate"]),
            model_id=data["model_id"],
            seconds=float(data["seconds"]),
            created_utc=data["created_utc"],
        )


def slugify(name: str) -> str:
    """Filesystem-safe, stable slug for a profile filename."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "profile"


class ProfileStore:
    """Reads/writes ``VoiceProfile`` records as ``<slug>.json`` in one directory."""

    def __init__(self, directory: str) -> None:
        self.directory = directory

    def save(self, profile: VoiceProfile) -> str:
        os.makedirs(self.directory, exist_ok=True)
        path = os.path.join(self.directory, f"{slugify(profile.name)}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(profile.to_dict(), fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        return path

    def load_all(self) -> list[VoiceProfile]:
        if not os.path.isdir(self.directory):
            return []
        out: list[VoiceProfile] = []
        for entry in sorted(os.listdir(self.directory)):
            if not entry.endswith(".json"):
                continue
            path = os.path.join(self.directory, entry)
            try:
                with open(path, encoding="utf-8") as fh:
                    out.append(VoiceProfile.from_dict(json.load(fh)))
            except (json.JSONDecodeError, KeyError, ValueError, OSError):
                # A malformed profile must never crash a live session.
                continue
        return out
