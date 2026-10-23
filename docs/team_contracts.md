# Team 05 — Lab 3 integration contracts

This document is the integration agreement derived from the Lab 3 tutorial (Part B / Part C) and the team's six-person ownership split. **Use these exact names and import paths** to avoid merge conflicts.

## Layout
```text
data/offices.csv
data/handbook.json
docs/architecture.md
src/assistant_core/__init__.py
src/assistant_core/__main__.py
src/assistant_core/config.py
src/assistant_core/errors.py
src/assistant_core/models.py
src/assistant_core/knowledge.py
src/assistant_core/tools.py
src/assistant_core/router.py
src/assistant_core/responder.py
src/assistant_core/service.py
src/assistant_core/logging_setup.py
tests/
pyproject.toml
requirements.txt
.env.example
.gitignore
```

## M6 models/errors contract
```python
class Intent(str, Enum): GREETING="greeting"; FEE="fee"; OFFICE="office"; RULE="rule"; UNKNOWN="unknown"
class Message(BaseModel): text: str = Field(min_length=1, max_length=2000); session_id: str = "local"
class Source(BaseModel): id: str; title: str
class Response(BaseModel): answer: str; intent: Intent; sources: list[Source] = Field(default_factory=list); degraded: bool = False

class AssistantError(Exception): ...
class ConfigError(AssistantError): ...
class DataError(AssistantError): ...
class InvalidRequest(AssistantError): ...
class ProviderError(AssistantError): ...
```

## M2 config/log contract
```python
class Settings(BaseModel):
    data_dir: Path = Path("data")
    llm_provider: str = "stub"
    llm_api_key: str | None = Field(default=None, repr=False)
    credit_rate_vnd: int = 450_000
    retake_multiplier: float = 1.5
    max_credits: int = 30
    log_level: str = "INFO"

def load_settings(env_file: str | None = ".env") -> Settings: ...
def setup_logging(level: str = "INFO") -> None: ...
```
Log JSON to stderr. Keep API keys and raw user messages OUT of logs. No hardcoded credentials.

## M3 knowledge/responder contract
```python
@dataclass(frozen=True)
class Office: name: str; room: str; hours: str
class OfficeDirectory:
    @classmethod
    def from_csv(cls, path: Path) -> "OfficeDirectory": ...
    @property
    def names(self) -> set[str]: ...
    def find(self, text: str) -> Office | None: ...

@dataclass(frozen=True)
class Rule: id: str; title: str; text: str
class Handbook:
    @classmethod
    def from_json(cls, path: Path) -> "Handbook": ...
    def search(self, query: str) -> Rule | None: ...

class Responder(Protocol):
    def explain(self, question: str, rule: Rule) -> str: ...
class TemplateResponder:
    def explain(self, question: str, rule: Rule) -> str: ...
class StubLLMResponder:
    def __init__(self, fail: bool = False): ...
    def explain(self, question: str, rule: Rule) -> str: ...
```
Missing/malformed input files raise DataError at startup. Rule search should use deterministic keyword overlap. Provider failure raises ProviderError; no random sleeps/failures.

## M4 deterministic tools/router contract
```python
def parse_credits(text: str) -> tuple[int, int]: ...
def tuition(credits: int, retake: int, rate: int,
            retake_multiplier: float, max_credits: int) -> int: ...
def route(text: str, office_names: set[str]) -> Intent: ...
```
`tuition(18, 2, 450_000, 1.5, 30) == 9_450_000`; invalid credits raise InvalidRequest. Route returns GREETING / FEE / OFFICE / RULE; service may return UNKNOWN when no rule matched.

## M1 service/CLI contract
```python
class AssistantService:
    def __init__(self, settings: Settings, offices: OfficeDirectory,
                 handbook: Handbook, responder: Responder): ...
    def handle(self, msg: Message) -> Response: ...
```
`python -m assistant_core "tuition for 18 credits and 2 retake"` should produce a human answer; logging goes to stderr and answer stdout. ProviderError falls back to TemplateResponder and sets `degraded=True`, preserving sources.

## Test / submission gates
- At least 10 meaningful pytest tests including 9,450,000 VND characterisation and ProviderError fallback.
- `python -m pytest -q`, `python -m ruff check .`, and `python -m ruff format --check .`.
- Document modules, public service interface, and 3 architecture decisions.
- Each person completes `docs/lab3/before_after.md` and H1 AI extension review/AI-use log on their own work branch as specified by the tutorial (please clarify how to avoid filename collisions before merging individual worksheets).
- Never commit actual `.env` file.
