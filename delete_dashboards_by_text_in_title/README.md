# Delete Dashboards by Text within the Title

This script lets you delete dashboards based on text within the title or the title itself. For example, if you have dashboards named 'Dashboard One' and 'Dashboard Two', if you enter 'Dashboard' in the prompt, this will allow for the deletion of both dashboards. 

## Steps

1. If you do not have the datadog module installed, run:
```
pip install datadog
```

2. Run:
```
python delete_dashboards.py
```
This will prompt you to enter your API key, application key, and the text for the dashboard you want to delete, and will ask for confirmation before deleting the dashboards found.

## Note
The text you enter for the dashboards to delete is case-sensitive.