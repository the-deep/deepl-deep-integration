import os

EXTRACTED_FILE_NAME = "extract_text.txt"
DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
DEST_BUCKET_NAME = os.environ.get("DEST_S3_BUCKET")
PROCESSED_QUEUE_NAME = os.environ.get("PROCESSED_QUEUE")
DOCS_CONVERT_LAMBDA_FN_NAME = os.environ.get("DOCS_CONVERT_LAMBDA_FN_NAME")
DOCS_CONVERSION_BUCKET_NAME = os.environ.get("DOCS_CONVERSION_BUCKET_NAME")

DOMAIN_NAME = os.environ.get("EXTRACTOR_DOMAIN_NAME", "http://extractor:8001")

SENTRY_URL = os.environ.get("SENTRY_URL")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

VPC_PRIVATE_SUBNET = os.environ.get("VPC_PRIVATE_SUBNET")
ECS_CLUSTER_ID = os.environ.get("ECS_CLUSTER_ID")
ECS_TASK_DEFINITION = os.environ.get("ECS_TASK_DEFINITION")
ECS_CONTAINER_NAME = os.environ.get("ECS_CONTAINER_NAME")

CLIENT_ID = os.environ.get("CLIENT_ID")
URL = os.environ.get("URL")
CALLBACK_URL = os.environ.get("CALLBACK_URL")