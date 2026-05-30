from __future__ import annotations

from pathlib import Path

from player_view.services.audio import AudioService
from player_view.services.asr import ASRService
from player_view.services.diarization import DiarizationService
from player_view.models.voice_profile import ProfileStore

audio: AudioService | None = None
asr: ASRService | None = None
diarization: DiarizationService | None = None
profiles: ProfileStore | None = None


def init(profile_dir: Path | None = None):
    global audio, asr, diarization, profiles
    audio = AudioService()
    asr = ASRService()
    asr.init()
    diarization = DiarizationService()
    diarization.init()
    profiles = ProfileStore(profile_dir or Path('profiles'))


def teardown():
    global audio, asr, diarization, profiles
    if audio and audio.recording:
        audio.stop()
    audio = asr = diarization = profiles = None
