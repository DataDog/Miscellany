#
# Datadog Monitor w/o Module
# https://www.terraform.io/docs/providers/datadog/r/monitor.html
#
resource "datadog_monitor" "common_disk_full" {
  name = "[${var.common_name}] {{host.name}} {{device.name}} disks are full - [${var.monitor_suffix}]"
  type = "metric alert"
  message = <<EOT
  {{host.name}} disk are full, let's understand why @slack-channel-testing123

  {{#is_alert}}

  Disk space is critical, above {{threshold}}
  @pagerduty-Datadog-Demo-Test

  {{/is_alert}}
EOT
  query = "avg(last_5m):max:system.disk.in_use{role:nginx} by {name,host,device} > 0.9"
  thresholds {
    warning = 0.8
    critical = 0.9
    warning_recovery  = 0.79
    critical_recovery = 0.89
  }
  notify_no_data = false
  evaluation_delay = 360
  no_data_timeframe = 20
  include_tags = true
  tags = ["cake:test", "solutions-engineering", "kelner:hax", "service:nginx", "team:example"]
}
#
# Datadog Monitor w/ local Module
# https://www.terraform.io/docs/providers/datadog/r/monitor.html
#
module "cpu_monitor" {
  source              = "./datadog_metric_monitor_module"
  name                = "[${var.common_name}] {{host.name}} CPU is {{value}} - [${var.monitor_suffix}]"
  message             = <<EOT
  {{host.name}} w/ ip {{host.ip}} CPU is high!
  CPU has been above {{threshold}} for the last 5 minutes!
  @pagerduty-Datadog-Demo
EOT
  query               = "avg(last_5m):max:system.cpu.user{role:demo} by {host} >= 1"
  critical-threshold  = 1
  warning-threshold   = 0.95
  warning-recovery    = 0.9
  critical-recovery   = 0.97
}
