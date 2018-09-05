#############################################################################
# Variables
# https://www.terraform.io/docs/configuration/variables.html
#############################################################################
variable "aws_region" {
  description = "The region to provision AWS resources in."
}
variable "common_name" {
  description = "The common environment name to use for most resources."
  default = "datadog-demo"
}
variable "aws_vpc_cidr_block" {
  description = "The CIDR block to use for the AWS VPC."
  default = "10.0.0.0/16"
}
variable "aws_vpc_cidr_public_subnets" {
  description = "The public subnet CIDR blocks"
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}
variable "aws_amis" {
  description = "AWS AMIs for Amazon Linux 2017.03.0 (HVM) with SSD Volume."
  default = {
    "us-east-1" = "ami-55ef662f"
    "us-east-2" = "ami-15e9c770"
    "us-west-2" = "ami-bf4193c7"
    "ca-central-1" = "ami-d29e25b6"
  }
}
variable "aws_instance_type" {
  default = "t2.nano"
  description = "The AWS instance type to launch."
}
variable "aws_public_key_material" {
  description = "The public SSH key material to load onto the instances."
}
variable "datadog_api_key" {
  description = "The Datadog API Key. This should be set via environment variable: 'export TF_VAR_DATADOG_API_KEY=<your-api-key>'"
}
# For example purposes
variable "monitor_suffix" {
  default = "Kelner Example from Terraform"
  description = "A suffic that gets applied to end of monitor names"
}
