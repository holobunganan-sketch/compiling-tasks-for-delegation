# Context

## Known Facts
- The project is a Python repository.
- `src/greeting.py` contains the target function.
- `tests/test_greeting.py` contains focused tests for that function.

## Environment
- Working directory is the repository root.
- Python and `pytest` are available.

## Assumptions
- Existing tests are green before the change; CHUNK-001 verifies this before mutation.

## Boundaries
- Execute only the active chunk.
- Do not preload later chunks.
- Do not alter unrelated modules.
