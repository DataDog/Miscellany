# Webhooks
This is a collection of [Webhooks](https://docs.datadoghq.com/integrations/webhooks/) which use the Datadog API.

## About creating Webhooks
Webhooks only perform a POST request against a given URL. Each Webhook will require the following fields:

**URL** - The URL for the Datadog API endpoint.
**Payload** - This will be the *body* of the POST request. It needs to be in JSON format.
**Custom headers** - These are used to authenticate against the Datadog API.
**Custom variables** - These are values which you may want to re-use between webhooks. They can be referenced within the URL, Payload, or custom headers.
**Built-in variables** - Webhooks by default have a collection of variables about the Alert, Event, etc where they are called. Here is the full [list of variables](https://docs.datadoghq.com/integrations/webhooks/#usage)

## Getting started
Install the Webhooks integration through the [Datadog Integrations page](https://app.datadoghq.com/account/settings#integrations/webhooks).
You'll want to create new Variables for the Webhook authentication. These will store the [Datadog API and Application keys](https://docs.datadoghq.com/account_management/api-app-keys/) you want to use for the Webhooks.
 - $DD_API_KEY
 - $DD_APPLICATION_KEY

 For every Webhook you create, use the following Custom Headers:
 ```
 {
"Content-Type": "application/json",
"DD-API-KEY": "$DD_API_KEY",
"DD-APPLICATION-KEY": "$DD_APPLICATION_KEY"
}
```

## Resources
* [Datadog API docs](https://docs.datadoghq.com/api/latest/)
* [Webhook integration doc](https://docs.datadoghq.com/integrations/webhooks)
* [Calling on Datadog's API with the Webhooks Integration](https://docs.datadoghq.com/developers/guide/calling-on-datadog-s-api-with-the-webhooks-integration/)
* [Send SMS alerts with webhooks and Twilio](https://www.datadoghq.com/blog/send-alerts-sms-customizable-webhooks-twilio/)
