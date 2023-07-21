# <img src="https://cdn.pixabay.com/photo/2016/10/15/15/17/digital-1742679_1280.jpg" alt="code generation Icon" width="" height="">

## What does this script do

When using the V2 metric submission API endpoint (https://docs.datadoghq.com/api/latest/metrics/#submit-metrics) users cannot specify multiple hots tags on the same `series` parameter.

Instead, we need to define a seperate `series` for each hostname.

This could be a tedious process especially if we have a large number of hosts with different metric value and timestamps.

`generate.sh` will automatically create a ready to use script that contains the proper API call to submit multiple data points for multiple hosts in different timestamps. 

## Instructions

Before launching the `generate.sh` script, make sure to fill up the `data.csv` file with the list of host names, their metric values and their timestamp accordingly.

Once done you can launch the `generate.sh` script which will automatically generate another script `send.sh` which could be executed to submit the metrics. 
