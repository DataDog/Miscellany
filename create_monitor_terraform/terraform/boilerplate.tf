#
# Require version of terraform
# https://www.terraform.io/docs/configuration/terraform.html
#
terraform {
  required_version = ">= 0.11.2"
}
#
# DD Provider: https://www.terraform.io/docs/providers/datadog/index.html
#
provider "datadog" {
  # Define DATADOG_API_KEY and DATADOG_APP_KEY in environment variables
}
#
# AWS Provider: https://www.terraform.io/docs/providers/aws/index.html
#
provider "aws" {
  region = "${var.aws_region}"
  # Define Auth via Environment, Shared Creds file, etc as documented in
  # https://www.terraform.io/docs/providers/aws/index.html#environment-variables
}
#
# Get the availability zones for our given region
# https://www.terraform.io/docs/providers/aws/d/availability_zones.html
#
data "aws_availability_zones" "available" {}
