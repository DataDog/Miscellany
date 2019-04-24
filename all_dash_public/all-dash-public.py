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
    # @ckelner: These won't work - no way to get:
        # - boolean as to whether the dashboard is public or not
        # - public token from API at this time
            # - If we could, then we could use the public dash API:
                # - https://api.datadoghq.com/api/v1/public_dashboard/<token>
            # - token generation is a combo of public org id and a randomly generated token
                # def generate_token(cls, org_public_id):
                #    '''
                #    TOKEN_LENGTH size is set to 16 bytes.
                #     - The random token size will be 32 chars
                #     - The org_public_id is limited to 16 chars
                #    So the full token size will be less than 49 chars
                #    '''
        # - public URL, or any indicator that the board is public
    # result = api.Dashboard.get_all()
    # result = api.Screenboard.get_all()
    # result = api.Screenboard.get(<redacted>)
    # result = api.Dashboard.get(<redacted>)
    #
    # Using various dashboard list API calls we can get this information though
    # https://docs.datadoghq.com/api/?lang=python#dashboard-lists
    #
    # Logic:
    # 1. Fetch all dashboard lists
    # 2. Check that they have more than 1 dashboard in the list
    # 3. Fetch each dashboard list item (the list itself doesn't contain the
    # boolean we need to know if the dashboard is public or not)
    # 4. Check is the dashboard is public or not
    # 5. Check the dashboard id against a running dictionary we have to
    # guarentee our dict is unique dashboards only
    # 6. If unique place it in our dict to return to the user
    spinner = Halo(text="Getting all public dashboards; This might take awhile...", spinner="dots")
    spinner.start()

    # dict to hold the public dashboard info
    public_dashboards = {}
    # list of dashboard items (of undetermined state)
    dashboard_items = []
    # unique list of dashboard items
    unique_dashboard_items = []

    # get all dashboard lists
    d_lists = api.DashboardList.get_all()["dashboard_lists"]
    # iterate over the lists
    for d_list in d_lists:
        # ignore those with no dashboards
        if d_list["dashboard_count"] > 0:
            dashboard_items.extend(api.DashboardList.get_items(d_list["id"])["dashboards"])

    # remove all dupes from dashboard_items
    # in part to satisfy https://github.com/DataDog/Miscellany/pull/68/files#r277914541
    for dash in dashboard_items:
        if dash not in unique_dashboard_items:
            unique_dashboard_items.append(dash)

    # iterate over unique dashboard_items
    for dash in unique_dashboard_items:
        # check if the dashboard is shared (public)
        if dash["is_shared"] == True:
            # save it - but only if it is a new dash we haven't saved already
            # @ckelner: likely unnecessary since we guarentee unique above
            # if dash["id"] not in public_dashboards:
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
