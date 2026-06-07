# openai-plugin-downloader

CLI tool to discover and download ChatGPT/OpenAI plugin repos from GitHub by topic search.

## Overview

Searches GitHub for repositories tagged with `chatgpt-plugin`, lists them by stars, and downloads any as zip archives for offline use.

## Prerequisites

- Python 3.10+
- A GitHub account (optional — unauthenticated requests are rate-limited to 10/min)

## Installation

```bash
git clone https://github.com/patilanirudh/Generated_projects
cd Generated_projects/openai-plugin-downloader
pip install -r requirements.txt
```

## Configuration

| Variable | Description | Required |
|---|---|---|
| `GITHUB_TOKEN` | Personal access token for higher rate limits (60 req/min vs 10) | No |
| `OUTPUT_DIR` | Default download directory (default: `./plugins`) | No |

## Usage

**List plugins:**
```bash
python app.py list
python app.py list --query weather --limit 10
```

**Download plugins:**
```bash
python app.py download
python app.py download --query weather --limit 3 --output ./my-plugins
```

**With GitHub token (recommended):**
```bash
GITHUB_TOKEN=ghp_... python app.py list
```

**Sample output:**
```
Plugin                                                        Stars  Language
-------------------------------------------------------------------------------------
taranjeet/zapier-chatgpt-plugin                                 892  Python
  Zapier ChatGPT Plugin
transitive-bullshit/chatgpt-plugin-ts                           541  TypeScript
```

## License

MIT
