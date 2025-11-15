output "website_bucket_name" {
  description = "Name of the S3 bucket hosting the static website"
  value       = module.env.website_bucket_name
}

output "website_bucket_arn" {
  description = "ARN of the S3 bucket hosting the static website"
  value       = module.env.website_bucket_arn
}

output "cloudfront_url" {
  description = "CloudFront distribution URL for the frontend"
  value       = module.env.cloudfront_url
}

output "api_base_url" {
  description = "API base URL (via CloudFront)"
  value       = module.env.api_base_url
}

