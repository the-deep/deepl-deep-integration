terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.9.0"
    }
  }
  required_version = "1.1.2"
  backend "s3" {
    bucket         = "terraform-state-deep"
    key            = "deep_deepl_integration/terraform.tfstate"
    region         = "us-east-1"
#    dynamodb_table = "terraform-lock-integration-db"
    encrypt        = true
  }
}

#resource "aws_dynamodb_table" "terraform_locks" {
#  hash_key       = "LockID"
#  name           = "terraform-lock-integration-db"
#  billing_mode   = "PAY_PER_REQUEST"
#  attribute {
#    name = "LockID"
#    type = "S"
#  }
#}

provider "aws" {
  region = var.aws_region
  # profile = var.aws_profile
}

module "sqs_lambda_module" {
  source = "./modules/sqs_lambda_extract_docs"
  processed_docs_bucket = "${module.s3_module.te_bucket_name}"
  processed_docs_bucket_arn = "${module.s3_module.te_bucket_arn}"

  docs_extract_fn_image_name = var.docs_extract_fn_image_name
  aws_region = var.aws_region

  docs_convert_lambda_fn_name = var.docs_convert_lambda_fn_name

  reserved_input_queue_id = "${module.reserved_sqs_lambda_module.reserved_input_queue_id}"
  reserved_input_queue_arn = "${module.reserved_sqs_lambda_module.reserved_input_queue_arn}"

  environment = var.environment

  sentry_url = var.sentry_url
}

module "reserved_sqs_lambda_module" {
  source = "./modules/reserved_sqs_lambda_extract_docs"
  processed_docs_bucket = "${module.s3_module.te_bucket_name}"
  processed_docs_bucket_arn = "${module.s3_module.te_bucket_arn}"

  docs_extract_fn_image_name = var.docs_extract_fn_image_name
  aws_region = var.aws_region

  docs_convert_lambda_fn_name = var.docs_convert_lambda_fn_name

  environment = var.environment

  sentry_url = var.sentry_url
}

module "sqs_lambda_predict_module" {
  source = "./modules/sqs_lambda_entry_predict"
  processed_docs_bucket = "${module.s3_module.te_bucket_name}"

  model_endpoint_name = var.model_endpoint_name
  geolocation_fn_name = var.geolocation_fn_name
  reliability_fn_name = var.reliability_fn_name
  model_info_fn_name = var.model_info_fn_name

  reserved_entry_input_queue_predict_id = "${module.reserved_sqs_lambda_predict_module.reserved_entry_input_queue_predict_id}"
  reserved_entry_input_queue_predict_arn = "${module.reserved_sqs_lambda_predict_module.reserved_entry_input_queue_predict_arn}"

  aws_region = var.aws_region
  environment = var.environment

  sentry_url = var.sentry_url
}

module "reserved_sqs_lambda_predict_module" {
  source = "./modules/reserved_lambda_entry_predict"
  processed_docs_bucket = "${module.s3_module.te_bucket_name}"

  model_endpoint_name = var.model_endpoint_name
  geolocation_fn_name = var.geolocation_fn_name
  reliability_fn_name = var.reliability_fn_name
  model_info_fn_name = var.model_info_fn_name

  aws_region = var.aws_region
  environment = var.environment

  sentry_url = var.sentry_url
}

module "apigateway_module" {
  source = "./modules/api_gateway"

  api_gateway_name = var.api_gateway_name

  vpce_id = var.vpce_id
  vpc_id = var.vpc_id

  predict_entry_invoke_arn = "${module.sqs_lambda_predict_module.entry_input_pred_request_predict_invoke_arn}"
  process_doc_invoke_arn = "${module.sqs_lambda_module.extract_doc_invoke_arn}"

  predict_entry_lambda_fn_name = "${module.sqs_lambda_predict_module.entry_input_pred_request_lambda_fn_name}"
  input_te_lambda_fn_name = "${module.sqs_lambda_module.input_te_lambda_fn_name}"

  entry_input_pred_request_fn_alias_arn = "${module.sqs_lambda_predict_module.entry_input_pred_request_fn_alias_arn}"
  entry_input_pred_reqeust_fn_alias_name = "${module.sqs_lambda_predict_module.entry_input_pred_reqeust_fn_alias_name}"

  input_te_lambda_fn_alias_arn = "${module.sqs_lambda_module.input_te_lambda_fn_alias_arn}"
  input_te_lambda_fn_alias_name = "${module.sqs_lambda_module.input_te_lambda_fn_alias_name}"

  vf_tags_invoke_arn = "${module.sqs_lambda_predict_module.vf_tags_invoke_arn}"
  vf_tags_fn_name = "${module.sqs_lambda_predict_module.vf_tags_fn_name}"

  model_info_invoke_arn = "${module.sqs_lambda_predict_module.model_info_invoke_arn}"
  model_info_fn_name = "${module.sqs_lambda_predict_module.model_info_fn_name}"

  environment = var.environment
}

module "s3_module" {
  source = "./modules/s3"

  environment = var.environment
}