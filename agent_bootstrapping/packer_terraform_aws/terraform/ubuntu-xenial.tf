# EC2 Setup
data "aws_ami" "ubuntu_xenial" {
  most_recent = true

  filter {
    name   = "name"
    values = [var.instance_info["ubuntu_xenial_ami_string"]]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = [var.owner_id]
}

data "template_file" "ubuntu_xenial_user_data" {
  template = file("./user_data/enable_ddog_agent_ubuntu_xenial.sh.tpl")

  vars = {
    secret_id = aws_secretsmanager_secret.ddog_api_key.name
  }
}

resource "aws_instance" "ddog_instance_ubuntu_xenial" {
  count = 0
  ami = data.aws_ami.ubuntu_xenial.id
  instance_type = var.instance_info["ubuntu_xenial_instance_type"]
  key_name = var.ssh_key["name"]
  associate_public_ip_address = true
  subnet_id = aws_subnet.main_subnet_00.id
  vpc_security_group_ids = [aws_security_group.admin.id, aws_security_group.internal.id]
  iam_instance_profile = aws_iam_instance_profile.ddog_api_key.id
  user_data = data.template_file.ubuntu_xenial_user_data.rendered
  tags = {
    Name = var.instance_info["ubuntu_xenial_name"]
  }
}