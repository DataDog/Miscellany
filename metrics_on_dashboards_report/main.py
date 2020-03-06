
from datadog import api

import api_init
import get
import config

#testing
import json

if __name__ == "__main__":
    api_init.init(config.API_KEY, config.APP_KEY)
    api_init.test_init()

    print("Getting Your Metrics Report\n\n")

    if config.CHECK_DASHBOARDS:
        print("***DASHBOARDS***\n")
        dash_resp = api.Dashboard.get_all()
        dash_id_list = get.all_id_list(dash_resp, "dash")
        get.metric_report(dash_id_list, config.METRICS_TO_EVAL, "dash")

    if config.CHECK_MONITORS:
        print("***MONITORS***\n")
        monitor_resp = api.Monitor.get_all()
        monitor_id_list = get.all_id_list(monitor_resp, "monitor")
        get.metric_report(monitor_id_list,config.METRICS_TO_EVAL, "monitor")