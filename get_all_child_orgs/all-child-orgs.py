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
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get all child orgs; this will use your existing chrome" +
            "cookies; You need to be logged into the parent org you wish to" +
            "get all child orgs for; This mirrors the data found on: " +
            "https://app.datadoghq.com/account/multi-org-usage"
    )

    spinner = Halo(text="Getting all child orgs...", spinner="dots")
    spinner.start()

    # @ckelner: Support: This works with our internal systems also, just
    # change the URL to point at internal systems
    url = "https://app.datadoghq.com"
    cookiez = chrome_cookies(url)
    r = requests.get(url + "/account/usage/multi_org_summary", cookies=cookiez)
    if r.status_code == 403:
        spinner.stop()
        print "Multi-org not enabled"
        sys.exit()

    org_summary = r.json()["orgs"]
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
                "name": org["name"],
                "public_id": org["id"]
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
