# All Child Orgs
Get all child orgs; this will use your existing chrome cookies; You need to be logged into the parent org you wish to get all child orgs for; This mirrors the data found on: https://app.datadoghq.com/account/multi-org-usage

## Disclaimer
These projects are not a part of Datadog's subscription services and are
provided for example purposes only. They are NOT guaranteed to be bug free
and are not production quality. If you choose to use to adapt them for use
in a production environment, you do so at your own risk.

This script uses a Datadog HTTP endpoint which is subject to change at any
time with no guarantee.

# Run Code
- Use `pyenv` to set your Python version to `2.7.15`
- Setup a python virtualenv: `virtualenv all_child_orgs`
- Activate the virtualenv: `source all_child_orgs/bin/activate`
- Run `pip install -r requirements.txt`
- Run `python all-child-orgs.py`

# Output
Script will pretty print a json dict of all public dashboards; should look like:

```
[
  {
      "public_id": "zzzzz-kelnerhax3",
      "name": "9cd818ea5"
  },
  {
      "public_id": "zzzzz-kelnerhax4",
      "name": "a446b1b33"
  }
]
==============================
Script complete. Found 480 child orgs.
JSON has been dumped to ./org_list.json
Exiting...
```
