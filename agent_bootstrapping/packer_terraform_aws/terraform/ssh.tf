resource "aws_key_pair" "ddog_ssh_key" {
  key_name   = var.ssh_key["name"]
  public_key = file(var.ssh_key["file"])
}