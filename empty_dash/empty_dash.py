#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
from datadog import initialize
from datadog import api


def createEmptyDashboard():
    print "Creating an empty dashboard"
    result = api.Screenboard.create(
        board_title='Datadog Empty Dash Test',
        description='Testing an empty dashboard',
        # worth noting that 'graphs' isn't actually a valid parameter
        # should use widgets; see https://docs.datadoghq.com/api/screenboards/#creating-boards
        # however this is how the customer was trying to create/update a board
        graphs=None
    )
    print result
    return result['id']

def updateEmptyDashboard(id):
    print "Updating dashboard %s" % (id)
    result = api.Screenboard.update(
        id,
        board_title='Datadog Empty Dash Test',
        description='Testing an empty dashboard',
        # worth noting that 'graphs' isn't actually a valid parameter
        # should use widgets; see https://docs.datadoghq.com/api/screenboards/#creating-boards
        # however this is how the customer was trying to create/update a board
        graphs=None
    )
    print result


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
        id = createEmptyDashboard()
        updateEmptyDashboard(id)
