from __future__ import annotations

import os

import httpx
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))

FALLBACK_SCRIPT = (
    "Not bad, not bad at all. While we figure out the next bit, "
    "try this on for size. Imagine you are a very old wizard "
    "who has just stubbed his toe on a cauldron. "
    "Now imagine that wizard is also trying to sell you a used horse. "
    "The horse's name is Frederick and he does not like being sold. "
    "Red leather yellow leather, red leather yellow leather. "
    "See? Still going. The machine appreciates your commitment."
)

SYSTEM_PROMPT = """\
You write flowing, self-aware monologues for voice actors recording voice \
profiles for a tabletop RPG. The actor reads your text aloud into a microphone.

Your script should:
- Read like a single continuous narrative monologue, not a list
- Be meta and self-referential — the actor knows they're being recorded, \
lean into that ("still going, impressive", "the machine is learning you")
- Naturally prompt vocal range: weave in moments where the actor should \
shift to a different voice (gruff dwarf, haughty noble, panicked merchant) \
as part of the story, not as stage directions
- Embed tongue twisters and tricky phonetics INTO the narrative flow, \
not as standalone exercises
- Include "try not to laugh" moments — absurd imagery, escalating nonsense
- Be genuinely fun to read aloud — something an actor would enjoy performing
- ~65 words (about 30 seconds of speech)
- Plain prose only. No brackets, no labels, no stage directions, no lists
- Continue seamlessly from the previous chunk's tone and narrative thread
- Higher levels = harder phonetics, more absurd situations, faster pivots \
between character voices, sillier premises that dare the actor to break

The actor's name may appear in the text. Keep the voice warm and conspiratorial, \
like a game show host who's rooting for the contestant.\
"""


class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v4-flash")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self._client: httpx.AsyncClient | None = None

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=10.0,
            )
        return self._client

    async def generate_script(self, level: int, previous_chunk: str) -> str:
        if not self.available:
            return FALLBACK_SCRIPT

        client = self._get_client()
        try:
            resp = await client.post(
                "/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": (
                                f"Level {level}. Previous chunk the actor just read:\n"
                                f'"{previous_chunk}"\n\n'
                                f"Generate the next ~65 words, increasing difficulty."
                            ),
                        },
                    ],
                    "max_tokens": 200,
                    "temperature": 0.9,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return FALLBACK_SCRIPT

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
