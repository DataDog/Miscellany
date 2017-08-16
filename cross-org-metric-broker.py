from datadog import initialize, api 
import sys
import time
import json
import yaml

def load_config():
    f = open(str(sys.path[0] + '/cross-org-metric-broker.yaml'))
    config = yaml.safe_load(f)
    f.close()

    return config

def get_metrics(auth_key, metrics):
    options = {
        'api_key': auth_key['api_key'],
        'app_key': auth_key['app_key']
    }
    initialize(**options)

    end = int(time.time())
    start = end - 60

    results = []
    for metric in metrics:
        result = api.Metric.query(start=start, end=end, query=metric['metric'])
        results.append(result)

    return results

def post_metrics(auth_key, customer_name, hostname, pointlist, metric_name):
    options = {
        'api_key': auth_key['primary_api_key'],
        'app_key': auth_key['primary_app_key']
    }
    initialize(**options)

    CurrentPosixTime = time.time()
    CurrentPosixTime10 = time.time() + 10

    api.Metric.send(metric=metric_name, points=pointlist, host=hostname, tags=["customer:"+customer_name])


def convert_pointlist_to_seconds(pointlist):
    plc = len(pointlist)

    for i in range(0, plc):
        point = pointlist[i]
        time = point[0] / 1000
        point[0] = time
        pointlist[i] = point

    return pointlist

def add_host_tag(auth_key, hostname, customer_name):
    options = {
        'api_key': auth_key['primary_api_key'],
        'app_key': auth_key['primary_app_key']
    }

    initialize(**options)

    api.Tag.create(hostname, tags=["customer:"+customer_name])


def process_metrics():
    config = load_config()
    primary_key = config['init_config']
    customer_keys = config['instances']
    metrics = config['metrics']

    for customer_key in customer_keys:
        customer_name = customer_key['account_name']

        metric_data = get_metrics(customer_key, metrics)

        for payload in metric_data:
            for series in payload['series']:
                pointlist = convert_pointlist_to_seconds(list(series['pointlist']))
                metric_name = str(series['expression'])
                metric_name = metric_name.rpartition('{')[0]
                hostname = series['scope']

                print "account name: " + customer_name
                print "metric name: " + metric_name
                print "metric data: " + str(pointlist)

                post_metrics(primary_key, customer_name, hostname, pointlist, metric_name)
                add_host_tag(primary_key, hostname, customer_name)

process_metrics()
