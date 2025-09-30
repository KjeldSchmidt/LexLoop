terraform {
  required_version = ">= 1.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.14"
    }
  }

  backend "s3" {
    bucket  = "lexloop-base-tfstate"
    key     = "base.tfstate"
    region  = "eu-central-1"
    encrypt = true
  }
}

provider "aws" {
  region = local.region
}
