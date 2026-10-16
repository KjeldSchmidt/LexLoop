terraform {
  backend "s3" {
    # These values are the outputs of the base infrastructure
    bucket       = "lexloop-tfstate-a2d59717"
    key          = "lexloop.dev.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}

module "env" {
  source = "../../modules/env"

  env                       = "dev"
  supabase_access_token     = var.supabase_access_token
  frontend_url              = var.frontend_url
  google_oauth_redirect_url = var.google_oauth_redirect_url
}
