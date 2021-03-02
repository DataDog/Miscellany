# Admin SG
resource "aws_security_group" "admin" {
  name        = "admin"
  description = "Allow inbound SSH traffic to Admin VPC from allowed IPs"
  vpc_id      = aws_vpc.main_vpc.id
  tags = {
    Name = "BrightOps Main Admin Security Group"
  }
}

resource "aws_security_group_rule" "ingress_ssh_admin_allowed_cidrs" {
    type        = "ingress"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidrs
    security_group_id = aws_security_group.admin.id
}
resource "aws_security_group_rule" "ingress_https_admin_allowed_cidrs" {
    type        = "ingress"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidrs
    security_group_id = aws_security_group.admin.id
}

resource "aws_security_group_rule" "ingress_winrm_ssl_admin_allowed_cidrs" {
    type        = "ingress"
    from_port   = 5986
    to_port     = 5986
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidrs
    security_group_id = aws_security_group.admin.id
}

resource "aws_security_group_rule" "ingress_rdp_admin_allowed_cidrs" {
    type        = "ingress"
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidrs
    security_group_id = aws_security_group.admin.id
}

resource "aws_security_group_rule" "ingress_winrm_admin_allowed_cidrs" {
    type        = "ingress"
    from_port   = 5985
    to_port     = 5985
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidrs
    security_group_id = aws_security_group.admin.id
}

resource "aws_security_group_rule" "egress_admin" {
    type            = "egress"
    from_port       = 0
    to_port         = 0
    protocol = "-1"
    security_group_id = aws_security_group.admin.id
    source_security_group_id = aws_security_group.internal.id
}

resource "aws_security_group_rule" "egress_admin_all" {
    type            = "egress"
    from_port       = 0
    to_port         = 0
    protocol = "-1"
    security_group_id = aws_security_group.admin.id
    cidr_blocks = ["0.0.0.0/0"]
}

# Internal SG
resource "aws_security_group" "internal" {
  name        = "internal"
  description = "Allow all inbound traffic to the Internal VPC from Admin SG and SELF SG"
  vpc_id      = aws_vpc.main_vpc.id
  tags = {
    Name = "BrightOps Main Internal Security Group"
  }
}

resource "aws_security_group_rule" "ingress_internal_from_admin" {
    type            = "ingress"
    from_port       = 0
    to_port         = 0
    protocol = "-1"
    security_group_id = aws_security_group.internal.id
    source_security_group_id = aws_security_group.admin.id
}

resource "aws_security_group_rule" "ingress_internal" {
    type            = "ingress"
    from_port       = 0
    to_port         = 0
    protocol = "-1"
    security_group_id = aws_security_group.internal.id
    source_security_group_id = aws_security_group.internal.id
}

resource "aws_security_group_rule" "egress_internal" {
    type            = "egress"
    from_port       = 0
    to_port         = 0
    protocol = "-1"
    security_group_id = aws_security_group.internal.id
    cidr_blocks = ["0.0.0.0/0"]
}