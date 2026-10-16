resource "aws_secretsmanager_secret" "auth" {
  name                    = "${local.project_slug}/auth/${var.env}"
  description             = "LexLoop auth secrets (JWT + Google OAuth) for ${var.env}"
  recovery_window_in_days = 0
  tags                    = local.common_tags
}

# Placeholder only — real values are written by CI (`put-secret-value`) or console.
# Terraform must not overwrite runtime secret contents on later applies.
resource "aws_secretsmanager_secret_version" "auth" {
  secret_id = aws_secretsmanager_secret.auth.id
  secret_string = jsonencode({
    JWT_SIGNING_SECRET         = ""
    GOOGLE_OAUTH_CLIENT_ID     = ""
    GOOGLE_OAUTH_CLIENT_SECRET = ""
  })

  lifecycle {
    ignore_changes = [secret_string]
  }
}
