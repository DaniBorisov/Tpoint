# AI Assistance

A task management and AI chat API built with FastAPI, PostgreSQL, and Ollama.

## Prerequisites

- Python 3.13
- PostgreSQL (or Docker)
- [Ollama](https://ollama.com) (optional, for chat endpoint)

## Dev Setup

```bash
git clone https://github.com/DaniBorisov/Tpoint.git
cd Tpoint
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure as needed.

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

Start Ollama with a compatible model:

```bash
ollama pull llama3.2
ollama serve
```

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

API docs at `http://localhost:8000/docs`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/tasks/db` | List all tasks (PostgreSQL, optional `?priority=` filter) |
| GET | `/tasks/db/{task_id}` | Get task by ID (PostgreSQL) |
| POST | `/tasks/db` | Create a task (PostgreSQL) |
| GET | `/messages/` | List all messages |
| POST | `/messages/` | Send a message and get an LLM response |

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM and database access
- **PostgreSQL** — persistent storage
- **Ollama** — local LLM for chat
- **Pydantic** — data validation
