resource "aws_sqs_queue" "input_queue" {
  name_prefix               = "input-queue-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 5

  tags = {
    Environment = "${var.environment}"
  }
}

resource "aws_sqs_queue" "processed_queue" {
  name_prefix               = "processed-queue-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 5
  redrive_policy            = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.failed_msgs_dlq.arn
    maxReceiveCount     = 4
  })

  tags = {
    Environment = "${var.environment}"
  }
}

resource "aws_sqs_queue" "failed_msgs_dlq" {
  name_prefix               = "failed-msgs-dlq-${var.environment}-"
  delay_seconds             = 0
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 5

  tags = {
      Environment = "${var.environment}"
  }
}

module "input_request_fn" {
    source = "terraform-aws-modules/lambda/aws"

    function_name = "te-input-func-${var.environment}"
    handler = "app.send_msg_sqs"
    runtime = "python3.8"
    timeout = 30

    source_path = [
    {
        path = "${path.module}/../../lambda_fns/input_request"
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
            "sqs:SendMessageBatch",
            "s3:GetObject"
        ],
        "Resource": ["*"]
    }
    ]
    })

    environment_variables = {
        INPUT_QUEUE = aws_sqs_queue.input_queue.id
    }
}

resource "aws_lambda_event_source_mapping" "sqs_to_extract_lambda_trigger" {
  event_source_arn = aws_sqs_queue.input_queue.arn
  function_name    = module.extract_docs_fn.lambda_function_arn
}

module "predict_entry_fn" {
    source = "terraform-aws-modules/lambda/aws"

    function_name = "entry-prediction-handler-${var.environment}"
    handler = "app.predict_entry_handler"
    runtime = "python3.8"
    timeout =  60

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
                    "sagemaker:InvokeEndpoint"
                ],
                "Resource": ["*"]
            }
        ]
    })

    environment_variables = {
        EP_NAME_MODEL = var.ep_name_model
    }
}

module "extract_docs_fn" {
    source = "terraform-aws-modules/lambda/aws"

    function_name = "te-extract-docs-func-${var.environment}"
    handler = "app.process_docs"
    runtime = "python3.8"
    timeout = 30

    source_path = [
    {
        path = "${path.module}/../../lambda_fns/extract_docs"
        pip_requirements = "${path.module}/../../lambda_fns/extract_docs/requirements.txt"
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
                    "sqs:GetQueueUrl",
                    "sqs:ListQueues",
                    "sqs:SendMessageBatch",
                    "s3:PutObject"
                ],
                "Resource": ["*"]
            }
        ]
    })

    build_in_docker = true
    store_on_s3 = true
    s3_bucket = "${var.processed_docs_bucket}"

    environment_variables = {
        INPUT_QUEUE = aws_sqs_queue.input_queue.id
        DEST_S3_BUCKET = "${var.processed_docs_bucket}"
        PROCESSED_QUEUE = aws_sqs_queue.processed_queue.id
    }
}

module "output_request_fn" {
    source = "terraform-aws-modules/lambda/aws"

    function_name = "te-output-request-func-${var.environment}"
    handler = "app.output_request"
    runtime = "python3.8"
    timeout = 30

    source_path = [
        {
            path = "${path.module}/../../lambda_fns/output_request"
            pip_requirements = "${path.module}/../../lambda_fns/output_request/requirements.txt"
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
                "Resource": ["*"]
            }
        ]
    })

    build_in_docker = true
    store_on_s3 = true
    s3_bucket = "${var.processed_docs_bucket}"

    environment_variables = {
        SIGNED_URL_EXPIRY_SECS = "${var.signed_url_expiry_secs}"
    }
}

resource "aws_lambda_event_source_mapping" "sqs_to_output_lambda_trigger" {
  event_source_arn = aws_sqs_queue.processed_queue.arn
  function_name    = module.output_request_fn.lambda_function_arn
}

module "transfer_dlq_msg" {
    source = "terraform-aws-modules/lambda/aws"

    function_name = "te-transfer-dlq-msg-func-${var.environment}"
    handler = "app.dlq_msgs_handler"
    runtime = "python3.8"
    timeout = 30

    source_path = [
        {
            path = "${path.module}/../../lambda_fns/dlq_msgs"
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
        PROCESSED_QUEUE = aws_sqs_queue.processed_queue.id
    }
}

resource "aws_lambda_event_source_mapping" "transfer_dlq_msgs_lambda_trigger" {
  event_source_arn = aws_sqs_queue.failed_msgs_dlq.arn
  function_name    = module.transfer_dlq_msg.lambda_function_arn
}