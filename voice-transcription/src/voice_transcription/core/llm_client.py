"""OpenRouter / OpenAI-compatible LLM client for script generation."""

from __future__ import annotations

from typing import Protocol

import httpx

from .config import LLMConfig

SYSTEM_PROMPT = """\
You are a teleprompter script writer for voice-acting sessions. Generate \
phonetically rich, varied text that exercises the full range of the human voice: \
plosives, fricatives, sibilants, nasals, and vowels. Mix tones — whispers, \
shouts, conversational, dramatic. Include tongue twisters, emotional shifts, \
and varied sentence lengths.

Continue naturally from the existing script. Do NOT repeat or summarize what \
came before. Write 3-5 new paragraphs (~200 words). Output ONLY the new text — \
no commentary, no labels, no markdown headers."""

TAIL_TOKENS = 100


class ScriptGenerationError(Exception):
    pass


class ScriptGenerator(Protocol):
    async def generate(self, existing_script: str) -> str: ...


def build_prompt(existing_script: str) -> list[dict[str, str]]:
    tail_words = existing_script.split()[-TAIL_TOKENS:]
    tail = " ".join(tail_words)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Continue from:\n\n{tail}"},
    ]


class OpenRouterClient:
    def __init__(self, config: LLMConfig) -> None:
        self._config = config

    async def generate(self, existing_script: str) -> str:
        messages = build_prompt(existing_script)
        url = f"{self._config.base_url}/chat/completions"
        payload = {
            "model": self._config.model,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.9,
        }
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }
        try:
            async with httpx.AsyncClient() as http:
                resp = await http.post(url, json=payload, headers=headers, timeout=30.0)
                resp.raise_for_status()
                data = resp.json()
        except ScriptGenerationError:
            raise
        except Exception as exc:
            raise ScriptGenerationError(f"LLM request failed: {exc}") from exc

        choices = data.get("choices", [])
        if not choices:
            raise ScriptGenerationError("LLM returned no choices")
        return choices[0]["message"]["content"].strip()
