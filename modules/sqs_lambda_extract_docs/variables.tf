variable aws_region {}

variable environment {}

variable "signed_url_expiry_secs" {
    type = number
    default = 3600
}

variable "processed_docs_bucket" {}

variable "processed_docs_bucket_arn" {}

variable "docs_extract_fn_image_name" {}

variable "docs_convert_lambda_fn_name" {}

variable reserved_input_queue_id {}
variable reserved_input_queue_arn {}