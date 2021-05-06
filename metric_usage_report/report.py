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

def search_widget(dashboard, widget, metric, report):
    if metric in str(widget["definition"].get("requests")):
        # initialize dashboard entry
        if dashboard["id"] not in report[metric]["dashboards"]:
            db_link = "https://app.datadoghq.com{db_url}".format(db_url = dashboard.get("url"))

            report[metric]["dashboards"][dashboard["id"]] = {
                "title":dashboard.get("title"),
                "link": db_link,
                "author": dashboard.get("author_handle"),
                "widgets": []}

        widget_link = "{db_link}?fullscreen_widget={w_id}".format(
            db_link = report[metric]["dashboards"][dashboard["id"]]["link"], 
            w_id = widget["id"])
        title = widget["definition"].get("title") or "untitled"
        report[metric]["dashboards"][dashboard["id"]]["widgets"].append({
            "title": title,
            "link": widget_link})

def search_dashboard(dashboard, report):
    if "widgets" not in dashboard:
        print("\nNo widgets object found in dashboard\n", dashboard)
        return
    for metric in config.METRICS_TO_EVAL:
        for widget in dashboard.get("widgets"):
            # nested loop through group widgets
            if widget["definition"].get("type") == "group":
                for child_widget in widget["definition"]["widgets"]:
                    search_widget(dashboard, child_widget, metric, report)
                break
            
            search_widget(dashboard, widget, metric, report)

def output_csv_file(report):
    with open(config.CSV_OUTPUT_PATH, "w") as file:
        file.write("Metric,Source,Dashboard Title,Dashboard Link,Author,Widget Title, Widget Link\n")
        for metric in config.METRICS_TO_EVAL:
            for dashboard in report[metric]["dashboards"].values():
                for widget in dashboard["widgets"]:
                    file.write("{metric},dashboard,\"{db_title}\",{db_link},{author},\"{w_title}\",{w_link}\n".format(
                        metric = metric,
                        db_title = dashboard["title"].replace("\"","\"\""),
                        db_link = dashboard["link"],
                        author = dashboard["author"],
                        w_title = widget["title"].replace("\"","\"\""),
                        w_link = widget["link"]
                    ))
            for monitor in report[metric]["monitors"]:
                monitor_link = "https://app.datadoghq.com/monitors/{}".format(monitor["id"])

                file.write("{metric},monitor,\"{title}\",{link},{author},,\n".format(
                    metric = metric,
                    title = monitor["name"].replace("\"","\"\""),
                    link = monitor_link,
                    author = monitor["creator"]["handle"],
                ))


def output_json_file(report):
    with open(config.JSON_OUTPUT_PATH, "w") as file:
        json.dump(report, file, indent=4)

def output_md_file(report):
    with open(config.MARKDOWN_OUTPUT_PATH, "w") as file:
        file.write("# Metric Usage Report\n\n")

        # generate table of contents
        file.write("### Table of Contents\n")
        for i, metric in enumerate(config.METRICS_TO_EVAL):
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
        for metric in config.METRICS_TO_EVAL:
            file.write("## {}\n\n".format(metric))
            # dashboards table
            file.write("### Dashboards\n\n")
            file.write("| Title | Author | Widgets |\n")
            file.write("|-|-|-|\n")
            for dashboard in report[metric]["dashboards"].values():
                widgets = ""
                for widget in dashboard["widgets"]:
                    widgets += "- [{w_name}]({w_link})<br> ".format(
                        w_name = widget["title"].replace("|","\|"), 
                        w_link = widget["link"])
                file.write("| [{db_title}]({db_link}) | {auth} | {widgets} |\n".format(
                    db_title=dashboard["title"].replace("|","\|"),
                    db_link = dashboard["link"],
                    auth = dashboard["author"],
                    widgets = widgets[:-5]
                    )) # slice removes the extra newline character
            file.write("\n")
            #monitors table
            file.write("### Monitors\n\n")

            file.write("| Title | Author |\n")
            file.write("|-|-|\n")
            for monitor in report[metric]["monitors"]:
                monitor_link = "https://app.datadoghq.com/monitors/{}".format(monitor["id"])
                file.write("| [{monitor_title}]({monitor_link}) | {author} |\n".format(
                    monitor_title = monitor["name"].replace("|","\|"),
                    monitor_link = monitor_link,
                    author = monitor["creator"]["handle"]
                ))
            file.write("\n[In-app Monitor Search](https://app.datadoghq.com/monitors/manage?q=metric%3A%22{}%22)\n\n".format(metric))


 
if __name__ == "__main__":
    report_init.init()

    print("Generating your metric usage report\n")

    # # initialize report
    report = {}
    for metric in config.METRICS_TO_EVAL:
        report[metric] = {"dashboards": {}, "monitors": {}}

    # generate dashboard report from file
    if os.path.isfile(config.DB_CACHE_PATH):
        print("Cache file found, loading dashboards from", config.DB_CACHE_PATH)
        with open(config.DB_CACHE_PATH, "r") as file:
            db_count = file.readline()
            print("db_count:",db_count)
            for i, line in enumerate(file):
                search_dashboard(json.loads(line), report)

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
                search_dashboard(db_response, report)

                file.write(json.dumps(db_response))
                file.write("\n") # concatenating strings is expensive, writing a newline to a file is not

                progress_bar.print_progress(i+1, db_count, bar_length = 50)

    # monitor logic is much easier, since it's possible to search by metric used
    for metric in config.METRICS_TO_EVAL:
        monitors = api.Monitor.search(query="metric:{}".format(metric))
        report[metric]["monitors"] = monitors["monitors"]

    # create file outputs
    output_json_file(report)
    output_md_file(report)
    output_csv_file(report)