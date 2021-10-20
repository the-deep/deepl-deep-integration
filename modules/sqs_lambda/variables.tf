variable environment {}

variable "signed_url_expiry_secs" {
    default = 3600
}

variable "processed_docs_bucket" {
    default = "lambda-sqs-test-bucket-1"
}

variable ep_name_1d_model {
    default = "model-1d"
}