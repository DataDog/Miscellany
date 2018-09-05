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
  query = "avg(last_5m):max:system.disk.in_use{${var.tags}} by {host} > ${var.threshold}"
  thresholds {
    critical = "${var.threshold}"
  }
  notify_no_data = false
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
variable "threshold" {
  description = "The threshold to trip the monitor into alert status"
}
#############################################################################
# Outputs
#############################################################################
output "id" {
    value = "${datadog_monitor.metric_monitor.id}"
}
