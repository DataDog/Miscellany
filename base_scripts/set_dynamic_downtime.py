#!/usr/bin/env python
"""
 This script provides a simple way to dynamically schedule a downtime
 on a tag scope. Currently a very basic script to display how it might
 be done.

 Ways to expand would this sript would be to split it into two scripts, one
 to set the downtime and the other to end it. The interim period would have
 the downtime id passed to a parent process or written to a file to be read
 from later.
"""
from datadog import initialize, api
import time
import logging
import argparse

def initialize_api(api_key, app_key):
    options = {
            'api_key': api_key,
            'app_key': app_key
    }

    initialize(**options)

def main():
    API_KEY = ''
    APP_KEY = ''

    # Initiatlize the board
    initialize_api(API_KEY, APP_KEY)

    # Downtime will automaticall start now, so this is
    # time in seconds you want downtime to run
    # Example: 3 * 60 * 60 = 3 hours
    end_ts = int(time.time()) + (3 * 60)

    # The tag scope for the downtime. Unfortunately, no way to
    # reference a monitor to scope the downtime to.
    SCOPE = ''

    logging.debug("Creating Downtime with scope {0} and end-time {1}".format(SCOPE, end_ts)
    result = api.Downtime.create(scope=SCOPE, end=end_ts)
    logging.debug("Result: {0}".format(result))
    downtime_id = result['id']
    logging.info("Downtime ID: {0}".format(downtime_id))

    logging.debug("Sleeping")
    time.sleep(30)

    logging.info("Deleting downtime id {0}".format(downtime_id))
    api.Downtime.delete(downtime_id)

def setup_command_line_parser():
    """
        Sets up command line argument parser. Additional arguments could be added
        easily. For example if the version needed to be passed in with -v you
        could add it as a positional argument like so:
        parser.add_argument("-v", "--version", help="Current version of application"
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true', help="Run script in debug mode")
    args = parser.parse_args()
    return parser

if __name__ == "__main__":

    parser = setup_command_line_parser()

    args = parser.parse_args()
    # Check to see if we want to run as debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    main()
