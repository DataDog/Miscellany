from datadog import initialize, api
import requests
import json
import time
import sys
import argparse

## Arguments to run the script

parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", type=int, help="increase output verbosity, use --verbosity 1 to enable")
parser.add_argument("integration", type=str,
                    help="specify the integration namespace for your dashboard. Ex: mysql, ntp, system")
args = parser.parse_args()
integration = args.integration

## Keys and timeframe

api_key = "xxx"
app_key = "xxx"
timestamp = int(time.time()) - 86400


## Init

options = {
    'api_key': str(api_key),
    'app_key': str(app_key)
}

initialize(**options)

## Metrics endpoint

r = requests.get("https://app.datadoghq.com/api/v1/metrics?api_key="+ api_key + "&application_key=" + app_key + "&from="+str(timestamp)+"")

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
graphs = []

print("building dashboard: ", title)

## Building each widget

for i in range(len(metrics_list)):

	#DEBUG
	if args.verbosity == 1:
		print("building widget: ", metrics_list[i])
	
	graphs.append({
	    "definition": {
	        "events": [],
	        "requests": [
	            {"q": "avg:" + str(metrics_list[i]) + "{$host} by {host}"} # changing unicode str to regular str
	        ],
	    "viz": "timeseries"
	    },
	    "title": str(metrics_list[i])
	})

template_variables = [{
    "name": "host",
    "prefix": "host",
    "default": "*"
}]

read_only = True

#DEBUG
if args.verbosity == 1:
	print("this is your graphs", graphs)

try:
	dashboard = api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
	print("dashboard for " + integration + " was successfully created check it out here: http://app.datadoghq.com/dash/"+ str(dashboard['dash']['id']))
	
	#DEBUG
	if args.verbosity == 1:
		print(dashboard)

except:
	print("Something went wrong, enable debug log by running python fullmetrics_dash.py <integration> 1, current error: ", sys.exc_info()[0])
	raise
