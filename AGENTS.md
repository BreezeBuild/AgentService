# Breeze Agentic guide

This is the standalone Python/FastAPI Agentic service for BreezeBuild. Keep its
build, dependencies, tests, and deployment separate from the Web, Core, and
Workspace repositories.

## Service boundaries

- Core owns users, projects, and other platform metadata. It alone provisions
  users. Do not duplicate that data model or write to Core's database.
- Workspace owns generated Spring Boot source workspaces, files, revisions, and
  later build/preview execution. Agentic will use explicit Workspace APIs to
  inspect and modify project code; do not edit Workspace files or databases
  directly from this service.
- The Next.js Route Handlers are the browser-facing API layer. Do not introduce
  another API gateway here. Temporal orchestrates long-running cross-service
  flows when their workers and service contracts are implemented.
- The current `/api/v1/chat` route is a scaffold without authentication,
  project authorization, Workspace tools, or conversation persistence. Do not
  describe these capabilities as implemented.

## Implementation conventions

- Follow the existing `src/breeze_agentic` package, `uv`, Ruff, and pytest
  setup. Add dependencies only for the feature being implemented.
- Keep FastAPI routes thin and put agent behavior in the agent package. Validate
  request and response models explicitly, and test behavior without requiring
  live OpenAI calls by default.
- Keep API keys in environment variables or an ignored `.env`; never log or
  commit credentials, raw tokens, or unnecessary prompt contents.
- When integration endpoints are introduced, authenticate callers and check
  project authorization before accessing project code. Do not trust a user ID
  supplied in a request body as proof of identity.
- BreezeBuild-generated UUIDs and accepted `X-Request-ID` values must be UUIDv7;
  external IDs such as Clerk user IDs are not subject to that rule.

## Change discipline

Make feature changes on branches and open PRs against `main`. Do not push
directly to `main`, and do not merge PRs on the reviewer's behalf. Keep changes
scoped to the requested feature and verify with `uv run pytest` and
`uv run ruff check .`.
