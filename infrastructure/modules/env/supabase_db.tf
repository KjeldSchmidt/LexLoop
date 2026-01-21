resource "supabase_project" "_" {
  organization_id   = local.supabase_org_id
  name              = "${local.project_slug}-db-${var.env}"
  database_password = random_password.supabase_password.result
  region            = local.region
}

resource "random_password" "supabase_password" {
  length  = 64
  special = false
}

# Database connection URLs for Supabase pooler.
# Session mode (5432): Full Postgres features, one connection per session. Use for migrations/DDL.
# Transaction mode (6543): Connection returned to pool per transaction. Use for Lambda/serverless.
locals {
  db_url_base        = "postgresql+psycopg://postgres.${supabase_project._.id}:${random_password.supabase_password.result}@aws-1-${local.region}.pooler.supabase.com"
  db_url_session     = "${local.db_url_base}:5432/postgres"
  db_url_transaction = "${local.db_url_base}:6543/postgres"
}
