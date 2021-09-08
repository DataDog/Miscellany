# Synthetics related Webhooks
These examples use the [Synthetics](https://docs.datadoghq.com/synthetics/) API endpoint. Running a Synthetics Test from Webhook allows for more flexibility when working with API calls. Synthetics Test for example, can do other HTTP methods besides POST.

## Getting started
First complete the general Webhook Getting started.

You will need to create [Synthetics Global Variables(https://docs.datadoghq.com/synthetics/settings/?tab=specifyvalue#global-variables)] for your Datadog API and Application keys.
 - DD_API_KEY
 - DD_APPLICATION_KEY

These will need to be added to each Test as Request-Headers under Advanced Options > [Request Options](https://docs.datadoghq.com/synthetics/api_tests/http_tests?tab=requestoptions). The `content-type` header will be added automatically when setting the *Request Body* to `application/json`.

![request headers](/webhooks/images/request_headers.png)

**Finding the Synthetic Test** `public_id`:
You will need the `public_id` for the Synthetic Test you want to run. This can be found in the URL when viewing a Test. The `public_id` for the following example is `bxt-grk-tuv`:
```
https://app.datadoghq.com/synthetics/details/bxt-grk-tuv
```
The `public_id` can also be found using the [Datadog Synthetics API](https://docs.datadoghq.com/api/latest/synthetics/#get-the-list-of-all-tests).

## Considerations
When setting up these tests you will typically want these to be paused. This way they will only run when the Webhook is called.

When using a Synthetics Test to create/update an API endpoint, only a single location should be used. This will prevent possible data issues. For example, if you're updating a Notebook with a new cell, you would create multiple new cells if running from more than one location.

## Webhook setup
URL: https://api.datadoghq.com/api/v1/synthetics/tests/trigger/ci

| Payload JSON                 | Description                   |
|------------------------------|-------------------------------|
| [trigger_synthetics_test.json](/webhooks/Synthetics/trigger_synthetic_test.json) | Trigger a Synthetics Test now |
|                              |                               |
|                              |                               |

## Resources
* [Datadog Synthetics docs](https://docs.datadoghq.com/synthetics/)
* [Datadog Synthetics API docs](https://docs.datadoghq.com/api/latest/synthetics/)