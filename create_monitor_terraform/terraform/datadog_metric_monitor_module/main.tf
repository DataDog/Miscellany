#
# Datadog Monitor Module
# https://www.terraform.io/docs/providers/datadog/r/monitor.html
#
# TODO: [ckelner] This only really serves as an example, you'd ideally want to
# variablize many more of these values unless you had a common pattern across
# all your alarms or a tier of alarms, e.g. `avg(last_5m)` and so on
resource "datadog_monitor" "metric_monitor" {
  name = "${var.name}"
  type = "metric alert"
  message = "${var.message}"
  query = "avg(last_5m):max:system.disk.in_use{${var.tags}} by {host}"
  thresholds {
    critical          = "${var.critical-threshold}"
    warning           = "${var.warning-threshold}"
    warning_recovery  = "${var.warning-recovery}"
    critical_recovery = "${var.critical-recovery}"
  }
  evaluation_delay = 360
  no_data_timeframe = 20
  include_tags = true
  notify_no_data = false
  tags = ["cake:test", "solutions-engineering", "kelner:hax"]
}
#############################################################################
# Variables
#############################################################################
variable "name" {
  description = "The name of the monitor"
}
variable "message" {
  description = "The message for the monitor"
}
variable "tags" {
  description = "The tags to narrow the query"
}
variable "critical-threshold" {
  description = "The critical threshold to trip the monitor into alert status"
}
variable "warning-threshold" {
  description = "The warning threshold to trip the monitor into warning status"
}
variable "warning-recovery" {
  description = "The threshold to resolve the monitor's warning status"
}
variable "critical-recovery" {
  description = "The threshold to resolve the monitor's alert status"
}
#############################################################################
# Outputs
#############################################################################
output "id" {
    value = "${datadog_monitor.metric_monitor.id}"
}
