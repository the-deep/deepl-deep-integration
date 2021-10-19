variable "environment" {}

variable "name" { default = "rapi" }
variable "ep_predict_entry" { default = "entry_predict" }

variable "ep_input_te" { default = "extract_docs" }

#variable "lambda_name" { default = "entry-prediction-handler-dev"}

#variable "process_doc_lambda_name" { default = "te-input-func-dev"}

variable "predict_entry_lambda_fn_name" {}
variable "input_te_lambda_fn_name" {}

variable "vpce_id" { default = "vpce-053ed1c5a7f24dacf" }

variable "predict_entry_invoke_arn" {}

variable "process_doc_invoke_arn" {}