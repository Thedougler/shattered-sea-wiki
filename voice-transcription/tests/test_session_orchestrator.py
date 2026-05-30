"""Tests for SessionOrchestrator — coordinates recording, script, and LLM."""

import asyncio
import unittest

from voice_transcription.core.script_buffer import ScriptBuffer
from voice_transcription.core.script_tracker import ScriptTracker
from voice_transcription.core.session_orchestrator import SessionOrchestrator


class FakeScriptGenerator:
    def __init__(self, responses: list[str] | None = None) -> None:
        self.responses = list(responses or ["Generated paragraph one.", "Generated paragraph two."])
        self.call_count = 0

    async def generate(self, existing_script: str) -> str:
        self.call_count += 1
        if self.responses:
            return self.responses.pop(0)
        return "Fallback generated text."


class StateTransitionTests(unittest.TestCase):
    def test_initial_state_is_idle(self) -> None:
        orch = SessionOrchestrator(
            script_buffer=ScriptBuffer("hello world"),
            script_tracker=ScriptTracker("hello world"),
        )
        self.assertFalse(orch.is_recording)
        self.assertEqual(orch.status, "idle")

    def test_start_transitions_to_recording(self) -> None:
        orch = SessionOrchestrator(
            script_buffer=ScriptBuffer("hello world"),
            script_tracker=ScriptTracker("hello world"),
        )
        orch.start()
        self.assertTrue(orch.is_recording)
        self.assertEqual(orch.status, "recording")

    def test_stop_transitions_to_idle(self) -> None:
        orch = SessionOrchestrator(
            script_buffer=ScriptBuffer("hello world"),
            script_tracker=ScriptTracker("hello world"),
        )
        orch.start()
        orch.stop()
        self.assertFalse(orch.is_recording)
        self.assertEqual(orch.status, "idle")

    def test_double_start_is_safe(self) -> None:
        orch = SessionOrchestrator(
            script_buffer=ScriptBuffer("hello world"),
            script_tracker=ScriptTracker("hello world"),
        )
        orch.start()
        orch.start()
        self.assertTrue(orch.is_recording)

    def test_stop_without_start_is_safe(self) -> None:
        orch = SessionOrchestrator(
            script_buffer=ScriptBuffer("hello world"),
            script_tracker=ScriptTracker("hello world"),
        )
        orch.stop()
        self.assertFalse(orch.is_recording)


class ScriptExtensionTests(unittest.IsolatedAsyncioTestCase):
    async def test_extend_if_needed_calls_generator(self) -> None:
        seed = " ".join(f"w{i}" for i in range(50))
        buf = ScriptBuffer(seed)
        tracker = ScriptTracker(seed)
        gen = FakeScriptGenerator(["New words here."])
        orch = SessionOrchestrator(
            script_buffer=buf, script_tracker=tracker, script_generator=gen,
        )
        tracker.advance([f"w{i}" for i in range(45)])
        await orch.extend_if_needed()
        self.assertEqual(gen.call_count, 1)
        self.assertIn("New words here.", buf.full_text)

    async def test_no_extension_when_plenty_ahead(self) -> None:
        seed = " ".join(f"w{i}" for i in range(500))
        buf = ScriptBuffer(seed)
        tracker = ScriptTracker(seed)
        gen = FakeScriptGenerator()
        orch = SessionOrchestrator(
            script_buffer=buf, script_tracker=tracker, script_generator=gen,
        )
        tracker.advance(["w0"])
        await orch.extend_if_needed()
        self.assertEqual(gen.call_count, 0)

    async def test_no_extension_without_generator(self) -> None:
        seed = "one two"
        buf = ScriptBuffer(seed)
        tracker = ScriptTracker(seed)
        orch = SessionOrchestrator(
            script_buffer=buf, script_tracker=tracker,
        )
        tracker.advance(["one", "two"])
        await orch.extend_if_needed()
        self.assertEqual(buf.token_count, 2)

    async def test_extension_updates_tracker(self) -> None:
        seed = " ".join(f"w{i}" for i in range(50))
        buf = ScriptBuffer(seed)
        tracker = ScriptTracker(seed)
        gen = FakeScriptGenerator(["alpha beta gamma"])
        orch = SessionOrchestrator(
            script_buffer=buf, script_tracker=tracker, script_generator=gen,
        )
        tracker.advance([f"w{i}" for i in range(45)])
        await orch.extend_if_needed()
        state = tracker.advance(["alpha"])
        self.assertEqual(state.matched_up_to, 50)


class SnapshotTests(unittest.TestCase):
    def test_snapshot_returns_current_state(self) -> None:
        buf = ScriptBuffer("one two three")
        tracker = ScriptTracker("one two three")
        orch = SessionOrchestrator(script_buffer=buf, script_tracker=tracker)
        tracker.advance(["one"])
        snap = orch.snapshot()
        self.assertEqual(snap["matched_up_to"], 0)
        self.assertEqual(snap["total_tokens"], 3)
        self.assertEqual(snap["status"], "idle")
        self.assertIn("one two three", snap["full_text"])


if __name__ == "__main__":
    unittest.main()
