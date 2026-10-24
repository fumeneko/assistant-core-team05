import pytest

from assistant_core.errors import InvalidRequest
from assistant_core.tools import parse_credits, tuition


def test_parse_credits_and_retake():
    assert parse_credits("tuition for 18 credits and 2 retake") == (18, 2)


def test_parse_credits_without_retake():
    assert parse_credits("tuition for 18 credits") == (18, 0)


def test_parse_credits_case_insensitive():
    assert parse_credits("18 CREDITS and 2 RETAKE") == (18, 2)


def test_parse_credits_without_credit_count():
    with pytest.raises(InvalidRequest):
        parse_credits("How much is tuition?")


def test_parse_credits_retake_before_credits():
    assert parse_credits("retake 2 for 18 credits") == (18, 2)


def test_tuition_expected_amount():
    assert tuition(18, 2, 450_000, 1.5, 30) == 9_450_000


def test_tuition_without_retake():
    assert tuition(18, 0, 450_000, 1.5, 30) == 8_100_000


def test_tuition_rejects_zero_credits():
    with pytest.raises(InvalidRequest):
        tuition(0, 0, 450_000, 1.5, 30)


def test_tuition_rejects_too_many_credits():
    with pytest.raises(InvalidRequest):
        tuition(31, 0, 450_000, 1.5, 30)


def test_tuition_rejects_negative_retake():
    with pytest.raises(InvalidRequest):
        tuition(18, -1, 450_000, 1.5, 30)


def test_tuition_rejects_negative_rate():
    with pytest.raises(InvalidRequest):
        tuition(18, 0, -450_000, 1.5, 30)
