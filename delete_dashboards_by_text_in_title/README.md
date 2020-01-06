# Delete Dashboards by Text within the Title

This script lets you delete dashboards based on their title.

## Steps

1. If you do not have the datadog module installed, run:
```
pip install datadog
```

2. Run:
```
python delete_dashboards.py
```

This will prompt you to enter your API key and application key (if they are not stored as an environment variable—`DD_API_KEY` and `DD_APP_KEY`), and the text to search for the dashboard(s) you want to delete. It will ask for confirmation before deleting the dashboards found and will also create a backup dashboard file named 'datadog_dashboards_backup.txt.'