resource "aws_s3_bucket" "bucket" {
    bucket_prefix = "${var.text_extraction_bucket}-${var.environment}-"
    force_destroy = true
    acl = "private"
}