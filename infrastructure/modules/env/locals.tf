locals {
  project_name = "lexloop"
  project_slug = "lex"
  region       = "eu-central-1"

  common_tags = {
    Project     = local.project_name
    Environment = var.env
    ManagedBy   = "terraform"
    Repository  = "https://github.com/KjeldSchmidt/LexLoop/"
  }

  supabase_org_id = "vmgjkugdrchtmuammsnz"
}
