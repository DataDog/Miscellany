# Metrics Usage Report

## Overview

This program utilizes the [datadogpy API library](https://github.com/DataDog/datadogpy) to accept a list of metric names and return a list of dashboards and monitors in your account that use those metrics in their queries.


## Instructions

1. Add your [API and App keys](https://docs.datadoghq.com/api/latest/authentication/) to [config.py](config.py).
2. Add your metric names into [config.py](config.py).
3. Run `python3 report.py`

Reports will be placed in the results folder under the names `report.*`

## Example Output

- [Markdown Example File](results/example_usage_report.md)
- [CSV Example File](results/example_usage_report.csv)
- [JSON Example File](results/example_usage_report.json)

## Technical Details 

### Caching

API calls are expensive and time consuming. To avoid requesting all dashboard definitions from your account every time you want a metric report, results are cached in json format in the file `db_cache.txt`. If that file exists, the script will automatically use those results instead.

To get a fresh list of dashboards, either rename or delete the file `db_cache.txt`.

### untitled Widgets

If a widget doesn't have a title, dashboards will generate one based off the query inside. That logic was a bit too complex for me to replicate, so I just named them `unitled` to avoid having an empty string when displaying the widget in the report.
