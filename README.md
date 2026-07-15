# Tpoint

A simple task management REST API built with FastAPI.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/tasks/` | List all tasks (optional `?priority=` filter) |
| GET | `/tasks/{task_id}` | Get task by ID |
| POST | `/tasks/` | Create a new task |
| GET | `/health` | Health check |
| GET | `/about` | Project info |
