provider "aws" {
  region = var.aws_region
  profile = var.aws_profile
}

module "sqs_lambda_module" {
  source = "./modules/sqs_lambda"
  processed_docs_bucket = "${module.s3_module.te_bucket_name}"

  environment = var.environment
}

module "apigateway_module" {
  source = "./modules/api_gateway"

  predict_entry_invoke_arn = "${module.sqs_lambda_module.predict_entry_invoke_arn}"
  process_doc_invoke_arn = "${module.sqs_lambda_module.extract_doc_invoke_arn}"

  predict_entry_lambda_fn_name = "${module.sqs_lambda_module.predict_entry_lambda_fn_name}"
  input_te_lambda_fn_name = "${module.sqs_lambda_module.input_te_lambda_fn_name}"

  environment = var.environment
}

module "s3_module" {
  source = "./modules/s3"

  environment = var.environment
}