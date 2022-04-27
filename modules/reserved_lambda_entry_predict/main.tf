data "aws_caller_identity" "reserved_current" {}

resource "aws_sqs_queue" "reserved_entry_input_queue_predict" {
  name_prefix               = "reserved-entry-input-queue-predict-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 0
  visibility_timeout_seconds = 60

  tags = {
    Environment = "${var.environment}"
  }
}

resource "aws_sqs_queue" "reserved_entry_input_processed_queue_predict" {
  name_prefix               = "reserved-input-processed-queue-predict-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 0
  redrive_policy            = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.reserved_entry_failed_msgs_dlq_predict.arn
    maxReceiveCount     = 3
  })

  tags = {
    Environment = "${var.environment}"
  }
}

resource "aws_sqs_queue" "reserved_entry_failed_msgs_dlq_predict" {
  name_prefix               = "reserved-entry-input-failed-msgs-dlq-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 0

  tags = {
      Environment = "${var.environment}"
  }
}

# module "reserved_entry_input_pred_request_fn" {
#     source = "terraform-aws-modules/lambda/aws"
#     publish = true

#     function_name = "reserved-entry-input-pred-func-${var.environment}"
#     handler = "app.entry_msg_sqs_handler"
#     runtime = "python3.8"
#     timeout = 30

#     source_path = [
#     {
#         path = "${path.module}/../../lambda_fns/entry_predict_input_request"
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
#         "Resource": [aws_sqs_queue.reserved_entry_input_queue_predict.arn]
#     }
#     ]
#     })

#     provisioned_concurrent_executions = 5

#     environment_variables = {
#         ENTRY_PREDICT_INPUT_QUEUE = aws_sqs_queue.reserved_entry_input_queue_predict.id
#     }
# }

resource "aws_lambda_event_source_mapping" "reserved_entry_prediction_trigger" {
  event_source_arn = aws_sqs_queue.reserved_entry_input_queue_predict.arn
  function_name    = "${module.reserved_predict_entry_fn.lambda_function_arn}:${module.reserved_predict_entry_fn.lambda_function_version}"
}

module "reserved_predict_entry_fn" {
    source = "terraform-aws-modules/lambda/aws"
    publish = true

    function_name = "reserved-entry-prediction-handler-${var.environment}"
    handler = "app.predict_entry_handler"
    runtime = "python3.8"
    timeout = 60

    source_path = [
    {
        path = "${path.module}/../../lambda_fns/entry_predict"
    }
    ]

    attach_policy_json    = true

    policy_json = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:InvokeFunction",
                    "sagemaker:InvokeEndpoint",
                    "sqs:SendMessage",
                    "sqs:ReceiveMessage",
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes",
                    "sqs:GetQueueUrl",
                    "sqs:ListQueues",
                    "sqs:SendMessageBatch",
                ],
                "Resource": [
                    aws_sqs_queue.reserved_entry_input_queue_predict.arn,
                    aws_sqs_queue.reserved_entry_input_processed_queue_predict.arn,
                    "arn:aws:sagemaker:us-east-1:${data.aws_caller_identity.reserved_current.account_id}:endpoint/${var.model_endpoint_name}",
                    "arn:aws:lambda:us-east-1:${data.aws_caller_identity.reserved_current.account_id}:function:${var.geolocation_fn_name}",
                    "arn:aws:lambda:us-east-1:${data.aws_caller_identity.reserved_current.account_id}:function:${var.reliability_fn_name}",
                    "arn:aws:lambda:${var.aws_region}:${data.aws_caller_identity.reserved_current.account_id}:function:${var.model_info_fn_name}-${var.environment}"
                ]
            }
        ]
    })

    provisioned_concurrent_executions = var.environment == "dev" ? 1 : 10
    reserved_concurrent_executions = 30

    environment_variables = {
        PREDICTION_QUEUE = aws_sqs_queue.reserved_entry_input_processed_queue_predict.id
        MODEL_ENDPOINT_NAME = var.model_endpoint_name
        GEOLOCATION_FN_NAME = var.geolocation_fn_name
        RELIABILITY_FN_NAME = var.reliability_fn_name
        MODEL_INFO_FN_NAME = "${var.model_info_fn_name}-${var.environment}"
        ENVIRONMENT = "${var.environment}"
        SENTRY_URL = "${var.sentry_url}"
    }
}

resource "aws_appautoscaling_target" "reserved_predict_entry_fn_autoscale" {
    max_capacity       = var.environment == "dev" ? 1 : 10
    min_capacity       = var.environment == "dev" ? 1 : 5
    resource_id        = "function:${module.reserved_predict_entry_fn.lambda_function_name}:${module.reserved_predict_entry_fn.lambda_function_version}"
    scalable_dimension = "lambda:function:ProvisionedConcurrency"
    service_namespace  = "lambda"
}

