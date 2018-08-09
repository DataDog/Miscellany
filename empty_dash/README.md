# Empty Dashboard
This script will create an empty dashboard to test a scenario where a customer
had updated a dashboard and passed in `graph=None` to the python client library
and then was unable to load the https://app.datadoghq.com/dash/list page. The
customer would receive a `500` error code when trying to load this page after
updating a dashboard w/ this parameter. This code does not seem to re-create the
scenario the customer was experiencing but may be useful to build upon in the
future.

# Run Code
- Setup a python virtualenv: `virtualenv empty_dash`
- Activate the virtualenv: `source empty_dash/bin/activate`
- Run `pip install -r requirements.txt`
- Run `python empty_dash.py -k <your-api-key> -a <your-app-key>`
  - Alternatively set `DATADOG_API_KEY` or `DD_API_KEY` and `DATADOG_APP_KEY` or
    `DD_APP_KEY` as environment variables
