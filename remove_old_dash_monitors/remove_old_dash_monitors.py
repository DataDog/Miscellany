#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
from datetime import datetime
from collections import OrderedDict
from datadog import initialize
from datadog import api

API_OBJS = OrderedDict([('Screenboard', 'screenboards'),
                        ('Timeboard'  , 'dashes'),
                        ('Monitor'    , ''      )])

def get_old_objs(endpoint, email, time_to_remove):
    ''' Returns all "old" dashboard or monitor IDs that belong to email older than time_to_remove '''
    func = "api." + endpoint + ".get_all()"
    response = eval(func)
    old_objs = set()
    objs = response[API_OBJS[endpoint]] if API_OBJS[endpoint] else response

    for obj in objs:
        oid, o_email, o_modified = 0, "", datetime.utcnow()

        if endpoint == 'Screenboard' or endpoint == 'Timeboard':
            oid, o_email, o_modified = _parse_response_dash(obj)
        elif endpoint == 'Monitor':
            oid, o_email, o_modified = _parse_response_mtr(obj)

        o_timediff = (datetime.utcnow() - o_modified).total_seconds()

        if o_email == email and o_timediff > time_to_remove:
            old_objs.add(oid)

    return old_objs

def delete_objs(endpoint, objs):
    func = "api." + endpoint + ".delete(obj)"
    for obj in objs:
        eval(func)

def _parse_response_dash(dash):
    ''' Helper: Return 3-tuple of dash ID, email and modified datetime '''
    # convert the modified timestamp to datetime
    # offset is stripped since it is always +00:00 on org 2, 11287 and does not match +HHMM format for %z

    return (dash['id'], dash['created_by']['email'], datetime.strptime(dash['modified'][:-6], '%Y-%m-%dT%H:%M:%S.%f'))

def _parse_response_mtr(mtr):
    ''' Helper: Return 3-tuple of monitor ID, email and modified datetime '''
    # convert the modified timestamp to datetime
    # offset is stripped since it is always +00:00 on org 2, 11287 and does not match +HHMM format for %z

    return (mtr['id'], mtr['creator']['email'], datetime.strptime(mtr['modified'][:-6], '%Y-%m-%dT%H:%M:%S.%f'))

def _confirm_deletion(objs):
    ''' Helper: Confirm deletion of objs; takes [Y/n] '''
    question = """Are you sure you would like to delete the following? [Y/n]
  Screenboards: {0}
  Timeboards:   {1}
  Monitors:     {2}"""
    yes = {'yes', 'y'}
    no  = {'no', 'n'}

    while True:
        print question.format(str([str(id) for id in objs[0][1]]), str([str(id) for id in objs[1][1]]), str([str(id) for id in objs[2][1]]))
        choice = raw_input().lower()

        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print "Please respond with 'yes' or 'no'\n"

if __name__ == "__main__":
    # init script args
    parser = argparse.ArgumentParser(
        description="Create an empty dashboard for testing purposes")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    parser.add_argument(
        "-e", "--email", help="Your Datadog email", type=str, default=None)
    parser.add_argument(
        "-t", "--time", help="Time since last modified; used for deletion", type=int, default=7889231)
    args = parser.parse_args()

    api_key = args.apikey or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv("DD_APP_KEY", None)
    email   = args.email  or os.getenv("DD_EMAIL",   None)

    # time since last modified in seconds; used as threshold for removing old objs
    time_to_remove  = args.time
    errors = []

    # check for args/env vars and print errors
    if not api_key:
        errors.append("""
                      You must supply your Datadog API key by either passing a
                      -k/--apikey argument or defining a DD_API_KEY environment
                      variable.""")
    if not app_key:
        errors.append("""
                      You must supply your Datadog application key by either
                      passing a -a/--appkey argument or defining a DD_APP_KEY
                      environment variable.""")
    if not email:
        errors.append("""
                      You must supply your Datadog email by either passing a
                      -e/--email argument or defining a DD_EMAIL environment
                      variable.""")

    if errors:
        for error in errors:
            print textwrap.dedent(error)
        sys.exit(2)
    else:
        # init client
        options = {
            'api_key': api_key,
            'app_key': app_key
        }
        initialize(**options)

        # get all old dashboards and monitors
        old_objs = [(endpoint, get_old_objs(endpoint, email, time_to_remove)) for endpoint in API_OBJS.keys()]

        # check if any to delete, confirm deletion, then delete
        if sum([len(obj[1]) for obj in old_objs]) == 0:
            print "No old dashboards or monitors were found!"
        elif (_confirm_deletion(old_objs)):
            for endpoint, objs in old_objs:
                delete_objs(endpoint, objs)

            print "Deleted all old dashboards and monitors."
        else:
            print "Cancelled removal operation."

