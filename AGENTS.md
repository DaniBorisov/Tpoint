# AGENTS.md

## Project

FastAPI task management API. In-memory storage (no database).

## Run

```bash
uvicorn app.main:app --reload
```

API docs at `http://localhost:8000/docs` when running.

## Structure

- `app/main.py` — FastAPI app, registers routers
- `app/api/` — Route handlers (tasks, health, about)
- `app/schemas/` — Pydantic request/response models
- `app/services/` — Business logic (class-based, injected via `Depends`)

## Conventions

- Python 3.13 (`str | None` union syntax, not `Optional[str]`)
- Services are instantiated per-request via `Depends(get_<service>)`
- No tests, linting, or formatting configured yet
