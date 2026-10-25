"""Command-line interface: python -m assistant_core 'your question'."""

import argparse
import sys

from pydantic import ValidationError

from assistant_core.config import load_settings
from assistant_core.errors import ConfigError, DataError
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.logging_setup import setup_logging
from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService


def build_service() -> AssistantService:
    """Wire the package dependencies together at application startup."""
    settings = load_settings()
    if settings.llm_provider != "stub":
        raise ConfigError("Lab 3 CLI supports LLM_PROVIDER=stub only; real providers arrive later.")

    setup_logging(settings.log_level)
    offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
    handbook = Handbook.from_json(settings.data_dir / "handbook.json")
    return AssistantService(
        settings=settings,
        offices=offices,
        handbook=handbook,
        responder=StubLLMResponder(),
    )


def answer_once(service: AssistantService, text: str) -> int:
    """Print only the answer to stdout; diagnostics go to stderr."""
    try:
        message = Message(text=text)
    except ValidationError:
        print("Invalid message: text must contain 1 to 2000 characters.", file=sys.stderr)
        return 2

    print(service.handle(message).answer)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Team 05 maintainable study assistant")
    parser.add_argument("question", nargs="*", help="Question to answer; omit to open interactive mode")
    args = parser.parse_args(argv)

    try:
        service = build_service()
    except (ConfigError, DataError, ValidationError) as exc:
        print(f"Startup error: {exc}", file=sys.stderr)
        return 1

    if args.question:
        return answer_once(service, " ".join(args.question))

    print("Assistant ready. Type 'quit' to exit.", file=sys.stderr)
    while True:
        try:
            text = input("> ")
        except (EOFError, KeyboardInterrupt):
            return 0

        if text.strip().lower() in {"quit", "exit"}:
            return 0
        if not text.strip():
            continue
        answer_once(service, text)


if __name__ == "__main__":
    raise SystemExit(main())
