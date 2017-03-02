#!/usr/bin/env python
"""
 Provides a simple replacement for log parsing in the agent. Could
 easily be modified into an agent check.

This script can be called from the command-line, but this just sets
 DEBUG mode. Could easily be modified to be passed in a version.


 To see the log format see this doc:
     http://docs.datadoghq.com/guides/logs/

 This script makes the assumption that it is the same log-line being parsed with
 the same units/metric. I.E., you cannot use it on something like this:

     me.web.requests 1320786966 157 metric_type=counter unit=request
     me.web.latency 1320786966 250 metric_type=gauge unit=ms


"""

from datadog import initialize, api
import logging
import argparse

def initialize_api(api_key, app_key):
    options = {
            'api_key': api_key,
            'app_key': app_key
    }

    initialize(**options)

def create_dictionary_from_log_line(log_line):
    log_dict = {"metric": log_line[0],
                "points": [(log_line[1], log_line[2])],
                "tags": [log_line[5]]
            }

    logging.debug(log_dict)
    return log_dict

def read_log_file(file_name):
    parsed_log_lines = []
    metric_unit = None
    metric_name = None
    with open(file_name, "r") as log_file:
        for line in log_file.readlines():
            log_line = line.split()
            parsed_log_lines.append(create_dictionary_from_log_line(log_line))

            if not metric_name:
                metric_name = log_line[0]

            if not metric_unit:
                metric_unit = log_line[4]

    return parsed_log_lines, metric_unit, metric_name

def main():
    API_KEY = ''
    APP_KEY = ''
    LOG_FILE_PATH  = ''

    initialize_api(API_KEY, APP_KEY)
    parsed_log_lines, unit_type, metric_name = read_log_file(LOG_FILE_PATH)

    logging.debug(parsed_log_lines)
    logging.debug(unit_type)
    logging.debug(metric_name)

    logging.info("Sending metrics:")
    response = api.Metric.send(parsed_log_lines)
    logging.info("Response: {0}".format(response))

    logging.info("Updating metric Metadata with unit")
    response = api.Metadata.update(metric_name=metric_name, unit=unit_type)
    logging.info("Response: {0}".format(response))

def setup_command_line_parser():
    """
        Sets up command line argument parser.
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
