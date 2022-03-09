output "entry_input_pred_request_predict_invoke_arn" {
  value = module.entry_input_pred_request_fn.lambda_function_invoke_arn
}

output "entry_input_pred_request_lambda_fn_name" {
  value = module.entry_input_pred_request_fn.lambda_function_name
}

output "vf_tags_invoke_arn" {
  value = module.vf_tags_fn.lambda_function_invoke_arn
}

output "vf_tags_fn_name" {
  value = module.vf_tags_fn.lambda_function_name
}

output "model_info_invoke_arn" {
  value = module.model_info_fn.lambda_function_invoke_arn
}

output "model_info_fn_name" {
  value = module.model_info_fn.lambda_function_name
}