aws_region = "us-east-1"
aws_profile = "default"
environment = "prod"

# api gateway
api_gateway_name = "rapi"
vpce_id = "vpce-05d8c268ef4c0c443"
vpc_id = "vpc-0947f040a9d4692a7"

# models
model_endpoint_name = "test-all-models-rsh"
geolocation_fn_name = "geolocations"
reliability_fn_name = "reliability"
model_info_fn_name = "model_info"

# ecr image name
docs_extract_fn_image_name = "extract-tool"

# docs convert lambda
docs_convert_lambda_fn_name = "libreoffice-dev-libreoffice"

# docs convert bucket name
docs_convert_bucket_name = "deep-large-docs-conversion"

# sentry url
sentry_url = "https://3b273f4c61ac4d94af28e85a66ea0b5a@o158798.ingest.sentry.io/1223576"

# VPC
az_count = 1
cidr_block = "172.18.0.0/16"

# ECS role
ecs_task_execution_role = "ECSTaskExecutionRole"

# ECS
fargate_cpu = "2048"
fargate_memory = "4096"
app_count = 1
app_image = "961104659532.dkr.ecr.us-east-1.amazonaws.com/deepex-parser"