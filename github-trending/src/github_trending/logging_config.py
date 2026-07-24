"""Structured logging configuration for the service."""

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """Configure root logging once, writing structured lines to stdout."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    )
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
