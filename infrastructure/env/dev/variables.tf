variable "supabase_access_token" {
  description = "Supabase Access Token"
  sensitive   = true
}

variable "jwt_signing_secret" {
  description = "Secret for signing auth JWTs"
  type        = string
  sensitive   = true
  default     = ""
}

variable "google_oauth_client_id" {
  type      = string
  sensitive = true
  default   = ""
}

variable "google_oauth_client_secret" {
  type      = string
  sensitive = true
  default   = ""
}

variable "frontend_url" {
  type    = string
  default = "http://localhost:5173"
}

variable "google_oauth_redirect_url" {
  type    = string
  default = ""
}
