from __future__ import annotations

import os

import httpx
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))

FALLBACK_SCRIPT = (
    'Peter Piper picked a peck of pickled peppers, '
    'a peck of pickled peppers Peter Piper picked. '
    'If Peter Piper picked a peck of pickled peppers, '
    "where's the peck of pickled peppers Peter Piper picked? "
    'Red leather yellow leather, red leather yellow leather. '
    'Unique New York, you know you need unique New York.'
)

SYSTEM_PROMPT = """\
You are a comedy writer generating vocal warm-up scripts for voice actors \
recording voice profiles for a D&D game. The script should be:

- Self-referential and meta (acknowledge the recording process)
- Include tongue twisters and phonetically diverse phrases
- Include "don't laugh" challenges and silly character voice prompts
- Exactly ~65 words (30 seconds at natural speaking pace)
- Plain prose only — no stage directions, no brackets, no labels
- Continue the tone and humor of the previous chunk
- Difficulty increases with level: level 2 is moderate, level 3+ gets absurd

The voice actor reads this aloud while their voice is captured. Make it fun.\
"""


class LLMService:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY', '')
        self.model = os.getenv('OPENROUTER_MODEL', 'deepseek/deepseek-v4-flash')
        self.base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self._client: httpx.AsyncClient | None = None

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                },
                timeout=10.0,
            )
        return self._client

    async def generate_script(self, level: int, previous_chunk: str) -> str:
        if not self.available:
            return FALLBACK_SCRIPT

        client = self._get_client()
        try:
            resp = await client.post('/chat/completions', json={
                'model': self.model,
                'messages': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': (
                        f'Level {level}. Previous chunk the actor just read:\n'
                        f'"{previous_chunk}"\n\n'
                        f'Generate the next ~65 words, increasing difficulty.'
                    )},
                ],
                'max_tokens': 200,
                'temperature': 0.9,
            })
            resp.raise_for_status()
            data = resp.json()
            return data['choices'][0]['message']['content'].strip()
        except Exception:
            return FALLBACK_SCRIPT

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
