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
        query = ""  # str | After entering a search query in your [Manage Monitor page][1] use the query parameter value in the URL of the page as value for this parameter. Consult the dedicated [manage monitor documentation][2] page to learn more.  The querycan     contain any number of space-separated monitor  attributes, for instance `query=\"type:metric status:alert\"`.  [1]: https://app.datadoghq.com/monitors/manage [2]: /monitors/manage_monitor/#find-the-monitors (optional)
        page = 0  # int | Page to start paginating from. (optional) if omitted the server will use the default value of 0
        per_page = 30  # int | Number of monitors to return per page. (optional) if omitted the server will use the default value of 30
        sort = "name,asc"  # str | String for sort order, composed of field and sort order separate by a comma, e.g. `name,asc`. Supported sort directions: `asc`, `desc`. Supported fields:  * `name` * `status` * `tags` (optional)
        # example passing only required values which don't have defaults set
        # and optional values
        try:
            # Monitors group search
            api_response = api_instance.search_monitors(query=query, page=page, per_page=per_page, sort=sort)
            for monitor in api_response['monitors']:               
                # Monitor is of type <class 'datadog_api_client.v1.model.monitor_search_result.MonitorSearchResult'>
                # https://github.com/DataDog/datadog-api-client-java/blob/8d53fa2bb4174147d12b17353473bc35042a7182/api_docs/v1/MonitorSearchResult.md
                # https://github.com/DataDog/datadog-api-client-java/blob/72ca579bcd71cd9254563927254bb9c79d4b5cf6/src/main/java/com/datadog/api/v1/client/model/MonitorSearchResult.java
                # Structure is as follows:
                # {'classification': '',
                # 'creator': {'handle': '', 'name': ''},
                # 'id': ,
                # 'last_triggered_ts': ,
                # 'metrics': [],
                # 'name': '',
                # 'notifications': [],
                # 'org_id': ,
                # 'scopes': [],
                # 'status': '',
                # 'tags': [''],
                # 'type': ''}
                #print(monitor['tags'])
                try:
                    # Example to add a tag to all monitors with a string in the name
                    name = monitor['name']
                    if 'Dummydog' in name:
                        tags = monitor['tags']
                        tags.append('batched')
                        body = MonitorUpdateRequest(
                            tags=tags     
                        )      
                        api_instance.update_monitor(monitor.get('id'),body)
                    ## Example to replace a tag with another value
                    #tags = monitor.get('tags') 
                    #if len(tags) != 0:                        
                    #    for tag in tags:                            
                    #        if 'dummy' in tag: 
                    #            print(tags)
                    #            tags[tags.index('dummy')] = 'dog'
                    #    #print(updatedTags)
                    #    print(tags)
                    #    body = MonitorUpdateRequest(
                    #        tags=tags     
                    #    )      
                    #    api_instance.update_monitor(monitor.get('id'),body)
                except ApiException as e:
                    print("Exception when calling MonitorsApi->update_monitor: %s\n" % e)
        except ApiException as e:
            print("Exception when calling MonitorsApi->search_monitor_groups: %s\n" % e)
