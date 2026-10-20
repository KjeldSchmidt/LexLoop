# Public DNS for lex-loop.de. Point Porkbun nameservers at the zone output
# `route53_name_servers` so ACM validation and CloudFront aliases work.
resource "aws_route53_zone" "main" {
  name = local.domain_name

  tags = {
    Project   = local.project_name
    ManagedBy = "terraform"
  }
}
