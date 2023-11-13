
# This is a tool for removing AWS host-level tags from your infrastructure in
# datadog. It is intended for users who have removed their EC2 instances from
# their AWS integration and if they no longer want to see AWS tags associated
# with the hosts that still run datadog-agents.

#standard libraries
import json

# 3rd Party
import requests

# Input Variables
API_KEY = 'YOUR_API_KEY_HERE'
APPLICATION_KEY = 'YOUR_APPLICATION_KEY_HERE'
TAG_SOURCE = 'Amazon Web Services'  # Can also be set to 'Users', 'Chef', or
                                    # or other source values.
                                    # See : https://docs.datadoghq.com/integrations/faq/list-of-api-source-attribute-value/
SITE = 'US1' # US1, US3, US5, EU1, US1-FED, AP1. 
             # See: https://docs.datadoghq.com/getting_started/site/ 
REMOVE_FROM_ALL_HOSTS = False  # change to true to remove from all hosts
                               # be careful not to remove tags you want to keep!
HOSTS = [  # if not all, specify what hosts you want to delete tags from
    'host_name'
]

# constants
SITES = {
    'US1': 'datadoghq.com',
    'US3': 'us3.datadoghq.com',
    'US5': 'us5.datadoghq.com',
    'EU1': 'datadoghq.eu',
    'US1-FED': 'ddog-gov.com',
    'AP1': 'ap1.datadoghq.com',
}

# functions
def remove_host_tags_by_source(hostname, source, session):
    remove_endpt = 'https://app.{}/api/v1/tags/hosts/{}'.format(SITES.get(SITE, SITES['US1']), hostname)
    session.params['source'] = source
    res = session.request(
        method='DELETE', url=remove_endpt, params=session.params
    )
    print('removed %s tags from %s with response: %s' % (TAG_SOURCE, hostname, res))


# main
s = requests.session()

s.params = {
    'api_key': API_KEY,
    'application_key': APPLICATION_KEY
}

if REMOVE_FROM_ALL_HOSTS is True:
    perma_link = 'https://app.{}/reports/v2/overview'.format(SITES.get(SITE, SITES['US1']))
    perma_content = s.request(
        method='GET', url=perma_link, params=s.params
    ).text
    perma_json = json.loads(perma_content)

    # if 'errors' in perma_json:
    #     print(perma_json)
    # else:
    for host in perma_json.get('rows', []):
        host_name = host['host_name']
        if TAG_SOURCE.lower() in set(s.lower() for s in host['tags_by_source']):
            remove_host_tags_by_source(host_name, TAG_SOURCE, s)
        else:
            print("no %s tags in %s, skipping." % (TAG_SOURCE, host_name))
        
else:
    for host in HOSTS:
        remove_host_tags_by_source(host, TAG_SOURCE, s)
