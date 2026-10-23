
"""Tests for M2 configuration and logging."""

import json
import logging

import pytest

from assistant_core.config import load_settings
from assistant_core.errors import ConfigError
from assistant_core.logging_setup import setup_logging


def test_default_settings(monkeypatch):
    for name in (
        "ASSISTANT_DATA_DIR",
        "LLM_PROVIDER",
        "LLM_API_KEY",
        "CREDIT_RATE_VND",
        "RETAKE_MULTIPLIER",
        "MAX_CREDITS",
        "LOG_LEVEL",
    ):
        monkeypatch.delenv(name, raising=False)

    settings = load_settings(env_file=None)

    assert settings.llm_provider == "stub"
    assert settings.credit_rate_vnd == 450_000
    assert settings.max_credits == 30
    assert settings.llm_api_key is None


def test_settings_from_environment(monkeypatch):
    monkeypatch.setenv("CREDIT_RATE_VND", "500000")
    monkeypatch.setenv("MAX_CREDITS", "24")

    settings = load_settings(env_file=None)

    assert settings.credit_rate_vnd == 500_000
    assert settings.max_credits == 24


def test_missing_api_key(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "remote")
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    with pytest.raises(ConfigError):
        load_settings(env_file=None)


def test_api_key_hidden_from_repr(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "remote")
    monkeypatch.setenv("LLM_API_KEY", "example-secret")

    settings = load_settings(env_file=None)

    assert "example-secret" not in repr(settings)


def test_invalid_numeric_config(monkeypatch):
    monkeypatch.setenv("CREDIT_RATE_VND", "invalid")

    with pytest.raises(ConfigError):
        load_settings(env_file=None)


def test_json_logging_to_stderr(capsys):
    setup_logging("INFO")
    logger = logging.getLogger("assistant_core")

    logger.info(
        "handled",
        extra={
            "intent": "fee",
            "latency_ms": 1.5,
            "session": "local",
            "degraded": False,
        },
    )

    captured = capsys.readouterr()
    result = json.loads(captured.err.strip())

    assert captured.out == ""
    assert result["level"] == "INFO"
    assert result["msg"] == "handled"
    assert result["intent"] == "fee"
    assert result["latency_ms"] == 1.5
    assert result["degraded"] is False


def test_logging_excludes_unapproved_fields(capsys):
    setup_logging()
    logger = logging.getLogger("assistant_core")

    logger.info(
        "handled",
        extra={
            "api_key": "example-secret",
            "raw_message": "private question",
        },
    )

    output = capsys.readouterr().err

    assert "example-secret" not in output
    assert "private question" not in output


def test_setup_logging_does_not_duplicate_handlers():
    setup_logging()
    setup_logging()

    logger = logging.getLogger("assistant_core")

    assert len(logger.handlers) == 1
