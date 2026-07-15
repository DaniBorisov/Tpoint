# AGENTS.md

## Project

FastAPI task management API with LLM integration. In-memory storage, Ollama as default LLM provider.

## Run

```bash
.venv\Scripts\python -m uvicorn app.main:app --reload
```

API docs at `http://localhost:8000/docs` when running.

## Structure

- `app/main.py` — FastAPI app, registers routers
- `app/api/` — Route handlers (tasks, health, about, messages)
- `app/schemas/` — Pydantic request/response models
- `app/services/` — Business logic (class-based, injected via `Depends`)
- `app/services/llm/` — LLM abstraction layer (base, ollama, factory)
- `.env` / `.env.example` — LLM provider config

## Conventions

- Python 3.13 (`str | None` union syntax, not `Optional[str]`)
- Services are instantiated per-request via `Depends(get_<service>)`
- Always create a new branch before starting work: `git checkout -b type/description`
  - Types: `feat`, `fix`, `refactor`, `chore`
- Never merge directly into master. Open a PR and merge via GitHub.
- Use `.venv\Scripts\python -m` prefix for uvicorn/pip (avoids venv activation issues on Windows)
- No tests, linting, or formatting configured yet
