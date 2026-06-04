"""Multi-microphone audio capture with device watchdog and graceful fallback."""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import AsyncIterator

import numpy as np

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000
BLOCK_SIZE = 1600  # 100ms at 16kHz
RING_BUFFER_SECONDS = 60
WATCHDOG_INTERVAL = 5.0


@dataclass
class AudioFrame:
    mic_id: str
    timestamp: float
    samples: np.ndarray  # float32 mono, 16kHz


@dataclass
class MicDevice:
    device_id: int
    name: str
    mic_id: str
    channels: int
    active: bool = True
    stream: object | None = field(default=None, repr=False)
    ring_buffer: np.ndarray | None = field(default=None, repr=False)
    write_pos: int = 0


def list_devices() -> list[dict]:
    """List all available input audio devices."""
    import sounddevice as sd

    devices = sd.query_devices()
    inputs = []
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            inputs.append(
                {
                    "id": i,
                    "name": dev["name"],
                    "channels": dev["max_input_channels"],
                    "sample_rate": dev["default_samplerate"],
                    "is_default": i == sd.default.device[0],
                }
            )
    return inputs


def find_devices_by_names(names: list[str]) -> list[dict]:
    """Find input devices matching a list of name substrings (case-insensitive)."""
    all_devs = list_devices()
    matched = []
    for name in names:
        name_lower = name.lower()
        for dev in all_devs:
            if name_lower in dev["name"].lower() and dev not in matched:
                matched.append(dev)
                break
    return matched


class MultiMicCapture:
    """Captures audio from multiple microphones concurrently."""

    def __init__(
        self,
        device_names: list[str] | None = None,
        sample_rate: int = SAMPLE_RATE,
        block_size: int = BLOCK_SIZE,
    ):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self._device_names = device_names
        self._mics: dict[str, MicDevice] = {}
        self._frame_queue: asyncio.Queue[AudioFrame] = asyncio.Queue()
        self._running = False
        self._session_start: float = 0.0
        self._watchdog_task: asyncio.Task | None = None

    @property
    def active_mics(self) -> list[str]:
        return [m.mic_id for m in self._mics.values() if m.active]

    @property
    def mic_names(self) -> dict[str, str]:
        return {m.mic_id: m.name for m in self._mics.values()}

    def _discover_devices(self) -> list[dict]:
        if self._device_names:
            devs = find_devices_by_names(self._device_names)
            if devs:
                return devs
            logger.warning("No configured mics found, falling back to default")

        all_devs = list_devices()
        default = [d for d in all_devs if d["is_default"]]
        return default if default else all_devs[:1]

    def _open_mic(self, dev: dict, mic_id: str) -> MicDevice:
        import sounddevice as sd

        mic = MicDevice(
            device_id=dev["id"],
            name=dev["name"],
            mic_id=mic_id,
            channels=dev["channels"],
            ring_buffer=np.zeros(self.sample_rate * RING_BUFFER_SECONDS, dtype=np.float32),
        )

        def callback(indata, frames, time_info, status):
            if status:
                logger.debug("Audio status on %s: %s", mic_id, status)
            mono = indata[:, 0].astype(np.float32) if indata.shape[1] > 1 else indata[:, 0]
            buf = mic.ring_buffer
            end = mic.write_pos + len(mono)
            if end <= len(buf):
                buf[mic.write_pos : end] = mono
            else:
                first = len(buf) - mic.write_pos
                buf[mic.write_pos :] = mono[:first]
                buf[: len(mono) - first] = mono[first:]
            mic.write_pos = end % len(buf)

            if self._running:
                frame = AudioFrame(
                    mic_id=mic_id,
                    timestamp=time.monotonic() - self._session_start,
                    samples=mono.copy(),
                )
                try:
                    self._frame_queue.put_nowait(frame)
                except asyncio.QueueFull:
                    pass

        stream = sd.InputStream(
            device=dev["id"],
            samplerate=self.sample_rate,
            channels=1,  # capture mono per mic
            blocksize=self.block_size,
            dtype="float32",
            callback=callback,
        )
        mic.stream = stream
        return mic

    async def start(self) -> list[str]:
        """Start capturing from all available mics. Returns list of active mic IDs."""
        devices = self._discover_devices()
        if not devices:
            raise RuntimeError("No audio input devices found")

        self._session_start = time.monotonic()
        self._running = True

        for i, dev in enumerate(devices):
            mic_id = f"mic_{i}"
            try:
                mic = self._open_mic(dev, mic_id)
                mic.stream.start()
                self._mics[mic_id] = mic
                logger.info("Opened mic %s: %s", mic_id, dev["name"])
            except Exception:
                logger.exception("Failed to open %s", dev["name"])

        if not self._mics:
            raise RuntimeError("Failed to open any audio input device")

        self._watchdog_task = asyncio.create_task(self._device_watchdog())
        return self.active_mics

    async def stop(self):
        """Stop all mic streams and the watchdog."""
        self._running = False
        if self._watchdog_task:
            self._watchdog_task.cancel()
            try:
                await self._watchdog_task
            except asyncio.CancelledError:
                pass

        for mic in self._mics.values():
            if mic.stream:
                try:
                    mic.stream.stop()
                    mic.stream.close()
                except Exception:
                    logger.exception("Error closing %s", mic.mic_id)
        self._mics.clear()

    async def frames(self) -> AsyncIterator[AudioFrame]:
        """Yield audio frames as they arrive from any mic."""
        while self._running:
            try:
                frame = await asyncio.wait_for(self._frame_queue.get(), timeout=1.0)
                yield frame
            except asyncio.TimeoutError:
                if not self.active_mics:
                    logger.warning("All mics disconnected, waiting for reconnect...")
                    await asyncio.sleep(WATCHDOG_INTERVAL)

    def get_ring_audio(self, mic_id: str, seconds: float) -> np.ndarray | None:
        """Get the last N seconds of audio from a mic's ring buffer."""
        mic = self._mics.get(mic_id)
        if not mic or mic.ring_buffer is None:
            return None
        n_samples = int(seconds * self.sample_rate)
        n_samples = min(n_samples, len(mic.ring_buffer))
        start = (mic.write_pos - n_samples) % len(mic.ring_buffer)
        if start < mic.write_pos:
            return mic.ring_buffer[start : mic.write_pos].copy()
        return np.concatenate([mic.ring_buffer[start:], mic.ring_buffer[: mic.write_pos]])

    async def _device_watchdog(self):
        """Periodically check for disconnected/reconnected mics."""
        while self._running:
            await asyncio.sleep(WATCHDOG_INTERVAL)
            try:
                import sounddevice as sd

                current_devices = sd.query_devices()
                current_ids = {
                    i for i, d in enumerate(current_devices) if d["max_input_channels"] > 0
                }

                for mic in self._mics.values():
                    was_active = mic.active
                    mic.active = mic.device_id in current_ids

                    if was_active and not mic.active:
                        logger.warning("Mic disconnected: %s (%s)", mic.mic_id, mic.name)
                        try:
                            mic.stream.stop()
                        except Exception:
                            pass

                    if not was_active and mic.active:
                        logger.info("Mic reconnected: %s (%s)", mic.mic_id, mic.name)
                        try:
                            dev_info = {
                                "id": mic.device_id,
                                "name": mic.name,
                                "channels": mic.channels,
                            }
                            new_mic = self._open_mic(dev_info, mic.mic_id)
                            mic.stream = new_mic.stream
                            mic.stream.start()
                        except Exception:
                            logger.exception("Failed to reopen %s", mic.name)
                            mic.active = False

            except Exception:
                logger.debug("Watchdog poll failed", exc_info=True)
