# Notebooks related Webhooks
[Notebooks](https://docs.datadoghq.com/notebooks/) can be helpful for tracking work and taking markdown notes alongside metrics charts. You may want to create a Notebook related to an Alert notification.

## Getting started
First complete the general Webhook Getting started.

## Considerations
The `create_notebook` example is a template which provides examples of different types of cell data that can be displayed. It may be helpful to prototype in a Notebook and export to JSON to easily copy/paste the proper cell format.

## Webhook setup
URL: https://api.datadoghq.com/api/v1/notebooks

| Payload JSON                            | Description                                                                                   |
|-----------------------------------------|-----------------------------------------------------------------------------------------------|
| [create_notebook.json ](/webhooks/Notebooks/create_notebook.json)                   | Create a Notebook containing Alert details ($EVENT_MSG)                                       |
| [list_webhook_variables_to_notebook.json](/webhooks/Notebooks/list_webhook_variables_to_notebook.json) | Creates a Notebook containing available Webhook Variables. Useful when working with Webhooks. |
|                                         |                                                                                               |
|                                         |                                                                                               |

## Resources
* [Datadog Notebook API](https://docs.datadoghq.com/api/latest/notebooks/)
* [Webhook integration doc](https://docs.datadoghq.com/integrations/webhooks)