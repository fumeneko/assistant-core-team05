"""Deterministic routing for student questions."""

from assistant_core.models import Intent


def route(text: str, office_names: set[str]) -> Intent:
    normalized = text.casefold().strip(" \t\n\r.,!?;:")

    if any(keyword in normalized for keyword in ("tuition", "fee", "học phí", "tín chỉ", "retake")):
        return Intent.FEE

    if any(office.casefold() in normalized for office in office_names if office.strip()):
        return Intent.OFFICE

    if any(keyword in normalized for keyword in ("rule", "regulation", "quy định", "nội quy", "thi")):
        return Intent.RULE

    if any(
        normalized == greeting or normalized.startswith(greeting + " ")
        for greeting in ("hello", "hi", "xin chào", "chào bạn")
    ):
        return Intent.GREETING

    return Intent.UNKNOWN
