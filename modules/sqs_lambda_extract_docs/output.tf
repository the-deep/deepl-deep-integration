output "extract_doc_invoke_arn" {
  value = module.input_request_fn.lambda_function_invoke_arn
}

output "input_te_lambda_fn_name" {
  value = module.input_request_fn.lambda_function_name
}