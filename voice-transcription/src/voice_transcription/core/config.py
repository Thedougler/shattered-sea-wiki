"""LLM configuration loaded from environment variables."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_MODEL = "anthropic/claude-sonnet-4-20250514"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


@dataclass(frozen=True)
class LLMConfig:
    api_key: str | None
    model: str
    base_url: str

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)


def load_llm_config(env: dict[str, str]) -> LLMConfig:
    api_key = env.get("OPENROUTER_API_KEY") or None
    return LLMConfig(
        api_key=api_key,
        model=env.get("OPENROUTER_MODEL", DEFAULT_MODEL),
        base_url=env.get("OPENROUTER_BASE_URL", DEFAULT_BASE_URL),
    )
