import time

from player_view.models.state import ChatMessage, SessionState
from player_view.models.voice_profile import ProfileStore


class SessionTranscriber:
    def __init__(
        self,
        asr,
        spatial,
        diarization,
        profiles: ProfileStore,
        session_state: SessionState,
        spatial_weight: float = 0.2,
    ):
        self._asr = asr
        self._spatial = spatial
        self._diarization = diarization
        self._profiles = profiles
        self._state = session_state
        self._spatial_weight = spatial_weight
        self._current_speaker: str | None = None
        self._current_text: list[str] = []
        self._last_finalized: str = ""
        self._seen_speakers: set[str] = set()

    def process_chunk(self, chunk):
        analysis = self._spatial.analyze(chunk)
        if not analysis.is_speech:
            return

        self._state.chunk_count += 1

        self._asr.feed_audio(analysis.best_channel_audio)
        result = self._asr.latest_result
        new_text = result.finalized_text
        if not new_text or new_text == self._last_finalized:
            return
        added = new_text[len(self._last_finalized) :].strip()
        self._last_finalized = new_text
        if not added:
            return

        embedding = self._diarization.extract_embedding(analysis.best_channel_audio)
        all_profiles = self._profiles.load_all()
        profile_tuples = [
            (
                p.character,
                p.embedding,
                p.spatial_fingerprint,
                p.spatial_m2,
                p.spatial_sample_count,
            )
            for p in all_profiles
        ]
        ranked = self._diarization.rank_against_with_spatial(
            embedding,
            analysis.fingerprint,
            profile_tuples,
            base_weight=self._spatial_weight,
        )
        speaker = ranked[0][0] if ranked else "Unknown"

        self._seen_speakers.add(speaker)
        self._state.speaker_count = len(self._seen_speakers)

        if speaker != self._current_speaker and self._current_speaker is not None:
            self._flush()

        self._current_speaker = speaker
        self._current_text.append(added)

        for p in all_profiles:
            if p.character == speaker:
                p.update_spatial(analysis.fingerprint)
                self._profiles.save(p)
                break

    def flush(self):
        if self._current_speaker and self._current_text:
            self._flush()

    def _flush(self):
        text = " ".join(self._current_text)
        msg = ChatMessage(
            speaker=self._current_speaker,
            text=text,
            timestamp=time.time(),
        )
        self._state.messages.append(msg)
        self._current_text = []
        self._current_speaker = None
