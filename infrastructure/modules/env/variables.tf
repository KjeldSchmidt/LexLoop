variable "env_name" {
  description = "The name of the environment, i.e. dev, stage, prod - used to derive unique resource names"
  type        = string

  validation {
    condition     = contains(["dev", "prod"], var.env_name)
    error_message = "Allowed values for env_name are 'dev' or 'prod'."
  }
}
