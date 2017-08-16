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

# Majority of S3 bucket code taken from http://www.awsomeblog.com/s3-bucket-permission-checker/

def analyze_bucket(client, bucket):
    bucket_location = client.get_bucket_location(
        Bucket=bucket)['LocationConstraint']
    new_client = boto3.client('s3', region_name=bucket_location)
    bucket_acl = new_client.get_bucket_acl(Bucket=bucket)
    permission = []

    for grants in bucket_acl['Grants']:
        if ('URI' in grants['Grantee']) and ('AllUser' in grants['Grantee']['URI']):
            permission.append(grants['Permission'])

    globalListAccess = 'NO'
    globalWriteAccess = 'NO'
    if len(permission) == 1:
        if permission[0] == 'READ':
            globalListAccess = 'YES'
            globalWriteAccess = 'NO'

        table_data = [
            ['BucketName', 'Region', 'GlobalListAccess', 'GlobalWriteAccess'],
            [bucket, bucket_location, globalListAccess, globalWriteAccess],
        ]
        table = DoubleTable(table_data)
        table.inner_row_border = True
        print(table.table)

    elif len(permission) > 1:
        if permission[0] == 'READ':
            globalListAccess = 'YES'
        if permission[1] == 'WRITE':
            globalWriteAccess = 'YES'
        else:
            globalWriteAccess = 'NO'

        table_data = [
            ['BucketName', 'Region', 'GlobalListAccess', 'GlobalWriteAccess'],
            [bucket, bucket_location, globalListAccess, globalWriteAccess],
        ]
        table = DoubleTable(table_data)
        table.inner_row_border = True
        print(table.table)


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
            client = boto3.client('s3')
            for bucket in res.buckets.all():
                analyze_bucket(client, bucket.name)
        except Exception as err:
            print(err)
