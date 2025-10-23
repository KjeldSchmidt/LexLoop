output "website_bucket_name" {
  description = "Name of the S3 bucket hosting the static website"
  value       = module.env.website_bucket_name
}

output "website_bucket_arn" {
  description = "ARN of the S3 bucket hosting the static website"
  value       = module.env.website_bucket_arn
}

