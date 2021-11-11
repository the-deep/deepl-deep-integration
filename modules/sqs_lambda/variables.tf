variable environment {}

variable "signed_url_expiry_secs" {
    type = number
    default = 3600
}

variable "processed_docs_bucket" {
}

variable ep_name_model {
    type = string
    default = "test-all-models-rsh"
}