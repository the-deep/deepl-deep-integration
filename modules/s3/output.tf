output "te_bucket_name" {
    value = aws_s3_bucket.processed_bucket.id
}

output "te_bucket_arn" {
    value = aws_s3_bucket.processed_bucket.arn
}