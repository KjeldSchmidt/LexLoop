locals {
  project_name      = "lexloop"
  project_shortname = "lex"
  region            = "eu-central-1"

  common_tags = {
    Project     = local.project_name
    Environment = var.env_name
    ManagedBy   = "terraform"
    Repository  = "https://github.com/KjeldSchmidt/LexLoop/"
  }
}
