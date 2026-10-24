"""Leader-owned integration tests for the public service interface."""

import json

import pytest

from assistant_core.config import Settings
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.models import Intent, Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService


@pytest.fixture
def service(tmp_path):
    (tmp_path / "offices.csv").write_text(
        "name,room,hours\nLibrary,B.201,Mon-Sat 07:00-20:00\n",
        encoding="utf-8",
    )
    (tmp_path / "handbook.json").write_text(
        json.dumps(
            [
                {
                    "id": "H26-5.3",
                    "title": "Thesis registration",
                    "text": "Students may register a thesis after 120 accumulated credits and GPA 2.0.",
                }
            ]
        ),
        encoding="utf-8",
    )
    return AssistantService(
        settings=Settings(data_dir=tmp_path),
        offices=OfficeDirectory.from_csv(tmp_path / "offices.csv"),
        handbook=Handbook.from_json(tmp_path / "handbook.json"),
        responder=StubLLMResponder(),
    )


def test_greeting(service):
    response = service.handle(Message(text="hi"))
    assert response.intent is Intent.GREETING
    assert "Hello!" in response.answer


def test_tuition_characterisation(service):
    response = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert response.intent is Intent.FEE
    assert "9,450,000" in response.answer


def test_office_lookup(service):
    response = service.handle(Message(text="where is the library"))
    assert response.intent is Intent.OFFICE
    assert "B.201" in response.answer


def test_rule_includes_source(service):
    response = service.handle(Message(text="thesis registration credits"))
    assert response.intent is Intent.RULE
    assert response.sources[0].id == "H26-5.3"
    assert not response.degraded


def test_rule_provider_failure_uses_fallback(service):
    service.responder = StubLLMResponder(fail=True)
    response = service.handle(Message(text="thesis registration credits"))
    assert response.intent is Intent.RULE
    assert response.degraded
    assert response.sources[0].id == "H26-5.3"
    assert "120" in response.answer


def test_unknown_rule(service):
    response = service.handle(Message(text="cafeteria menu"))
    assert response.intent is Intent.UNKNOWN
    assert not response.sources
