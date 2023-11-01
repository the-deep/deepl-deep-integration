data "aws_secretsmanager_secret" "sentry" {
    name = var.sentry_secret_name
}

data "aws_secretsmanager_secret_version" "latest_ver" {
    secret_id = data.aws_secretsmanager_secret.sentry.id
}

data "external" "sentry_json" {
  program = ["echo", "${data.aws_secretsmanager_secret_version.latest_ver.secret_string}"]
}