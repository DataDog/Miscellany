"""
 Metrics Without Limits Optimisation Tool

 This script will run through a provided list of metric names to obtain an allowlist of tags and aggregations
 that have been actively queried on by dashboards, notebooks, monitors, and through the API in the past 30 days
 and then apply these as a MWL tag configuration to a metric should the estimate MWL usage be less than using all tags.

 Please note: 
 - The script can and will by default overwrite existing tag configurations. 
 - The script only performs a comparison between the active queried configuration and all tags options.

 Requirements:
 - datadog_api_client version 2.3.0
 - requests version 2.28.1
"""

## List of metric names that should be checked.
metric_names = [
    "example.metric.1",
    "example.metric.2",
]

## Available Configuration Options
### ALL OPTIONS ARE REQUIRED ###
api_key = "<API KEY>" # Your Datadog API Key
app_key = "<APPLICATION KEY>" # Your Datadog APP Key
datadog_site = "datadoghq.com" # Select your datadog server
override_existing_tags = True # Set to False if you want to preserve your current MWL configurations (leaving as True will overwrite current configurations)
disable_metric = True # Set to False if you do not want this script to remove all tags from being queryable should a metric not be actively used
proxy_address = None # Only set if you need to run via a proxy
debug_mode = False # Enable debug mode for the datadog_api_client


############################################################################################################################
#############################                                                               ################################
############################# Note: It shouldnt't be neccesary to touch anything below here ################################
#############################                                                               ################################
############################################################################################################################


import requests, time
from datadog_api_client import ApiClient, Configuration, exceptions
from datadog_api_client.v1.api.metrics_api import MetricsApi as metrics_v1
from datadog_api_client.v2.api.metrics_api import MetricsApi as metrics_v2
from datadog_api_client.v2.model.metric_tag_configuration_type import MetricTagConfigurationType
from datadog_api_client.v2.model.metric_tag_configuration_create_attributes import (
    MetricTagConfigurationCreateAttributes,
)
from datadog_api_client.v2.model.metric_tag_configuration_update_attributes import (
    MetricTagConfigurationUpdateAttributes,
)
from datadog_api_client.v2.model.metric_tag_configuration_metric_types import MetricTagConfigurationMetricTypes
from datadog_api_client.v2.model.metric_tag_configuration_type import MetricTagConfigurationType
from datadog_api_client.v2.model.metric_tag_configuration_create_data import MetricTagConfigurationCreateData
from datadog_api_client.v2.model.metric_tag_configuration_create_request import MetricTagConfigurationCreateRequest
from datadog_api_client.v2.model.metric_tag_configuration_update_data import MetricTagConfigurationUpdateData
from datadog_api_client.v2.model.metric_tag_configuration_update_request import MetricTagConfigurationUpdateRequest

## Supported Metric Types of this script
metric_types = [
    "gauge",
    "count",
    "rate"
]

## Metric endpoint response error codes
common_error_codes = [400, 403, 404, 422]

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

## Data class
class metric_details:
    def __init__(self, metric_name, override_existing_tags=False, disable_metric=False):
        self.metric_name = metric_name
        self.metric_type = None
        self.active_tags = []
        self.active_aggregations = []
        self.estimated_ingested = 0
        self.estimated_indexed = 0
        self.current_config_state = None
        self.override_existing_tags = override_existing_tags
        self.update_metric = disable_metric

## Initialise the api client config
configuration = Configuration(
    api_key = {
        "apiKeyAuth": api_key,
        "appKeyAuth": app_key
    },
)
configuration.proxy = proxy_address
configuration.debug = debug_mode
configuration.server_variables["site"] = datadog_site

## Back off if we hit the rate limit
def rate_limit_sleeper(reset_remaining):
    print(f'Rate limited, backing off for {reset_remaining} seconds...')
    time.sleep(int(reset_remaining))


