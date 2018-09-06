# Datadog Metric by Host Monitor Module
A very simple module to create a Datadog metric monitor by host.
See:
- https://www.terraform.io/docs/providers/datadog/r/monitor.html
- https://docs.datadoghq.com/api/?lang=python#create-a-monitor

# Input Variables
- `name`: (Required) The name of the monitor
- `query`: (Required) The query to use for the metric monitor
- `message`: (Required) The message for the monitor
- `critical-threshold`: (Required) The critical threshold that will trigger the monitor
- `warning-threshold`: (Required) The warning threshold that will trigger the monitor
- `critical-recovery`: (Required) The critical recovery threshold that will take the monitor out of an alert state
- `warning-recovery`: (Required) The warning recovery threshold that will take the monitor out of an warning state

# Usage
```hcl
module "my_metric_monitor" {
  source               = "./datadog_metric_monitor_module"
  name                 = "My awesome monitor"
  query                = "avg(last_5m):max:system.cpu.user{${var.tags}} by {host} > 0"
  message              = "Something is broke! Wake up @pagerduty"
  tags                 = "role:demo"
  critical-threshold   = 100,
  warning-threshold    = 90,
  critical-recovery    = 90,
  warning-recovery     = 75
}
```

# Outputs
- `id` - the ID of the monitor
