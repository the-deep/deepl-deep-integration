output "entry_input_pred_request_predict_invoke_arn" {
  value = module.entry_input_pred_request_fn.lambda_function_invoke_arn
}

output "entry_input_pred_request_lambda_fn_name" {
  value = module.entry_input_pred_request_fn.lambda_function_name
}