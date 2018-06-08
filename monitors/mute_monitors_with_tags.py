# This script mutes all monitors that are tagged with a set of monitor tags. Parameters, including the API and
# application keys, the tag filter, and the end of the downtime, are set in code.

import calendar
from datetime import datetime, timedelta

from datadog import initialize, api

options = {
    'api_key': '',
    'app_key': ''
}

# A comma separated list of monitor tags to filter monitors
monitor_tags = "role:example"

# End time for the downtime (in UTC)
downtime_end = datetime(2018, 6, 8, 20)
# Alternatively, uncomment this line to specify the end time relative to the current time
#downtime_end = datetime.utcnow() + timedelta(hours=2)

initialize(**options)
downtime_end = calendar.timegm(downtime_end.timetuple())

monitors = api.Monitor.get_all(monitor_tags=monitor_tags)
for monitor in monitors:
    api.Monitor.mute(monitor["id"], end=downtime_end)
