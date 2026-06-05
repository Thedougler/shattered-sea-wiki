export const prerender = false;

import type { APIRoute } from 'astro';

const CHARACTER_SYSTEM = `You are a comedy writer generating teleprompter scripts for voice actors recording D&D character voices. Your scripts should be:

- Hilarious and entertaining — cheesy fantasy infomercials, dramatic tavern monologues, old-timey radio ads, overwrought proclamations, absurd fantasy product pitches
- Personalized to the character (use their name, reference their class/species/personality)
- Varied in emotion and pacing — mix dramatic gravitas with absurd comedy, whispered asides with booming declarations
- Full of vocal range opportunities — questions, exclamations, whispers, laughs, dramatic pauses
- Written as continuous prose the actor reads aloud (no stage directions, no brackets, no labels)
- About 500 words per chunk

The actor should feel like they're having fun, not doing homework. Think: if a fantasy radio station existed, these would be the ads between dragon weather reports.`;

const NORMAL_SYSTEM = `You are a comedy writer generating teleprompter scripts for someone recording their NORMAL speaking voice (not a character). The goal is to capture their natural voice, so the script should make them speak casually and naturally. Your scripts should be:

- Casual and conversational — behind-the-scenes DVD commentary vibes, podcast warmup banter, "talking to a friend" energy
- Meta and self-aware about the absurdity of reading a script to sound natural
- Funny in a low-key way — dry observations, silly tangents, gentle fourth-wall breaks about being a voice actor for a D&D campaign
- Include casual conversation prompts — "describe your lunch today", "rank the party members by who'd survive a zombie apocalypse", "what's the worst snack someone brought to a session"
- Written as continuous prose (no stage directions, no brackets)
- About 500 words per chunk

The speaker should forget they're being recorded. Make it feel like chatting, not performing.`;

export const POST: APIRoute = async ({ request }) => {
  const apiKey = import.meta.env.OPENROUTER_API_KEY || process.env.OPENROUTER_API_KEY;
  const model = import.meta.env.OPENROUTER_MODEL || process.env.OPENROUTER_MODEL || 'deepseek/deepseek-v4-flash';
  const baseUrl = import.meta.env.OPENROUTER_BASE_URL || process.env.OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1';

  if (!apiKey) {
    return new Response(JSON.stringify({ error: 'OpenRouter API key not configured' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  let body: { character: string; summary: string; mode: string; previousContext?: string };
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { character, summary, mode, previousContext } = body;
  if (!character || !mode) {
    return new Response(JSON.stringify({ error: 'Missing character or mode' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const systemPrompt = mode === 'character' ? CHARACTER_SYSTEM : NORMAL_SYSTEM;
  const userPrompt = previousContext
    ? `Character: ${character}\nBackground: ${summary || 'A mysterious adventurer'}\n\nContinue the script naturally from where we left off. The last bit was: "${previousContext}"\n\nWrite the next chunk — keep the energy going, vary the tone, and surprise the reader.`
    : `Character: ${character}\nBackground: ${summary || 'A mysterious adventurer'}\n\nWrite the opening chunk of the teleprompter script. Start strong — hook the reader immediately with something funny and engaging. Set the tone for a wild ride.`;

  try {
    const res = await fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userPrompt },
        ],
        max_tokens: 1024,
        temperature: 0.9,
      }),
    });

    if (!res.ok) {
      const err = await res.text();
      return new Response(JSON.stringify({ error: `OpenRouter error: ${res.status}`, detail: err }), {
        status: 502,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const data = await res.json();
    const script = data.choices?.[0]?.message?.content ?? '';

    return new Response(JSON.stringify({ script }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    return new Response(JSON.stringify({ error: message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
