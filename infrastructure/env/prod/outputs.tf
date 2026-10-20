output "website_bucket_name" {
  description = "Name of the S3 bucket hosting the static website"
  value       = module.env.website_bucket_name
}

output "website_bucket_arn" {
  description = "ARN of the S3 bucket hosting the static website"
  value       = module.env.website_bucket_arn
}

output "domain_name" {
  description = "Custom domain for this environment"
  value       = module.env.domain_name
}

output "cloudfront_url" {
  description = "Public frontend URL (custom domain)"
  value       = module.env.cloudfront_url
}

output "cloudfront_distribution_domain" {
  description = "CloudFront distribution domain name (*.cloudfront.net)"
  value       = module.env.cloudfront_distribution_domain
}

output "api_base_url" {
  description = "API base URL (via custom domain)"
  value       = module.env.api_base_url
}

output "auth_secrets_arn" {
  description = "Secrets Manager ARN for JWT + Google OAuth credentials"
  value       = module.env.auth_secrets_arn
}

output "auth_secrets_name" {
  description = "Secrets Manager name for JWT + Google OAuth credentials"
  value       = module.env.auth_secrets_name
}

output "db_url_session" {
  description = "Database URL (session mode, port 5432). Use for migrations and DDL."
  value       = module.env.db_url_session
  sensitive   = true
}

output "db_url_transaction" {
  description = "Database URL (transaction mode, port 6543). Use for Lambda/serverless."
  value       = module.env.db_url_transaction
  sensitive   = true
}

