variable "networking" {
  type = map
  description = "Network info for the VPC and it's subnets"
  default = {
    # VPC and IGW Details
    main_vpc_cidr_block = "10.12.23.0/24" # Small subnet for testing, feel free to change
    main_vpc_name = "Datadog Main VPC"
    main_igw_name = "Datadog Internet Gateway for Main VPC"
    # Subnet Details
    main_subnet_00 = "10.12.23.0/27" # 30 useable IPs
    main_subnet_00_name = "Datadog Main Subnet 00"
    main_subnet_00_route_table_name = "Datadog Route Table for Main Subnet 00"
    main_subnet_01 = "10.12.23.32/28" # 14 useable IPs
    main_subnet_01_name = "Datadog Main Subnet 01"
    main_subnet_01_route_table_name = "Datadog Route Table for Main Subnet 01"
    main_subnet_02 = "10.12.23.48/28" # 14 useable IPs
    main_subnet_02_name = "Datadog Main Subnet 02"
    main_subnet_02_route_table_name = "Datadog Route Table for Main Subnet 02"
  }
}

variable "allowed_cidrs" {
  type = list(string)
  description = "Allowed CIDRs for the Admin Security Group"
  default = ["0.0.0.0/0"]
}

variable "aws_region" {
  type = string
  description = "AWS Default Region"
  default = "CHANGEME"
}

variable "owner_id" {
  type = string
  description = "Account Owner ID for looking up AMIs"
  default = "CHANGEME"
  sensitive = true
}

variable "ddog_api_key" {
  type = string
  description = "Datadog API Key"
  default = "CHANGEME"
  sensitive = true
}

variable "iam" {
  type = map
  description = "IAM Policy Info"
  default = {
    iam_role_name = ""
    iam_instance_profile_name = ""
    iam_policy_name = ""
  }
}

variable "sg_info" {
  type = map
  description = "Security Group Info"
  default = {
    admin_sg_name = "Admin SG"
    internal_sg_name = "Internal SG"
  }
}

variable "admin_sg_name" {
    type = string
    description = "Friendly name for the Admin Security Group"
    default = "Admin SG"
}

variable "internal_sg_name" {
    type = string
    description = "Friendly name for the Internal Security Group"
    default = "Internal SG"
}

variable "instance_info" {
    type = map
    description = "Instance Info for each O/S"
    default = {
      ubuntu_xenial_name = "Ubuntu Xenial Datadog Instance"
      ubuntu_xenial_instance_type = "t2.micro"
      ubuntu_xenial_ami_string    = "ddog-ubuntu-xenial-*"
    }
}
variable "ssh_key" {
  type = map
  description = "EC2 instance SSH key settings"
  default = {
    name = "My Super Awesome SSH key"
    file = "/change/path/to/publick-key"
  }
}