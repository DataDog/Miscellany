import json, os
from datadog import api 
"""
This script uses the datadog HTTP API to copy dashboard definitions from a source to a destination.
TODO: switch from prints to logs
TODO: compartmentalize by type?
"""
# for easy management of auth credentials
# TODO: cleanup and generate during initialization probably add checks for null/empty values to surface errors more easily
# TODO: remove any key-env var passing, these should all just be environment variables
class AuthKeySet:
    def __init__(self, source_api, source_app, dest_api, dest_app):
        self.source_api = source_api
        self.source_app = source_app
        self.dest_api = dest_api
        self.dest_app = dest_app

def getKeys():
    source_prefix = 'SOURCE' 
    dest_prefix = 'DEST' 
    source_api_key = str.format('{}_API_KEY', source_prefix)
    source_app_key = str.format('{}_APP_KEY', source_prefix)
    dest_api_key = str.format('{}_API_KEY', dest_prefix)
    dest_app_key = str.format('{}_APP_KEY', dest_prefix)
    return AuthKeySet(os.environ[source_api_key], os.environ[source_app_key], os.environ[dest_api_key], os.environ[dest_app_key]) 

def auth(host_url, api_key, app_key):
    from datadog import initialize

    # magic to switch envs
    os.environ['DATADOG_HOST'] = host_url
    options = {
        'api_key': api_key,
        'app_key': app_key,
        }

    initialize(**options)

def migrate(source, destination, target_screenboard, target_timeboard, target_monitor): 
    auth_keys = getKeys()
    if target_screenboard:
        migrate_screenboard(source, destination, target_screenboard, auth_keys)
    if target_timeboard:
        migrate_timeboard(source, destination, target_timeboard, auth_keys)
    if target_monitor:
        migrate_monitor(source, destination, target_monitor, auth_keys)

"""
Screenboards
"""
def migrate_screenboard(source, destination, target, auth_keys):
    print (str.format('migrating screenboards ID {} from {} to {}', target, source, destination))
    dashes_by_name = {}

    auth(source, auth_keys.source_api, auth_keys.source_app)
    target_dash = fetch_screenboard(target)

    # the rest of our interactions will be with this auth set
    auth(destination, auth_keys.dest_api, auth_keys.dest_app)
    existing_dashes = fetch_all_screenboards()

    # create a dictionary that uses the monitor name as its key
    for dash in existing_dashes:
        dashes_by_name[dash['title']] = dash
    dash_exists = has_screenboard_match(target_dash, dashes_by_name)

    if dash_exists:
        print (str.format('found matching dash, proceeding to update'))
        existing_dash = dashes_by_name[target_dash['board_title']]
        updated_dash = update_screenboard(target_dash, existing_dash)
        print (json.dumps(updated_dash))
    else:
        print ('no match found, creating screenboard')
        new_dash = create_screenboard(target_dash)
        print(json.dumps(new_dash))

def fetch_screenboard(dash_id): 
    return api.Screenboard.get(dash_id)

def fetch_all_screenboards():
    return api.Screenboard.get_all()['screenboards']

def has_screenboard_match(dash, dash_dict):
    if dash['board_title'] in dash_dict.keys():
        return True
    return False

def create_screenboard(source):
    print('creating screenboard')
    # handle optional parameters
    description = ""
    template_vars = None
    width = None
    heigh = None
    read_only = False
    if 'description' in source.keys():
        description = source['description']
    if 'template_variables' in source.keys():
        template_vars = source['template_variables']
    if 'width' in source.keys():
        width = source['width']
    if 'height' in source.keys():
        height = source['height']
    if 'read_only' in source.keys():
        read_only = source['read_only']

    return api.Screenboard.create(
            board_title=source['board_title'],
            description=description,
            widgets=source['widgets'],
            template_variables=template_vars,
            width=width,
            height=height,
            read_only=read_only,
            )

"""
for now, this copies all elements from the target screenboard to the
existing screenboard in the new location 
"""
def update_screenboard(target, existing):
    # handle optional params 
    description = ""
    template_vars = None
    width = None
    heigh = None
    read_only = False
    if 'description' in target.keys():
        description = target['description']
    if 'template_variables' in target.keys():
        template_vars = target['template_variables']
    if 'width' in target.keys():
        width = target['width']
    if 'height' in target.keys():
        height = target['height']
    if 'read_only' in target.keys():
        read_only = target['read_only']

    return api.Screenboard.update(
            existing['id'],
            board_title=target['board_title'],
            description=description,
            widgets=target['widgets'],
            template_variables=template_vars,
            width=width,
            height=height,
            read_only=read_only,
            )
                           
            
