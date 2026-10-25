# Lab 3 — Before/after maintainability (M1 draft)

**Source:** original course monolith, compared with the Team 05 target modular design. Items marked *verify after integration* must be rechecked when other members' PRs are merged.

| Question | Before — monolith | After — assistant_core |
|---|---|---|
| Where would you change the credit rate? How many places? | Edit one in-code `RATE` constant | One environment variable `CREDIT_RATE_VND` (verify after integration) |
| Can tests run without internet or an API key? | No repeatable automated tests; random provider and debug key | Yes, deterministic stub and pytest; **verify after integration** |
| What if `handbook.json` is missing? | `load()` catches error, prints, and continues | Raise `DataError` at startup (verify M3 implementation) |
| Is any secret printed or logged? | Yes, literal `API_KEY` printed by `llm()` | No; key hidden in Settings and excluded from JSON logs (verify M2) |
| Time to find fee logic? | Search long `handle()` in a single script | Directly read `tools.py`, called by `service.py` |
| Number of module-level globals | 9, including 3 mutable | Target: 0 mutable application globals; verify after integration |
| Number of bare `except:` blocks | 3 | Target: 0; verify `ruff check --select BLE .` |
| Lines in longest function | Around 65 (`handle()`) | Small focused methods, target ~15 lines per method; verify actual counts |
| `ruff check` issues | Unchecked in original; visibly has style and unsafe exception handling | Target 0; **not yet run on integrated repository** |
| Swap LLM without touching service? | No; `llm()` logic is embedded in monolith | Yes; inject Responder Protocol implementation |

**Three sentences:** The largest improvement is separation of business logic, configuration, and provider errors behind the stable `AssistantService.handle` interface. The price is more files, explicit types, and dependency wiring, which is worth it for team ownership and testability. After full team integration I would strengthen malformed-CSV/JSON validation and add automated regression checks on every PR.

**Status:** Draft prepared by M1; convert targets to measured results only after team integration and passing quality gates.
