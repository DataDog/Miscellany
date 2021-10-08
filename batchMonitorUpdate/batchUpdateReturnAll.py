from datadog import initialize, api
import datadog_api_client.v1
from dateutil.parser import parse as dateutil_parser
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api import monitors_api
from datadog_api_client.v1.models import *
from pprint import pprint


options = {
    'api_key':  '<your-api-key',
    'app_key': '<your-app-key>'
}
# Script that allows for updating batches of monitors programmatically. 
initialize(**options)

if __name__=="__main__":

    monitorList = api.Monitor.get_all() # Returns a list of dictionaries containing monitor details.

    for monitor in monitorList: # Iterate over all returned monitors
        # Keys present in monitor dictionary
        # dict_keys(['restricted_roles', 'tags', 'deleted', 'query', 'message', 'matching_downtimes', 'id', 'multi', 'name', 'created', 'created_at', 'creator', 'org_id', 'modified', 'priority', 'overall_state_modified', 'overall_state', 'type', 'options'])
        # Monitor API https://docs.datadoghq.com/api/latest/monitors/
        # Example to change an email present in the notification section
        message = monitor.get('message')
        if 'datadoghq.com' in message:         
            api.Monitor.update(monitor.get('id'),message=message.replace('datadoghq.com', 'doge.com'))