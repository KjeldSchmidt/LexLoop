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

## Auth secrets

**Local:** copy [`backend/.env.example`](backend/.env.example) into `backend/.env`. For Google teacher login, set client ID/secret and add the callback URL in the Google Cloud console (typically `http://127.0.0.1:8000/api/auth/google/callback`).

**Deployed (dev/prod):** JWT + Google OAuth live in **AWS Secrets Manager** (`lex/auth/<env>`). Lambda reads them via `AUTH_SECRETS_ARN`. Non-secret config (`FRONTEND_URL`, `GOOGLE_OAUTH_REDIRECT_URL`) stays as Lambda env / Terraform vars.

Seed or update the secret either:

1. GitHub Actions secrets `JWT_SIGNING_SECRET`, `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET` (CI syncs into Secrets Manager on deploy), or
2. Console/CLI: set a JSON secret with those three keys on `lex/auth/dev` (or `prod`).

## Known gaps

- Frontend unit/e2e tests are mostly scaffolding
- Course/cohort membership (#11) not tied to accounts yet