#data "archive_file" "mappingfiles" {
#    type = "zip"
#    output_path = "${path.module}/../../python.zip"
#    source_dir = "${path.module}/../../mappings"
#}

resource "aws_lambda_event_source_mapping" "reserved_entry_prediction_output" {
  event_source_arn = aws_sqs_queue.reserved_entry_input_processed_queue_predict.arn
  function_name    = "${module.reserved_entry_predict_output_fn.lambda_function_arn}:${module.reserved_entry_predict_output_fn.lambda_function_version}"
}

module "reserved_entry_predict_output_fn" {
    source = "terraform-aws-modules/lambda/aws"
    publish = true

    function_name = "reserved-entry-prediction-output-handler-${var.environment}"
    handler = "app.entry_predict_output_handler"
    runtime = "python3.8"
    timeout = 30

    source_path = [
    {
        path = "${path.module}/../../lambda_fns/entry_predict_output_request"
        pip_requirements = "${path.module}/../../lambda_fns/entry_predict_output_request/requirements.txt"
    }
    ]

    attach_policy_json = true

    policy_json = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sqs:ReceiveMessage",
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes",
                    "sqs:GetQueueUrl",
                    "sqs:ListQueues",
                ],
                "Resource": [
                    aws_sqs_queue.reserved_entry_input_processed_queue_predict.arn,
                    aws_sqs_queue.reserved_entry_failed_msgs_dlq_predict.arn
                ]
            }
        ]
    })

    provisioned_concurrent_executions = var.environment == "dev" ? 1 : 5

    layers = ["${aws_lambda_layer_version.reserved_lambda_layer_mappings.arn}"]

    build_in_docker = true
    #store_on_s3 = true
    #s3_bucket = "${var.processed_docs_bucket}"

    environment_variables = {
        ENVIRONMENT = "${var.environment}"
        SENTRY_URL = "${var.sentry_url}"
    }
}

resource "aws_lambda_layer_version" "reserved_lambda_layer_mappings" {
    filename   = "${path.module}/../../lambda_layers/mappings/python.zip"
    layer_name = "reserved_tags_mapping_layer"

    compatible_runtimes = ["python3.8"]
    source_code_hash = base64sha256("${path.module}/../../lambda_layers/mappings/python.zip")
}

resource "aws_appautoscaling_target" "reserved_entry_predict_output_fn_autoscale" {
    max_capacity       = var.environment == "dev" ? 1 : 5
    min_capacity       = var.environment == "dev" ? 1 : 2
    resource_id        = "function:${module.reserved_entry_predict_output_fn.lambda_function_name}:${module.reserved_entry_predict_output_fn.lambda_function_version}"
    scalable_dimension = "lambda:function:ProvisionedConcurrency"
    service_namespace  = "lambda"
}

resource "aws_lambda_event_source_mapping" "reserved_transfer_dlq_msgs_lambda_trigger" {
  event_source_arn = aws_sqs_queue.reserved_entry_failed_msgs_dlq_predict.arn
  function_name    = "${module.reserved_entry_predict_transfer_dlq_msg.lambda_function_arn}:${module.reserved_entry_predict_transfer_dlq_msg.lambda_function_version}"
}

module "reserved_entry_predict_transfer_dlq_msg" {
    source = "terraform-aws-modules/lambda/aws"
    publish = true

    function_name = "reserved-entry-predict-transfer-dlq-msg-${var.environment}"
    handler = "app.entry_predict_dlq_msgs_handler"
    runtime = "python3.8"
    timeout = 30

    source_path = [
        {
            path = "${path.module}/../../lambda_fns/entry_predict_dlq_msgs"
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
                    aws_sqs_queue.reserved_entry_input_processed_queue_predict.arn,
                    aws_sqs_queue.reserved_entry_failed_msgs_dlq_predict.arn
                ]
            }
        ]
    })

    provisioned_concurrent_executions = var.environment == "dev" ? 1 : 5

    environment_variables = {
        PREDICTION_QUEUE = aws_sqs_queue.reserved_entry_input_processed_queue_predict.id
    }
}

resource "aws_appautoscaling_target" "reserved_entry_predict_transfer_dlq_msg_autoscale" {
    max_capacity       = var.environment == "dev" ? 1 : 5
    min_capacity       = var.environment == "dev" ? 1 : 2
    resource_id        = "function:${module.reserved_entry_predict_transfer_dlq_msg.lambda_function_name}:${module.reserved_entry_predict_transfer_dlq_msg.lambda_function_version}"
    scalable_dimension = "lambda:function:ProvisionedConcurrency"
    service_namespace  = "lambda"
}
