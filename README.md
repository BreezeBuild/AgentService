# Breeze Agentic

Modern FastAPI app scaffolded with LangChain, LangGraph, and OpenAI.

## Setup

```bash
cd breeze-agentic
cp .env.example .env
# add your OPENAI_API_KEY to .env
uv sync
```

## Run

```bash
uv run uvicorn breeze_agentic.main:app --reload
```

API docs: <http://127.0.0.1:8000/docs>

## Endpoints

- `GET /api/v1/health`
- `POST /api/v1/chat`

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello Breeze"}'
```

## Quality checks

```bash
uv run pytest
uv run ruff check .
```
