#!/usr/bin/env python3
"""Generate images via OpenRouter's chat completions API.

Reads OPENROUTER_API_KEY (required) and OPENROUTER_IMAGE_MODEL (optional)
from .env or environment. Accepts a prompt, saves the image, prints the path.

Usage:
    python3 generate-image.py "a dragon perched on a lighthouse at sunset"
    python3 generate-image.py "portrait of an elven ranger" --output ranger.png
    python3 generate-image.py "fantasy archipelago map" --aspect 16:9 --image-size 2K
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = "google/gemini-2.5-flash-image"
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_env():
    """Load variables from .env files. Does not overwrite existing env vars."""
    for env_path in [Path.cwd() / ".env", Path.home() / ".env"]:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    if key and key not in os.environ:
                        os.environ[key] = value


def extract_image_bytes(result):
    """Extract image bytes from the chat completions response.

    OpenRouter returns images in choices[0].message.images[] as base64 data URLs,
    or sometimes inline in content as markdown image tags with data URIs.
    """
    choices = result.get("choices", [])
    if not choices:
        return None, None

    message = choices[0].get("message", {})

    # Primary path: images array
    images = message.get("images", [])
    if images:
        url = images[0].get("image_url", {}).get("url", "")
        return _decode_data_url(url)

    # Fallback: look for inline_data in content parts
    content = message.get("content")
    if isinstance(content, list):
        for part in content:
            if part.get("type") == "image" or part.get("type") == "image_url":
                url = part.get("image_url", {}).get("url", "")
                if url:
                    return _decode_data_url(url)
            if part.get("type") == "inline_data":
                data = part.get("data", "")
                mime = part.get("mime_type", "image/png")
                if data:
                    return base64.b64decode(data), _ext_from_mime(mime)
    elif isinstance(content, str):
        # Check for data URI in markdown image syntax
        match = re.search(r"data:(image/[^;]+);base64,([A-Za-z0-9+/=]+)", content)
        if match:
            mime = match.group(1)
            return base64.b64decode(match.group(2)), _ext_from_mime(mime)

    return None, None


def _decode_data_url(url):
    """Decode a data:image/...;base64,... URL into bytes and extension."""
    if not url:
        return None, None
    match = re.match(r"data:(image/[^;]+);base64,(.+)", url, re.DOTALL)
    if match:
        mime = match.group(1)
        return base64.b64decode(match.group(2)), _ext_from_mime(mime)
    # If it's a regular URL, download it
    if url.startswith("http"):
        data = urllib.request.urlopen(url, timeout=60).read()
        ext = ".png"
        if ".jpg" in url or ".jpeg" in url:
            ext = ".jpg"
        elif ".webp" in url:
            ext = ".webp"
        return data, ext
    return None, None


def _ext_from_mime(mime):
    """Map MIME type to file extension."""
    mapping = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }
    return mapping.get(mime, ".png")


def _make_request(body, api_key):
    """Send a request to OpenRouter and return the parsed JSON response."""
    payload = json.dumps(body).encode()
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/anthropics/claude-code",
            "X-Title": "Claude Code Image Gen",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read())


def generate_image(prompt, *, model=None, aspect=None, image_size=None, output=None):
    """Call OpenRouter chat completions with image modality and save the result."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print(
            "Error: OPENROUTER_API_KEY not set.\n"
            "Add it to ~/.env or project .env:\n"
            "  OPENROUTER_API_KEY=sk-or-v1-...",
            file=sys.stderr,
        )
        sys.exit(1)

    model = model or os.environ.get("OPENROUTER_IMAGE_MODEL", DEFAULT_MODEL)

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
    }

    image_config = {}
    aspect = aspect or os.environ.get("OPENROUTER_IMAGE_ASPECT")
    image_size = image_size or os.environ.get("OPENROUTER_IMAGE_SIZE")
    if aspect:
        image_config["aspect_ratio"] = aspect
    if image_size:
        image_config["image_size"] = image_size
    if image_config:
        body["image_config"] = image_config

    print(f"Generating with {model}...", file=sys.stderr)

    try:
        result = _make_request(body, api_key)
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        # Image-only models (e.g. Grok Imagine) don't support text output —
        # retry with image-only modality
        if "modalities" in body_text.lower() and "text" in body.get("modalities", []):
            print(
                "Model is image-only, retrying without text modality...",
                file=sys.stderr,
            )
            body["modalities"] = ["image"]
            try:
                result = _make_request(body, api_key)
            except urllib.error.HTTPError as e2:
                body_text2 = e2.read().decode(errors="replace")
                try:
                    msg = (
                        json.loads(body_text2)
                        .get("error", {})
                        .get("message", body_text2)
                    )
                except json.JSONDecodeError:
                    msg = body_text2[:500]
                print(f"API error {e2.code}: {msg}", file=sys.stderr)
                sys.exit(1)
        else:
            try:
                msg = json.loads(body_text).get("error", {}).get("message", body_text)
            except json.JSONDecodeError:
                msg = body_text[:500]
            print(f"API error {e.code}: {msg}", file=sys.stderr)
            sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    img_bytes, ext = extract_image_bytes(result)
    if not img_bytes:
        # Dump the response structure for debugging
        print("Error: Could not extract image from response", file=sys.stderr)
        # Show structure without huge base64 blobs
        debug = json.dumps(result, indent=2)
        if len(debug) > 2000:
            debug = debug[:2000] + "\n... (truncated)"
        print(debug, file=sys.stderr)
        sys.exit(1)

    if not output:
        output = Path.cwd() / f"generated-image{ext}"
    else:
        output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(img_bytes)

    # Log any text content the model returned alongside the image
    choices = result.get("choices", [])
    if choices:
        content = choices[0].get("message", {}).get("content")
        if (
            isinstance(content, str)
            and content.strip()
            and not content.startswith("data:")
        ):
            # Strip out any inline data URIs for logging
            text_only = re.sub(r"!\[.*?\]\(data:image/[^)]+\)", "", content).strip()
            if text_only:
                print(f"Model note: {text_only}", file=sys.stderr)

    print(str(output.resolve()))


def main():
    parser = argparse.ArgumentParser(
        description="Generate images via OpenRouter API (chat completions with image modality)",
        epilog="Env vars: OPENROUTER_API_KEY (required), OPENROUTER_IMAGE_MODEL, OPENROUTER_IMAGE_ASPECT, OPENROUTER_IMAGE_SIZE",
    )
    parser.add_argument("prompt", help="Text prompt describing the image to generate")
    parser.add_argument(
        "--model",
        "-m",
        help=f"Model ID (default: $OPENROUTER_IMAGE_MODEL or {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--aspect",
        "-a",
        help="Aspect ratio, e.g. 1:1, 16:9, 4:3 (default: model default)",
    )
    parser.add_argument(
        "--image-size",
        "-s",
        help="Image size: 0.5K, 1K, 2K, 4K (default: model default)",
    )
    parser.add_argument(
        "--output", "-o", help="Output file path (default: ./generated-image.png)"
    )
    args = parser.parse_args()

    load_env()
    generate_image(
        args.prompt,
        model=args.model,
        aspect=args.aspect,
        image_size=args.image_size,
        output=args.output,
    )


if __name__ == "__main__":
    main()
