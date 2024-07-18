# This script replaces a given domain from all monitors' notification body to a new domain. 
# Use case: Updates to a company's email domain
# Example how to run from shell: python3 replace_domain_in_monitor_notification_bulk.py --api_key=myapikey --app_key=myappkey --api_host=myapihost --old_domain=myolddomain --new_domain=mynewdomain
# Note: api_host is "https://app.datadoghq.com/" for us1.prod. 

from datadog import initialize, api
from datadog.api.exceptions import HttpTimeout, ClientError, ApiError
from argparse import ArgumentParser
import json

parser = ArgumentParser()
parser.add_argument('--api_key', dest='api_key', required=True)
parser.add_argument('--app_key', dest='app_key', required=True)
parser.add_argument('--api_host', dest='api_host', required=True)
parser.add_argument('--old_domain', dest='old_domain', required=True)
parser.add_argument('--new_domain', dest='new_domain', required=True)

args = parser.parse_args()

options = {
  'api_key': args.api_key,
  'app_key': args.app_key,
  'api_host': args.api_host,
}

initialize(**options)


def replace_email_domain(notification_text, old_domain, new_domain):
  notification_text_with_new_domain = notification_text.replace(old_domain, new_domain)
  return notification_text_with_new_domain

def update_monitor_notification(monitor_id, new_notification):
  try:
    api.Monitor.update(monitor_id, message=new_notification)
  except (HttpTimeout, ClientError, ApiError) as e:
    print('Exception:', e)

print(json.dumps(api.Monitor.get_all(), indent=4))
# Switch domain for all monitors' notification body
[update_monitor_notification(monitor['id'], replace_email_domain(monitor['message'], args.old_domain, args.new_domain)) 
for monitor 
in api.Monitor.get_all()]
