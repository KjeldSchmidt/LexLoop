output "tfstate_bucket_name" {
  description = "Name of the S3 bucket for Terraform state"
  value       = aws_s3_bucket.tfstate.bucket
}

output "tfstate_bucket_arn" {
  description = "ARN of the S3 bucket for Terraform state"
  value       = aws_s3_bucket.tfstate.arn
}


output "cicd_role_arn" {
  description = "ARN of the IAM role for CI/CD deployments"
  value       = aws_iam_role.cicd_deploy.arn
}

output "cicd_role_name" {
  description = "Name of the IAM role for CI/CD deployments"
  value       = aws_iam_role.cicd_deploy.name
}
