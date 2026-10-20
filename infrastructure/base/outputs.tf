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

output "domain_name" {
  description = "Apex domain managed in Route53"
  value       = local.domain_name
}

output "route53_zone_id" {
  description = "Route53 hosted zone ID for the apex domain"
  value       = aws_route53_zone.main.zone_id
}

output "route53_name_servers" {
  description = "Nameservers to configure at the domain registrar (Porkbun)"
  value       = aws_route53_zone.main.name_servers
}
