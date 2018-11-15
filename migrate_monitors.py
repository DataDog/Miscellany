import json
import os
import requests
import pprint

from datadog import initialize, api

# source /opt/datadog/datadog-agent/venv/bin/activate

# FROM org

DD_API_KEY = os.getenv('DD_API_KEY', '') # from org api
DD_APP_KEY = os.getenv('DD_APP_KEY', '') # from org app

options = {
    'api_key': DD_API_KEY,
    'app_key': DD_APP_KEY
}

initialize(**options)
good_keys = ['tags', 'deleted', 'query', 'message', 'matching_downtimes', 'multi', 'name', 'type', 'options']

# tags example
search_string = 'env:system'
search_key = 'tags' # common fields: name, query, tags, type

# query example
# search_string = 'disk'
# search_key = 'query' # common fields: name, query, tags, type

# get all monitors w/ matching query string
monitors = api.Monitor.get_all()
new_monitors = []
for monitor in monitors:
    new_monitor = {}
    search_field = monitor[search_key]
    if search_string == search_field or search_string in search_field:
        for k, v in monitor.items():
            if k in good_keys:
                new_monitor[k] = v
        new_monitors.append(new_monitor)

#pprint.pprint(new_monitors)

# TO org

options = {
    'api_key': 'new_api', # to org api
    'app_key': 'new_app'  # to org app
}

initialize(**options)

for monitor_dict in new_monitors:
    res = api.Monitor.create(
        type=monitor_dict['type'],
        query=monitor_dict['query'],
        name=monitor_dict['name'],
        message=monitor_dict['message'],
        tags=monitor_dict['tags'],
        options=monitor_dict['options']
        )
    print(res)
