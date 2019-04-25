'''
    Disclaimer:
    These projects are not a part of Datadog's subscription services and are
    provided for example purposes only. They are NOT guaranteed to be bug free
    and are not production quality. If you choose to use to adapt them for use
    in a production environment, you do so at your own risk.

    This script uses a Datadog HTTP endpoint which is subject to change at any
    time with no guarantee.

    See the README.md for how to use this script.
'''

#!/usr/bin/env python
import argparse
import json
from halo import Halo
import requests
from pycookiecheat import chrome_cookies

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get all child orgs; this will use your existing chrome" +
            "cookies; You need to be logged into the parent org you wish to" +
            "get all child orgs for; This mirrors the data found on: " +
            "https://app.datadoghq.com/account/multi-org-usage"
    )

    spinner = Halo(text="Getting all child orgs...", spinner="dots")
    spinner.start()

    # @ckelner: This SHOULD work with partlow, just change the url
    # to https://support-admin.us1.prod.dog -- could be made an args opt also
    url = "https://app.datadoghq.com"
    # cookie_path = "/Users/chriskelner/Library/Application Support/Google/Chrome/Profile 2/Cookies"
    #cookiez = chrome_cookies(url, cookie_file=cookie_path)
    cookiez = chrome_cookies(url)
    org_summary = requests.get(url + "/account/usage/multi_org_summary", cookies=cookiez).json()["orgs"]
    # poor man's debugging
    # print json.dumps(org_summary, indent=4)
    '''
    json objects look like:
        ...
        "orgs": [
            {
                "aws_host_top99p": 0,
                "infra_host_top99p": 0,
                "fargate_tasks_count_hwm": 0,
                "gcp_host_top99p": 0,
                "name": "zzzzz-kelnerhax4",
                "synthetics_check_calls_count_sum": 0,
                "trace_search_indexed_events_count_sum": 0,
                "custom_ts_avg": 0,
                "apm_host_top99p": 0,
                "agent_host_top99p": 0,
                "id": "a446b1b33",
                "ingested_events_bytes_sum": 0,
                "indexed_events_count_sum": 0,
                "container_hwm": 0
            },
            ...
        ]
    '''

    # list
    org_list = []
    # keep count
    count = 0
    for org in org_summary:
        # @ckelner: can't use parent API key to query for org details of a child
        # org, results in an error:
        # {
        #   "errors": [
        #       "Not allowed to access this organization"
        #   ]
        # }
        # org_details = json.loads(
        #    requests.get(
        #        "https://api.datadoghq.com/api/v1/org/" +
        #        str(org["id"]) + "?" +
        #        "api_key=" + api_key + "&" +
        #        "application_key=" + app_key
        #    ).text
        #)
        # poor man's debugging
        # print json.dumps(org, indent=4)
        org_list.append(
            {
                "name": org["id"],
                "public_id": org["name"]
            }
        )
        count+=1

    spinner.stop()
    # print it!
    print json.dumps(org_list, indent=4)
    with open('org_list.json', 'w') as outfile:
        json.dump(org_list, outfile, indent=4)
    print "="*30
    print "Script complete. Found " + str(count) + " child orgs."
    print "JSON has been dumped to ./org_list.json"
    print "Exiting..."
