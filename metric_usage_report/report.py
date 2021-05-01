# standard packages
import os
import json
import re

# installed packaged
from datadog import api

# local packages
import report_init
import config
import progress_bar

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
        
        if not report[metric][dashboard["id"]]["widgets"][widget["id"]]:
            report[metric][dashboard["id"]]["widgets"][widget["id"]] = "untitled"


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


def output_json_file(report):
    with open(config.JSON_OUTPUT_PATH, "w") as file:
        json.dump(report, file, indent=4)

def output_md_file(report):
    with open(config.MARKDOWN_OUTPUT_PATH, "w") as file:
        file.write("# Metric Usage Report\n\n")

        # generate table of contents
        file.write("### Table of Contents\n")
        for i, metric in enumerate(report):
            heading_link = metric
            # copying logic from https://github.com/gjtorikian/html-pipeline/blob/0e3d84/lib/html/pipeline/toc_filter.rb#L40-L45
            heading_link = heading_link.lower()
            heading_link = re.sub(r'[^\w \-_]', "", heading_link) 
            heading_link = re.sub(r'[ _]', "-", heading_link)
            file.write("- [{metric}](#{heading_link})\n".format(metric = metric, heading_link = heading_link))
            # header links are numbers when there is more than 1 present
            if(len(report) > 1):
                file.write("  - [Dashboards](#dashboards-{})\n".format(i+1))
                file.write("  - [Monitors](#monitors-{})\n".format(i+1))
            else:
                file.write("  - [Dashboards](#dashboards)\n")
                file.write("  - [Monitors](#monitors)\n")
        file.write("\n")

        # generate content
        for m_key, metric in report.items():
            file.write("## {metric}\n\n".format(metric = m_key))
            # dashboards table
            file.write("### Dashboards\n\n")
            file.write("| Title | Author | Widgets |\n")
            file.write("|-|-|-|\n")
            for d_key, dashboard in metric.items():

                db_link = "https://app.datadoghq.com{db_url}".format(db_url = dashboard["url"])
                widgets = ""
                for w_key, widget in dashboard["widgets"].items():
                    w_link = "{db_link}?fullscreen_widget={w_key}".format(db_link = db_link, w_key = w_key)
                    widgets += "- [{w_name}]({w_link})<br> ".format(w_name = widget, w_link = w_link)
                file.write("| [{db_title}]({db_link}) | {auth} | {widgets} |\n".format(
                    db_title=dashboard["title"],
                    db_link = db_link,
                    auth = dashboard["author"],
                    widgets = widgets[:-5])) # slice removes the extra newline character
            file.write("\n")

            #monitors table
            file.write("### Monitors\n\n")
            file.write("| Title | Author |\n")
            file.write("|-|-|\n")
            file.write("| | |\n")

 
if __name__ == "__main__":
    report_init.init()

    print("Getting your metrics report\n")

    # initialize metric report
    db_report = {}
    for metric in config.METRICS_TO_EVAL:
        db_report[metric] = {}

    # generate dashboard report from file
    if os.path.isfile(config.DB_CACHE_PATH):
        print("Cache file found, loading dashboards from", config.DB_CACHE_PATH)
        with open(config.DB_CACHE_PATH, "r") as file:
            db_count = file.readline()
            print("db_count:",db_count)
            for i, line in enumerate(file):
                search_dashboard(json.loads(line), db_report)

                progress_bar.print_progress(i+1, db_count, bar_length = 50)

    # generate dashboard report from API calls
    else:
        print("No cache file found, writing dashboard API results to", config.DB_CACHE_PATH)
        all_dashboards = api.Dashboard.get_all()
        db_ids = [db['id'] for db in all_dashboards.get("dashboards")]
        with open(config.DB_CACHE_PATH, "w") as file:
            db_count = len(db_ids)

            file.write(str(db_count) + "\n")
            for i, db_id in enumerate(db_ids):
                db_response = api.Dashboard.get(db_id)
                if "errors" not in db_response:
                    search_dashboard(db_response, db_report)

                    file.write(json.dumps(db_response))
                    file.write("\n") # concatenating strings is expensive, writing a newline to a file is not

                    progress_bar.print_progress(i+1, db_count, bar_length = 50)

    print("\n", db_report)
    output_md_file(db_report)

    # print("\n***MONITORS***\n")
    # monitor_resp = api.Monitor.get_all()
    # monitor_id_list = get.all_id_list(monitor_resp, "monitor")
    # api.Monitor.get(str(id))
    # get.metric_report(monitor_id_list,config.METRICS_TO_EVAL, "monitor")