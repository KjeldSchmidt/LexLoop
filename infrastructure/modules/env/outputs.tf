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

