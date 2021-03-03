from datadog import initialize, api
import requests
import json
import time
import sys
import argparse

## Arguments to run the script

parser = argparse.ArgumentParser()
parser.add_argument("integration", type=str,
                    help="specify the integration namespace for your dashboard. Ex: mysql, ntp, system")
parser.add_argument("--site", "-s", type=str, default="us", choices=["us", "eu"], 
	help="The site to send data, us (datadoghq.com) or eu (datadoghq.eu), default: us")
parser.add_argument("--verbosity", type=int, help="increase output verbosity, use --verbosity 1 to enable")
args = parser.parse_args()
integration = args.integration

## Keys and timeframe

api_key = "<API KEY>"
app_key = "<APP KEY>"
timestamp = int(time.time()) - 86400

if str(args.site) == "eu":
	api_host = "https://api.datadoghq.eu/"
	dashboard_site = "https://app.datadoghq.eu"
else:
	api_host = "https://app.datadoghq.com/"
	dashboard_site = "https://app.datadoghq.com"
## Init

options = {
    'api_key': str(api_key),	
    'app_key': str(app_key),
    'api_host': str(api_host)
}

initialize(**options)

## Metrics endpoint

r = requests.get(api_host + "api/v1/metrics?api_key="+ api_key + "&application_key=" + app_key + "&from="+str(timestamp)+"")

r.json()
metrics_list = []

print("init: ", metrics_list)

for i in range(len(r.json()['metrics'])):
	if integration in  r.json()['metrics'][i]:
		metrics_list.append(r.json()['metrics'][i])

## Resiliency: Test if metrics are available for the integration
if len(metrics_list)>0:
	print("you have", len(metrics_list), "metrics available for "+ integration)
else:
	print("you don't have any metrics available for "+ integration + " try a longer timeframe or check the name of the integration")
	exit()

## Building the dashboard

title = integration
description = "All your "+ integration + " metrics"
widgets = []

print("building dashboard: ", title)

## Building each widget

for i in range(len(metrics_list)):

	#DEBUG
	if args.verbosity == 1:
		print("building widget: ", metrics_list[i])
	
	widgets.append({
        'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "avg:" + str(metrics_list[i]) + "{*} by {host}"}
        ],
        'title': str(metrics_list[i])
    }
	})

template_variables = [{
    "name": "host",
    "prefix": "host",
    "default": "*"
}]

is_read_only = True
layout_type = 'ordered'

#DEBUG
if args.verbosity == 1:
	print("These are your widgets: ", widgets)

try:
	dashboard = api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     template_variables=template_variables)
    
	print("dashboard for " + integration + " was successfully created check it out here: " + str(dashboard_site) + str(dashboard['url']))
	
	#DEBUG
	if args.verbosity == 1:
		print(dashboard)

except:
	print("Something went wrong, enable debug log by running python fullmetrics_dash.py <integration> 1, current error: ", sys.exc_info()[0])
	raise
