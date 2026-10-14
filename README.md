# LexLoop

An experimental, collaborative shared learning space for schools.

Vocabulary learning: linked terms (nodes), tags, and courses.

## Layout

| Path | Role |
|------|------|
| [`backend/`](backend/) | FastAPI API on AWS Lambda (Mangum), SQLAlchemy, Alembic, Supabase Postgres |
| [`frontend/`](frontend/) | Vue 3 + Vite + Pinia, typed client from OpenAPI |
| [`infrastructure/`](infrastructure/) | Terraform: AWS (S3, CloudFront, API Gateway, Lambda) + Supabase |

Production traffic: CloudFront serves the SPA; `/api/*` is proxied to API Gateway → Lambda. The FastAPI app uses `root_path="/api"`.

## Local setup

```bash
./do setup          # backend deps + git hooks
./frontend/do setup # npm install
```

Run database, API, and UI (separate terminals):

```bash
./backend/do db-up
./backend/do db-migrate-up
./backend/do run          # http://127.0.0.1:8000
./frontend/do run         # Vite; uses VITE_API_URL from frontend/.env
```

Quality checks:

```bash
./do quality-gates
```

After changing API routes or models:

```bash
./do update-api-schema
```

## Agent guidance

See [`AGENTS.md`](AGENTS.md) for conventions, the OpenAPI contract, and known gaps.

## Known gaps

- Login UI is a stub; `/auth` exists but domain routes are not auth-gated
- Frontend unit/e2e tests are mostly scaffolding
