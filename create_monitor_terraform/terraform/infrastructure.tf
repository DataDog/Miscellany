# TODO: [ckelner] could be better served by breaking into seperate files
# Note: [ckelner] `${terraform.workspace}` is references in places, but this
# repo does not make heavy use of workspaces, see the Hashicorp docs for more
# info: https://www.terraform.io/docs/state/workspaces.html
################################################################################
#################### NETWORKING ################################################
################################################################################
#
# Hashicorp AWS VPC Module: https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/1.17.0
#
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name = "vpc-example"
  cidr = "10.0.0.0/16"
  azs             = ["${data.aws_availability_zones.available.names}"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Terraform = "true"
    Environment = "dev"
  }
}
#
# AWS Firewalls
#
# Example using a module
# https://github.com/ckelner/tf_aws_http_sg
#
module "http_security_group" {
  source      = "github.com/ckelner/tf_aws_http_sg"
  vpc_id      = "${module.vpc.vpc_id}"
  name_prefix = "${var.common_name}-${terraform.workspace}"
  description = "For allowing HTTP Traffic to the web node"
  tags        = {
    "Terraform" = "true"
    "Environment" = "${terraform.workspace}"
  }
}
#
# Security Group not using a module
# https://www.terraform.io/docs/providers/aws/r/security_group.html
#
resource "aws_security_group" "web_sg" {
  name_prefix = "${var.common_name}-${terraform.workspace}"
  description = "Security Group for web node SSH"
  vpc_id      = "${module.vpc.vpc_id}"
  tags        = {
    "Terraform" = "true"
    "Environment" = "${terraform.workspace}"
  }
}
#
# Security Group Rules
# https://www.terraform.io/docs/providers/aws/r/security_group_rule.html
#
resource "aws_security_group_rule" "inbound_ssh_from_anywhere" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = "${aws_security_group.web_sg.id}"
}
resource "aws_security_group_rule" "outbound_to_anywhere" {
  type            = "egress"
  from_port       = 0
  to_port         = 0
  protocol        = "-1"
  cidr_blocks     = ["0.0.0.0/0"]
  security_group_id = "${aws_security_group.web_sg.id}"
}
################################################################################
#################### COMPUTE ###################################################
################################################################################
#
# AWS SSH Key Pair; Public key is placed on instances to enable SSH
# https://www.terraform.io/docs/providers/aws/r/key_pair.html
#
resource "aws_key_pair" "aws_ssh_key" {
  key_name   = "${var.common_name}-${terraform.workspace}"
  public_key = "${var.aws_public_key_material}"
}
#
# Random Shuffle for choosing subnet
# https://www.terraform.io/docs/providers/random/r/shuffle.html
#
resource "random_shuffle" "subnet" {
  input = ["${module.vpc.public_subnets}"]
  result_count = 1
}
#
# AWS EC2 Instance
# https://www.terraform.io/docs/providers/aws/r/autoscaling_group.html
#
resource "aws_instance" "web" {
  ami = "${lookup(var.aws_amis, var.aws_region)}"
  instance_type = "${var.aws_instance_type}"
  vpc_security_group_ids = [
    "${aws_security_group.web_sg.id}",
    "${module.http_security_group.id}"
  ]
  # sticks this instance in a random subnet
  subnet_id = "${random_shuffle.subnet.result[0]}"
  # TODO: [ckelner] should be in it's own file and templatized
  # TODO: [ckelner] should probably use a provisoner like ansible, see the repo
  # for an example: https://github.com/ckelner/datadog-ansible-vagrant-terraform/blob/master/main.tf#L40-L60
  # TODO: [ckelner] would be good to configre the nginx Datadog integration YAML
  user_data = <<-EOF
              #!/bin/bash
              sudo yum install nginx -y
              sudo chkconfig nginx on
              sudo service nginx start
              # kelnerhax: rely on AWS firewalls instead, easier to manage as IaC
              sudo service iptables stop
              sudo chkconfig iptables off
              DD_API_KEY="${var.datadog_api_key}" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
              EOF
  key_name = "${aws_key_pair.aws_ssh_key.key_name}"
  associate_public_ip_address = true
  tags {
    "name" = "${var.common_name}-${terraform.workspace}"
    "terraform" = "true"
    "environment" = "${terraform.workspace}"
    "role" = "nginx"
    "creator" = "ckelner"
  }
}
