# Lab 3 — Monolith code-smell review (M1)

Source: `public_materials/lab03/monolith/assistant_monolith.py` (read directly from course repository).

| # | Smell in the original code | Evidence | New owner/module |
|---|---|---|---|
| 1 | Hardcoded API key | `API_KEY` set in source and printed by `llm()` | M2 `config.py` + `logging_setup.py` |
| 2 | Hardcoded fee/rate/model/debug | `RATE`, `RETAKE_RATE`, `MODEL`, `DEBUG` | M2 `config.py` |
| 3 | Mutable globals | `history`, `offices`, `handbook` | M3 `knowledge.py`, M1 `service.py` |
| 4 | Bare `except:` | twice in `load()`, once in `main()` | M6 `errors.py`, M3 `knowledge.py`, M1 CLI |
| 5 | Mixed responsibilities | `handle()` parses fees, routes, reads rules and calls AI | M1 `service.py`, M4 `router.py`/`tools.py` |
| 6 | Magic string responses | `"empty"`, `"saved"`, `"too many credits"` | M6 `models.py` and `errors.py` |
| 7 | `print` used for debugging | `llm()`, `main()` and `save_history()` | M2 `logging_setup.py` |
| 8 | Ad hoc tests | `test()` only prints examples; no assertions | M4 tests + M1 `tests/test_service.py` |
| 9 | Fragile paths | `BASE + "/data/..."` and manual open | M2 `config.py`, M3 `knowledge.py` |
| 10 | Nondeterministic provider | `random.random()` and `time.sleep()` in `llm()` | M3 `responder.py` |

Refactoring preserves greeting, office lookup, tuition, and handbook answers with source attribution. History/stats/save are not part of the Lab 3 target interface and should not be recreated unless the instructor requests them.
