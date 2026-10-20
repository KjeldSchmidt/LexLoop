locals {
  region            = "eu-central-1"
  project_name      = "lexloop"
  project_shortname = "lex"
  domain_name       = "lex-loop.de"
  account_id        = data.aws_caller_identity.current.account_id
}


data "aws_caller_identity" "current" {}
