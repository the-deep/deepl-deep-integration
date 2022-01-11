resource "aws_api_gateway_rest_api" "api" {
  name = "${var.api_gateway_name}-${var.environment}"

  endpoint_configuration {
    types = ["PRIVATE"]
    vpc_endpoint_ids = [var.vpce_id]
  }
}

# The resource for the endpoint
resource "aws_api_gateway_resource" "predict_entry_resource" {
  path_part   = var.ep_predict_entry
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_resource" "doc_input_resource" {
  path_part   = var.ep_input_te
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

# How the gateway will be interacted from clientt
resource "aws_api_gateway_method" "predict_entry_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.predict_entry_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "process_doc_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.doc_input_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

# Integration between lambda and terraform
resource "aws_api_gateway_integration" "gateway_integration_1" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.predict_entry_resource.id
  http_method = aws_api_gateway_method.predict_entry_method.http_method
  # Lambda invokes requires a POST method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.predict_entry_invoke_arn
}

resource "aws_api_gateway_integration" "gateway_integration_2" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.doc_input_resource.id
  http_method = aws_api_gateway_method.process_doc_method.http_method
  # Lambda invokes requires a POST method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.process_doc_invoke_arn
}



# Define lambda permissions to grant API gateway, source arn is not needed
resource "aws_lambda_permission" "allow_api_gateway" {
  action        = "lambda:InvokeFunction"
  function_name = var.predict_entry_lambda_fn_name
  principal     = "apigateway.amazonaws.com"
}

resource "aws_lambda_permission" "allow_api_gateway2" {
  action        = "lambda:InvokeFunction"
  function_name = var.input_te_lambda_fn_name
  principal     = "apigateway.amazonaws.com"
}

resource "aws_api_gateway_rest_api_policy" "api_policy" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Deny",
        Principal = "*",
        Action = "execute-api:Invoke",
        Resource = "execute-api:/*/*/*",
        Condition = {
          StringNotEquals = {
            "aws:sourceVpce": var.vpce_id
          }
        }
      },
      {
        Effect = "Allow",
        Principal = "*",
        Action = "execute-api:Invoke",
        Resource = "execute-api:/*/*/*"
      }
    ]
  })
}

# Deployment of the endpoint
resource "aws_api_gateway_deployment" "ep_deploy" {
    depends_on = [
      aws_api_gateway_method.predict_entry_method,
      aws_api_gateway_method.process_doc_method,
      aws_api_gateway_integration.gateway_integration_1,
      aws_api_gateway_integration.gateway_integration_2
    ]
    rest_api_id = aws_api_gateway_rest_api.api.id
}

# Setting stage
resource "aws_api_gateway_stage" "gateway_stage" {
    deployment_id = aws_api_gateway_deployment.ep_deploy.id
    rest_api_id = aws_api_gateway_rest_api.api.id
    stage_name = var.environment
}


