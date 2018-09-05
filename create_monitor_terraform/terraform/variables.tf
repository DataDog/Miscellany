#############################################################################
# Variables
# https://www.terraform.io/docs/configuration/variables.html
#############################################################################
variable "common_name" {
  description = "The common environment name to use for most resources."
  default = "datadog-demo"
}
# For example purposes
variable "monitor_suffix" {
  default = "Kelner Example from Terraform"
  description = "A suffix that gets applied to end of monitor names"
}
