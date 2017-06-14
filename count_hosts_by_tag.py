#!/usr/bin/env python
import re
import requests


def get_all_hosts(api_key, app_key):
    params = {
        "metrics": "avg:aws.ec2.cpuutilization,avg:azure.vm.percentage_cpu,avg:gcp.gce.instance.cpu.utilization,avg:system.cpu.idle,avg:system.cpu.iowait,avg:system.load.norm.15,avg:vsphere.cpu.usage",
        "with_apps": "true",
        "with_sources": "true",
        "with_aliases": "true",
        "with_meta": "true",
        "with_mute_status": "true",
        "with_tags": "true",
        "api_key": api_key,
        "application_key": app_key
    }
    response = requests.get(url="https://app.datadoghq.com/reports/v2/overview", params=params)
    if response.ok:
        return response.json()


def get_host_tag_counts(hosts, tag):
    tag_pattern = re.compile(r"^%s[:.*]{0,1}" % tag)
    host_count_by_tag = {}
    # Query each host, building a count for each passed tag
    for host in hosts["rows"]:
        # Build unique list of tags from all sources
        tags = set()
        for src, src_tags in host["tags_by_source"].iteritems():
            [tags.add(t) for t in filter(tag_pattern.match, src_tags)]
        # Filter out all tags that do not match tag search pattern
        # tags = filter(tag_pattern.match, tags)
        for t in tags:
            if t not in host_count_by_tag:
                host_count_by_tag[t] = 0
            host_count_by_tag[t] += 1
    return host_count_by_tag


if __name__ == "__main__":
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(description="Count hosts in your infrastructure by a given tag")
    parser.add_argument("-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument("-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    parser.add_argument("tag", help="Tag used to count number of hosts", type=str)
    args = parser.parse_args()
    api_key = args.apikey or os.getenv("DATADOG_API_KEY", None)
    app_key = args.appkey or os.getenv("DATADOG_APP_KEY", None)
    errors = []
    if not api_key:
        errors.append("You must supply your Datadog API key by either passing a -k/--apikey argument or defining \
                       a DATADOG_API_KEY environment variable.")
    if not app_key:
        errors.append("You must supply your Datadog app key by either passing a -a/--appkey argument or defining \
                       a DATADOG_API_KEY environment variable.")
    if errors:
        for error in errors:
            print error
        sys.exit(2)
    print "Querying hosts with tag \"%s\"..." % args.tag
    hosts = get_all_hosts(api_key, app_key)
    host_tag_counts = get_host_tag_counts(hosts, args.tag)
    for tag, host_count in sorted(host_tag_counts.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        print "%s \t %s" % (host_count, tag)