resource "aws_secretsmanager_secret" "ddog_api_key" {
  name = "ddog_api_key"
}

resource "aws_secretsmanager_secret_version" "ddog_api_key" {
  secret_id     = aws_secretsmanager_secret.ddog_api_key.id
  secret_string = var.ddog_api_key
}