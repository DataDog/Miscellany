#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
from datadog import initialize
from datadog import api
import json
from halo import Halo

def getAllPublicDashboards():
    # @ckelner: These won't work - no way to get public token from API at this time
    # result = api.Dashboard.get_all()
    # result = api.Screenboard.get_all()
    # result = api.Screenboard.get(<redacted>)
    # result = api.Dashboard.get(<redacted>)
    spinner = Halo(text="Getting all public dashboards; This might take awhile...", spinner="dots")
    spinner.start()

    # dict to hold the public dashboard info
    public_dashboards = {}
    # get all dashboard lists
    d_lists = api.DashboardList.get_all()["dashboard_lists"]
    # iterate over the lists
    for list in d_lists:
        # ignore those with no dashboards
        if list["dashboard_count"] > 0:
            # get each dashboard
            dashboards = api.DashboardList.get_items(list["id"])["dashboards"]
            for dash in dashboards:
                # check if the dashboard is shared (public)
                if dash["is_shared"] == True:
                    # save it - but only if it is a new dash we haven't saved already
                    if dash["id"] not in public_dashboards:
                        public_dashboards[dash["id"]] = dash

    spinner.stop()
    # print it!
    print json.dumps(public_dashboards, indent=4, sort_keys=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create an empty dashboard for testing purposes")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    args = parser.parse_args()
    api_key = args.apikey or os.getenv("DATADOG_API_KEY", None) or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv("DATADOG_APP_KEY", None) or os.getenv("DD_APP_KEY", None)
    errors = []
    if not api_key:
        errors.append("""
                      You must supply your Datadog API key by either passing a
                      -k/--apikey argument or defining a DATADOG_API_KEY or
                      DD_API_KEY environment variable.""")
    if not app_key:
        errors.append("""
                      You must supply your Datadog application key by either
                      passing a -a/--appkey argument or defining a
                      DATADOG_APP_KEY or DD_APP_KEY environment variable.""")
    if errors:
        for error in errors:
            print textwrap.dedent(error)
        sys.exit(2)
    else:
        # Initialize the dd client
        options = {
            'api_key': api_key,
            'app_key': app_key
        }
        initialize(**options)
        getAllPublicDashboards()
