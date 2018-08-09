#-*- coding: utf-8 -*-

# stdlib
import time

# 3rd party
import requests
import datadog


api_key = '<API_KEY>'
app_key = '<APPLICATION KEY>'

options = {
    'api_key': api_key,
    'application_key': app_key
}

datadog.initialize(**options)


BASE_URL = 'https://api.datadoghq.com/api/v1/'

ENDPOINTS = [
    'query', # https://docs.datadoghq.com/api/?lang=bash#query-time-series-points
    'graph/snapshot', # https://docs.datadoghq.com/api/?lang=bash#graph-snapshot
    'metrics', # https://docs.datadoghq.com/api/?lang=bash#get-list-of-active-metrics
]


PARAMS = {

    'query': {
        'from': int(time.time() - 3600),
        'to': int(time.time()),
        'query': 'system.cpu.idle{*}by{host}'
    },

    'graph/snapshot': {
        'metric_query': 'system.load.1{*}',
        'start': int(time.time() - 3600),
        'end': int(time.time()),
    },

    'metrics': {
        'from': int(time.time()) - 60
    },

}



API_QUANTITIES = [
    'X-RateLimit-Limit',
    'X-RateLimit-Period',
    'X-RateLimit-Remaining',
    'X-RateLimit-Reset',
]


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


###### Get the data

payload = []

for endpoint in ENDPOINTS:

    url = BASE_URL + endpoint
    params = merge_two_dicts(options,PARAMS[endpoint])

    # print "endpoint: %s" %endpoint
    # print "url: %s" %url
    # print "params"
    # print params

    res = requests.get(url, params=params)

    # print "res.headers"
    # print res.headers

    for qu in API_QUANTITIES:
        payload.append({
            'metric': qu,
            'points': int(res.headers[qu]),
            'tags': ["endpoint:%s"%endpoint]
        })

# Post metrics

datadog.api.Metric.send(payload)
