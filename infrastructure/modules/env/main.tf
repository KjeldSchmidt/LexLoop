terraform {
  required_version = ">= 1.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.14"
    }

    supabase = {
      source  = "supabase/supabase"
      version = "~> 1.0"
    }
  }
}

provider "aws" {
  region = local.region

  default_tags {
    tags = local.common_tags
  }
}

provider "supabase" {
  access_token = env.SUPABASE_ACCESS_TOKEN
}
