# Lab 3 architecture — Team 05

## 1. Modules and single responsibilities

| Module | Responsibility | Owner |
|---|---|---|
| `config.py` | Validate environment-based settings | M2 |
| `errors.py` | Named failure types | M6 |
| `models.py` | Pydantic Message/Response/Source and Intent contract | M6 |
| `router.py` | Classify user message intent with deterministic rules | M4 |
| `knowledge.py` | Load and search office CSV and handbook JSON | M3 |
| `tools.py` | Pure tuition parsing and calculation | M4 |
| `responder.py` | Pluggable rule-answer interface, stub and template | M3 |
| `service.py` | Coordinate inputs, routing, calculations, search and fallback | M1 |
| `logging_setup.py` | JSON logs to stderr without leaking secrets | M2 |
| `__main__.py` | Assemble dependencies and expose the CLI | M1 |

All runtime modules live in `src/assistant_core/`, with data in `data/` and tests in `tests/`.

## 2. Service interface

```python
AssistantService.handle(msg: Message) -> Response
```

- Input: `Message(text: str, session_id: str = "local")`; text length 1–2000.
- Output: `Response(answer: str, intent: Intent, sources: list[Source], degraded: bool)`.
- Intent values: `greeting`, `fee`, `office`, `rule`, `unknown`.
- Source contains the handbook rule ID and title, when a rule was used.
- A provider failure is caught inside the service, a local template is used instead, and `degraded=True`.
- Invalid input is rejected by Pydantic; missing or malformed data must fail at startup with `DataError`.
- Future FastAPI and UI clients call this method rather than reimplementing routing.

```text
CLI (__main__)
  -> Message validation (models)
  -> AssistantService.handle
       -> route (router)
       -> fee: parse_credits + tuition (tools)
       -> office: OfficeDirectory (knowledge)
       -> rule: Handbook (knowledge) -> Responder (stub)
                                      -> TemplateResponder (fallback)
  -> Response (answer, intent, sources, degraded)
```

## 3. Architecture decisions and reasons

1. **Keep fee calculations in pure functions**, not in the LLM: prices are deterministic, offline, auditable and testable with the 9,450,000 VND characterisation case.
2. **Depend on a Responder interface**, injected into AssistantService: fake/stub responders make failures reproducible, while a real Week 4 provider can be added without modifying service routing; provider errors degrade gracefully.
3. **Separate configuration and telemetry from business logic**: `.env.example` documents nonsecret settings, secrets are not committed or logged, structured JSON logs go to stderr while user answers go to stdout.

## 4. Team integration and quality checks

The six members work on distinct files according to `docs/team_contracts.md`. The Tech Lead reviews PRs and integrates them in dependency order: M6 and M5 first; M2, M3 and M4 next; M1 service/CLI last.

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m assistant_core "tuition for 18 credits and 2 retake"
```

Acceptance: at least 10 meaningful tests pass, lint is clean, fallback test asserts `degraded=True` and sources remain present, and the real `.env` never enters version control.

**Status:** This note describes the target integrated architecture. Module implementation/testing is complete only after all member PRs are reviewed and merged.
