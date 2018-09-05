#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
from datadog import initialize
from datadog import api
import json

def createMonitor():
    print "Creating a test monitor"
    # Create a new monitor
    options = {
        "notify_no_data": True,
        "no_data_timeframe": 20,
        "evaluation_delay": 360,
        "thresholds": {
            'critical': 100,
            'warning': 80,
            'critical_recovery': 70,
            'warning_recovery': 50
        }
    }
    tags = ["cake:test", "solutions-engineering"]
    result = api.Monitor.create(
        type="metric alert",
        query="avg(last_1h):sum:system.net.bytes_rcvd{host:host0} > 100",
        name="Bytes received on host0",
        message="We may need to add web hosts if this is consistently high.",
        tags=tags,
        options=options
    )
    print json.dumps(result, indent=4, sort_keys=True)
    return result['id']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a monitor for testing purposes")
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
        id = createMonitor()
