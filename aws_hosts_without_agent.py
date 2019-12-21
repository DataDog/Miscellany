# 3p
import requests

# stdlib
import json
import pprint

api_key = 'YOUR_API_KEY_GOES_HERE'
app_key = 'YOUR_APPLICATION_KEY_GOES_HERE'

url = "https://app.datadoghq.com/reports/v2/overview?\
window=3h&with_apps=true&with_sources=true&with_aliases=true\
&with_meta=true&with_tags=true&api_key=%s&application_key=%s"

infra = json.loads(requests.get(url %(api_key,app_key)).text)

for host in infra['rows']:
    if (('aws' in host['apps']) and ('agent' not in host['apps'])):

        ip = ''
        try:
            gohai = json.loads(host['meta']['gohai'])
            ip = gohai['network']['ipaddress']
        except:
            pass

        print "%s  %s" %(host['name'],ip)
