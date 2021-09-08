# Incidents related Webhooks
[Incidents](https://docs.datadoghq.com/monitors/incident_management) are closely tied with Alerts. Here we have an example of creating an Incident with an Alert notification. The Payload can be modified to set severity and other details.

## Getting started
First complete the general Webhook Getting started.

You will need to designate a user as the Incident Commander. This User ID can be added as a custom Webhook variable the same as API and Application keys.

To determine the User's ID use the following [User API call](https://docs.datadoghq.com/api/latest/users/). Replace `USERNAME` with part or all of the user's name or email address. The response is quite long but the user details should be at the end in the `data` block. You'll see the `id` below `"type": "users",`.

**cURL**
```
curl --location -g --request GET 'https://api.datadoghq.com/api/v2/users?filter=USERNAME&filter[status]=Active'
```

## Considerations
If the Alert is flapping, a large number of Incidents may be created. Keep this in mind when deciding which Alerts to use with this Webhook.

You may want to create multiple versions of this Webhook for different Severity levels or other specific details such as Incident Commander.

The Payload has an example of a markdown comment made to the Incident Timeline. This can be used as an example for your own custom message.

## Webhook setup
URL: https://api.datadoghq.com/api/v2/incidents

| Payload JSON               | Description                                                     |
|----------------------------|-----------------------------------------------------------------|
| [create_incident_SEV-1.json](webhooks/Incidents/create_incident_SEV-1.json) | Create a SEV1 Incident with details from the Alert notification |
|                            |                                                                 |
|                            |                                                                 |

To use your webhook, add @webhook-<WEBHOOK_NAME> in the text of the metric alert you want to trigger the webhook.

## Resources
* [Datadog Incidents API](https://docs.datadoghq.com/api/latest/incidents/)
* [Webhook integration doc](https://docs.datadoghq.com/integrations/webhooks)