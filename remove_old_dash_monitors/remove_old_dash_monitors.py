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

def get_old_objs(endpoint, email, removal_time, exclude_tags, exclude_dashes, force_delete_all):
    ''' Returns all "old" dashboard or monitor IDs that belong to email older than removal_time '''
    func = "api." + endpoint + ".get_all()"
    response = eval(func)
    old_objs = set()
    objs = response[API_OBJS[endpoint]] if API_OBJS[endpoint] else response

    for obj in objs:
        oid, o_email, o_modified, tags = 0, "", datetime.utcnow(), []

        if endpoint == 'Screenboard' or endpoint == 'Timeboard':
            oid, o_email, o_modified = _parse_response_dash(obj)
        elif endpoint == 'Monitor':
            oid, o_email, o_modified, tags = _parse_response_mtr(obj)

        o_timediff = (datetime.utcnow() - o_modified).total_seconds()

        if (force_delete_all or o_email == email) and o_timediff > removal_time:
            if endpoint == 'Screenboard' or endpoint == 'Timeboard':
                # if dashboard, check exclude_dashes
                if str(oid) not in exclude_dashes:
                    old_objs.add(oid)
            elif endpoint == 'Monitor':
                # if monitor, check exclude_tags
                if not [t for t in tags if t in exclude_tags]:
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
    ''' Helper: Return 4-tuple of monitor ID, email, modified datetime, and tags '''
    # convert the modified timestamp to datetime
    # offset is stripped since it is always +00:00 on org 2, 11287 and does not match +HHMM format for %z

    return (mtr['id'], mtr['creator']['email'], datetime.strptime(mtr['modified'][:-6], '%Y-%m-%dT%H:%M:%S.%f'), mtr['tags'])

def _confirm_deletion(objs):
    ''' Helper: Confirm deletion of objs; takes [Y/n] '''
    question = """Are you sure you would like to delete the following? [Y/n]
  Screenboards: {0}
  Timeboards:   {1}
  Monitors:     {2}"""
    yes = {'yes', 'y'}
    no  = {'no', 'n'}

    while True:
        sb_str = [str(id) for id in objs[0][1]]
        tb_str = [str(id) for id in objs[1][1]]
        mt_str = [str(id) for id in objs[2][1]]
        print question.format(sb_str, tb_str, mt_str)

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
        "-r", "--removaltime", help="Removal time; time since last modification to determine if something should be removed", type=int, default=7889231)
    parser.add_argument(
        "-t", "--excludetags", help="Tags to exclude from deletion; only applies to monitors", type=str, default="")
    parser.add_argument(
        "-d", "--excludedashes", help="Dashboard IDs to exclude from deletion", type=str, default="")
    parser.add_argument(
        "-f", "--forcedeleteall", help="Force delete all regardless of owner/email", action='store_true', default=False)
    args = parser.parse_args()

    api_key = args.apikey or os.getenv("DD_API_KEY", None)
    app_key = args.appkey or os.getenv("DD_APP_KEY", None)
    email   = args.email  or os.getenv("DD_EMAIL",   None)

    # time since last modified in seconds; used to determine if something is "old"
    removal_time  = args.removaltime
    exclude_tags = args.excludetags.split(',')
    exclude_dashes = args.excludedashes.split(',')
    force_delete_all = args.forcedeleteall
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
        old_objs = [(endpoint, \
                     get_old_objs(endpoint, email, removal_time, exclude_tags, exclude_dashes, force_delete_all)) \
                     for endpoint in API_OBJS.keys()]

        # check if any to delete, confirm deletion, then delete
        if sum([len(obj[1]) for obj in old_objs]) == 0:
            print "No old dashboards or monitors were found!"
        elif (_confirm_deletion(old_objs)):
            for endpoint, objs in old_objs:
                delete_objs(endpoint, objs)

            print "Deleted all old dashboards and monitors."
        else:
            print "Cancelled removal operation."

