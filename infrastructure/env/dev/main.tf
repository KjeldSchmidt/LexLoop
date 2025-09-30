terraform {
  backend "s3" {
    # These values should be replaced with outputs from the base infrastructure
    bucket       = "lexloop-tfstate-a2d59717"
    key          = "lexloop.dev.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}

module "env" {
  source = "../../modules/env"

  env_name = "dev"
}
