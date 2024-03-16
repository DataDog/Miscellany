# This script appends a given email address from all monitors' notification body.
# Use case: if switching emails, this script can be used after remove_email_from_monitor_notification_bulk.py
# Example how to run from shell: python3 main.py --api_key=myapikey --app_key=myappkey --email_address=abc@datadoghq.com

from datadog import initialize, api
from datadog.api.exceptions import HttpTimeout, ClientError, ApiError

from argparse import ArgumentParser
import json

parser = ArgumentParser()
parser.add_argument("--api_key", dest="api_key", required=True)
parser.add_argument("--app_key", dest="app_key", required=True)
parser.add_argument("--email_address", dest="email_address", required=True)

args = parser.parse_args()

options = {
  'api_key': args.api_key,
  'app_key': args.app_key
}

initialize(**options)


def add_email_to_notification(notification_text, email):
  notification_text_with_email = notification_text + " @" + email
  return notification_text_with_email

def update_monitor_with_notification(monitor_id, notification_new):
  try:
    api.Monitor.update(monitor_id, message=notification_new)
  except (HttpTimeout, ClientError, ApiError) as e:
    print("Exception:", e)

print(json.dumps(api.Monitor.get_all(), indent=4))
# Add specified email from all monitors' notification body
[update_monitor_with_notification(monitor["id"], add_email_to_notification(monitor["message"], args.email_address)) 
for monitor 
in api.Monitor.get_all()]