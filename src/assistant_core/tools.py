"""Deterministic tools for parsing credits and calculating tuition."""

from assistant_core.errors import InvalidRequest


def parse_credits(text: str) -> tuple[int, int]:
    """Extract credit count and retake count from a tuition question."""
    words = text.lower().replace("?", " ").split()
    credits = 0
    retake = 0

    for i, word in enumerate(words):
        if not word.isdigit():
            continue

        number = int(word)

        if i + 1 < len(words) and words[i + 1].startswith("retake"):
            retake = number
        elif credits == 0:
            credits = number

    if credits <= 0:
        raise InvalidRequest("Credit count must be positive.")

    return credits, retake


def tuition(
    credits: int,
    retake: int,
    rate: int,
    retake_multiplier: float,
    max_credits: int,
) -> int:
    """Calculate tuition including retake fees."""
    if credits <= 0 or credits > max_credits:
        raise InvalidRequest("Invalid credit count.")

    if retake < 0:
        raise InvalidRequest("Retake count cannot be negative.")

    if rate < 0 or retake_multiplier < 0:
        raise InvalidRequest("Tuition rates cannot be negative.")

    total = credits * rate + retake * rate * retake_multiplier
    return int(total)
