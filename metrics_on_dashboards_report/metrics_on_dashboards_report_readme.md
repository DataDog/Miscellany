#Metrics on Dashboards Report

This program is a simple console program written in Python 2.7.10, and utilizes the datadogpy API library to return a list of dashboards that have any metric in a series of user provided metrics present in their queries.

This program requires that the datadogpy library be installed on the machine or environment on which the program is running.  Download and installation instructions can be found [here](https://github.com/DataDog/datadogpy)

Once you have copied this program locally, it can be run in a terminal from the directory it is sotred in by running `python metrics_on_dashboards_report.py`.  Simply follow the on screen instructions, and receive a report of Dashboards where any of the metrics you provide are used.

This program is for anyone wondering "where the heck am I using this metric on my Dashboards?"

*Note*: The calls that this program makes to the API use deprecated libraries that Datadog still offers support for.  Efforts to rewrite this program with the new Dashboard API over the separate Timeboard and Screenboard API calls are not currently planned, though I may do this in the future.