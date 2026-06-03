#!/usr/bin/env python3
"""Edit images via OpenRouter's chat completions API.

Sends an input image with an editing instruction to a vision-capable model
that supports image output. Saves the result without overwriting the original.

Usage:
    python3 edit-image.py input.png "add a glowing aura around the character's hands"
    python3 edit-image.py portrait.png "change the background to a stormy sea" --output portrait-stormy.png
    python3 edit-image.py scene.jpg "make the lighting warmer, golden hour" --model google/gemini-3-pro-image-preview
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = "google/gemini-2.5-flash-image"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SUPPORTED_MIMES = {"image/png", "image/jpeg", "image/webp", "image/gif"}


def load_env():
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
    choices = result.get("choices", [])
    if not choices:
        return None, None

    message = choices[0].get("message", {})

    images = message.get("images", [])
    if images:
        url = images[0].get("image_url", {}).get("url", "")
        return _decode_data_url(url)

    content = message.get("content")
    if isinstance(content, list):
        for part in content:
            if part.get("type") in ("image", "image_url"):
                url = part.get("image_url", {}).get("url", "")
                if url:
                    return _decode_data_url(url)
            if part.get("type") == "inline_data":
                data = part.get("data", "")
                mime = part.get("mime_type", "image/png")
                if data:
                    return base64.b64decode(data), _ext_from_mime(mime)
    elif isinstance(content, str):
        match = re.search(r"data:(image/[^;]+);base64,([A-Za-z0-9+/=]+)", content)
        if match:
            mime = match.group(1)
            return base64.b64decode(match.group(2)), _ext_from_mime(mime)

    return None, None


def _decode_data_url(url):
    if not url:
        return None, None
    match = re.match(r"data:(image/[^;]+);base64,(.+)", url, re.DOTALL)
    if match:
        mime = match.group(1)
        return base64.b64decode(match.group(2)), _ext_from_mime(mime)
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
    return {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }.get(mime, ".png")


def _mime_from_path(path):
    mime, _ = mimetypes.guess_type(str(path))
    if mime and mime in SUPPORTED_MIMES:
        return mime
    ext = path.suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/png")


def _make_request(body, api_key):
    payload = json.dumps(body).encode()
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/anthropics/claude-code",
            "X-Title": "Claude Code Image Edit",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read())


def edit_image(
    input_path,
    prompt,
    *,
    model=None,
    aspect=None,
    image_size=None,
    output=None,
    replace=False,
):
    input_path = Path(input_path).resolve()
    if not input_path.exists():
        print(f"Error: Input image not found: {input_path}", file=sys.stderr)
        sys.exit(1)

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

    mime = _mime_from_path(input_path)
    img_data = input_path.read_bytes()
    b64 = base64.b64encode(img_data).decode("utf-8")
    data_url = f"data:{mime};base64,{b64}"

    size_mb = len(img_data) / (1024 * 1024)
    if size_mb > 10:
        print(
            f"Warning: Input image is {size_mb:.1f} MB. Large images increase cost and may timeout.",
            file=sys.stderr,
        )

    body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url},
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
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

    print(f"Editing with {model}...", file=sys.stderr)

    try:
        result = _make_request(body, api_key)
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
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
        print("Error: Could not extract image from response", file=sys.stderr)
        debug = json.dumps(result, indent=2)
        if len(debug) > 2000:
            debug = debug[:2000] + "\n... (truncated)"
        print(debug, file=sys.stderr)
        sys.exit(1)

    if replace:
        out_path = input_path
    elif output:
        out_path = Path(output)
    else:
        out_path = input_path.parent / f"{input_path.stem}-edited{ext}"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(img_bytes)

    choices = result.get("choices", [])
    if choices:
        content = choices[0].get("message", {}).get("content")
        if (
            isinstance(content, str)
            and content.strip()
            and not content.startswith("data:")
        ):
            text_only = re.sub(r"!\[.*?\]\(data:image/[^)]+\)", "", content).strip()
            if text_only:
                print(f"Model note: {text_only}", file=sys.stderr)

    print(str(out_path.resolve()))


def main():
    parser = argparse.ArgumentParser(
        description="Edit images via OpenRouter API (sends input image + prompt, returns edited image)",
        epilog="Env vars: OPENROUTER_API_KEY (required), OPENROUTER_IMAGE_MODEL, OPENROUTER_IMAGE_ASPECT, OPENROUTER_IMAGE_SIZE",
    )
    parser.add_argument("input", help="Path to the source image to edit")
    parser.add_argument("prompt", help="Editing instruction describing what to change")
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
        "--output",
        "-o",
        help="Output file path (default: {input_stem}-edited.{ext})",
    )
    parser.add_argument(
        "--replace",
        "-r",
        action="store_true",
        help="Overwrite the input file with the edited result",
    )
    args = parser.parse_args()

    load_env()
    edit_image(
        args.input,
        args.prompt,
        model=args.model,
        aspect=args.aspect,
        image_size=args.image_size,
        output=args.output,
        replace=args.replace,
    )


if __name__ == "__main__":
    main()
