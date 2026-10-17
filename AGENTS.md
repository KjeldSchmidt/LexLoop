# Agent guide for LexLoop

## Monorepo tasks

Use the bash `do` scripts; do not invent one-off scripts.

| Task | Command |
|------|---------|
| Root quality | `./do quality-gates` |
| Setup | `./do setup` |
| Regenerate OpenAPI + TS types | `./do update-api-schema` |
| Verify OpenAPI / schema.ts freshness | `./do check-api-schema` |
| Backend | `./backend/do …` (`run`, `test`, `types`, `build`, migrations, …) |
| Frontend | `./frontend/do …` (`run`, `test-check`, `build`, …) |
| Infra | `./infrastructure/do …` (`apply`, `fmt-check`, …) |

## API contract (single source of truth)

1. Change FastAPI controllers / Pydantic models under `backend/lexloop/`.
2. Run `./do update-api-schema` — updates committed `backend/openapi.json` and `frontend/src/api/schema.ts`.
3. Update `frontend/src/api/index.ts` wrappers to match generated `paths`.
4. CI fails if OpenAPI or `schema.ts` drifts (`./do check-api-schema`).

POST bodies use FastAPI `Body(embed=True)`. Clients must send wrappers:

```json
{ "node": { "term": "…", "definition": "…", "tags": [], "course_uuid": "…" } }
```

Same pattern for `tag` and `link`.

List endpoints are course-scoped:

- `GET /courses`
- `GET /course/{course_uuid}/nodes`
- `GET /course/{course_uuid}/tags`
- `GET /course/{course_uuid}/links`

Paginated list responses use `{ items, total, offset, limit }` with query params `offset` (default 0) and `limit` (default 50, max 100). Unpaginated exceptions: `GET /links/types` (fixed enum) and `GET /tags/node/{node_uuid}` (few tags per node).

Pass `course_uuid` from route/UI context (e.g. `/class/:id`). Do not hardcode course IDs in app code.

## Backend notes

- Layers: `controller` → `service` → `repository`; DTOs in `model/`.
- Domain DB access is **sync** SQLAlchemy (`get_db`). Auth (fastapi-users) uses a separate **async** engine/session. Do not merge them casually.
- Production schema: Alembic. Tests: `Base.metadata.create_all` + `db_seed.sql` (possible drift — prefer matching migrations when adding tables).
- Lint/format: Ruff. Types: mypy (strict). Both run in `./backend/do quality-gates`.
- Docstrings: prefer them on public controller/service functions and modules. Do not skip them on new public APIs.
- Pydantic / fastapi-users model classes may keep `# type: ignore[explicit-any]` under `disallow_any_explicit`; do not use bare `# type: ignore`.

## Frontend notes

- Vue 3 `<script setup>` + TypeScript, Pinia, vue-router, `openapi-fetch`.
- Prefer typed API wrappers in `frontend/src/api/index.ts` over ad-hoc `fetch`.
- Prefer `v-model` over `document.getElementById` when editing forms.
- Course selection lives on `UserStartPage`; class routes carry `course_id` / `course_uuid` into pages and modals.

## Auth

- **Teachers:** fastapi-users `user` table; Google OAuth at `/auth/google/*`; cookie `lexloop-userauth`. Public `/auth/register` is disabled.
- **Students:** separate `lexloop_students` (username + password only; no email/name); `/students/login`; cookie `lexloop-studentauth`.
- Domain routes require an authenticated principal (teacher or student).
- Secrets: local via `backend/.env`; deployed via Secrets Manager `lex/auth/<env>` (Lambda `AUTH_SECRETS_ARN`). Credentials are managed in SM; CI refreshes CloudFront `FRONTEND_URL` + OAuth redirect URI into the same secret after apply.

## Infrastructure

- **AWS** (eu-central-1): S3 static site, CloudFront, API Gateway HTTP API, Lambda (Python 3.13).
- **Supabase** Postgres (session pooler for migrations, transaction pooler for Lambda).
- Bootstrap IAM is GitHub OIDC → `lexloop-cicd-deploy-role` in `infrastructure/base/`.
## Tests

- Backend controller tests under `backend/lexloop/**/*_test.py` are the pattern to extend.
- Frontend Vitest/Cypress are mostly scaffolding; type-check is the strong frontend gate.
