variable "env" {
  description = "The name of the environment, i.e. dev, stage, prod - used to derive unique resource names"
  type        = string

  validation {
    condition     = contains(["dev", "prod"], var.env)
    error_message = "Allowed values for env_name are 'dev' or 'prod'."
  }
}

variable "domain_name" {
  description = "Custom domain for this environment (e.g. lex-loop.de, beta.lex-loop.de)"
  type        = string
}

variable "supabase_access_token" {
  description = "Supabase Access Token"
  sensitive   = true
}
