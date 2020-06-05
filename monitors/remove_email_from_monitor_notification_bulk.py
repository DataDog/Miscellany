# This script removes a given email address from all monitors' notification body.
# Use case: after offboarding an employee, need to remove their email address from monitor notifications
# Example how to run from shell: python3 main.py --api_key=myapikey --app_key=myappkey --email_address=abc@datadoghq.com

from datadog import initialize, api
from datadog.api.exceptions import HttpTimeout, ClientError, ApiError

from argparse import ArgumentParser

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


def remove_email_from_notification(notification_text, email):
    return notification_text.replace("@" + email, "").rstrip()


def update_monitor_with_notification(monitor_id, notification_new):
    try:
        api.Monitor.update(monitor_id, message=notification_new)
    except (HttpTimeout, ClientError, ApiError) as e:
        print("Exception:", e)


# Remove specified email from all monitors' notification body
[update_monitor_with_notification(monitor["id"], remove_email_from_notification(monitor["message"], args.email_address))
 for
 monitor in api.Monitor.get_all()]
