from datadog import initialize, api

options = {
    'api_key': '<api-key>',
    'app_key': '<app-key>'
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
            
