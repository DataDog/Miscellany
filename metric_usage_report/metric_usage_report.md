# Metrics on Dashboards Report

#### Overview
This program is for anyone wondering "where the heck am I using this metric in my account?"

It is a simple console program written in Python 3 that utilizes the datadogpy API library to return a list of places in your account that contains any metric in a series of user provided metrics present on dashboards and/or monitors.

This program requires that the datadogpy library be installed on the machine or environment on which the program is running.  Download and installation instructions can be found [here](https://github.com/DataDog/datadogpy)

The command to install datadogpy for Python3 is `pip3 install datadog`

**NOTE**: This program is not recommended for use with Python3.  Python3 string objects do not use utf-8 encoding, meaning that any non ASCII character in a board or metric name will break this program if it runs in Python2.

#### How to Run It
Once you have copied this program locally, it can be run in a terminal from the directory it is stored in by running `python3 main.py`.  All required values should first be entered into the constant variables located in config.py

### Sample Config File
```
#Your Datadog API Key
API_KEY = "<redacted>"

#Your Datadog Application Key
APP_KEY = "<redacted>"

# should the program check for metrics present in dashboards?
CHECK_DASHBOARDS = True

# should the program check for metrics present in monitors?
CHECK_MONITORS = True

# a list of strings, values should match metrics tpresent in your account
METRICS_TO_EVAL = ["pi.temp", "datadog.agent.up", "system.cpu.idle"]
```



#### Sample Run Through
Below is a sample run of the program:

```
API Intialized!


Getting Your Metrics Report


***DASHBOARDS***



	Title: RasPi Screenboard

		 Metric: pi.temp

		 Metric: system.cpu.idle


	Title: Nate's Work Comp Stats

		 Metric: datadog.agent.up


	Title: EXAMPLE

		 Metric: system.cpu.idle


	Title: EXAMPLE 2

		 Metric: system.cpu.idle

***MONITORS***



	Title: Temperature Monitor: BigBoy

		 Metric: pi.temp
```