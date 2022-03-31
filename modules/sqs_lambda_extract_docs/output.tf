output "extract_doc_invoke_arn" {
  value = module.input_request_fn.lambda_function_invoke_arn
}

output "input_te_lambda_fn_name" {
  value = module.input_request_fn.lambda_function_name
}

output "input_te_lambda_fn_alias_arn" {
  value = aws_lambda_alias.input_request_fn_alias.invoke_arn
}

output "input_te_lambda_fn_alias_name" {
  value = aws_lambda_alias.input_request_fn_alias.name
}