"""Tests for the OpenRouter LLM client."""

import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from voice_transcription.core.config import LLMConfig
from voice_transcription.core.llm_client import (
    OpenRouterClient,
    ScriptGenerationError,
    build_prompt,
)


class BuildPromptTests(unittest.TestCase):
    def test_includes_existing_script_tail(self) -> None:
        msgs = build_prompt("one two three four five six seven eight nine ten")
        user_msg = msgs[-1]["content"]
        self.assertIn("ten", user_msg)

    def test_system_prompt_describes_teleprompter(self) -> None:
        msgs = build_prompt("some script")
        system_msg = msgs[0]["content"]
        self.assertIn("phonetic", system_msg.lower())

    def test_messages_structure(self) -> None:
        msgs = build_prompt("hello")
        self.assertEqual(msgs[0]["role"], "system")
        self.assertEqual(msgs[-1]["role"], "user")


class OpenRouterClientTests(unittest.IsolatedAsyncioTestCase):
    def _cfg(self, **overrides) -> LLMConfig:
        defaults = dict(
            api_key="sk-test",
            model="test-model",
            base_url="https://test.api/v1",
        )
        defaults.update(overrides)
        return LLMConfig(**defaults)

    def _mock_http(self, response):
        mock_instance = AsyncMock()
        mock_instance.post.return_value = response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=False)
        return mock_instance

    def _ok_response(self, content: str) -> MagicMock:
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "choices": [{"message": {"content": content}}]
        }
        resp.raise_for_status = MagicMock()
        return resp

    async def test_sends_correct_request(self) -> None:
        resp = self._ok_response("New generated text here.")
        with patch("httpx.AsyncClient") as MockClient:
            mock_http = self._mock_http(resp)
            MockClient.return_value = mock_http

            client = OpenRouterClient(self._cfg())
            result = await client.generate("existing script text")

            self.assertEqual(result, "New generated text here.")
            call_args = mock_http.post.call_args
            self.assertIn("/chat/completions", call_args[0][0])
            payload = call_args[1]["json"]
            self.assertEqual(payload["model"], "test-model")

    async def test_raises_on_error_response(self) -> None:
        resp = MagicMock()
        resp.raise_for_status.side_effect = Exception("500 error")

        with patch("httpx.AsyncClient") as MockClient:
            MockClient.return_value = self._mock_http(resp)

            client = OpenRouterClient(self._cfg())
            with self.assertRaises(ScriptGenerationError):
                await client.generate("existing script")

    async def test_raises_on_empty_choices(self) -> None:
        resp = MagicMock()
        resp.json.return_value = {"choices": []}
        resp.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as MockClient:
            MockClient.return_value = self._mock_http(resp)

            client = OpenRouterClient(self._cfg())
            with self.assertRaises(ScriptGenerationError):
                await client.generate("existing script")


if __name__ == "__main__":
    unittest.main()
