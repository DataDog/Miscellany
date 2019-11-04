#Metrics on Dashboards Report

####Overview
This program is for anyone wondering "where the heck am I using this metric on my Dashboards?"
It is a simple console program written in Python 3.7.1, that utilizes the datadogpy API library to return a list of dashboard titles that contain any metric in a series of user provided metrics present on the dashboard's widgets.

This program requires that the datadogpy library be installed on the machine or environment on which the program is running.  Download and installation instructions can be found [here](https://github.com/DataDog/datadogpy)

The command to install datadogpy for Python3 is `pip3 install datadog`

**NOTE**: This program is not recommended for use with Python2.  Python2 string objects do not use utf-8 encoding, meanign that any non ASCII character in a board or metric name will break this program if it runs in Python2.

####How to Run It
Once you have copied this program locally, it can be run in a terminal from the directory it is stored in by running `python3 metrics_on_dashboards_report.py`.  Simply follow the in-console instructions, and receive a report of Dashboards where any of the metrics you provide are used.

####Sample Run Through
Below is a sample run of the program:

```
This program is designed to return a list of Datadog Dashboards that contain specific metrics. 

To get started, please enter your API Key:
<KEY REDACTED>


Thank you.  Please enter a valid app_key
<KEY REDACTED>	


How many metrics would you like to search for?
2



Enter metric #1: system.cpu.idle
Enter metric #2: datadog.agent.up

--------

api_key: <KEY REDACTED>

app_key: <KEY REDACTED>

number of metrics to search: 2

list of metrics to search for: ['system.cpu.idle', 'datadog.agent.up']

If this is correct enter 'y' to continue, or enter any other key to start over: y



Intializing API...


API Intialized!


Getting All Dashboards


All Dashboards Received!


Getting Dashboard Id's


ID's received


Getting Your Report




	Board: EXAMPLE

		 Metric: system.cpu.idle


	Board: RasPi Screenboard

		 Metric: system.cpu.idle


	Board: Nate's Work Comp Stats

		 Metric: datadog.agent.up


	Board: EXAMPLE 2

		 Metric: system.cpu.idle
```