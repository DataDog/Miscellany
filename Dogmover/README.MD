# DogMover

![Alt text](./dogmover.png "A moving dog.")

This tool was originally built to help migrate customers screenboards, timeboards and monitors from our US instance to our EU instance. The tool also supports moving the data within the same instances (eg., EU to EU, or US to US and even EU to US.)

## Install
1. Clone this repository.
2. Install all python dependencies: `pip install -r requirements.txt --upgrade`
2. Add your _api_key_, _app_key_ to `config.json` for both the source (the organization where you will pull the data from) and the destination (to where you will be pushing the data to). See `config.json.example`. 

## Usage
To pull (export) a organizations screenboards, do:
`./dogmover.py pull screenboards --dry-run`
To push (import) a organizations screenboards, do:
`./dogmover.py push screenboards --dry-run`

The arguments supported are:
`./dogmover.py pull|push screenboards|timeboards|monitors [--dry-run] `

If you feel safe with the output Dogmover is giving you, run without `--dry-run` to make an actual pull/push.

### Note
1. When not running in `--dry-run` mode, all pulls will create a JSON file locally on your file system, which can be useful if you are looking to backup data with pull (for say, version controlling). The files are stored in:
``` 
./screnboards/*.json
./timeboards/*.json
./monitors/*.json
```

2. If you are pushing monitors, all your monitors will be automatically muted to suppress monitors from triggering false/positive alerts as we help migrate customers from one instance to another. This is done as a scheduled downtime, remove it in the GUI if this is not what you want.

### Known issues
1. EU instance is not supported in Datadogpy <0.3.0, please make sure to run `pip install -r requirements.txt --upgrade` or Dogmover may not work as expected for you.
