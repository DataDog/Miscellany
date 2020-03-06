# Datadog Widget Updater

A small utility to batch update Datadog dashboard widgets.

## Setting up your Python environment

Create a Python environment and install dependencies.

```bash
# Create a Python virtual environment
python3 -m venv venv
# Activate the environment
. venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

## Usage

This utility can be used in (a) dry-run mode and (b) destructive mode. The former will provide you with a list of dashboard to update and the latter will actually update the dashboards queries.

```bash
python --destructive|--dry_run old_metric new_metric
```

If you wanted to get a list of all dashboards that in which the `old_metric` value would be updated to `new_metric`, you would use the `--dry_run` option. For example, let's say we get an idea of which dashboards would be updated if we swapped `system.mem.*` for `docker.mem.*`, you would run:

```bash
python --dry_run system.mem docker.mem
# DASHBOARD: Support #293783 - CPU by Nico Suarez-Canton
# URL: /dashboard/b9r-4hb-qin/support-293783---cpu
# UPDATED: False
# DASHBOARD: Support #293783 - Memory by Nico Suarez-Canton
# URL: /dashboard/yrt-6hd-qay/support-293783---memory
# UPDATED: False
```

In contrast, the `--destructive` flag will allow you to update the dashboards. The output will be the same but it will confirm the update.

```bash
python --destructive system.mem docker.mem
# DASHBOARD: Support #293783 - CPU by Nico Suarez-Canton
# URL: /dashboard/b9r-4hb-qin/support-293783---cpu
# UPDATED: True
# DASHBOARD: Support #293783 - Memory by Nico Suarez-Canton
# URL: /dashboard/yrt-6hd-qay/support-293783---memory
# UPDATED: True
```
