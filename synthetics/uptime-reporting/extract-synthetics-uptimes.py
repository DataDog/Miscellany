import csv
import sys
from datetime import datetime
from time import time

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.synthetics_api import (
    SyntheticsApi,
    SyntheticsFetchUptimesPayload,
)

UPTIME_PERIOD_IN_SECONDS = 60 * 60 * 24 * 30  # 1 month

configuration = Configuration()
## https://github.com/DataDog/datadog-api-client-python?tab=readme-ov-file#authentication
# configuration.api_key["apiKeyAuth"] = "XXX"
# configuration.api_key["appKeyAuth"] = "XXX"

with ApiClient(configuration) as api_client:
    api_instance = SyntheticsApi(api_client)

    print("Fetching tests...")
    response = api_instance.list_tests()
    print(f"Found {len(response["tests"])} tests, fetching uptimes...")
    public_ids = [test["public_id"] for test in response["tests"]]
    tests = {test["public_id"]: {"name": test["name"]} for test in response["tests"]}

    to_ts_in_seconds = int(time())
    from_ts_in_seconds = to_ts_in_seconds - UPTIME_PERIOD_IN_SECONDS
    resp = api_instance.fetch_uptimes(
        SyntheticsFetchUptimesPayload(
            public_ids=list(tests.keys()),
            from_ts=from_ts_in_seconds,
            to_ts=to_ts_in_seconds,
        )
    )
    for uptime in resp:
        public_id = uptime["public_id"]
        if uptime["overall"].get("errors"):
            tests[public_id]["uptime"] = "No uptime data"
            tests[public_id]["alert_periods"] = []
        else:
            overall_uptime = uptime["overall"]
            tests[public_id]["uptime"] = "{:0.2f}%".format(overall_uptime["uptime"])
            tests[public_id]["alert_periods"] = []
            for i, [timestamp, status] in enumerate(overall_uptime["history"]):
                if status == 1:  # 1 represents an alert state
                    alert_start = timestamp
                    alert_end = (
                        overall_uptime["history"][i + 1][0]
                        if i + 1 < len(overall_uptime["history"])
                        else to_ts_in_seconds
                    )
                    format_alert = lambda timestamp: datetime.fromtimestamp(
                        timestamp
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    tests[public_id]["alert_periods"].append(
                        f"FROM {format_alert(alert_start)} TO {format_alert(alert_end)}"
                    )

    output = csv.writer(sys.stdout)
    output.writerow(["Test name", "Uptime Percentage", "Alert periods"])
    for test in tests.values():
        output.writerow(
            [
                test["name"],
                test["uptime"],
                ";".join(test["alert_periods"])
                if test["alert_periods"]
                else "No alert periods",
            ]
        )
