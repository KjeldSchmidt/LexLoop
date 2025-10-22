resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  default_root_object = "index.html"

  origin {
    domain_name = aws_s3_bucket.static_site.bucket_regional_domain_name
    origin_id   = "${local.project_slug}-frontend-${var.env}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  origin {
    domain_name = aws_apigatewayv2_api.api.api_endpoint
    origin_id   = "${local.project_slug}-api-${var.env}"
    origin_path = "/$default"
  }

  default_cache_behavior {
    target_origin_id       = "${local.project_slug}-frontend-${var.env}"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
  }

  ordered_cache_behavior {
    path_pattern           = "/api/*"
    target_origin_id       = "${local.project_slug}-api-${var.env}"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "POST", "PUT", "DELETE"]
    cached_methods         = ["GET", "HEAD"]
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for S3 bucket"
}
