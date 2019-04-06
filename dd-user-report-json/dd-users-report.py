#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
from datadog import initialize
from datadog import api
import json


def getAndPrintUsers(admin_only, enabled_only, verified_only, standard_only):
    '''
        {
            "access_role": "st",
            "disabled": false,
            "email": "person@email.com",
            "handle": "string",
            "icon": "url",
            "is_admin": false,
            "name": "string",
            "role": null,
            "verified": true
        },
    # is admin
    # "access_role": "adm",
    # "is_admin": true,

    # is enabled
    # "disabled": false,

    # is verified (non-pending)
    # "verified": true
    '''

    print "Getting users from target Datadog account..."
    users = api.User.get_all()["users"]

    if admin_only:
        admins = []
        for user in users:
            if user["is_admin"]:
                admins.append(user)
        users = admins

    if enabled_only:
        enabled = []
        for user in users:
            if user["disabled"] is False:
                enabled.append(user)
        users = enabled

    if verified_only:
        verified = []
        for user in users:
            if user["verified"]:
                verified.append(user)
        users = verified

    if standard_only:
        standard = []
        for user in users:
            if user["access_role"] == "st":
                standard.append(user)
        users = standard

    print json.dumps(users, indent=4, sort_keys=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get a list of users from a Datadog Account")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    parser.add_argument(
        "-o", "--adminonly", help="Only print admins", action='store_true', default=False)
    parser.add_argument(
        "-s", "--standardonly", help="Only print standard users", action='store_true', default=False)
    parser.add_argument(
        "-e", "--enabledonly", help="Only print enabled accounts", action='store_true', default=False)
    parser.add_argument(
        "-v", "--verifiedonly", help="Only print verified (non-pending) accounts", action='store_true', default=False)
    args = parser.parse_args()
    api_key = args.apikey or os.getenv(
        "DATADOG_API_KEY", None) or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv(
        "DATADOG_APP_KEY", None) or os.getenv("DD_APP_KEY", None)
    admin_only = args.adminonly
    enabled_only = args.enabledonly
    verified_only = args.verifiedonly
    standard_only = args.standardonly
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
        getAndPrintUsers(admin_only, enabled_only,
                         verified_only, standard_only)