## Function to check and update an individual metric
def metric_check(configuration, metric_name, override_existing_tags, disable_metric):
    with ApiClient(configuration) as api_client:
        api_instance = metrics_v1(api_client)
        metric = metric_details(metric_name, override_existing_tags, disable_metric)

        ## Check metric type
        while True:
            try:
                response = api_instance.get_metric_metadata(
                    metric_name = metric.metric_name,
                )
            except Exception as e:
                if e.status == 429:
                    rate_limit_sleeper(e.headers['X-RateLimit-Reset'])
                    continue
                elif e.status in common_error_codes:
                    return({"error": f'Error encountered: {e.body["errors"]}'})
                else:
                    return({"error": f'Unhandled exception: {e}'})
            break
        if response['type'] not in metric_types:
            return({"error": f'{metric.metric_name} is not a suitable metric type for this script. Moving to next metric...'}) 
        metric.metric_type = response['type']
        
        api_instance = metrics_v2(api_client)
        ## get active configurations
        ## TODO: update this to the official ddog library when released
        while True:
            try:
                response = requests.get(
                    url = f'https://api.datadoghq.com/api/v2/metrics/{metric.metric_name}/active-configurations',
                    headers={
                        "DD-API-KEY":configuration.api_key["apiKeyAuth"],
                        "DD-APPLICATION-KEY":configuration.api_key["appKeyAuth"],
                        "Accept": "application/json",
                    },
                    params={
                        "window[seconds]": "2592000"
                    }
                )
                response.raise_for_status()
            except Exception as e:
                if response.status_code == 429:
                    reset_remaining = int(response.headers['X-RateLimit-Reset'])
                    print(f'Rate limited, backing off for {reset_remaining} seconds...')
                    time.sleep(reset_remaining)
                    continue
                else:
                    return({"error": f'Unhandled exception: {e}'})
            break
        metric.active_tags = response.json()['data']['attributes']['active_tags']
        metric.update_metric = (not len(metric.active_tags) and metric.update_metric) or len(metric.active_tags)
        metric.active_aggregations = response.json()['data']['attributes']['active_aggregations']
        if default_aggr[metric.metric_type] not in metric.active_aggregations: metric.active_aggregations.append(default_aggr[metric.metric_type])

        ## Get current tag configuration
        while True:
            try:
                response = api_instance.list_tag_configuration_by_name(
                    metric_name = metric.metric_name,
                )
                metric.current_config_state = True if "tags" in response['data']['attributes'] else False
            except (exceptions.NotFoundException,NameError,KeyError):
                metric.current_config_state = False
            except Exception as e:
                if e.status == 429:
                    rate_limit_sleeper(e.headers['X-RateLimit-Reset'])
                    continue
                elif e.status in common_error_codes:
                    return({"error": f'Error encountered: {e.body["errors"]}'})
                else:
                    return({"error": f'Unhandled exception: {e}'})
            break

        ## Get current estimate of ingestion volume
        while True:
            try:
                response = api_instance.list_volumes_by_metric_name(
                    metric_name = metric.metric_name,
                )
                metric.estimated_ingested = response['data']['attributes']['ingested_volume']
            except Exception as e:
                if e.status == 429:
                    rate_limit_sleeper(e.headers['X-RateLimit-Reset'])
                    continue
                elif e.status in common_error_codes:
                    return({"error": f'Error encountered: {e.body["errors"]}'})
                else:
                    return({"error": f'Unhandled exception: {e}'})
            break

        ## Get MWL estimation with active tag/aggr configuration
        while True:
            try:
                response = api_instance.estimate_metrics_output_series(
                    metric_name = metric.metric_name,
                    filter_groups = ','.join(metric.active_tags),
                    filter_num_aggregations = len(metric.active_aggregations)
                )
                metric.estimated_indexed = response['data']['attributes']['estimated_output_series']
            except exceptions.ApiException: 
                return({"error": f'Unable to determine a MWL estimate for {metric.metric_name}, skipping.'})
            except Exception as e:
                if e.status == 429:
                    rate_limit_sleeper(e.headers['X-RateLimit-Reset'])
                    continue
                elif e.status in common_error_codes:
                    return({"error": f'Error encountered: {e.body["errors"]}'})
                else:
                    return({"error": f'Unhandled exception: {e}'})
            break

        ## Update the tag configuration if needed
        ### Reset a metric to all tags if we want to overide a current configuration, and all tags is a better option than setting active tags/aggr
        if metric.override_existing_tags and metric.current_config_state and metric.estimated_ingested <= metric.estimated_indexed:
            while True:
                try:
                    api_instance.delete_tag_configuration(
                        metric_name = metric.metric_name,
                    )
                    return({"success": {'metric': metric.metric_name, 'ingest_estimate': metric.estimated_ingested, 'mwl_estimate': metric.estimated_indexed}})
                except Exception as e:
                    if e.status == 429:
                        rate_limit_sleeper(e.headers['X-RateLimit-Reset'])
                        continue
                    elif e.status in common_error_codes:
                        return({"error": f'Error encountered: {e.body["errors"]}'})
                    else:
                        return({"error": f'Unhandled exception: {e}'})
        ### Update a metric to have active tags/aggr as MWL config if overriding is allowed.
        elif metric.update_metric and metric.override_existing_tags and metric.current_config_state and metric.estimated_ingested > metric.estimated_indexed:
            body = MetricTagConfigurationUpdateRequest(
                data = MetricTagConfigurationUpdateData(
                    type = MetricTagConfigurationType("manage_tags"),
                    id = metric.metric_name,
                    attributes = MetricTagConfigurationUpdateAttributes(
                        tags = metric.active_tags,
                        aggregations = metric.active_aggregations
                    ),
                ),
            )
            while True:
                try:
                    response = api_instance.update_tag_configuration(
                        metric_name = metric.metric_name,
                        body = body,
                    )
                    return({"success": {'metric': metric.metric_name, 'ingest_estimate': metric.estimated_ingested, 'mwl_estimate': metric.estimated_indexed}})
                except Exception as e:
                    if e.status == 429:
                        rate_limit_sleeper(e.headers['X-RateLimit-Reset'])
                        continue
                    elif e.status in common_error_codes:
                        return({"error": f'Error encountered: {e.body["errors"]}'})
                    else:
                        return({"error": f'Unhandled exception: {e}'})
        ## Create a tag/aggr config for a metric to have active tags/aggr as MWL if one doesnt exist and it should.
        elif metric.update_metric and not metric.current_config_state and metric.estimated_ingested > metric.estimated_indexed:
            body = MetricTagConfigurationCreateRequest(
                data=MetricTagConfigurationCreateData(
                    type=MetricTagConfigurationType("manage_tags"),
                    id=metric.metric_name,
                    attributes=MetricTagConfigurationCreateAttributes(
                        tags=metric.active_tags,
                        metric_type=MetricTagConfigurationMetricTypes(metric.metric_type),
                        aggregations = metric.active_aggregations,
                    ),
                ),
            )
            while True:
                try:
                    response = api_instance.create_tag_configuration(
                        metric_name=metric.metric_name,
                        body = body,
                    )
                    return({"success": {'metric': metric.metric_name, 'ingest_estimate': metric.estimated_ingested, 'mwl_estimate': metric.estimated_indexed}})
                except Exception as e:
                    if e.status == 429:
                        rate_limit_sleeper(e.headers['X-RateLimit-Reset'])
                        continue
                    elif e.status in common_error_codes:
                        return({"error": f'Error encountered: {e.body["errors"]}'})
                    else:
                        return({"error": f'Unhandled exception: {e}'})
        ### Otherwise, if optimal setting already exists, do nothing.
        else:
            return({"success": {'metric': metric.metric_name, 'ingest_estimate': metric.estimated_ingested, 'mwl_estimate': metric.estimated_indexed}})

## Run the function for each metric
for metric_name in metric_names:
    result = metric_check(configuration, metric_name, override_existing_tags, disable_metric)
    if "error" in result:
        print(f'\n{10 * "*"}\nError for {metric_name}\nError: {result["error"]}')
    elif "success in result":
        print(f'\n{10 * "*"}\nSuccess for {metric_name}\nIngested Estimate for {metric_name}: {result["success"]["ingest_estimate"]}\nMWL Estimate for {metric_name}: {result["success"]["mwl_estimate"]}\n{metric_name} uses the {"all tags configuration." if result["success"]["ingest_estimate"] <= result["success"]["mwl_estimate"] else "active tags configuration."}')
