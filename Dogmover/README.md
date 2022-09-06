# Dogmover

___
### ⚠️ Dogmover has been deprecated in favor of the Datadog Sync CLI Tool ⚠️
### https://github.com/DataDog/datadog-sync-cli
___

![Dogmover](https://github.com/DataDog/Miscellany/blob/master/Dogmover/dogmover.png "A moving dog.")

This tool is built to help migrate Datadog `dashboards`, `monitors`, `users`, `synthetic api tests`, `synthetic browser tests`, `aws accounts`, `log pipelines`, `notebooks`, and `slos` from one Datadog organization (eg. in US) to another (eg. in EU). The tool also supports moving these resources within the same instances (eg. EU to EU _or_ US to US).

**Note:** It does _not_ move any historical data (eg., metrics, log messages, synthetic test results) as this is not supported due to security reasons.

## Install
1. Clone this repository.
2. Install all python dependencies: `pip install -r requirements.txt --upgrade`
3. Add your _api_key_, _app_key_ to `config.json` for both the source (the organization where you will pull the resources from) and the destination (to where you will be pushing the resources to). See `config.json.example`. 


## Usage
To pull (export) dashboards, run:

`./dogmover.py pull dashboards --dry-run`

To push (import) dashboards, run:

`./dogmover.py push dashboards --dry-run`

The arguments supported are:

`./dogmover.py pull|push dashboards|monitors|users|synthetics_api_tests|synthetics_browser_tests|awsaccounts|logpipelines|notebooks|slos [--dry-run] [-h]`

If you feel safe with the output Dogmover is giving you, run without `--dry-run` to commit your push/pull into your Datadog account.

## (optional) Usage via container

###  Install via container
1. Create image with Python 3 and relevant dependencies `docker build -t "dogmover" .`
2. Make sure the `dogmover.py` is executable `chmod +x dogmover.py`
3. Add your _api_key_, _app_key_ to `config.json` for both the source (the organization where you will pull the resources from) and the destination (to where you will be pushing the resources to). See `config.json.example`. 

### Usage via container
Usage is similar to the one without container:
`docker run --rm -v $(pwd):/dogmover dogmover pull|push dashboards|monitors|users|synthetics_api_tests|synthetics_browser_tests|awsaccounts|logpipelines|notebooks|slos [--dry-run] [-h]`

## Notes
### The --dry-run argument
If you are not using the `--dry-run` argument, all your pulls will create a JSON file locally on your file system, which can be useful if you are looking to backup your resources (for say, version controlling) or to modify the contents before pushing. The files are stored in:
``` 
./dashboards/*.json
./monitors/*.json
./users/*.json
./synthetics_api_tests/*.json
./synthetics_browser_tests/*.json
./awsaccounts/*.json
./logpipelines/*.json
./notebooks/*.json
./slos/*.json
```

### The --tag argument
You can choose to pull specific synthetic tests|monitors based on their tags, example usage:
`dogmover.py pull synthetics_api_tests --tag env:prod --tag application:abc`
`dogmover.py pull monitors --tag team:web`

`--tag` is currently only supported for synthetics_api_tests, synthetics_browser_tests and monitors.

### Pushing monitors will schedule a managed downtime
Pushing monitors will automatically schedule a managed downtime for _all_ your monitors, this is to suppress false/positive alerts. You can remove this scheduled downtime by navigating to `Monitors -> Manage downtime` in Datadog.


## Author
* Misiu Pajor (misiu.pajor@datadoghq.com)

## Contributors
Evangelos Thomatos (et.thomatos@datadoghq.com)
