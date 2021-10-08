from datadog_api_client.v1 import ApiClient, ApiException
from datadog_api_client.v1.api import monitors_api
from datadog_api_client.v1.models import *
import datadog_api_client.v1

# It isn't recommended to manipulate the message attribute using this script. The object returned from the search query does not contain this information and as such, attempting to update the message, any previous content will be removed.

if __name__=="__main__":
    configuration = datadog_api_client.v1.Configuration(
    host = "https://api.datadoghq.com"
    )

    # Configure API key authorization: apiKeyAuth
    configuration.api_key['apiKeyAuth'] = '<your-api-key'
    # Configure API key authorization: appKeyAuth
    configuration.api_key['appKeyAuth'] = '<your-app-key>'
        

    with ApiClient(configuration) as api_client:
    # Create an instance of the API class
        api_instance = monitors_api.MonitorsApi(api_client)
        query = ""  
        page = 0 
        per_page = 30
        try:
            # Monitors group search
            api_response = api_instance.search_monitors(query=query, page=page, per_page=per_page)
            for monitor in api_response['monitors']:               
                    try:
                    # Example to add a tag to all monitors with a string in the name
                    name = monitor['name']
                    if 'Dummydog' in name:
                        tags = monitor['tags']
                        tags.append('dummy')
                        body = MonitorUpdateRequest(
                            tags=tags     
                        )      
                        api_instance.update_monitor(monitor.get('id'),body)
                    ## Example to replace a tag with another value
                    #tags = monitor.get('tags') 
                    #if len(tags) != 0:                        
                    #    for tag in tags:                            
                    #        if 'dummy' in tag:                       
                    #            tags[tags.index('dummy')] = 'dog'
                    #    body = MonitorUpdateRequest(
                    #        tags=tags     
                    #    )      
                    #    api_instance.update_monitor(monitor.get('id'),body)
                except ApiException as e:
                    print("Exception when calling MonitorsApi->update_monitor: %s\n" % e)
        except ApiException as e:
            print("Exception when calling MonitorsApi->search_monitor_groups: %s\n" % e)
