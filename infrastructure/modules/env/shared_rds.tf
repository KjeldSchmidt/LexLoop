# Shared PoC Postgres from tck-labs-base (see that repo's infrastructure/README).
# One RDS instance, logical DB per project+env: lexloop_dev / lexloop_prod.

data "aws_secretsmanager_secret_version" "shared_rds" {
  secret_id = "tck-labs/shared/rds"
}

locals {
  rds_creds = jsondecode(data.aws_secretsmanager_secret_version.shared_rds.secret_string)

  app_db_name = "${local.project_name}_${var.env}"

  # Same host for migrations and Lambda (no pooler). SSL required by RDS.
  db_url_session = format(
    "postgresql+psycopg://%s:%s@%s:%s/%s?sslmode=require",
    urlencode(local.rds_creds.username),
    urlencode(local.rds_creds.password),
    local.rds_creds.host,
    tostring(local.rds_creds.port),
    local.app_db_name,
  )
  db_url_transaction = local.db_url_session
}
