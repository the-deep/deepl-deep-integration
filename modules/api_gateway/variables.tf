variable "environment" {}

variable "api_gateway_name" {}
variable "ep_predict_entry" { default = "entry_predict" }

variable "ep_input_te" { default = "extract_docs" }

variable "vf_tags" { default = "vf_tags" }

variable "model_info" { default = "model_info" }

#variable "lambda_name" { default = "entry-prediction-handler-dev"}

#variable "process_doc_lambda_name" { default = "te-input-func-dev"}

variable "predict_entry_lambda_fn_name" {}
variable "input_te_lambda_fn_name" {}

variable "entry_input_pred_request_fn_alias_arn" {}
variable "entry_input_pred_reqeust_fn_alias_name" {}

variable "input_te_lambda_fn_alias_arn" {}
variable "input_te_lambda_fn_alias_name" {}

variable "vpce_id" {}
variable "vpc_id" {}

variable "predict_entry_invoke_arn" {}

variable "process_doc_invoke_arn" {}

variable "vf_tags_invoke_arn" {}
variable "vf_tags_fn_name" {}

variable "model_info_invoke_arn" {}
variable "model_info_fn_name" {}