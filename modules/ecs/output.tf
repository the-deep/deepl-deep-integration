output private_subnet_id {
    value = aws_subnet.private[0].id
}

output ecs_cluster_id {
    value = aws_ecs_cluster.cluster.id
}

output ecs_task_definition {
    value = aws_ecs_task_definition.task-def.arn
}

output ecs_container_name {
    value = var.ecs_container
}