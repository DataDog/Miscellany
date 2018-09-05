#
# Datadog Monitor w/o Module
# https://www.terraform.io/docs/providers/datadog/r/monitor.html
#
# Note: take note of how we can include terraform values in our monitor's
# template -- if we wanted a very specific monitor for a specific host, where
# we likely had some very static resource, we could include things like the ip
# address for that host easily by invoking `${aws_instance.web.public_ip}` - but
# typically you'd want to leverage datadog to get this information, e.g.
# `{{host.ip}}` as you see in the second example; this only serves as an example
resource "datadog_monitor" "common_disk_full" {
  name = "[${var.common_name}] {{host.name}} {{device.name}} disks are full - [${var.monitor_suffix}]"
  type = "metric alert"
  message = <<EOT
  {{host.name}} with ip ${aws_instance.web.public_ip} disk are full, let's
  understand why @slack-channel

  {{#is_alert}}

  Disk space is critical, above {{threshold}}
  @pagerduty-Datadog-Demo

  {{/is_alert}}

  ## Links
  ** provisioned by terraform, [modify here](https://github.com/ckelner/terraform-datadog) or your changes will be discarded **
EOT
  # note that we are using the `role` tag we applied to our EC2 instance
  query = "avg(last_5m):max:system.disk.in_use{role:nginx} by {name,host,device} > 0.9"
  thresholds {
    warning = 0.8
    critical = 0.9
  }
  notify_no_data = false
  tags = ["service:nginx", "team:example"]
}
#
# Datadog Monitor w/ local Module
# https://www.terraform.io/docs/providers/datadog/r/monitor.html
#
module "cpu_monitor" {
  source      = "./datadog_metric_monitor_module"
  name        = "[${var.common_name}] {{host.name}} CPU is {{value}} - [${var.monitor_suffix}]"
  message     = <<EOT
  {{host.name}} w/ ip {{host.ip}} CPU is high!
  CPU has been above {{threshold}} for the last 5 minutes!
  @pagerduty-Datadog-Demo
EOT
  tags        = "role:demo"
  threshold   = 0.9
}
