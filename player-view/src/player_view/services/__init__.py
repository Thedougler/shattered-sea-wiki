from __future__ import annotations

from pathlib import Path

from player_view.services.audio import AudioService
from player_view.services.asr import ASRService
from player_view.services.diarization import DiarizationService
from player_view.services.spatial import SpatialAnalyzer
from player_view.services.session_transcriber import SessionTranscriber
from player_view.models.voice_profile import ProfileStore
from player_view.models.state import SessionState

audio: AudioService | None = None
asr: ASRService | None = None
diarization: DiarizationService | None = None
profiles: ProfileStore | None = None
spatial: SpatialAnalyzer | None = None
transcriber: SessionTranscriber | None = None
session_state: SessionState | None = None


def init(profile_dir: Path | None = None):
    global audio, asr, diarization, profiles, spatial, transcriber, session_state
    audio = AudioService()
    asr = ASRService()
    asr.init()
    diarization = DiarizationService()
    diarization.init()
    profiles = ProfileStore(profile_dir or Path('profiles'))
    spatial = SpatialAnalyzer()
    session_state = SessionState()
    transcriber = SessionTranscriber(
        asr=asr, spatial=spatial, diarization=diarization,
        profiles=profiles, session_state=session_state,
    )


def teardown():
    global audio, asr, diarization, profiles, spatial, transcriber, session_state
    if audio and audio.recording:
        audio.stop()
    audio = asr = diarization = profiles = spatial = transcriber = session_state = None
