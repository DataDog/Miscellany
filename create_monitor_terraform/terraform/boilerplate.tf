#
# Require version of terraform
# https://www.terraform.io/docs/configuration/terraform.html
#
terraform {
  required_version = ">= 0.11.8"
}
#
# DD Provider: https://www.terraform.io/docs/providers/datadog/index.html
#
provider "datadog" {
  # Define DATADOG_API_KEY and DATADOG_APP_KEY in environment variables
}
