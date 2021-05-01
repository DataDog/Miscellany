# Metrics on Dashboards Report

## Overview

This program utilizes the [datadogpy API library](https://github.com/DataDog/datadogpy) to accept a list of metric names and return a list of dashboards in your account that use those metrics in their queries.


## How to Run It

1. Add your [API and App keys](https://docs.datadoghq.com/api/latest/authentication/) to [config.py](config.py).
2. Add your metric names into [config.py](config.py).
3. Run `python3 report.py`


## Caching

API calls are expensive and time consuming. To avoid requesting all dashboard definitions from your account every time you want a metric report, results are cached in json format in the file `db_cache.txt`. If that file exists, the script will automatically use those results instead.

To get a fresh list of dashboards, either rename or delete the file `db_cache.txt`.
