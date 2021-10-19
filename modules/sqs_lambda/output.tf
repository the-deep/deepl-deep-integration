output "predict_entry_invoke_arn" {
  value = module.predict_entry_fn.lambda_function_invoke_arn
}

output "extract_doc_invoke_arn" {
  value = module.input_request_fn.lambda_function_invoke_arn
}

output "predict_entry_lambda_fn_name" {
  value = module.predict_entry_fn.lambda_function_name
}

output "input_te_lambda_fn_name" {
  value = module.input_request_fn.lambda_function_name
}