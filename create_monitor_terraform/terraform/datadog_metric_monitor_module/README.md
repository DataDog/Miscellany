# Datadog Metric by Host Monitor Module
A very simple module to create a Datadog metric monitor by host.

# Input Variables
- `name`: (Required) The name of the monitor
- `message`: (Required) The message for the monitor
- `tags`: (Required) Tags to filter on for the metric query
- `threshold`: (Required) The threshold that will trigger the monitor

# Usage
```hcl
module "my_metric_monitor" {
  source      = "./datadog_metric_monitor_module"
  name        = "My awesome monitor"
  message     = "Something is broke! Wake up @pagerduty"
  tags        = "role:demo"
  threshold   = 0.9
}
```

# Outputs
- `id` - the ID of the monitor
