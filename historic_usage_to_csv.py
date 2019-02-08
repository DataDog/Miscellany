"""
Disclaimer:
These projects are not a part of Datadog's subscription services and are provided for example purposes only
They are NOT guaranteed to be bug free and are not production quality
If you choose to use to adapt them for use in a production environment, you do so at your own risk.
"""

import datetime
import os
import time
import csv
import requests
import simplejson

from argparse import ArgumentParser, RawTextHelpFormatter

"""
This script is meant to pull historical usage metrics and export them to CSV.  Set variables in __init__.
"""

class UsageReport(object):

    def __init__(self, api_key, app_key, start_hour, end_hour, type, filename):
        self.api_key = api_key
        self.app_key= app_key
        self.type = type
        self.filename = filename
        self.url = 'https://app.datadoghq.com/api/v1/usage/' + type + '?api_key=' + api_key + '&application_key=' + app_key + '&start_hr=' + start_hour + '&end_hr=' + end_hour

    def get_usage_metrics(self):
        usage_metrics = []
        error_messages = []
        try:
            metrics = requests.get(self.url).json()
            if metrics.get('errors', None):
                print(metrics['errors'])
                return usage_metrics
            usage_metrics = metrics.get('usage', None)
            error_messages = metrics.get('errors', [])
            for m in error_messages:
                print('Error when retrieving metrics: {}'.format(m))
        except requests.exceptions.MissingSchema:
            print('Invalid URL format: {}'.format(url))
        except requests.exceptions.ConnectionError:
            print('Could not connect to url: {}'.format(url))
        except simplejson.scanner.JSONDecodeError:
            print('The response did not contain JSON data')
        return usage_metrics

    def gen_usage_report(self):
        # Get usage metrics from Datadog
        metrics = self.get_usage_metrics()
        # print(metrics)
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, mode='a+') as output_file:
            metric_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if not file_exists:
                if self.type == 'hosts':
                    metric_writer.writerow(['hour', 'total_host_count', 'container_count', 'apm_host_count', 'agent_host_count', 'gcp_host_count', 'aws_host_count'])
                elif self.type == 'timeseries':
                    metric_writer.writerow(['hour', 'num_custom_timeseries'])
                elif self.type == 'logs':
                    metric_writer.writerow(['hour', 'indexed_events_count', 'ingested_events_bytes'])
            for m in metrics:
                hour = m.get('hour', False)
                if self.type == 'hosts':
                    metric_writer.writerow([hour, m['host_count'], m['container_count'], m['apm_host_count'], m['agent_host_count'], m['gcp_host_count'], m['aws_host_count']])
                elif self.type == 'timeseries':
                    metric_writer.writerow([hour, m['num_custom_timeseries']])
                elif self.type == 'logs':
                    metric_writer.writerow([hour, m['indexed_events_count'], m['ingested_events_bytes']])


if __name__ == '__main__':
    parser = ArgumentParser(description='Poll datadog API for usage metrics and export to CSV.  Example: \n\npython historic_usage_to_csv.py -a your-api-key -k your-app-key -s 2018-11-01T01 -e 2018-11-04T01 -t logs -f log_usage.csv', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-a', '--api_key', help='Datadog API key', required=True)
    parser.add_argument('-k', '--app_key', help='Datadog APP key', required=True)
    parser.add_argument('-s', '--start_hour', help='YYYY-MM-DDTHH (ex. 2018-11-01T01)', required=True)
    parser.add_argument('-e', '--end_hour', help='YYYY-MM-DDTHH (ex. 2018-12-01T01)', required=True)
    parser.add_argument('-t', '--type', help='One of "hosts", "logs", or "timeseries" (metrics)', required=True)
    parser.add_argument('-f', '--filename',help='Filename to export metrics', required=True)


    args = parser.parse_args()
    api_key = args.api_key
    app_key = args.app_key
    start_hour = args.start_hour
    end_hour = args.end_hour
    type = args.type
    filename = args.filename

    if type not in ['hosts', 'logs', 'timeseries']:
        print('\nError: Argument "endpoint" must be one of "hosts", "logs", or "timeseries"\n')
        exit(0)
    print(args)

    UsageReport(api_key, app_key, start_hour, end_hour, type, filename).gen_usage_report()
