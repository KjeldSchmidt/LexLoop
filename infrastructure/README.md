# Infrastructure

Terraform for LexLoop on **AWS** (eu-central-1) with **Supabase** Postgres.

## Layout

| Path | Role |
|------|------|
| [`base/`](base/) | Bootstrap: Terraform state bucket, GitHub OIDC IAM role (`lexloop-cicd-deploy-role`) |
| [`env/dev`](env/dev/), [`env/prod`](env/prod/) | Environment wiring only — sets variables and instantiates the shared module |
| [`modules/env/`](modules/env/) | All env resources: S3 website, CloudFront, API Gateway + Lambda, Supabase project/DB URLs |

No resources are defined in the `env/*` folders beyond module instantiation and env-specific variables.

## Stack

- **Frontend:** S3 bucket + CloudFront (SPA). `/api/*` is forwarded to the API origin.
- **API:** API Gateway HTTP API → Lambda (Python 3.13, Mangum handler `lexloop.main.aws_handler`). Artifact: `backend/lex-api-bundle.zip` (build with `./backend/do build` before apply).
- **Database:** Supabase Postgres. Session pooler URL for Alembic migrations; transaction pooler URL for Lambda `DB_URL`.

## Bootstrap vs CI

1. Apply `base/` with a human AWS principal (creates OIDC deploy role and state backend).
2. CI assumes `lexloop-cicd-deploy-role` via GitHub Actions OIDC and applies `env/dev` (and prod when configured).

## Commands

```bash
./infrastructure/do fmt-check
./infrastructure/do lint
./infrastructure/do apply dev    # interactive
./infrastructure/do apply-auto dev
./infrastructure/do get-bucket dev
```

## Known leftovers

- Lambda IAM still grants DynamoDB; the application uses Postgres only. Do not add DynamoDB usage to match the policy — clean up the policy in a later change.
