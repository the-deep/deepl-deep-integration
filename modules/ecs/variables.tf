variable aws_region {}

variable az_count {}

variable environment {}

variable ecs_task_execution_role {}

variable fargate_cpu {}

variable fargate_memory {}

variable app_count {}

variable app_image {}

variable cidr_block {}

variable ecs_cluster_name {
    default = "deepex-parser-ecs-cluster"
}

variable ecs_task_definition {
    default = "deepex-parser-ecs-task"
}

variable ecs_service {
    default = "deepex-parser-ecs-service"
}

variable ecs_container {
    default = "deepex-parser-container"
}