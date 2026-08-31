# AI Assistance

A task management and AI chat API built with FastAPI, PostgreSQL, and LLM providers (Ollama or OpenAI).

## Prerequisites

- Python 3.13
- PostgreSQL (or Docker)
- [Ollama](https://ollama.com) (optional, for local chat)
- OpenAI API key (optional, for OpenAI provider)

## Dev Setup

```bash
git clone https://github.com/DaniBorisov/Tpoint.git
cd Tpoint
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure as needed.

## Configuration

- `DATABASE_URL` — main PostgreSQL connection string.
- `TEST_DATABASE_URL` — PostgreSQL connection string used by the test suite. Required; the suite refuses to run unless it points to the `ai_assistant_test` database.
- `DATABASE_ECHO` — default `false`. When `true`, logs every SQL statement executed against the database.
- `LOG_LEVEL` — default `INFO`. Sets application log verbosity (see below).
- `LLM_PROVIDER` — ollama or openai; selects which LLM backend the app uses. Default ollama.
- `OPENAI_API_KEY` — required when `LLM_PROVIDER=openai`.
- `OPENAI_MODEL` — OpenAI model name, default `gpt-5-nano`.
- `OLLAMA_MODEL` — Ollama model, default `llama3.2`.

### Log levels

- `INFO` — logs standard application events: task and message creation, LLM calls, message retrieval.
- `DEBUG` — everything in `INFO` plus fine-grained detail for troubleshooting during development.

### Database

Start PostgreSQL with Docker:

```bash
docker compose up -d postgres
```

This creates an `ai_assistant` database on port 5432.

### Apply migrations

```bash
alembic upgrade head
```

### LLM (optional)

The app supports two LLM providers, selected with `LLM_PROVIDER`:
`ollama` (default) or `openai`.

For Ollama, start it with a compatible model:

```bash
ollama pull llama3.2
ollama serve
```

For OpenAI, set `LLM_PROVIDER=openai` and `OPENAI_API_KEY` in `.env`.

## Run

### Option A — local dev

```bash
uvicorn app.main:app --reload
```

### Option B — full Docker stack

Builds both the backend and PostgreSQL:

```bash
docker compose up --build
```

If docker volumes build with older version clean the volumes:

```bash
docker compose down -v
```

API docs at `http://localhost:8000/docs`

## Run tests

The test suite runs against a dedicated `ai_assistant_test` database. Start
PostgreSQL and create the test database, then run `pytest`:

```bash
docker compose up -d postgres
docker exec ai_assistant_postgres createdb -U postgres ai_assistant_test
pytest
```

The test schema is created automatically before the suite runs. Each test
cleans up after itself, so the database is reused across runs.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/tasks/db` | List all tasks (PostgreSQL, optional `?priority=` filter) |
| GET | `/tasks/db/{task_id}` | Get task by ID (PostgreSQL) |
| POST | `/tasks/db` | Create a task (PostgreSQL) |
| GET | `/messages/` | List all messages |
| POST | `/messages/` | Send a message and get an LLM response |
| POST | `/agent/` | Run the agent loop (tool use + LLM) |
| GET | `/agent/person` | Extract person info (OpenAI only) |
| POST | `/agent/summarize-email` | Summarize an email (OpenAI only) |

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM and database access
- **Alembic** — database migrations
- **PostgreSQL** — persistent storage
- **Ollama** — local LLM provider
- **OpenAI** — hosted LLM provider
- **Pydantic** — data validation
- **Pytest** — unit, integration, and API tests
