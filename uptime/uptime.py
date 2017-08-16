import os
import os.path
import sys
import time

from checks import AgentCheck, CheckException

# Modify this function to allow custom logic for determining whether the host is up. Note that this check is run in
# the main collector thread, so slow tasks performed in this function may reduce the agent's reporting frequency.
def is_up():
    return True

# See the following site for why this code is necessary on Windows.
# http://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html
replace = None
if sys.platform == 'win32':
    import win32api, win32con
    def replace(src, dst):
        win32api.MoveFileEx(src, dst, win32con.MOVEFILE_REPLACE_EXISTING)
else:
    replace = os.rename

class UptimeMetricAggregator:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.value = 0

class UptimeInterval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class UptimeCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)
        self.instance_cleanup_times = {}

    def check(self, instance):
        uptime_log_directory = instance['uptime_log_directory']

        # Logs previous uptimes. Only updated if a downtime occurs, or if one
        # of the past uptimes becomes older than the retention period.
        uptime_log_path = os.path.join(uptime_log_directory, 'uptime.log')

        now_ref_ts = int(time.time())

        # The metrics array can be empty, but it can't be missing
        metrics = [UptimeMetricAggregator(metric['name'], now_ref_ts - metric['timespan'], now_ref_ts)
            for metric in instance.get('metrics')]

        # The default retention is one year.
        # One year in seconds: 60 * 60 * 24 * 365.25 = 31557600
        retention = instance.get('retention', 31557600)
        min_cleanup_period = instance.get('min_cleanup_period', 3600)

        last_cleanup_ts = self.instance_cleanup_times.get(_instance_key(instance))
        if not last_cleanup_ts or last_cleanup_ts - now_ref_ts > min_cleanup_period:
            strip_old_entries = True
            self.instance_cleanup_times[_instance_key(instance)] = now_ref_ts
        # no need to update if first entry is retained
        else:
            strip_old_entries = False

        last_interval = None
        tmp_uptime_log_path = uptime_log_path + ".tmp"
        if os.path.isfile(uptime_log_path):
            with open(uptime_log_path, 'r') as uptime_log_file:
                interval = line_to_interval(uptime_log_file.readline())
                # We will later process each line in the file, so we must seek the beginning
                uptime_log_file.seek(0)
                if interval:
                    # We don't need to strip old entries if there are none.
                    if strip_old_entries and interval.end > now_ref_ts - retention:
                        strip_old_entries = False
                    if strip_old_entries:
                        with open(tmp_uptime_log_path, 'w') as tmp_uptime_log:
                            process_uptime_log_file(uptime_log_file, metrics, tmp_uptime_log, now_ref_ts - retention)
                            tmp_uptime_log.flush()
                            os.fsync(tmp_uptime_log)
                    else:
                        process_uptime_log_file(uptime_log_file, metrics)
            # Must wait until both files are closed
            if strip_old_entries:
                replace(tmp_uptime_log_path, uptime_log_path)
            last_interval = interval


        # Tracks the current uptime. Updated each time the check is run. A
        # separate file is used to avoid copying the entire log each time the
        # check runs.
        uptime_path = os.path.join(uptime_log_directory, 'uptime')
        downtime_threshold = instance['downtime_threshold']
        prev_interval = read_uptime_interval(uptime_path)
        current_interval = get_current_interval(now_ref_ts, prev_interval,
                                                downtime_threshold)
        update_metrics_with_interval(metrics, current_interval)

        # The following conditions must be met for us to add an interval to
        # the uptime log:
        # - the previous interval must exist
        # - the start of the current interval must differ from the start of
        # the previous interval
        # - the previous interval must have nonzero length (end > start)
        # - if the uptime history has an entry check that the last entry isn't
        # the same as the previous interval:
        # If the system crashes after adding an entry to the uptime log, but
        # before writing the current interval, we may find ourselves trying to
        # add an entry to the uptime log that already exists the next time the
        # check runs. Entries in the uptime log should be unique, so we must
        # check that the entry hasn't already been added. We check the second
        # entry to guard against a partial write, which would corrupt the log
        # file (which could be fixed with manual intervention), but would not cause
        # any uptime date to be lost.
        if (prev_interval and current_interval.start != prev_interval.start and
                prev_interval.start != prev_interval.end and
                (last_interval is None or
                    last_interval.end != prev_interval.end)):
            # add_entry_to_uptime_log(prev_interval, uptime_log_path)
            # The uptime log will be updated relatively infrequently, so it doesn't
            # make sense to add extra code to append entries when adding an interval.
            update_metrics_with_interval(metrics, prev_interval)
            add_entry_to_uptime_log(prev_interval, uptime_log_path)

        write_current_interval(current_interval, uptime_path)

        for metric in metrics:
            self.gauge(metric.name, float(metric.value) / (metric.end - metric.start))

def process_uptime_log_file(uptime_log_file, metrics, new_uptime_log_file=None, retention_min_ts=None):
    for line in uptime_log_file:
        interval = line_to_interval(line)
        update_metrics_with_interval(metrics, interval)
        if new_uptime_log_file and interval.end > retention_min_ts:
            new_uptime_log_file.write(line)

def update_metrics_with_interval(metrics, interval):
    for metric in metrics:
        if interval.end > metric.start:
            if interval.start > metric.start:
                metric.value = metric.value + interval.end - interval.start
            else:
                metric.value = metric.value + interval.end - metric.start

def _instance_key(instance):
    """ Returns a unique value for each valid instance of this check.

    The uptime_log_directory must be unique for each instance of the check, so we just use that.
    """
    return instance['uptime_log_directory']

# Generate the current uptime interval. The current interval depends
# the previous interval (whether it's None, how long ago it ended) and
# the downtime_threshold (did the previous interval end longer than
# downtime_threshold seconds ago).
def get_current_interval(current_time, prev_interval, downtime_threshold):
    if not is_up():
        return prev_interval
    if (not prev_interval or
            current_time - prev_interval.end > downtime_threshold):
        return UptimeInterval(current_time, current_time)
    else:
        return UptimeInterval(prev_interval.start, current_time)

def write_current_interval(current_interval, uptime_path):
    tmp_uptime_path = uptime_path + ".tmp"
    with open(tmp_uptime_path, 'w') as tmp_uptime_file:
        tmp_uptime_file.write(interval_to_line(current_interval))
        # We need to flush the file and call fsync to ensure that it is written to disk immediately. Experiments have
        # shown that closing the file object and renaming it are not sufficient to ensure that the file is written to
        # disk right away.
        tmp_uptime_file.flush()
        os.fsync(tmp_uptime_file)
    replace(tmp_uptime_path, uptime_path)

def add_entry_to_uptime_log(prev_interval, uptime_log_path):
    with open(uptime_log_path, 'a') as uptime_log:
        uptime_log.write(interval_to_line(prev_interval))
        uptime_log.flush()
        os.fsync(uptime_log)

def interval_to_line(interval):
    return "{0} {1}\n".format(interval.start, interval.end)

def line_to_interval(line):
    entry = line.rstrip('\n').split(' ')
    interval = UptimeInterval(int(entry[0]), int(entry[1]))
    if interval.start > interval.end:
        raise CheckException(
            "Invalid interval: first value ({0}) was greater than second ({1})"
            "".format(interval.start, interval.end))
    return interval

def read_uptime_interval(path):
    if os.path.isfile(path):
        with open(path) as uptime_file:
            return line_to_interval(uptime_file.readline())
    else:
        return None
