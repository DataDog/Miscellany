#!/bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
  export AWS_DEFAULT_REGION=`curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | jq -c -r .region`
  ddog_api_key=`aws secretsmanager get-secret-value --secret-id ${secret_id} --query SecretString --output text`
  sed -i "s/PREINSTALL/$ddog_api_key/" /etc/datadog-agent/datadog.yaml
  systemctl enable datadog-agent
  systemctl restart datadog-agent
