data "aws_caller_identity" "reserved_current_user" {}

resource "aws_sqs_queue" "reserved_input_queue" {
  name_prefix               = "reserved-input-queue-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 0
  visibility_timeout_seconds = 900

  tags = {
    Environment = "${var.environment}"
  }
}

resource "aws_sqs_queue" "reserved_processed_queue" {
  name_prefix               = "reserved-processed-queue-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 0
  redrive_policy            = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.reserved_failed_msgs_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Environment = "${var.environment}"
  }
}

resource "aws_sqs_queue" "reserved_failed_msgs_dlq" {
  name_prefix               = "reserved-failed-msgs-dlq-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 0

  tags = {
      Environment = "${var.environment}"
  }
}

# module "reserved_input_request_fn" {
#     source = "terraform-aws-modules/lambda/aws"
#     publish = true

#     function_name = "reserved-te-input-func-${var.environment}"
#     handler = "app.send_msg_sqs"
#     runtime = "python3.8"
#     timeout = 30

#     source_path = [
#     {
#         path = "${path.module}/../../lambda_fns/extract_docs_input_request"
#     }
#     ]

#     attach_policy_json    = true

#     policy_json = jsonencode({
#     "Version": "2012-10-17",
#     "Statement": [
#     {
#         "Effect": "Allow",
#         "Action": [
#             "sqs:SendMessage",
#             "sqs:GetQueueUrl",
#             "sqs:ListQueues",
#             "sqs:SendMessageBatch"
#         ],
#         "Resource": [aws_sqs_queue.reserved_input_queue.arn]
#     }
#     ]
#     })

#     provisioned_concurrent_executions = 5

#     environment_variables = {
#         INPUT_QUEUE = aws_sqs_queue.reserved_input_queue.id
#     }
# }

resource "aws_lambda_event_source_mapping" "reserved_sqs_to_extract_lambda_trigger" {
  event_source_arn = aws_sqs_queue.reserved_input_queue.arn
  function_name    = "${module.reserved_extract_docs_fn.lambda_function_arn}:${module.reserved_extract_docs_fn.lambda_function_version}" #module.reserved_extract_docs_fn.lambda_function_arn
  batch_size       = 2
}

module "reserved_extract_docs_fn" {
    source  = "terraform-aws-modules/lambda/aws"
    publish = true

    function_name = "reserved-te-extract-docs-func-${var.environment}"
    handler       = "app.process_docs"
    runtime       = "python3.8"
    timeout       = 900

    source_path = [{
        path = "${path.module}/../../lambda_fns/extract_docs"
        pip_requirements = "${path.module}/../../lambda_fns/extract_docs/requirements.txt"
    }]

    memory_size    = 2048

    attach_policy_json    = true
    policy_json = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:InvokeFunction",
                    "sqs:SendMessage",
                    "sqs:ReceiveMessage",
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes",
                    "sqs:GetQueueUrl",
                    "sqs:ListQueues",
                    "sqs:SendMessageBatch",
                    "s3:PutObject"
                ],
                "Resource": [
                    aws_sqs_queue.reserved_input_queue.arn,
                    aws_sqs_queue.reserved_processed_queue.arn,
                    "${var.processed_docs_bucket_arn}",
                    "${var.processed_docs_bucket_arn}/*",
                    "arn:aws:lambda:us-east-1:${data.aws_caller_identity.reserved_current_user.account_id}:function:${var.docs_convert_lambda_fn_name}"
                ]
            }
        ]
    })

    provisioned_concurrent_executions = var.environment == "dev" ? 1 : 10
    reserved_concurrent_executions = 30

    build_in_docker = true
    environment_variables = {
        INPUT_QUEUE = aws_sqs_queue.reserved_input_queue.id
        DEST_S3_BUCKET = "${var.processed_docs_bucket}"
        PROCESSED_QUEUE = aws_sqs_queue.reserved_processed_queue.id
        DOCS_CONVERT_LAMBDA_FN_NAME = "${var.docs_convert_lambda_fn_name}"
        ENVIRONMENT = "${var.environment}"
        SENTRY_URL = "${var.sentry_url}"
    }
}

# resource "aws_lambda_provisioned_concurrency_config" "reserved_extract_docs_concurrency" {
#     function_name = aws_lambda_alias.reserved_extract_docs_alias.function_name
#     provisioned_concurrent_executions = 5
#     qualifier = module.reserved_extract_docs_fn.lambda_function_version #aws_lambda_alias.reserved_extract_docs_alias.name
# }

