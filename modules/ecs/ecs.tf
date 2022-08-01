resource "aws_ecs_cluster" "cluster" {
  name = "${var.ecs_cluster_name}-${var.environment}"
}

data "template_file" "config" {
  template = file("./modules/ecs/templates/ecr_image/image.json")

  vars = {
    container_name = var.ecs_container
    app_image      = var.app_image
    fargate_cpu    = var.fargate_cpu
    fargate_memory = var.fargate_memory
    aws_region     = var.aws_region
    environment    = var.environment
  }
}

resource "aws_ecs_task_definition" "task-def" {
  family                   = "${var.ecs_task_definition}-${var.environment}"
  task_role_arn            = aws_iam_role.ecs-custom-tasks.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  container_definitions    = data.template_file.config.rendered
}

resource "aws_ecs_service" "service" {
  name            = "${var.ecs_service}-${var.environment}"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task-def.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"

  network_configuration {
    #security_groups  = [aws_security_group.ecs_sg.id]
    subnets          = aws_subnet.private.*.id
    assign_public_ip = false
  }

  depends_on = [
    aws_iam_role_policy_attachment.ecs_task_execution_role,
    aws_iam_role_policy_attachment.ecs-tasks
  ]
}