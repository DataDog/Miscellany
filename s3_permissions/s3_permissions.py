#!/usr/bin/env python
import argparse
import os
import sys
import textwrap
from datadog import initialize
from datadog import api
import boto3
import json
from terminaltables import DoubleTable

def analyze_bucket(bucket):
    client = boto3.client('s3')
    bucket_acl = client.get_bucket_acl(Bucket=bucket)
    permission = []

    for grants in bucket_acl['Grants']:
        if ('URI' in grants['Grantee']) and ('AllUser' in grants['Grantee']['URI']):
            permission.append(grants['Permission'])

    globalListAccess = 'NO'
    globalWriteAccess = 'NO'
    points=0
    if len(permission) >= 1:
        if len(permission) == 1:
            if permission[0] == 'READ':
                globalListAccess = 'YES'
                points+=1
            if permission[0] == 'WRITE':
                globalWriteAccess = 'YES'
                points+=1
        if len(permission) > 1:
            if permission[0] == 'READ':
                globalListAccess = 'YES'
                points+=1
            if permission[0] == 'WRITE':
                globalWriteAccess = 'YES'
                points+=1
            if permission[1] == 'READ':
                globalListAccess = 'YES'
                points+=1
            if permission[1] == 'WRITE':
                globalWriteAccess = 'YES'
                points+=1

        if globalListAccess == 'YES' or globalWriteAccess == 'YES':
            table_data = [
                ['BucketName', 'GlobalListAccess', 'GlobalWriteAccess'],
                [bucket, globalListAccess, globalWriteAccess],
            ]
            table = DoubleTable(table_data)
            table.inner_row_border = True
            print(table.table)

    api.Metric.send(
        metric="bucket.exposed",
        host="aws.s3.bucket." + bucket,
        points=points, #0=ok, 1=read exposed, 2=write exposed
        tags=["aws","s3","s3permissions"]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create an empty dashboard for testing purposes")
    parser.add_argument(
        "-k", "--apikey", help="Your Datadog API key", type=str, default=None)
    parser.add_argument(
        "-a", "--appkey", help="Your Datadog app key", type=str, default=None)
    args = parser.parse_args()
    api_key = args.apikey if args.apikey else os.getenv("DD_API_KEY")
    app_key = args.appkey if args.appkey else os.getenv("DD_APP_KEY")
    errors = []
    if not api_key:
        errors.append("""
                      You must supply your Datadog API key by either passing a
                      -k/--apikey argument or defining a DD_API_KEY
                      environment variable.""")
    if not app_key:
        errors.append("""
                      You must supply your Datadog application key by either
                      passing a -a/--appkey argument or defining a
                      DD_APP_KEY environment variable.""")
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
        try:
            res = boto3.resource('s3')
            for bucket in res.buckets.all():
                analyze_bucket(bucket.name)
        except Exception as err:
            print(err)
