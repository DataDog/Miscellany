# Remove old dashboards & monitors

## Purpose

This Python script will remove all old dashboards and monitors from an account belonging to the email as specified in the script's parameter.

An object is determined to be "old" if it the time since it was last modified is 3 months or greater by default; this timeframe can be modified.

It uses the [Datadog API endpoint](https://docs.datadoghq.com/api/?lang=python) to get a list/dict of all screenboards, timeboards, and monitors.

Eventually, an option will be added to check/remove everything, regardless of the creator.

This is useful for cleaning up accounts with a large number of old dashboards and monitors that have not been used for a very long time, as manually deleting these can be a hassle.

## Usage

##### `./remove_old_dash_monitors.py [OPTIONS...]`

##### Options

`-k`, `--apikey` DD API key

`-a`, `--appkey` DD app key

`-e`, `--email` DD email used to login

`-t`, `--time` (Optional) Time to remove; time since last modified in seconds to determine if something is "old"

##### Environment variables

Can be used as an alternative for API/app keys and email.

* `DD_API_KEY`
* `DD_APP_KEY`
* `DD_EMAIL`

##### Example use

```bash
$ ./remove_old_dash_monitors.py -t 604800
Are you sure you would like to delete the following? [Y/n]
  Screenboards: ['471289', '456220']
  Timeboards:   ['897928', '919162']
  Monitors:     ['6384800', '6509900']
y
Deleted all stale dashboards and monitors.
```
