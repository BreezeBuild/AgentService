# Breeze Agentic

Breeze Agentic is BreezeBuild's standalone Python/FastAPI service for AI-assisted
development. It is a separate repository from the Next.js web app, Core, and
Workspace. The intended integration is for Agentic to inspect and modify project
code through Workspace APIs; those APIs are not connected yet.

This repository currently contains a small LangGraph/OpenAI chat scaffold, not
the project-editing agent. It exposes a health endpoint and a single chat
endpoint. The chat graph makes one OpenAI call and returns its response; it does
not read project files, call Workspace, maintain conversation history, or run
tools.

## Requirements and setup

- Python 3.14 (see `.python-version`)
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key for `POST /api/v1/chat`; health checks do not need one

From this repository's directory:

```bash
uv sync
cp .env.example .env
# Replace the placeholder OPENAI_API_KEY in .env with your own key.
uv run uvicorn breeze_agentic.main:app --reload
```

On PowerShell, use `Copy-Item .env.example .env` instead of `cp` if preferred.
The server defaults to `http://127.0.0.1:8000`, with interactive API docs at
`http://127.0.0.1:8000/docs`. `.env` is ignored by Git; never commit a real key.

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | Required for chat requests |
| `OPENAI_MODEL` | Model used by the chat graph; defaults to `gpt-4o-mini` |
| `ENVIRONMENT` | Label returned by the health endpoint; defaults to `development` |

## Current API

| Method | Path | Behavior |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Returns `status`, service name, and environment |
| `POST` | `/api/v1/chat` | Accepts a non-empty `message` and returns `response` |

Example chat request:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello Breeze"}'
```

The chat endpoint currently has no authentication or project authorization and
must not be exposed publicly as a production project API. Without an OpenAI
key, it returns an error. Core remains the owner of project/user metadata;
Workspace will own source files and revisions. Agentic must not write directly
to either service's database or filesystem when that integration is built.

## Development checks

```bash
uv run pytest
uv run ruff check .
```

The existing test checks the health endpoint. Chat's external OpenAI call is
not covered by that test and requires a configured key to try manually.

## Collaboration

Changes to this repository are proposed from a feature branch in a pull request
targeting `main`. The initial scaffold was the only direct `main` push. Keep
future work small and reviewable; do not merge a PR on behalf of the reviewer.
