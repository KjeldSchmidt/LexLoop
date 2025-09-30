provider "aws" {
  region = "eu-central-1"
}

terraform {
  backend "s3" {
    # These values should be replaced with outputs from the base infrastructure
    bucket       = "lexloop-tfstate-a2d59717"
    key          = "lexloop.prod.tfstate"
    region       = "eu-central-1"
    encrypt      = true
    use_lockfile = true
  }
}

module "env" {
  source       = "../../aws-modules/env"
  env_name     = "prod"
  project_name = "lexloop"
  region       = "eu-central-1"
}
