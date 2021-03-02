locals { 
  ami_name_prefix = "ddog-ubuntu-xenial"
  region = "us-east-2"
  instance_type = "t2.micro"
  ddog_url = "datadoghq.com" # Change to datadoghq.eu for EU
  ddog_major_version = "7"
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
  # Uncomment if you want to use a custom subnet
  # subnet_id = "CHANGEME"
}

source "amazon-ebs" "ubuntu-xenial" {
  ami_name      = "${local.ami_name_prefix}-${local.timestamp}"
  instance_type = local.instance_type
  region        = local.region
  # Uncomment the subnet_id if you are using a custom subnet
  # subnet_id     = local.subnet_id
  associate_public_ip_address = true
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-xenial-16.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu-xenial"]

  provisioner "shell" {
      inline = [
          "sudo apt-get update -y",
          "sudo apt-get install awscli -y",
          "sudo DD_AGENT_MAJOR_VERSION=${local.ddog_major_version} DD_API_KEY=PREINSTALL DD_INSTALL_ONLY=true DD_SITE=\"${local.ddog_url}\" bash -c \"$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)\""
        ]
  }
}

