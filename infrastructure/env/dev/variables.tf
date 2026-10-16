variable "supabase_access_token" {
  description = "Supabase Access Token"
  sensitive   = true
}

variable "frontend_url" {
  type    = string
  default = "http://localhost:5173"
}

variable "google_oauth_redirect_url" {
  type    = string
  default = ""
}
