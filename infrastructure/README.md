# Infrastructure

Terraform for LexLoop on **AWS** (eu-central-1) with **shared tck-labs Postgres RDS**.

## Layout

| Path | Role |
|------|------|
| [`base/`](base/) | Bootstrap: Terraform state bucket, GitHub OIDC IAM role, Route53 hosted zone for `lex-loop.de` |
| [`env/dev`](env/dev/), [`env/prod`](env/prod/) | Environment wiring only — sets variables and instantiates the shared module |
| [`modules/env/`](modules/env/) | All env resources: S3 website, CloudFront + custom domain, API Gateway + Lambda, DB URL from shared RDS |

No resources are defined in the `env/*` folders beyond module instantiation and env-specific variables.

## Stack

- **Frontend:** S3 bucket + CloudFront (SPA). `/api/*` is forwarded to the API origin.
- **Domains:** `lex-loop.de` (prod), `beta.lex-loop.de` (dev). ACM certs for CloudFront are in `us-east-1` (AWS requirement); everything else stays in `eu-central-1`.
- **API:** API Gateway HTTP API → Lambda (Python 3.13, Mangum handler `lexloop.main.aws_handler`). Artifact: `backend/lex-api-bundle.zip` (build with `./backend/do build` before apply).
- **Auth secrets:** Secrets Manager `lex/auth/<env>` (JWT + Google OAuth + frontend URLs). Lambda gets `AUTH_SECRETS_ARN` only. Put credentials in SM; CI merges `FRONTEND_URL` / OAuth redirect after apply.
- **Database:** Shared RDS from the **tck-labs-base** lab stack (Secrets Manager `tck-labs/shared/rds`). Logical DBs `lexloop_dev` / `lexloop_prod`. Same URL for migrations and Lambda (`sslmode=require`). `./backend/do db-migrate-remote` creates the logical DB if missing, then runs Alembic.

## Custom domain setup (Porkbun → Route53)

DNS is authoritative in Route53. At Porkbun you only change **nameservers** — do not create A/CNAME records there for the app.

1. Apply `base/` (creates the hosted zone).
2. Read nameservers:
   ```bash
   cd infrastructure/base && terraform output -json route53_name_servers
   ```
3. In Porkbun → domain `lex-loop.de` → **Authoritative Nameservers** → switch from Porkbun defaults to the four AWS NS values from the output. Leave glue/DNSSEC off unless you know you need them.
4. Wait until NS have propagated (`dig NS lex-loop.de +short` should show the Route53 servers).
5. Apply `env/dev` / `env/prod`. Terraform will:
   - issue ACM certs (DNS-validated in Route53),
   - attach them to CloudFront,
   - create `A`/`AAAA` alias records for `lex-loop.de` and `beta.lex-loop.de`.

Until step 4 is done, env apply can hang on ACM certificate validation.

Also register Google OAuth redirect URIs for the custom domains:
`https://lex-loop.de/api/auth/google/callback` and `https://beta.lex-loop.de/api/auth/google/callback`.

## Bootstrap vs CI

1. Apply `base/` with a human AWS principal (creates OIDC deploy role, state backend, Route53 zone).
2. Point Porkbun NS at the Route53 zone (see above).
3. CI assumes `lexloop-cicd-deploy-role` via GitHub Actions OIDC and applies `env/dev` (and prod when configured).

## Commands

```bash
./infrastructure/do fmt-check
./infrastructure/do lint
./infrastructure/do apply dev    # interactive
./infrastructure/do apply-auto dev
./infrastructure/do get-bucket dev
./infrastructure/do deploy-base  # hosted zone + bootstrap
```
