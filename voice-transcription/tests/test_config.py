"""Tests for LLM config loading from environment variables."""

import unittest

from voice_transcription.core.config import LLMConfig, load_llm_config


class LoadLLMConfigTests(unittest.TestCase):
    def test_all_keys_present(self) -> None:
        env = {
            "OPENROUTER_API_KEY": "sk-or-test-key",
            "OPENROUTER_MODEL": "anthropic/claude-sonnet-4-20250514",
            "OPENROUTER_BASE_URL": "https://custom.endpoint/v1",
        }
        cfg = load_llm_config(env)
        self.assertEqual(cfg.api_key, "sk-or-test-key")
        self.assertEqual(cfg.model, "anthropic/claude-sonnet-4-20250514")
        self.assertEqual(cfg.base_url, "https://custom.endpoint/v1")
        self.assertTrue(cfg.enabled)

    def test_missing_api_key_disables(self) -> None:
        cfg = load_llm_config({})
        self.assertIsNone(cfg.api_key)
        self.assertFalse(cfg.enabled)

    def test_default_model(self) -> None:
        env = {"OPENROUTER_API_KEY": "sk-or-test-key"}
        cfg = load_llm_config(env)
        self.assertIn("claude", cfg.model.lower())

    def test_default_base_url(self) -> None:
        env = {"OPENROUTER_API_KEY": "sk-or-test-key"}
        cfg = load_llm_config(env)
        self.assertEqual(cfg.base_url, "https://openrouter.ai/api/v1")

    def test_empty_api_key_treated_as_missing(self) -> None:
        env = {"OPENROUTER_API_KEY": ""}
        cfg = load_llm_config(env)
        self.assertFalse(cfg.enabled)


if __name__ == "__main__":
    unittest.main()
