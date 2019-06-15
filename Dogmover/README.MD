# DogMover

![Alt text](./dogmover.png "A moving dog.")

This tool was originally built to help migrate customers `dashboards`, `monitors`, `users` and `synthetic tests` from our US to EU instance. The tool also supports moving the data within the same instances (eg., EU to EU _or_ US to US)

## Install
1. Clone this repository.
2. Install all python dependencies: `pip install -r requirements.txt --upgrade`
2. Add your _api_key_, _app_key_ to `config.json` for both the source (the organization where you will pull the data from) and the destination (to where you will be pushing the data to). See `config.json.example`. 

## Usage
To pull (export) dashboards, run:
`./dogmover.py pull dashboards --dry-run`
To push (import) dashboards, run:
`./dogmover.py push dashboards --dry-run`

The arguments supported are:
`./dogmover.py pull|push screenboards|timeboards|monitors [--dry-run] [-h]`

If you feel safe with the output Dogmover is giving you, run without `--dry-run` to commit your push/pulls into your Datadog account.

### Note
### The --dry-run flag
If you are not using the `--dry-run` flag, all your pulls will create a JSON file locally on your file system, which can be useful if you are looking to backup your data (for say, version controlling) or to modify the contents before pushing. The files are stored in:
``` 
./dashboards/*.json
./monitors/*.json
./users/*.json
./synthetics/*.json
```

### Pushing monitors will schedule a managed downtime
Pushing monitors will automatically schedule a managed downtime for _all_ your monitors, this is to suppress false/positive alerts. You can remove this scheduled downtime by navigating to `Monitors -> Manage downtime` in Datadog.