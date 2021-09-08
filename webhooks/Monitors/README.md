# Monitor related Webhooks
When working with [Datadog Monitors](https://docs.datadoghq.com/monitors/monitor_types/), the Monitors API allows for various functionality. The focus of these examples are on muting to help reduce Alert noise/fatigue.

The API typically can only work with one monitor at a time. Since it does not handle an array of Monitor IDs, there are some limitations to working with this API with Webhooks. For more complex evaluation, consider using a Lambda to create more complex Alert handling.

## Getting started
First complete the general Webhook Getting started.

## Considerations
The API endpoints used here require using a built-in variable for hostname within the URL.

The host unmute endpoint does not require a Payload.

When muting a host, a custom message can be added to the Payload which will display on the Host Muted Event.

Be sure to unmute host when the alert resolves.

## Webhook setup
| Payload JSON   | URL                                                    | Description                                       |
|----------------|--------------------------------------------------------|---------------------------------------------------|
| [mute_host.json](/webhooks/Monitors/mute_host.json) | https://api.datadoghq.com/api/v1/host/$HOSTNAME/mute   | Mute the host to prevent additional notifications |
| [NONE]         | https://api.datadoghq.com/api/v1/host/$HOSTNAME/unmute | Unmute host when the Alert has recovered          |
|                |                                                        |                                                   |
|                |                                                        |                                                   |

## Resources
* [Datadog Alert Monitors API](https://docs.datadoghq.com/api/latest/monitors/)
* [Datadog Hosts API](https://docs.datadoghq.com/api/latest/hosts/)