# resource "aws_lambda_alias" "reserved_extract_docs_alias" {
#     name = "reserved_extract_docs"
#     function_name = module.reserved_extract_docs_fn.lambda_function_arn
#     function_version = module.reserved_extract_docs_fn.lambda_function_version
# }

resource "aws_appautoscaling_target" "reserved_extract_docs_autoscale" {
    max_capacity       = var.environment == "dev" ? 1 : 10
    min_capacity       = var.environment == "dev" ? 1 : 5
    resource_id        = "function:${module.reserved_extract_docs_fn.lambda_function_name}:${module.reserved_extract_docs_fn.lambda_function_version}"
    scalable_dimension = "lambda:function:ProvisionedConcurrency"
    service_namespace  = "lambda"
}

module "reserved_output_request_fn" {
    source = "terraform-aws-modules/lambda/aws"
    publish = true

    function_name = "reserved-te-output-request-func-${var.environment}"
    handler = "app.output_request"
    runtime = "python3.8"
    timeout = 30

    source_path = [
        {
            path = "${path.module}/../../lambda_fns/extract_docs_output_request"
            pip_requirements = "${path.module}/../../lambda_fns/extract_docs_output_request/requirements.txt"
        }
    ]

    attach_policy_json    = true

    policy_json = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sqs:SendMessage",
                    "sqs:ReceiveMessage",
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes",
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    aws_sqs_queue.reserved_processed_queue.arn,
                    aws_sqs_queue.reserved_failed_msgs_dlq.arn,
                    "${var.processed_docs_bucket_arn}",
                    "${var.processed_docs_bucket_arn}/*"
                ]
            }
        ]
    })

    provisioned_concurrent_executions = var.environment == "dev" ? 1 : 5

    build_in_docker = true
    #store_on_s3 = true
    #s3_bucket = "${var.processed_docs_bucket}"

    environment_variables = {
        SIGNED_URL_EXPIRY_SECS = "${var.signed_url_expiry_secs}"
        ENVIRONMENT = "${var.environment}"
        SENTRY_URL = "${var.sentry_url}"
    }
}

resource "aws_appautoscaling_target" "reserved_output_fn_autoscale" {
    max_capacity       = var.environment == "dev" ? 1 : 5
    min_capacity       = var.environment == "dev" ? 1 : 2
    resource_id        = "function:${module.reserved_output_request_fn.lambda_function_name}:${module.reserved_output_request_fn.lambda_function_version}"
    scalable_dimension = "lambda:function:ProvisionedConcurrency"
    service_namespace  = "lambda"
}

resource "aws_lambda_event_source_mapping" "reserved_sqs_to_output_lambda_trigger" {
  event_source_arn = aws_sqs_queue.reserved_processed_queue.arn
  function_name    = "${module.reserved_output_request_fn.lambda_function_arn}:${module.reserved_output_request_fn.lambda_function_version}"
  batch_size       = 2
}

module "reserved_transfer_dlq_msg" {
    source = "terraform-aws-modules/lambda/aws"
    publish = true
    
    function_name = "reserved-te-transfer-dlq-msg-func-${var.environment}"
    handler = "app.dlq_msgs_handler"
    runtime = "python3.8"
    timeout = 30

    source_path = [
        {
            path = "${path.module}/../../lambda_fns/extract_docs_dlq_msgs"
        }
    ]

    attach_policy_json    = true

    policy_json = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sqs:SendMessage",
                    "sqs:ReceiveMessage",
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes"
                ],
                "Resource": [
                    aws_sqs_queue.reserved_processed_queue.arn,
                    aws_sqs_queue.reserved_failed_msgs_dlq.arn
                ]
            }
        ]
    })

    provisioned_concurrent_executions = var.environment == "dev" ? 1 : 5

    environment_variables = {
        PROCESSED_QUEUE = aws_sqs_queue.reserved_processed_queue.id
    }
}

resource "aws_appautoscaling_target" "reserved_transfer_dlq_msg_autoscale" {
    max_capacity       = var.environment == "dev" ? 1 : 5
    min_capacity       = var.environment == "dev" ? 1 : 2
    resource_id        = "function:${module.reserved_transfer_dlq_msg.lambda_function_name}:${module.reserved_transfer_dlq_msg.lambda_function_version}"
    scalable_dimension = "lambda:function:ProvisionedConcurrency"
    service_namespace  = "lambda"
}

resource "aws_lambda_event_source_mapping" "reserved_transfer_dlq_msgs_lambda_trigger" {
  event_source_arn = aws_sqs_queue.reserved_failed_msgs_dlq.arn
  function_name    = "${module.reserved_transfer_dlq_msg.lambda_function_arn}:${module.reserved_transfer_dlq_msg.lambda_function_version}"
  batch_size       = 2
}
