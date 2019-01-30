"""Usage:
  dogmover.py pull (<type>) [--dry-run]
  dogmover.py push (<type>) [--dry-run]

Example, try with --dry-run first:
    dogmover.py pull timeboards --dry-run
    dogmover.py push timeboards --dry-run
    to make actual changes:
    dogmover.py pull timeboards
    and finally push to another organization:
    dogmover.py push timeboards

    Supported arguments:
    dogmover.py pull|push screenboards|monitors|dashboards

Options:
  -h, --help
  -d, --dry-run
"""
__author__ = "Misiu Pajor <misiu.pajor@datadoghq.com>"
__version__ = "1.0.0"
from docopt import docopt
import json
import os
import glob
from datadog import initialize, api

def _init_options(action):
    config_file = "config.json"
    try:
        with open(config_file) as f:
            config = json.load(f)
    except IOError:
        exit("No configuration file named: {} could be found.".format(config_file))
    
    options = {}
    if action == "pull":   
        options = {
            'api_key': config["source_api_key"],
            'app_key': config["source_app_key"],
            'api_host': config["source_api_host"]
        }
    elif action == "push":
            options = {
                'api_key': config["dest_api_key"],
                'app_key': config["dest_app_key"],
                'api_host': config["dest_api_host"]
            }

    initialize(**options)
    return options

def _ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def _json_to_file(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    _ensure_directory(path)
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, sort_keys = True, indent = 4)
    return filePathNameWExt

def _files_to_json(type):
    files = glob.glob('{}/*.json'.format(type))
    return files


def pull_screenboards():
    path = "none, running in dry mode."
    count = 0
    screenboards = api.Screenboard.get_all()

    for board in screenboards["screenboards"]:
        count = count + 1 
        json_data = api.Screenboard.get(board["id"])
        if not arguments["--dry-run"]:
            path = _json_to_file('screenboards', str(board["id"]), json_data)
        print("Pulling: {} with id: {}, writing to file: {}".format(board["title"].encode('utf8'), board["id"], path))
    print("Retrieved '{}' screenboards.".format(count))

def pull_timeboards():
    path = "none, running in dry mode."
    count = 0
    timeboards = api.Timeboard.get_all()

    for board in timeboards["dashes"]:
        count = count + 1
        json_data = api.Timeboard.get(board["id"])
        if not arguments["--dry-run"]:
            path = _json_to_file('timeboards', str(board["id"]), json_data) 
        print("Pulling: '{}' with id: {}, writing to file: {}".format(board["title"].encode('utf8'), board["id"], path))
    print("Retrieved '{}' timeboards.".format(count))


def pull_monitors():
    path = "none, running in dry mode."
    good_keys = ['tags', 'deleted', 'query', 'message', 'matching_downtimes', 'multi', 'name', 'type', 'options', 'id']
    new_monitors = []
    count = 0

    monitors = api.Monitor.get_all()
    for monitor in monitors:
        count = count + 1
        new_monitor = {}
        for k, v in monitor.items():
            if k in good_keys:
                new_monitor[k] = v
        if not arguments["--dry-run"]:
            path = _json_to_file('monitors', str(new_monitor["id"]), new_monitor)
        print("Pulling: {} with id: {}, writing to file: {}".format(new_monitor["name"].encode('utf8'), new_monitor["id"], path))
    print("Retrieved '{}' monitors.".format(count))
    return new_monitors


def push_screenboards():
    path = "none, running in dry mode."
    count = 0

    screenboards = _files_to_json("screenboards")
    if not screenboards:
        exit("No screenboards have been pulled yet. Consider pulling screenboards first.")
    for screenboard in screenboards:
        with open(screenboard) as f:
            data = json.load(f)
            count = count + 1
            if 'description' not in data:
                data["description"] = ""
            if 'width' not in data:
                data["width"] = "1024"
            # skip screenboards with no widgets in them
            if 'widgets' not in data:
                print("...Skipping {} as this screenboard has no widgets in it.".format(data["board_title"].encode("utf8")))
                continue
            print("Pushing {}".format(data["board_title"].encode('utf8')))    
            if not arguments["--dry-run"]:
                api.Screenboard.create(board_title=data["board_title"],
                                    description=data["description"],
                                    widgets=data["widgets"],
                                    template_variables=data["template_variables"],
                                    width=data["width"])
            print("Pushed {} screenboards".format(count))

def push_timeboards():
    path = "none, running in dry mode."
    count = 0

    timeboards = _files_to_json("timeboards")
    if not timeboards:
        exit("No timeboards have been pulled yet. Consider timeboards first.")
    for timeboard in timeboards:
        with open(timeboard) as f:
            data = json.load(f)
            count = count + 1
            if not 'template_variables' in data["dash"]:
                data["dash"]["template_variables"] = ""
            # skip timeboards with no graphs in them
            if not data["dash"]["graphs"]:
                print("...Skipping '{}' as this timeboard has no widgets in it.".format(data["dash"]["title"].encode('utf8')))
                continue
            print("Pushing: {}".format(data["dash"]["title"].encode('utf8')))
            if not arguments["--dry-run"]:
                api.Timeboard.create(title=data["dash"]["title"],
                                    description=data["dash"]["description"],
                                    graphs=data["dash"]["graphs"],
                                    read_only=data["dash"]["read_only"])
            print("Pushed {} timeboards.".format(count))


def push_monitors():
    path = "none, running in dry mode."
    count = 0

    monitors = _files_to_json("monitors")
    if not monitors:
        exit("No monitors have been pulled yet. Consider pulling monitors first.")
    for monitor in monitors:
        with open(monitor) as f:
            data = json.load(f)
            count = count + 1
            print("Pushing: {}".format(data["name"].encode('utf8')))
            if not arguments["--dry-run"]:
                api.Monitor.create(type=data['type'],
                                    query=data['query'],
                                    name=data['name'],
                                    message=data['message'],
                                    tags=data['tags'],
                                    options=data['options'])
    print("Pushed {} monitors.".format(count))
    if not arguments["--dry-run"]:
        print("NOTE! All monitors have been automatically muted to suppress monitors from triggering false/positive alert. Please make sure to remove th scheduled downtime in the GUI if this is not what you wanted.")
        api.Monitor.mute_all()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1rc')

    if arguments["--dry-run"]:
        print("You are running in dry-mode. No actual pull/push will be done to the organizations.")

    if arguments["pull"]:
        _init_options("pull")
        if arguments['<type>'] == 'screenboards':
            pull_screenboards()
        elif arguments['<type>'] == 'timeboards':
            pull_timeboards()
        elif arguments['<type>'] == 'monitors':
            pull_monitors()
    elif arguments["push"]:
        _init_options("push")
        if arguments['<type>'] == 'screenboards':
            push_screenboards()
        elif arguments['<type>'] == 'timeboards':
            push_timeboards()
        elif arguments['<type>'] == 'monitors':
            push_monitors()
