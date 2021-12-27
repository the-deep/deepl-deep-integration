resource "aws_sqs_queue" "entry_input_queue_predict" {
  name_prefix               = "entry-input-queue-predict-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 5

  tags = {
    Environment = "${var.environment}"
  }
}

resource "aws_sqs_queue" "entry_input_processed_queue_predict" {
  name_prefix               = "entry-input-processed-queue-predict-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 5
  redrive_policy            = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.entry_failed_msgs_dlq_predict.arn
    maxReceiveCount     = 4
  })

  tags = {
    Environment = "${var.environment}"
  }
}

resource "aws_sqs_queue" "entry_failed_msgs_dlq_predict" {
  name_prefix               = "entry-input-failed-msgs-dlq-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 5

  tags = {
      Environment = "${var.environment}"
  }
}

module "entry_input_pred_request_fn" {
    source = "terraform-aws-modules/lambda/aws"

    function_name = "entry-input-pred-func-${var.environment}"
    handler = "app.entry_msg_sqs_handler"
    runtime = "python3.8"
    timeout = 30

    source_path = [
    {
        path = "${path.module}/../../lambda_fns/entry_request_input_pred"
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
            "sqs:GetQueueUrl",
            "sqs:ListQueues",
            "sqs:SendMessageBatch"
        ],
        "Resource": ["*"]
    }
    ]
    })

    environment_variables = {
        ENTRY_PREDICT_INPUT_QUEUE = aws_sqs_queue.entry_input_queue_predict.id
    }
}

resource "aws_lambda_event_source_mapping" "entry_prediction_trigger" {
  event_source_arn = aws_sqs_queue.entry_input_queue_predict.arn
  function_name    = module.predict_entry_fn.lambda_function_arn
}

module "predict_entry_fn" {
    source = "terraform-aws-modules/lambda/aws"
    function_name = "entry-prediction-handler-${var.environment}"
    handler = "main.predict_entry_handler"
    runtime = "python3.8"

    source_path = [
    {
        path = "${path.module}/../../lambda_fns/predict_entry"
    }
    ]

    attach_policy_json    = true

    policy_json = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:*",
                    "sagemaker:InvokeEndpoint",
                    "sqs:SendMessage",
                    "sqs:ReceiveMessage",
                    "sqs:DeleteMessage",
                    "sqs:GetQueueAttributes",
                    "sqs:GetQueueUrl",
                    "sqs:ListQueues",
                    "sqs:SendMessageBatch",
                ],
                "Resource": ["*"]
            }
        ]
    })

    environment_variables = {
        PREDICTION_QUEUE = aws_sqs_queue.entry_input_processed_queue_predict.id
        EP_NAME_MODEL = var.ep_name_model
    }
}

#data "archive_file" "mappingfiles" {
#    type = "zip"
#    output_path = "${path.module}/../../python.zip"
#    source_dir = "${path.module}/../../mappings"
#}

resource "aws_lambda_event_source_mapping" "entry_prediction_output" {
  event_source_arn = aws_sqs_queue.entry_input_processed_queue_predict.arn
  function_name    = module.entry_predict_output_fn.lambda_function_arn
}

module "entry_predict_output_fn" {
    source = "terraform-aws-modules/lambda/aws"
    function_name = "entry-prediction-output-handler-${var.environment}"
    handler = "app.entry_predict_output_handler"
    runtime = "python3.8"

    source_path = [
    {
        path = "${path.module}/../../lambda_fns/entry_predict_output"
        pip_requirements = "${path.module}/../../lambda_fns/entry_predict_output/requirements.txt"
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
                "Resource": ["*"]
            }
        ]
    })

    layers = ["${aws_lambda_layer_version.lambda_layer.arn}"]

    build_in_docker = true
    store_on_s3 = true
    s3_bucket = "${var.processed_docs_bucket}"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = "${path.module}/../../python.zip"
  layer_name = "tags_mapping_layer"

  compatible_runtimes = ["python3.8"]
}

module "entry_predict_transfer_dlq_msg" {
    source = "terraform-aws-modules/lambda/aws"

    function_name = "entry-predict-transfer-dlq-msg-${var.environment}"
    handler = "app.entry_predict_dlq_msgs_handler"
    runtime = "python3.8"

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
                "Resource": ["*"]
            }
        ]
    })

    environment_variables = {
        PREDICTION_QUEUE = aws_sqs_queue.entry_input_processed_queue_predict.id
    }
}

resource "aws_lambda_event_source_mapping" "transfer_dlq_msgs_lambda_trigger" {
  event_source_arn = aws_sqs_queue.entry_failed_msgs_dlq_predict.arn
  function_name    = module.entry_predict_transfer_dlq_msg.lambda_function_arn
}