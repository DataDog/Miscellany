from datadog import initialize, api
import sys
import time
import json
import yaml

def load_config():
    f = open(str(sys.path[0] + '/multi_org_create_users.yaml'))
    config = yaml.safe_load(f)
    f.close()

    return config

def create_users(auth_key, users):
    options = {
        'api_key': auth_key['api_key'],
        'app_key': auth_key['app_key']
    }
    initialize(**options)

    results = []
    for user in users:
        result = api.User.create(handle=user['handle'], name=user['name'], access_role=user['access_role'])
        results.append(result)

    return results

def process_orgs():
    config = load_config()
    org_keys = config['organizations']
    users = config['users']

    results = []
    for org_key in org_keys:
        result = create_users(org_key, users)
        results.append(result)

    print results

process_orgs()
