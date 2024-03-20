"""
List tags by metric name returns "Success" response

"""
import json
from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
# using readlines()
file1 = open('path/to/file/having/list/of/metrics', 'r')
Lines = file1.readlines()
 
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    metric = line.strip()
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = ""
    configuration.api_key["appKeyAuth"] = ""
    #get list of all tags of the metric
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.list_tags_by_metric_name(
            metric_name = metric,
        )
        #split to fetch just tag name and not value
        tags = [tag.split(":")[0] for tag in response['data']['attributes']['tags']]
        list_alltags = []
        for tag in tags:
           list_alltags.append(tag)
        myset_alltags = set(list_alltags)
    #get list of active tags of the same metric    
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.list_active_metric_configurations(
        metric_name= metric,
        )
        active_tags = response['data']['attributes']['active_tags']
        myset_active = set(active_tags)
        #get the list of unused tags by subtracting active tags from all tags list 
        missing = list(sorted(myset_alltags - myset_active))
        print("metric:", metric,"All tags: ",myset_alltags,"Active tags: ",myset_active,"Unused tags: ",missing)
