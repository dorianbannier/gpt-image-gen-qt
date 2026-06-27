# GPT Image Generator

A free, open-source desktop app to generate images using the **OpenAI API** (`gpt-image-2` and `dall-e-3`) — no subscription required, just your API key.

Built with PyQt6, runs on **Windows and Linux** (macOS build available but untested).

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-green?logo=qt&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--image--2%20%7C%20dall--e--3-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## What is this?

GPT Image Generator is a lightweight desktop application that lets you generate images from text prompts using [OpenAI's gpt-image-2 model](https://platform.openai.com/docs/guides/images). It provides a clean, native-feeling interface without requiring a browser or a monthly subscription — you only pay for what you generate via the OpenAI API.

**Ideal for:**
- Anyone who wants to use gpt-image-2 without the OpenAI web interface
- Designers and creatives who generate images as part of their workflow
- Developers testing prompts before integrating them into their apps
- Users who want a simple alternative to Midjourney or Adobe Firefly without creating yet another account

---

## Screenshot

![App preview](screenshots/apercu.png)

---

## Features

- **Text-to-image generation** using OpenAI `gpt-image-2` (default) or `dall-e-3`
- **Quality and format control**: adapts automatically to the selected model
  - *gpt-image-2*: auto / low / medium / high quality — PNG / JPEG / WebP
  - *dall-e-3*: standard / hd quality — PNG
- **One-click save** of the generated image
- **API key stored locally** (`~/.config/gpt-image-gen/config.json`) — never sent anywhere else
- **Bilingual**: English by default, French available via toolbar toggle
- **macOS-inspired UI**: clean light theme, native feel on any platform
- **No subscription** — pay-per-use via your OpenAI API key

---

## Installation

### Windows

Download the latest `.exe` from the [Releases](../../releases) page.

No installation required — just double-click `GPT-Image-Generator.exe`.

### macOS *(untested)*

Download `GPT-Image-Generator-macOS.zip` from the [Releases](../../releases) page, unzip it and move `GPT-Image-Generator.app` to your Applications folder.

> macOS builds are generated automatically but have not been tested on a real Mac. Feedback welcome.

### Linux

**Requirements**: Python 3.11+

```bash
git clone https://github.com/dorianbannier/gpt-image-gen-qt.git
cd gpt-image-gen-qt
./run.sh
```

`run.sh` automatically creates a virtual environment and installs dependencies on first run.

### Manual dependency install

```bash
pip install PyQt6 openai
python app.py
```

---

## Getting an OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new secret key
3. On first launch, click **API Key…** in the toolbar and paste your key

Your key is saved locally and never transmitted to anyone other than OpenAI.

---

## Generation Parameters

### gpt-image-2 (default)

| Parameter | Options | Description |
|-----------|---------|-------------|
| **Quality** | auto, low, medium, high | Speed / quality trade-off |
| **Format** | PNG, JPEG, WebP | Output file format |

### dall-e-3

| Parameter | Options | Description |
|-----------|---------|-------------|
| **Quality** | standard, hd | Standard or high definition |

---

## Why gpt-image-2?

`gpt-image-2` is OpenAI's latest image generation model. Compared to DALL-E 3, it offers:
- Better prompt adherence
- Higher quality output at lower cost
- Support for transparent backgrounds (PNG/WebP)
- Pay-per-image pricing with no monthly commitment

---

## Windows Build (developers)

The GitHub Actions workflow automatically builds a `.exe` and a macOS `.app` on every push to `main`.

To trigger manually: **Actions → Build → Run workflow**

Uses [PyInstaller](https://pyinstaller.org/) in single-file mode.

---

## MCP Server

The project includes an MCP server (`mcp_server.py`) that exposes image generation as a tool for any [MCP-compatible client](https://modelcontextprotocol.io) — Claude Code, Claude Desktop, Cursor, Zed, Continue, and others.

### Setup

**1. Install dependencies** (once):

```bash
pip install mcp openai
```

**2. Register the server** in your MCP client's config file:

```json
{
  "mcpServers": {
    "gpt-image-gen": {
      "command": "python3",
      "args": ["/absolute/path/to/gpt-image-gen-qt/mcp_server.py"]
    }
  }
}
```

Common config file locations:
- **Claude Code**: `~/.claude/settings.json`
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
- **Cursor / Zed / Continue**: see your client's MCP documentation

**3. Restart your client** — it will detect the server automatically.

> The API key is read from `~/.config/gpt-image-gen/config.json` (the same file used by the desktop app). Set it once in the app, and the MCP server picks it up with no extra configuration.

### Usage

Once connected, ask your AI assistant to generate an image:

```
Generate an image of a fox in a snowy forest, high quality
```

Generated images are saved to `~/Images/gpt-image-gen/` and the file path is returned.

### Tool parameters

| Parameter | Options | Default |
|-----------|---------|---------|
| `prompt` | Any text | *(required)* |
| `model` | `gpt-image-2`, `dall-e-3` | `gpt-image-2` |
| `quality` | gpt-image-2: `auto` `low` `medium` `high` — dall-e-3: `standard` `hd` | `auto` |
| `format` | `png`, `jpeg`, `webp` *(gpt-image-2 only)* | `png` |

---

## Tech Stack

- [PyQt6](https://pypi.org/project/PyQt6/) — cross-platform GUI framework
- [openai](https://pypi.org/project/openai/) — official OpenAI Python client
- [mcp](https://pypi.org/project/mcp/) — MCP server SDK (Claude Code integration)
- [PyInstaller](https://pyinstaller.org/) — Windows & macOS packaging
- [GitHub Actions](https://github.com/features/actions) — CI/CD

---

## Author

Made by **Dorian Bannier** — contributions and feedback welcome.

## License

MIT — free to use, modify and distribute.
