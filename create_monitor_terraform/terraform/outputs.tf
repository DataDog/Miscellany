#############################################################################
# Outputs
# https://www.terraform.io/docs/configuration/outputs.html
#############################################################################
output "datadog_common_disk_full_monitor_id" {
    value = "${datadog_monitor.common_disk_full.id}"
}
output "datadog_cpu_high_module_monitor_id" {
    value = "${module.cpu_monitor.id}"
}
