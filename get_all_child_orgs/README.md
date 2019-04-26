# All Child Orgs
Get all child orgs; this will use your existing chrome cookies; You need to be logged into the parent org you wish to get all child orgs for; This mirrors the data found on: https://app.datadoghq.com/account/multi-org-usage

## Disclaimer
These projects are not a part of Datadog's subscription services and are
provided for example purposes only. They are NOT guaranteed to be bug free
and are not production quality. If you choose to use to adapt them for use
in a production environment, you do so at your own risk.

This script uses a Datadog HTTP endpoint which is subject to change at any
time with no guarantee.

# Motivation
Currently (2019-04) the DD API does not return all child orgs when querying https://docs.datadoghq.com/api/?lang=bash#get-organization - the orgs array only returns a single org. This was tested against multiple know orgs with many child orgs.

Ideally we'd like to query these child orgs and get API keys for them so we can perform actions on their behalf, but that also is not supported today (see: https://docs.datadoghq.com/api/?lang=bash#key-management).

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
      "name": "zzzzz-kelnerhax3",
      "public_id": "9cd818ea5"
  },
  {
      "name": "zzzzz-kelnerhax4",
      "public_id": "a446b1b33"
  }
]
==============================
Script complete. Found 480 child orgs.
JSON has been dumped to ./org_list.json
Exiting...
```
