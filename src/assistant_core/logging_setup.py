"""Configure structured JSON logging."""

import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    """Format approved log fields as one JSON object."""

    def format(self, record: logging.LogRecord) -> str:
        data = {
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        for key in ("intent", "latency_ms", "session", "degraded"):
            if hasattr(record, key):
                data[key] = getattr(record, key)

        return json.dumps(data, ensure_ascii=False)


def setup_logging(level: str = "INFO") -> None:
    """Send assistant logs to stderr in JSON format."""
    level_number = getattr(logging, level.upper(), None)

    if not isinstance(level_number, int):
        raise ValueError("Invalid logging level")

    logger = logging.getLogger("assistant_core")
    logger.setLevel(level_number)
    logger.propagate = False

    for old_handler in logger.handlers[:]:
        logger.removeHandler(old_handler)
        old_handler.close()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
