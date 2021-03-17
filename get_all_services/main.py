#!/usr/bin/env python
import argparse
import os
import time
import requests
import json
import re

def searchMetrics(config, query):
    headers = {
        'DD-API-KEY': config["api_key"],
        'DD-APPLICATION-KEY': config["app_key"]
    }
    params = {
        'q': 'metrics:{}'.format(query)
    }
    url = '{}api/v1/search'.format(config["api_host"])
    r = requests.get(url, headers=headers, params=params)
    return r.json()

def queryTimeseries(config, metric_query):
    headers = {
        'DD-API-KEY': config["api_key"],
        'DD-APPLICATION-KEY': config["app_key"]
    }
    current_time = int(time.time())
    days = 15
    params = {
        'query': metric_query,
        'from': current_time - 60 * 60 * 24 * days,
        'to': current_time
    }
    url = '{}api/v1/query'.format(config["api_host"])
    r = requests.get(url, headers=headers, params=params)
    return r.json()

def searchTraceHitsMetrics(config):
    metrics = searchMetrics(config, 'trace.').get('results', {}).get('metrics', [])
    res = {}
    for m in metrics:
        pattern = re.compile(".*\.hits$")
        if pattern.match(m):
            res[m] = res.get(m, 0) + 1
    resArr = []
    for attr, value in res.items():
        resArr.append(attr)
    return resArr

def getTagValuesForMetric(config, metric_name, tags):
    metric_query = metric_name + '{*} by {' + ','.join(tags) + '}'
    timeseries = queryTimeseries(config, metric_query).get('series', [])
    tag_combinations = []
    for s in timeseries:
        expression = s.get('expression', '')
        tag_values = re.search('\{(.*)\}', expression)
        # tag_combinations.append(tag_values[0])
        tag_combinations.append(tag_values[1].split(","))
    print("getTagValuesForMetric - metric_name:" + metric_name + ", tag keys: " + ','.join(tags))
    return tag_combinations

def getAllServices(config, secondary_primary_tag = None):
    metrics = searchTraceHitsMetrics(config)
    tagKeys = ["env", "service"]
    if secondary_primary_tag is not None:
        tagKeys.append(secondary_primary_tag)
    res = []
    for m in metrics:
        tagCombinations = getTagValuesForMetric(config, m, tagKeys)
        res = res + tagCombinations
    return res

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create an empty dashboard for testing purposes")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    parser.add_argument(
        "-s", "--apiHost", help="Your Datadog api host (default: https://api.datadoghq.com/ for eu: https://api.datadoghq.eu/)", type=str, default="https://api.datadoghq.com/")
    parser.add_argument(
        "-t", "--secondaryPrimaryTag", help="Your secondary primary tag", type=str, default=None)
    args = parser.parse_args()
    api_key = args.apikey or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv("DD_APP_KEY", None)
    apiHost = args.apiHost or "https://api.datadoghq.com/"
    secondaryPrimaryTag = args.secondaryPrimaryTag or None
    errors = []
    if not api_key:
        errors.append("""
                      You must supply your Datadog API key by either passing a
                      -k/--apikey argument or defining a DD_API_KEY environment
                      variable.""")
    if not app_key:
        errors.append("""
                      You must supply your Datadog application key by either
                      passing a -a/--appkey argument or defining a DD_APP_KEY
                      environment variable.""")
    if errors:
        for error in errors:
            # print textwrap.dedent(error)
            print(error)
        sys.exit(2)

    # START: Initialize the Datadog client
    config = {
        "api_host": apiHost,
        "api_key": api_key,
        "app_key": app_key,
    }
    # END: Initialize the Datadog client
    services = getAllServices(config, secondaryPrimaryTag)
    print(services)
