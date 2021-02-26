# Network Setup
data "aws_availability_zones" "available" {}

resource "aws_vpc" "main_vpc" {
  cidr_block = var.networking["main_vpc_cidr_block"]
  enable_dns_hostnames = true

  tags = {
    Name = var.networking["main_vpc_name"]
  }
}

resource "aws_subnet" "main_subnet_00" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = var.networking["main_subnet_00"]
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = var.networking["main_subnet_00_name"]
  }
}

resource "aws_internet_gateway" "main_gw" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    Name = var.networking["main_igw_name"]
  }
}

# Route tables
resource "aws_route_table" "main_subnet_00" {
  vpc_id = aws_vpc.main_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_gw.id
  }
  tags = {
    Name = var.networking["main_subnet_00_route_table_name"]
  }
}

resource "aws_route_table_association" "main_subnet_00" {
  subnet_id      = aws_subnet.main_subnet_00.id
  route_table_id = aws_route_table.main_subnet_00.id
}