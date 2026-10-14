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

Pass `course_uuid` from route/UI context (e.g. `/class/:id`). Do not hardcode course IDs in app code.

## Backend notes

- Layers: `controller` → `service` → `repository`; DTOs in `model/`.
- Domain DB access is **sync** SQLAlchemy (`get_db`). Auth (fastapi-users) uses a separate **async** engine/session. Do not merge them casually.
- Production schema: Alembic. Tests: `Base.metadata.create_all` + `db_seed.sql` (possible drift — prefer matching migrations when adding tables).
- Lint/format: Ruff. Types: mypy (strict). Both run in `./backend/do quality-gates`.

## Frontend notes

- Vue 3 `<script setup>` + TypeScript, Pinia, vue-router, `openapi-fetch`.
- Prefer typed API wrappers in `frontend/src/api/index.ts` over ad-hoc `fetch`.
- Prefer `v-model` over `document.getElementById` when editing forms.
- Course selection lives on `UserStartPage`; class routes carry `course_id` / `course_uuid` into pages and modals.

## Auth (unfinished)

- Backend exposes `/auth` (fastapi-users, JWT cookie).
- Domain CRUD is **not** wired to `current_user()`.
- Login/register UI is a stub. Do not “complete” auth unless the task asks for it.

## Infrastructure

- **AWS** (eu-central-1): S3 static site, CloudFront, API Gateway HTTP API, Lambda (Python 3.13).
- **Supabase** Postgres (session pooler for migrations, transaction pooler for Lambda).
- Bootstrap IAM is GitHub OIDC → `lexloop-cicd-deploy-role` in `infrastructure/base/`.
- Known leftover: Lambda IAM policy still allows DynamoDB; the app does **not** use DynamoDB — do not add DynamoDB to “match” the policy.

## Tests

- Backend controller tests under `backend/lexloop/**/*_test.py` are the pattern to extend.
- Frontend Vitest/Cypress are mostly scaffolding; type-check is the strong frontend gate.
