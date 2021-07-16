from datadog import initialize, api

options = {
    'api_key': 'cb00f763b5dafdfb8fd60ea0e4d30891',
    'app_key': '285b7bccce83db39f8b9f588eef77201b3e67dff'
}

initialize(**options)

# Script that allows for updating batches of monitors programmatically. 

if __name__=="__main__":
    monitorList = api.Monitor.get_all() # Returns a list of dictionaries containing monitor details.

    for monitor in monitorList: # Iterate over all returned monitors
        # Keys present in monitor dictionary
        # dict_keys(['restricted_roles', 'tags', 'deleted', 'query', 'message', 'matching_downtimes', 'id', 'multi', 'name', 'created', 'created_at', 'creator', 'org_id', 'modified', 'priority', 'overall_state_modified', 'overall_state', 'type', 'options'])
        # Monitor API https://docs.datadoghq.com/api/latest/monitors/

        # Example to change an email present in the notification section
        message = monitor.get('message')
        if '<old-email>' in message:         
            api.Monitor.update(monitor.get('id'),message=message.replace('<old-email>', '<new-email>'))
            
