#Metrics on Dashboards Report

####Overview
This program is a simple console program written in Python 2.7.10, and utilizes the datadogpy API library to return a list of dashboards that have any metric in a series of user provided metrics present in their queries.

This program requires that the datadogpy library be installed on the machine or environment on which the program is running.  Download and installation instructions can be found [here](https://github.com/DataDog/datadogpy)

####How to Run It
Once you have copied this program locally, it can be run in a terminal from the directory it is stored in by running `python metrics_on_dashboards_report.py`.  Simply follow the on screen instructions, and receive a report of Dashboards where any of the metrics you provide are used.

####Sample Run Through
Below is a sample run of the program:

```This program is designed to return a list of Datadog Dashboards that contain specific metrics.
To get started, please enter your API Key:
<KEY_REDACTED>


Thank you.  Please enter a valid app_key
<KEY_REDACTED>


How many metrics would you like to search for?
2


Enter metric #1: system.mem.total
Enter metric #2: datadog.agent.running
api_key: <KEY_REDACTED>
app_key: <KEY_REDACTED>
number of metrics to search: 2
list of metrics to search for: ['system.mem.total', 'datadog.agent.running']
If this is correct enter 'y' to continue, or enter any other key to start over: y


Intializing API...

Intialized!

Getting All Screenboards

All Screenboards Received!

Getting All Timeboards

All Timeboards Received!

Getting Screenboard Id's

Screenboard Id's Received!

Getting Metrics on Dashboards


SCREENBOARDS:


        Board: Nate's Work Comp Stats

                 Metric: system.mem.total

                 Metric: datadog.agent.running

TIMEBOARDS:


        Board: SE_HiringChallenge_RunThrough_Board_1

                 Metric: datadog.agent.running
```

This program is for anyone wondering "where the heck am I using this metric on my Dashboards?"

*Note*: The calls that this program makes to the API use deprecated libraries that Datadog still offers support for.  Efforts to rewrite this program with the new Dashboard API over the separate Timeboard and Screenboard API calls are not currently planned, though I may do this in the future.