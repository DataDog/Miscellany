"""
Disclaimer
These projects are not a part of Datadog's subscription services and are provided for example purposes only.
They are NOT guaranteed to be bug free and are not production quality.
If you choose to use to adapt them for use in a production environment, you do so at your own risk.
"""

import json
import os
import requests
import pprint

from datadog import initialize, api

DD_API_KEY = os.getenv('DD_API_KEY', '')
DD_APP_KEY = os.getenv('DD_APP_KEY', '')

options = {
    'api_key': DD_API_KEY,
    'app_key': DD_APP_KEY
}

initialize(**options)

# query datadog api
def get_hosts(filter_string):
    host_count = api.Hosts.search(filter=initial_filter_string)['total_matching']
    print('%r hosts matching initial_filter_string' % host_count)
    num_req = host_count // 100 + 1
    print('%r number of api requests to query all matching hosts' % num_req)
    matching_hosts = []
    start_index = 0
    for i in range(1, num_req+1):
        print('api request %r of %r' % (i, num_req))
        host_list = api.Hosts.search(filter=initial_filter_string, sort_field='apps', count=100, start=start_index)['host_list']
        start_index += 100
        for host in host_list:
            matching_hosts.append(host)
    return matching_hosts

# filter list returned by API by searchin on host[key]
def filter_hosts_by_query_key(matching_hosts, query_key, query_string):
    filtered_hosts = []
    for host in matching_hosts:
        value = host.get(query_key, None)
        if query_string in value: # contains, startswith, endswith, etc
            new_hosts.append(host)
    return filtered_hosts

# query datadog api
initial_filter_string = '' # string to query datadog api for matching hosts.  this may return more hosts than you are looking for.
matching_hosts = get_hosts(initial_filter_string)

# optional, uncomment to enable
# query_key = 'host_name' # any key of the host object (i.e. 'platform', 'id') to use when iterating over the search results.  host_name is default.
# query_string = 'ldmx' # query string to run against search string
# matching_hosts = filter_hosts_by_query_key(matching_hosts, query_key, query_string)

hosts_with_tags = []

for host in matching_hosts:
    host_name = host.get('host_name', None)
    current_tags = host.get('tags_by_source')
    new_tags = []
    skip_tags = ['hostname', 'GOOS']
    meta = host.get('meta', None)
    try:
        # gohai is the key of the system metadata
        gohai = json.loads(meta.get('gohai', None))

        # create tags by iterating over metadata
        platform = gohai.get('platform', None)
        if platform:
            for k, v in platform.items():
                if k in skip_tags: # skip tags
                    continue
                new_tags.append(k + ':' + v)

        # create a single tag
        cpu = gohai.get('cpu', None)
        if cpu:
           model_name = cpu.get('model_name', None)
           if model_name:
               new_tags.append('cpu_model_name:' + model_name)

    except Exception as e:
        print(e)
        continue
    hosts_with_tags.append({'host_name': host_name, 'tags': new_tags})

# add tags to host (it may take ~5 minutes to appear)
for host in hosts_with_tags:
    host_name = host.get('host_name', None)
    new_tags = host.get('tags', None)
    if host_name and new_tags:
        print('Updating host: {} with tags: {}'.format(host_name, new_tags))
        res = api.Tag.create(host_name, tags=new_tags)
        if 'errors' in res:
            print(res['errors'])
