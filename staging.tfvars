aws_region = "us-east-1"
aws_profile = "default"
environment = "staging"

# api gateway
api_gateway_name = "rapi"
vpce_id = "vpce-02c7bb08b571074e1"
vpc_id = "vpc-0e65245d5e4c2deaf"

# models
model_endpoint_name = "main-model-cpu"
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
sentry_secret_name = "staging/sentry_url" # get the name from secrets manager

# VPC
az_count = 1
cidr_block = "172.16.0.0/16"

# ECS role
ecs_task_execution_role = "ECSTaskExecutionRole"

# ECS
fargate_cpu = "1024"
fargate_memory = "2048"
app_count = 1
app_image = "961104659532.dkr.ecr.us-east-1.amazonaws.com/deepex-parser-staging"
