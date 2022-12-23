variable environment {}

variable aws_region {}

variable model_endpoint_name {}

variable geolocation_fn_name {}

variable reliability_fn_name {}

variable model_info_fn_name {}

variable processed_docs_bucket {}

variable sentry_url {}

variable lambda_concurrency_max {
    default = 3
}

variable lambda_concurrency_min {
    default = 2
}