# Datadog Metric by Host Monitor Module
A very simple module to create a Datadog metric monitor by host.
See: https://www.terraform.io/docs/providers/datadog/r/monitor.html

# Input Variables
- `name`: (Required) The name of the monitor
- `message`: (Required) The message for the monitor
- `tags`: (Required) Tags to filter on for the metric query
- `critical-threshold`: (Required) The critical threshold that will trigger the monitor
- `warning-threshold`: (Required) The warning threshold that will trigger the monitor

# Usage
```hcl
module "my_metric_monitor" {
  source               = "./datadog_metric_monitor_module"
  name                 = "My awesome monitor"
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
