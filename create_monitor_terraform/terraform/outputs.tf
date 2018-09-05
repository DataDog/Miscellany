#############################################################################
# Outputs
# https://www.terraform.io/docs/configuration/outputs.html
#############################################################################
output "vpc_id" {
    value = "${module.vpc.vpc_id}"
}
output "subnet_ids" {
    value = ["${module.vpc.public_subnets}"]
}
output "instance_id" {
    value = "${aws_instance.web.id}"
}
output "instance_ip" {
    value = "${aws_instance.web.public_ip}"
}
output "datadog_common_disk_full_monitor_id" {
    value = "${datadog_monitor.common_disk_full.id}"
}
output "datadog_cpu_high_module_monitor_id" {
    value = "${module.cpu_monitor.id}"
}
