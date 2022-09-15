from csv import excel_tab
from distutils.command.config import config
from multiprocessing.sharedctypes import Value
import re, requests
from typing_extensions import Self
from urllib import request, response
from datadog_api_client import ApiClient, Configuration, exceptions
from datadog_api_client.v1.api.metrics_api import MetricsApi as metrics_v1
from datadog_api_client.v2.api.metrics_api import MetricsApi as metrics_v2
from datadog_api_client.v2.model.metric_tag_configuration_type import MetricTagConfigurationType
from datadog_api_client.v2.model.metric_tag_configuration_update_attributes import (
    MetricTagConfigurationUpdateAttributes,
)
from datadog_api_client.v2.model.metric_tag_configuration_update_data import MetricTagConfigurationUpdateData
from datadog_api_client.v2.model.metric_tag_configuration_update_request import MetricTagConfigurationUpdateRequest

## Supported Metric Types of this script
metric_types = [
    "gauge",
    "count",
    "rate"
]

## Default aggregations by type
default_aggr = {
        "gauge" :{
            "time":"avg",
            "space":"avg"
        },
        "count" :{
            "time":"sum",
            "space":"sum"
        },
        "rate" :{
            "time":"sum",
            "space":"sum"
        },
}

class metric_details:
    def __init__(self, metric_name):
        self.metric_name = metric_name
        self.metric_type = None
        self.active_tags = []
        self.active_aggregations = []
        self.estimated_ingested = 0
        self.estimated_indexed = 0
        self.current_config_state = None

metric_names = [
    "example_metric_1",
    "example_metric_2"
]

configuration = Configuration(
    api_key = {
        "apiKeyAuth":"<API KEY>",
        "appKeyAuth":"<APPLICATION KEY>"
    },
)

with ApiClient(configuration) as api_client:
    for metric_name in metric_names:
        api_instance = metrics_v1(api_client)
        metric = metric_details(metric_name)
        response = api_instance.get_metric_metadata(
            metric_name=metric.metric_name,
        )
        if response['type'] not in metric_types:
            print(f'Metric: {metric.metric_name} is not a suitable metric type for this script. Moving to next metric...')
            continue 
        metric.metric_type=response['type']
        api_instance = metrics_v2(api_client)
        ## TODO: update this to the official ddog library when released
        active_response = requests.get(
            url=f'https://api.datadoghq.com/api/v2/metrics/{metric.metric_name}/active-configurations',
            headers={
                "DD-API-KEY":configuration.api_key["apiKeyAuth"],
                "DD-APPLICATION-KEY":configuration.api_key["appKeyAuth"],
                "Accept": "application/json"
            }
        )
        metric.active_tags = active_response.json()['data']['attributes']['active_tags']
        metric.active_aggregations = active_response.json()['data']['attributes']['active_aggregations']
        if default_aggr[metric.metric_type] not in metric.active_aggregations: metric.active_aggregations.append(default_aggr[metric.metric_type])

        try:
            response = api_instance.list_tag_configuration_by_name(
                metric_name=metric.metric_name,
            )
            metric.current_config_state = True if "tags" in response['data']['attributes'] else False
        except (exceptions.NotFoundException,NameError,KeyError):
            metric.current_config_state = False

        response = api_instance.list_volumes_by_metric_name(
            metric_name=metric.metric_name,
        )
        metric.estimated_ingested = response['data']['attributes']['ingested_volume']
        
        try:
            response = api_instance.estimate_metrics_output_series(
                metric_name=metric.metric_name,
                filter_groups=','.join(metric.active_tags),
                filter_num_aggregations= len(metric.active_aggregations)
            )
            metric.estimated_indexed = response['data']['attributes']['estimated_output_series']
        except exceptions.ApiException: 
            print(f'Unable to determine a MWL estimate for {metric.metric_name}, skipping.')
            continue

        if metric.current_config_state and metric.estimated_ingested < metric.estimated_indexed:
            api_instance.delete_tag_configuration(
                metric_name=metric.metric_name,
            )
            print(f'Metric: {metric.metric_name}\nEstimated without MWL: {metric.estimated_ingested}\nEstimated with MWL: {metric.estimated_indexed}\nCleared previous MWL configuration for {metric.metric_name}, it is better to not use MWL here.')
        elif metric.current_config_state and metric.estimated_ingested > metric.estimated_indexed:
            body = MetricTagConfigurationUpdateRequest(
                data=MetricTagConfigurationUpdateData(
                    type=MetricTagConfigurationType("manage_tags"),
                    id=metric.metric_name,
                    attributes=MetricTagConfigurationUpdateAttributes(
                        tags=metric.active_tags,
                        aggregations=metric.active_aggregations
                    ),
                ),
            )
            response = api_instance.update_tag_configuration(
                metric_name=metric.metric_name,
                body=body
            )
            print(f'Metric: {metric.metric_name}\nEstimated without MWL: {metric.estimated_ingested}.\nEstimated with MWL: {metric.estimated_indexed}\nApplied active tags as MWL configuration for {metric.metric_name}, it is better to use MWL here.')
        else:
            print(f'Metric: {metric.metric_name}\nEstimated without MWL: {metric.estimated_ingested}.\nEstimated with MWL: {metric.estimated_indexed}\nNo previous MWL configuration existed for {metric.metric_name} and it is better to not use MWL here.')
