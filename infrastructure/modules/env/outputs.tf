output "website_bucket_name" {
  description = "Name of the S3 bucket hosting the static website"
  value       = aws_s3_bucket.static_site.bucket
}

output "website_bucket_arn" {
  description = "ARN of the S3 bucket hosting the static website"
  value       = aws_s3_bucket.static_site.arn
}

output "domain_name" {
  description = "Custom domain for this environment"
  value       = var.domain_name
}

output "cloudfront_url" {
  description = "Public frontend URL (custom domain)"
  value       = "https://${var.domain_name}"
}

output "cloudfront_distribution_domain" {
  description = "CloudFront distribution domain name (*.cloudfront.net)"
  value       = aws_cloudfront_distribution.cdn.domain_name
}

output "api_base_url" {
  description = "API base URL (via custom domain)"
  value       = "https://${var.domain_name}/api"
}

output "auth_secrets_arn" {
  description = "Secrets Manager ARN for JWT + Google OAuth credentials"
  value       = aws_secretsmanager_secret.auth.arn
}

output "auth_secrets_name" {
  description = "Secrets Manager name for JWT + Google OAuth credentials"
  value       = aws_secretsmanager_secret.auth.name
}

output "db_url_session" {
  description = "Database URL (session mode, port 5432). Use for migrations and DDL - supports all Postgres features."
  value       = local.db_url_session
  sensitive   = true
}

output "db_url_transaction" {
  description = "Database URL (transaction mode, port 6543). Use for Lambda/serverless - better connection pooling."
  value       = local.db_url_transaction
  sensitive   = true
}

