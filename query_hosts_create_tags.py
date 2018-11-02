import json
import os
import requests
import pprint

from datadog import initialize, api

# source /opt/datadog/datadog-agent/venv/bin/activate

DD_API_KEY = os.getenv('DD_API_KEY', '')
DD_APP_KEY = os.getenv('DD_APP_KEY', '')

options = {
    'api_key': DD_API_KEY,
    'app_key': DD_APP_KEY
}

initialize(**options)

initial_filter_string = '' # string to query datadog api for matching hosts.  this may return more hosts than you are looking for.

query_key = 'host_name' # any key of the host object (i.e. 'platform', 'id') to use when iterating over the search results.  host_name is default.
query_string = 'splunk' # query string to run against search string
create_tags = False # set to true to create tags on matchings hosts

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

print('Matching host count: %r' % len(matching_hosts))

# run a second, more granular query to identify hosts
all_hostnames = []
hosts_to_tag = []
for host in matching_hosts:
    host_name = host['host_name'] # get the host name for adding tags
    all_hostnames.append(host_name)
    value = host[query_key] # ex host['platform'], hosts['id'], etc
    if query_string in value: # contains, startswith, endswith, etc
        hosts_to_tag.append(host_name)
        print('identified host %s' % host_name)

print('Host count: %r' % host_count)
print('Unique host names: %r' % len(set(all_hostnames)))
print('Hosts to tag: %r' % len(hosts_to_tag))

if create_tags:
    # add a tag to hosts
    for host_name in hosts_to_tag:
        res = api.Tag.create(host_name, tags=['tag_name:tag_value'])
        if 'errors' in res:
            print(res['errors'])
else:
    print("Set 'create_tags' = True to create tags for matchings hosts.")
