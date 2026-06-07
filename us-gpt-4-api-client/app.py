"""
groq-chat-client — CLI client for Groq-hosted LLMs with streaming,
multi-turn conversation history, and retry on rate limits.
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

from pathlib import Path

from dotenv import load_dotenv
from groq import Groq, APIConnectionError, APIError, RateLimitError

# Load from the shared project .env — walk up 4 levels to trail/, then Ai_job/.env
_ENV_PATH = Path(__file__).resolve().parents[4] / "Ai_job" / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

HISTORY_PATH = Path.home() / ".local" / "share" / "groq-client" / "history.json"
MAX_HISTORY_TURNS = 20
DEFAULT_MODEL = "llama-3.3-70b-versatile"
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
    "deepseek-r1-distill-llama-70b",
]

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "WARNING"),
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)


def _load_history() -> list[dict]:
    if HISTORY_PATH.exists():
        try:
            return json.loads(HISTORY_PATH.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Could not read history: %s", exc)
    return []


def _save_history(messages: list[dict]) -> None:
    try:
        HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        trimmed = messages[-(MAX_HISTORY_TURNS * 2):]
        HISTORY_PATH.write_text(json.dumps(trimmed, indent=2))
    except OSError as exc:
        log.warning("Could not save history: %s", exc)


def _send_with_retry(
    client: Groq,
    messages: list[dict],
    model: str,
    max_tokens: int,
    stream: bool,
) -> str:
    for attempt in range(3):
        try:
            if stream:
                collected: list[str] = []
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    stream=True,
                )
                for chunk in response:
                    text = chunk.choices[0].delta.content or ""
                    print(text, end="", flush=True)
                    collected.append(text)
                print()
                return "".join(collected)
            else:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content or ""

        except RateLimitError:
            if attempt == 2:
                raise
            wait = 2 ** (attempt + 1)
            log.warning("Rate limited — retrying in %ds", wait)
            time.sleep(wait)
        except APIConnectionError as exc:
            log.error("Connection error: %s", exc)
            sys.exit(1)
        except APIError as exc:
            log.error("API error: %s", exc)
            sys.exit(1)
    return ""


def run_interactive(
    client: Groq,
    model: str,
    max_tokens: int,
    system: str,
    stream: bool,
    no_history: bool,
) -> None:
    messages: list[dict] = [] if no_history else _load_history()
    if system:
        messages = [m for m in messages if m["role"] != "system"]
        messages.insert(0, {"role": "system", "content": system})

    print(f"Groq client [{model}] — 'exit' to quit, 'clear' to reset history")
    print("-" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break
        if user_input.lower() == "clear":
            messages = [m for m in messages if m.get("role") == "system"]
            print("History cleared.")
            continue

        messages.append({"role": "user", "content": user_input})
        print("\nAssistant: ", end="", flush=True)

        try:
            reply = _send_with_retry(client, messages, model, max_tokens, stream)
        except RateLimitError:
            print("\nRate limit exceeded. Try again later.", file=sys.stderr)
            messages.pop()
            continue

        messages.append({"role": "assistant", "content": reply})
        if not no_history:
            _save_history(messages)


def run_single(
    client: Groq,
    prompt: str,
    model: str,
    max_tokens: int,
    system: str,
    stream: bool,
    fmt: str,
) -> None:
    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    if stream and fmt == "text":
        _send_with_retry(client, messages, model, max_tokens, stream=True)
    else:
        reply = _send_with_retry(client, messages, model, max_tokens, stream=False)
        if fmt == "json":
            print(json.dumps({"model": model, "prompt": prompt, "response": reply}))
        else:
            print(reply)


def main() -> int:
    parser = argparse.ArgumentParser(description="CLI client for Groq LLMs.")
    parser.add_argument("prompt", nargs="?",
                        help="Single prompt. Omit for interactive mode.")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
                        choices=AVAILABLE_MODELS,
                        help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--max-tokens", type=int, default=2048,
                        help="Max tokens in response (default: 2048)")
    parser.add_argument("--system", default="",
                        help="System prompt")
    parser.add_argument("--no-stream", action="store_true",
                        help="Disable streaming output")
    parser.add_argument("--no-history", action="store_true",
                        help="Do not load or save conversation history")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format for single-prompt mode")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get a free key at https://console.groq.com/keys", file=sys.stderr)
        return 1

    client = Groq(api_key=api_key)

    if args.prompt:
        run_single(client, args.prompt, args.model, args.max_tokens,
                   args.system, not args.no_stream, args.format)
    else:
        run_interactive(client, args.model, args.max_tokens,
                        args.system, not args.no_stream, args.no_history)
    return 0


if __name__ == "__main__":
    sys.exit(main())
