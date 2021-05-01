
from datadog import api

import report_init
import get
import config
import sys
import json
import os

def search_widget(dashboard, widget, report):
    if str(widget["definition"].get("requests")).find(metric) >= 0:
        # initialize dashboard entry
        if dashboard["id"] not in report[metric]:
            report[metric][dashboard["id"]] = {"title":dashboard.get("title"),
                "url":dashboard.get("url"),
                "author":dashboard.get("author_handle"),
                "widgets":{}}

        # add widget to list
        report[metric][dashboard["id"]]["widgets"][widget["id"]] = widget["definition"].get("title","")


def search_dashboard(dashboard, report):
    if "widgets" not in dashboard:
        print("No widgets object found in dashboard\n", dashboard)
        return
    for widget in dashboard.get("widgets"):

        for metric in config.METRICS_TO_EVAL:

            # nested loop through group widgets
            if widget["definition"].get("type") == "group":
                for child_widget in widget["definition"]["widgets"]:
                    search_widget(dashboard, child_widget, report)
                break
            
            search_widget(dashboard, widget, report)


# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '=' * filled_length + '>' + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


if __name__ == "__main__":
    report_init.init()

    print("Getting your metrics report\n")

    # initialize metric report
    report = {}
    for metric in config.METRICS_TO_EVAL:
        report[metric] = {}

    if os.path.isfile(config.DB_CACHE_PATH):
        print("Cache file found, loading dashboard date from", config.DB_CACHE_PATH)
        with open(config.DB_CACHE_PATH, "r") as file:
            db_count = file.readline()
            print("db_count:",db_count)
            for i, line in enumerate(file):
                search_dashboard(json.loads(line), report)

                print_progress(i+1, db_count, bar_length = 50)

    else:
        print("No cache file found, writing API results to", config.DB_CACHE_PATH)
        all_dashboards = api.Dashboard.get_all()
        db_ids = [db['id'] for db in all_dashboards.get("dashboards")]
        with open(config.DB_CACHE_PATH, "w") as file:
            db_count = len(db_ids)

            file.write(str(db_count) + "\n")
            for i, db_id in enumerate(db_ids):
                db_response = api.Dashboard.get(db_id)
                if "errors" not in db_response:
                    search_dashboard(db_response, report)

                    file.write(json.dumps(db_response))
                    file.write("\n") # concatenating strings is expensive, writing a newline to a file is not

                    print_progress(i+1, db_count, bar_length = 50)

    print("\n", report)


    # print("\n***MONITORS***\n")
    # monitor_resp = api.Monitor.get_all()
    # monitor_id_list = get.all_id_list(monitor_resp, "monitor")
    # get.metric_report(monitor_id_list,config.METRICS_TO_EVAL, "monitor")