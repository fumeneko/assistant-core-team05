"""Deterministic routing for student questions."""
import re

from assistant_core.models import Intent

def _contains_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    return any(
        re.search(rf"(?<!\w){re.escape(keyword)}(?!\w)", text)
        for keyword in keywords
    )


def route(text: str, office_names: set[str]) -> Intent:
    normalized = text.casefold().strip(" \t\n\r.,!?;:")

    if _contains_keyword(
        normalized,
        ("tuition", "fee", "học phí", "tín chỉ", "retake"),
    ):
        return Intent.FEE

    if any(
        office.casefold() in normalized
        for office in office_names
        if office.strip()
    ):
        return Intent.OFFICE

    if _contains_keyword(
        normalized,
        ("rule", "regulation", "quy định", "nội quy", "thi"),
    ):
        return Intent.RULE

    if any(
        normalized == greeting or normalized.startswith(greeting + " ")
        for greeting in ("hello", "hi", "xin chào", "chào bạn")
    ):
        return Intent.GREETING

    return Intent.UNKNOWN
