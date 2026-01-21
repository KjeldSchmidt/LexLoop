output "website_bucket_name" {
  description = "Name of the S3 bucket hosting the static website"
  value       = aws_s3_bucket.static_site.bucket
}

output "website_bucket_arn" {
  description = "ARN of the S3 bucket hosting the static website"
  value       = aws_s3_bucket.static_site.arn
}

output "cloudfront_url" {
  description = "CloudFront distribution URL for the frontend"
  value       = "https://${aws_cloudfront_distribution.cdn.domain_name}"
}

output "api_base_url" {
  description = "API base URL (via CloudFront)"
  value       = "https://${aws_cloudfront_distribution.cdn.domain_name}/api"
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

