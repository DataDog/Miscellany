# Logs related Webhooks
The Datadog API for [Logs](https://docs.datadoghq.com/logs/) has several categories for general [Logs](https://docs.datadoghq.com/api/latest/logs/), [Archives](https://docs.datadoghq.com/api/latest/logs-archives/), [Indexes](https://docs.datadoghq.com/api/latest/logs-indexes/), [Metrics](https://docs.datadoghq.com/api/latest/logs-metrics/), [Pipelines](https://docs.datadoghq.com/api/latest/logs-pipelines/) and [Restriction queries](https://docs.datadoghq.com/api/latest/logs-restriction-queries/).

Several of the API calls requires using HTTP PUT rather than POST. Since Webhooks only use the POST method, we use utilize Synthetics Tests to perform the PUT method and trigger these Tests to run via Webhook as needed.

Once the Synthetics Tests are created, use the [Synthetics trigger Webhook](/webhooks/Synthetics) to create associated Webhooks. The Webhooks will be used as a notification channel for Monitors.

## Getting started
First complete the general Webhook Getting started.
Set up the [Synthetics trigger Webhook](/webhooks/Synthetics).

## Synthetics API Test setup

### Create Synthetics API Test
Create [Synthetic API HTTP Test](https://docs.datadoghq.com/synthetics/api_tests/http_tests). Use a PUT method with the URL listed below.

Expand Advanced Options. Create these 2 Request Headers (see [Synthetics trigger Webhook](/webhooks/Synthetics) for creating variables).
 - DD_API_KEY = `{{ DD_API_KEY }}`
 - DD_APPLICATION_KEY = `{{ DD_APPLICATION_KEY }}`

 ![request headers](/webhooks/images/request_headers.png)

 Click *Request Body* and set the *Body Type* to `application/json`. Paste in the `synthetics-payload` JSON for the [Request Body](https://docs.datadoghq.com/synthetics/api_tests/http_tests/?tab=requestbody).

 Give the Test a meaningful name such as:
 ```
 Disable exclusion filter {exclusion_filter_name} on {index_name}
 ```

 Keep in mind that the Index will be updated when the **Test URL** button is used. Be sure to set the state of the Index as needed.

 **Define assertions**: When status code is 200

 **Select locations**: Choose 1 location to run the test from.

 **Specify test frequency**: 1 days.

 **Notify your team**: Create a message to notify if this test fails.
 ```
The Synthetics Test to disable exclusion filter {exclusion_filter_name} on {index_name} has failing.

Check the Index exclusion filter to confirm appropriate state.
```

 After creating the Test, click the *Pause Scheduling* button at the top right corner.

## Synthetics setup
| Synthetics Payload JSON                          | URL                                                               | Description                                                       |
|--------------------------------------------------|-------------------------------------------------------------------|-------------------------------------------------------------------|
| [synthetics-payload_disable_exclusion_filter.json](/webhooks/Logs/synthetics-payload_disable_exclusion_filter.json) | https://api.datadoghq.com/api/v1/logs/config/indexes/{index_name} | Disable an exclusion filter for Debug logs on a given index_name  |
| [synthetics-payload_enable_exclusion_filter.json](/webhooks/Logs/synthetics-payload_enable_exclusion_filter.json)  | https://api.datadoghq.com/api/v1/logs/config/indexes/{index_name} | Enable an exclusion filter for Debug logs on a given index_name   |
| [synthetics-payload_set_main_index_limit.json](/webhooks/Logs/synthetics-payload_set_main_index_limit.json)     | https://api.datadoghq.com/api/v1/logs/config/indexes/main         | Set a [daily quota](https://docs.datadoghq.com/logs/log_configuration/indexes#set-daily-quota) on the default "main" index                     |
|                                                  |                                                                   |                                                                   |
|                                                  |                                                                   |                                                                   |

## Considerations
For the use case of disabling/enabling exclusion filters, be sure to return the filter to it's original state when the alert resolves.

## Resources
* [Datadog Logs configuration](https://docs.datadoghq.com/logs/log_configuration/)
