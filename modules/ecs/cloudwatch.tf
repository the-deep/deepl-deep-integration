resource "aws_cloudwatch_log_group" "testapp_log_group" {
  name              = "/ecs/deepex-parser-${var.environment}"
  retention_in_days = 30

  tags = {
    Name = "cw-log-group-deepex-parser-${var.environment}"
  }
}

resource "aws_cloudwatch_log_stream" "myapp_log_stream" {
  name           = "log-stream-deepex-parser-${var.environment}"
  log_group_name = aws_cloudwatch_log_group.testapp_log_group.name
}