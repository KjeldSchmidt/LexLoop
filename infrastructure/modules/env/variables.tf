variable "env" {
  description = "The name of the environment, i.e. dev, stage, prod - used to derive unique resource names"
  type        = string

  validation {
    condition     = contains(["dev", "prod"], var.env)
    error_message = "Allowed values for env_name are 'dev' or 'prod'."
  }
}

variable "supabase_access_token" {
  description = "Supabase Access Token"
  sensitive   = true
}

variable "jwt_signing_secret" {
  description = "Secret for signing auth JWTs (teachers and students)"
  type        = string
  sensitive   = true
  default     = ""
}

variable "google_oauth_client_id" {
  description = "Google OAuth client ID for teacher login"
  type        = string
  sensitive   = true
  default     = ""
}

variable "google_oauth_client_secret" {
  description = "Google OAuth client secret for teacher login"
  type        = string
  sensitive   = true
  default     = ""
}

variable "frontend_url" {
  description = "Frontend origin for CORS (e.g. CloudFront URL)"
  type        = string
  default     = "http://localhost:5173"
}

variable "google_oauth_redirect_url" {
  description = "Optional absolute Google OAuth callback URL"
  type        = string
  default     = ""
}
