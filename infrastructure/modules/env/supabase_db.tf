resource "supabase_project" "_" {
  organization_id   = local.supabase_org_id
  name              = "${local.project_slug}-db-${var.env}"
  database_password = random_password.supabase_password.result
  region            = local.region
  instance_size     = "nano"
}

resource "random_password" "supabase_password" {
  length           = 64
  special          = true
}
