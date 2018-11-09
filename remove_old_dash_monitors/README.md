# Remove old dashboards & monitors

## Purpose

This Python script will remove all old dashboards and monitors from an account belonging to the email as specified in the script's parameter. It uses the [Datadog API endpoint](https://docs.datadoghq.com/api/?lang=python) to get a list/dict of all screenboards, timeboards, and monitors.

A dashboard or monitor is determined to be "old" if it the time since it was last modified is 3 months or greater by default; this timeframe can be modified.

You can also specify any dashboard IDs to exclude, as well as monitor tags to avoid deleting.

This is useful for cleaning up accounts with a large number of old dashboards and monitors that have not been used for a very long time, as manually deleting these can be a hassle.

## Usage

##### `./remove_old_dash_monitors.py [OPTIONS...]`

#### Options

`-k`, `--apikey` DD API key

`-a`, `--appkey` DD app key

`-e`, `--email` DD email used to login

`-r`, `--removaltime` (Optional) Removal time in seconds; time since last modification to determine if something is "old" and should be removed. Defaults to 7889231 (3 months)

`-t`, `--excludetags` (Optional) Tags to exclude from deletion; only applies to monitors. Format is string separated by commas

`-d`, `--excludedashes` (Optional) Dashboard IDs to exclude from deletion. Format is string separated by commas

`-f`, `--forcedeleteall` (Optional) Force delete all dashboards and monitors, regardless of owner/email. **CAUTION:** This is a dangerous option!

#### Environment variables

Can be used as an alternative for API/app keys and email.

* `DD_API_KEY`
* `DD_APP_KEY`
* `DD_EMAIL`

#### Example use

To perform the cleanup with the following conditions:

* Delete all dashboards & monitors older than 1 week since last modification
* Don't delete the following dashboards: `963954`, `456220`, `471289`
* Don't delete any of the monitors that have any of the following tags: `random_tag`, `keep_alive`

```bash
$ ./remove_old_dash_monitors.py -r 604800 -d "963954,456220,471289" -t "random_tag,keep_alive"
Are you sure you would like to delete the following? [Y/n]
  Screenboards: ['474394', '478109']
  Timeboards:   ['897928', '919162']
  Monitors:     ['6384800']
Y
Deleted all old dashboards and monitors.
```
