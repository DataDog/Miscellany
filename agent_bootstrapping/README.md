# Datadog Agent Bootstrapping

How to automate the Datadog Agent install into various build and deployment processes.

* [Link](./packer_terraform_aws/README.md) | Build an AMI that is updated with the Datadog agent pre-installed using Packer, then deploy the same image using Terraform while enabling the agent by pulling the API key from AWS Secrets Manager.
  * Tech Used:
    * Packer
    * Terraform
    * AWS EC2, VPC, IAM and Secrets Manager