aws_region = "us-east-1"
aws_profile = "default"
environment = "staging"

# api gateway
api_gateway_name = "rapi"
vpce_id = "vpce-02c7bb08b571074e1"
vpc_id = "vpc-0e65245d5e4c2deaf"

# models
model_endpoint_name = "test-all-models-rsh"
geolocation_fn_name = "geolocations"
reliability_fn_name = "reliability"
model_info_fn_name = "model_info"

# ecr image name
docs_extract_fn_image_name = "extract-tool"

# docs convert lambda
docs_convert_lambda_fn_name = "libreoffice-dev-libreoffice"

# sentry url
sentry_url = "https://3b273f4c61ac4d94af28e85a66ea0b5a@o158798.ingest.sentry.io/1223576"