"""
Timeboards
"""
def migrate_timeboard(source, destination, target, auth_keys):
    print (str.format('migrating timeboards ID {} from {} to {}', target, source, destination))
    dashes_by_name = {}

    auth(source, auth_keys.source_api, auth_keys.source_app)
    target_dash = fetch_timeboard(target)

    # using this set of creds for the rest of the operations
    auth(destination, auth_keys.dest_api, auth_keys.dest_app)
    existing_dashes = fetch_all_timeboards()

    # create a dictionary that uses the monitor name as its key
    for dash in existing_dashes:
        dashes_by_name[dash['title']] = dash
    dash_exists = has_timeboard_match(target_dash, dashes_by_name)
    if dash_exists:
        existing_dash = dashes_by_name[target_dash['title']]
        updated_dash = update_timeboard(target_dash, existing_dash)
        print (json.dumps(updated_dash))
    else:
        print ('no match found, creating timeboard')
        new_dash = create_timeboard(target_dash) 
        print(json.dumps(new_dash))

def fetch_timeboard(dash_id): 
    return api.Timeboard.get(dash_id)['dash']
        
def fetch_all_timeboards():
    return api.Timeboard.get_all()['dashes']

def has_timeboard_match(dash, dash_dict):
    if dash['title'] in dash_dict.keys():
        return True
    return False

def create_timeboard(source):
    print('creating timeboard')

    # handle optional parameters
    graphs = None
    template_vars = None
    read_only = False
    if 'graphs' in source.keys():
        graphs = source['graphs']
    if 'template_variables' in source.keys():
        template_vars = source['template_variables']
    if 'read_only' in source.keys():
        read_only = source['read_only']

    return api.Timeboard.create(
            title=source['title'],
            description=source['description'],
            graphs=graphs,
            template_variables=template_vars,
            read_only=read_only
            )
    
"""
for now, this copies over everything to the existing timeboard
"""
def update_timeboard(target, existing):
    print('updating timeboard')
    # handle optional parameters
    graphs = None
    template_vars = None
    read_only = False
    if 'graphs' in target.keys():
        graphs = target['graphs']
    if 'template_variables' in target.keys():
        template_vars = target['template_variables']
    if 'read_only' in target.keys():
        read_only = target['read_only']

    return api.Timeboard.update(
            existing['id'],
            title=target['title'],
            description=target['description'],
            graphs=graphs,
            template_variables=template_vars,
            read_only=read_only
            )

"""
Monitors
"""
def migrate_monitor(source, destination, target, auth_keys): 
    print (str.format('migrating monitor ID {} from {} to {}', target, source, destination))
    monitors_by_name = {}

    auth(source, auth_keys.source_api, auth_keys.source_app)
    target_monitor = fetch_monitor(target)

    auth(destination, auth_keys.dest_api, auth_keys.dest_app)
    existing_monitors = fetch_all_monitors()

    # create a dictionary that uses the monitor name as its key
    for monitor in existing_monitors:
        monitors_by_name[monitor['name']] = monitor
    monitor_exists = has_monitor_match(target_monitor, monitors_by_name)

    # not yet implemented
    if monitor_exists: 
        existing_monitor = monitors_by_name[target_monitor['name']]
        updated_monitor = update_monitor(target_monitor, existing_monitor)
        print (json.dumps(updated_monitor))
    else:
        print ('no similar monitor was found')
        new_monitor = create_monitor(target_monitor)
        print (json.dumps(new_monitor))

def fetch_monitor(location, api_key, app_key, monitor_id): 
    return api.Monitor.get(monitor_id, group_states='all')

def fetch_all_monitors(location, api_key, app_key):
    return api.Monitor.get_all(group_states='all')

## simple match on monitor names
def has_monitor_match(monitor, monitor_dict):
    if monitor['name'] in monitor_dict.keys():
        return True
    return False

def create_monitor(source, location, api_key, app_key):
    print ('creating monitor')

    # handle optional params
    message = "copied from another account"
    options = {}
    tags = None
    if 'message' in source.keys():
        message = source['message']
    if 'options' in source.keys():
        options = source['options']
    if 'tags' in source.keys():
        tags = source['tags']

    return api.Monitor.create(
            type=source['type'],
            query=source['query'],
            name=source['name'],
            message=message,
            tags=tags,
            options=options,
    )

"""
for now, this just copies over everything from the target monitor
"""
def update_monitor(target, existing):
    print ('updating monitor {} in {}')
    # handle optional params
    message = "copied from another account"
    opts = {}
    tags = None
    if 'message' in target.keys():
        message = target['message']
    if 'options' in target.keys():
        opts = target['options']
    if 'tags' in target.keys() and target['tags'] is not []:
        tags = target['tags']

    return api.Monitor.update(
            id=existing['id'],
            params=None,
            query=target['query'],
            name=target['name'],
            message=message,
            tags=tags,
            options=opts,
    )


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='migrate a monitor from one datadog account to another')
    parser.add_argument('-s', '--source', required=True, help='source base URL of the monitor to be copied. Ex: http://appname.datadoghq.com')
    parser.add_argument('-d', '--destination', required=True, help='destination base URL of the monitor to be copied. Ex: http://new_app.datadoghq.com')
    parser.add_argument('-sb', '--screenboard', required=False, help='a screenboard ID to migrate')
    parser.add_argument('-tb', '--timeboard', required=False, help='a timeboard ID to migrate')
    parser.add_argument('-m', '--monitor', required=False, help='a monitor ID to migrate')
    args = parser.parse_args()
    migrate(args.source, args.destination, args.screenboard, args.timeboard, args.monitor)
