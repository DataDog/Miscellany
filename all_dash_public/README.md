# All Public Dashboards
This script will get all public dashboards for a given DD org.

## Disclaimer
These projects are not a part of Datadog's subscription services and are
provided for example purposes only. They are NOT guaranteed to be bug free
and are not production quality. If you choose to use to adapt them for use
in a production environment, you do so at your own risk.

This script uses unpublished Datadog API endpoints which are subject to
change at any time with no guarantee.

# Why does this need a script?
The Datadog public APIs for Dashboards as-of 2019-04 (https://docs.datadoghq.com/api/?lang=python#dashboards) does not include any indicators that a Dashboard has been made public.  

By using various dashboard list API calls we can get this information though:
https://docs.datadoghq.com/api/?lang=python#dashboard-lists

[Full logic documented in a comment within the code](https://github.com/DataDog/Miscellany/blob/master/all_dash_public/all-dash-public.py#L12-L42).

# Run Code
- Use `pyenv` to set your Python version to `2.7.15`
- Setup a python virtualenv: `virtualenv all_dash`
- Activate the virtualenv: `source all_dash/bin/activate`
- Run `pip install -r requirements.txt`
- Run `python all-dash-public.py -k <your-api-key> -a <your-app-key>`
  - Alternatively set `DATADOG_API_KEY` or `DD_API_KEY` and `DATADOG_APP_KEY` or
    `DD_APP_KEY` as environment variables

# Output
Script will pretty print a json dict of all public dashboards; should look like:

```
{
  "23818": {
      "author": {
          "handle": "<redacted>",
          "name": "<redacted>"
      },
      "created": "2015-06-05T17:30:28.696235+00:00",
      "icon": null,
      "id": 23818,
      "is_favorite": false,
      "is_read_only": false,
      "is_shared": true,
      "modified": "2015-06-08T18:05:23.081090+00:00",
      "new_id": "5te-63y-6rm",
      "popularity": 0,
      "title": "Docker web infrastructure",
      "type": "custom_screenboard",
      "url": "/screen/23818/docker-web-infrastructure"
  },
  "137359": {
      "author": {
          "handle": "<redacted>",
          "name": "<redacted>"
      },
      "created": "2016-11-16T01:27:57.595832+00:00",
      "icon": null,
      "id": 137359,
      "is_favorite": false,
      "is_read_only": false,
      "is_shared": true,
      "modified": "2018-06-15T15:26:25.450240+00:00",
      "new_id": "q6e-nnm-d45",
      "popularity": 3,
      "title": "AWS Overview",
      "type": "custom_screenboard",
      "url": "/screen/137359/aws-overview"
  },
  "138348": {
      "author": {
          "handle": "<redacted>",
          "name": "<redacted>"
      },
      "created": "2016-11-18T17:56:35.542561+00:00",
      "icon": null,
      "id": 138348,
      "is_favorite": false,
      "is_read_only": true,
      "is_shared": true,
      "modified": "2018-07-05T17:36:53.159331+00:00",
      "new_id": "pgd-kev-qv9",
      "popularity": 1,
      "title": "DEVOPS BOARD",
      "type": "custom_screenboard",
      "url": "/screen/138348/devops-board"
  }
}
...
==============================
Script complete. Found 1051 public dashboards.
JSON has been dumped to ./public-dashboards.json
Exiting...
```
