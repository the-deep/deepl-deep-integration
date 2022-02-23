resource "aws_s3_bucket" "processed_bucket" {
    bucket_prefix = "${var.text_extraction_bucket}-${var.environment}-"
    force_destroy = true
    acl           = "private"
}

# resource "aws_s3_bucket_acl" "processed_bucket_acl" {
#     bucket = aws_s3_bucket.processed_bucket.id
#     acl    = "private"
# }

resource "aws_s3_bucket_policy" "processed_bucket_policy" {
    bucket = aws_s3_bucket.processed_bucket.id

    policy = jsonencode({
        Version     = "2012-10-17"
        Id          = "processed-bucket-policy"
        Statement   = [
            {
                Sid       = ""
                Effect    = "Allow"
                Principal = "*"
                Action    = [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                Resource = [
                    aws_s3_bucket.processed_bucket.arn,
                    "${aws_s3_bucket.processed_bucket.arn}/*",
                ]
            }
        ]
    })
}