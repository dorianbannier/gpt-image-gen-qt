#!/usr/bin/env python3
"""MCP server exposing image generation via gpt-image-2 / dall-e-3."""

import base64
import json
import os
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from openai import OpenAI

CONFIG_PATH = Path.home() / ".config" / "gpt-image-gen" / "config.json"
OUTPUT_DIR = Path.home() / "Images" / "gpt-image-gen"

mcp = FastMCP("gpt-image-gen")


def _load_api_key() -> str:
    if not CONFIG_PATH.exists():
        raise RuntimeError(
            f"No API key found. Launch the desktop app once and enter your key there."
        )
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    key = cfg.get("api_key", "").strip()
    if not key:
        raise RuntimeError("API key is empty in config. Open the desktop app to set it.")
    return key


@mcp.tool()
def generate_image(
    prompt: str,
    model: str = "gpt-image-2",
    quality: str = "auto",
    format: str = "png",
) -> str:
    """Generate an image from a text prompt using the OpenAI API.

    Args:
        prompt: Text description of the image to generate.
        model: "gpt-image-2" (default) or "dall-e-3".
        quality: For gpt-image-2: "auto" | "low" | "medium" | "high".
                 For dall-e-3: "standard" | "hd".
        format: Output format — "png" | "jpeg" | "webp" (gpt-image-2 only; dall-e-3 always returns PNG).

    Returns:
        Absolute path to the saved image file.
    """
    client = OpenAI(api_key=_load_api_key())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if model == "dall-e-3":
        valid_quality = quality if quality in ("standard", "hd") else "standard"
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            quality=valid_quality,
            response_format="b64_json",
        )
        image_data = base64.b64decode(response.data[0].b64_json)
        ext = "png"
    else:
        valid_quality = quality if quality in ("auto", "low", "medium", "high") else "auto"
        valid_format = format if format in ("png", "jpeg", "webp") else "png"
        kwargs = {
            "model": "gpt-image-2",
            "prompt": prompt,
            "n": 1,
            "output_format": valid_format,
        }
        if valid_quality != "auto":
            kwargs["quality"] = valid_quality
        response = client.images.generate(**kwargs)
        image_data = base64.b64decode(response.data[0].b64_json)
        ext = valid_format

    out_path = OUTPUT_DIR / f"{timestamp}.{ext}"
    out_path.write_bytes(image_data)
    return str(out_path)


if __name__ == "__main__":
    mcp.run()
