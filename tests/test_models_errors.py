import pytest
from pydantic import ValidationError

from assistant_core.errors import (
    AssistantError,
    ConfigError,
    DataError,
    InvalidRequest,
    ProviderError,
)
from assistant_core.models import Intent, Message, Response, Source


def test_message_valid():
    message = Message(text="Hello")

    assert message.text == "Hello"
    assert message.session_id == "local"


@pytest.mark.parametrize("text", ["", " " * 0])
def test_message_rejects_empty_text(text):
    with pytest.raises(ValidationError):
        Message(text=text)


def test_message_rejects_text_over_2000_characters():
    with pytest.raises(ValidationError):
        Message(text="a" * 2001)


def test_response_defaults():
    response = Response(answer="Hi", intent=Intent.GREETING)

    assert response.sources == []
    assert response.degraded is False


def test_source():
    source = Source(id="doc1", title="Example")

    assert source.id == "doc1"
    assert source.title == "Example"


@pytest.mark.parametrize(
    "error_type",
    [ConfigError, DataError, InvalidRequest, ProviderError],
)
def test_custom_errors_inherit_from_assistant_error(error_type):
    assert issubclass(error_type, AssistantError)
