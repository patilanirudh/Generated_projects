"""
typewriter_tool — animate any text to the terminal with a typewriter effect.

Reads from a file or stdin, prints each character with a configurable delay.
Useful for demos, presentations, and README walkthroughs.
"""

import argparse
import logging
import os
import sys
import time
from typing import TextIO

DEFAULT_SPEED = 40.0   # characters per second
NEWLINE_PAUSE = 0.20   # extra pause (seconds) after each newline

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "WARNING"),
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)


def typewrite(
    text: str,
    speed: float = DEFAULT_SPEED,
    newline_pause: float = NEWLINE_PAUSE,
    out: TextIO = sys.stdout,
) -> None:
    """Write *text* to *out* one character at a time with a timed delay."""
    char_interval = 1.0 / speed if speed > 0 else 0.0

    for ch in text:
        out.write(ch)
        out.flush()
        if ch == "\n" and newline_pause > 0:
            time.sleep(newline_pause)
        elif char_interval > 0:
            time.sleep(char_interval)

    if text and not text.endswith("\n"):
        out.write("\n")
        out.flush()


def read_input(path: str | None) -> str:
    """Read text from *path*, or from stdin if *path* is None or '-'."""
    if path and path != "-":
        try:
            with open(path, encoding="utf-8") as fh:
                return fh.read()
        except OSError as exc:
            log.error("Cannot read file '%s': %s", path, exc)
            sys.exit(1)
    if sys.stdin.isatty():
        log.warning("Reading from stdin — type your text and press Ctrl+D when done.")
    return sys.stdin.read()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print text to the terminal with a typewriter animation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  echo 'Hello, world!' | python app.py\n"
            "  python app.py --speed 80 myfile.txt\n"
            "  python app.py --speed 0 myfile.txt   # instant output\n"
        ),
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="File to animate. Reads from stdin if omitted or '-'.",
    )
    parser.add_argument(
        "-s", "--speed",
        type=float,
        default=DEFAULT_SPEED,
        metavar="CPS",
        help=f"Characters per second (default: {DEFAULT_SPEED}). Use 0 for instant.",
    )
    parser.add_argument(
        "--no-newline-pause",
        action="store_true",
        help="Disable the extra pause inserted after newlines.",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.speed < 0:
        print("Error: --speed must be >= 0", file=sys.stderr)
        return 1

    text = read_input(args.file)
    if not text:
        log.warning("Input is empty — nothing to display.")
        return 0

    pause = 0.0 if args.no_newline_pause else NEWLINE_PAUSE

    try:
        typewrite(text, speed=args.speed, newline_pause=pause)
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.stdout.flush()

    return 0


if __name__ == "__main__":
    sys.exit(main())
