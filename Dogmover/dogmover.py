#!/usr/bin/env python3
"""Usage:
  dogmover.py pull (<type>) [--tag tag]... [--dry-run] [-h]
  dogmover.py push (<type>) [--dry-run] [-h]

Examples:
    Dashboards:
        dogmover.py pull dashboards
        dogmover.py push dashboards

    Synthetic api tests using --tag that only pulls tests if all the defined tags exist on them:
        dogmover.py pull synthetic_api_tests p --tag env:production --tag application:abc
        dogmover.py push synthetic_api_tests

    Run with --dry-run without making any changes to your Datadog account:
        dogmover.py pull dashboards --dry-run
        dogmover.py push dashboards --dry-run
 
    Supported arguments:
    dogmover.py pull|push dashboards|monitors|users|synthetics_api_tests|synthetics_browser_tests|awsaccounts|logpipelines|notebooks (--tag tag) (--dry-run|-h)

    Note. --tag is currently only supported for synthetics_api_tests, synthetics_browser_tests and monitors.

Options:
  -h, --help
  -d, --dry-run
  --tag=<k:v>   Specify a tag in the format key:value
"""
__author__ = "Misiu Pajor <misiu.pajor@datadoghq.com>"
__version__ = "2.1.0"
from docopt import docopt
import json
import os
import glob
import requests
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

def pull_dashboards():
    path = False
    count = 0

    dashboards = api.Dashboard.get_all()
    for dashboard in dashboards["dashboards"]:
        count = count + 1
        json_data = api.Dashboard.get(dashboard["id"])
        if not arguments["--dry-run"]:
            path = _json_to_file('dashboards', dashboard["id"], json_data)
        print("Pulling dashboard: {} with id: {}, writing to file: {}".format(dashboard["title"].encode('utf8'), dashboard["id"], path))
    print("Retrieved '{}' dashboards.".format(count))

def pull_monitors(tag):
    path = False
    count = 0
    good_keys = ['tags', 'deleted', 'query', 'message', 'matching_downtimes', 'multi', 'name', 'type', 'options', 'id']
    tags = [] if not tag else tag
    monitors = api.Monitor.get_all()

    for monitor in monitors:
        if monitor["type"] == "synthetics alert":
                print("Skipping \"{}\" as this is a monitor belonging to a synthetic test. Synthetic monitors will be automatically re-created when you push synthetic tests.".format(monitor["name"].encode('utf8')))
                continue
        all_tags_found = True
        for tag in tags:
            if not tag in monitor["tags"]:
                all_tags_found = False
                print("Tag: {} not found in monitor: \"{}\" with tags {}".format(tag, monitor["name"].encode('utf8'), monitor["tags"]))
                break

        if all_tags_found == False:
            print("Skipping \"{}\" because its tags do not match the filter.".format(monitor["name"].encode('utf8')))

        if all_tags_found == True:
            count = count + 1

            new_monitor = {}
            for k, v in monitor.items():
                if k in good_keys:
                    new_monitor[k] = v
            if not arguments["--dry-run"]:
                path = _json_to_file('monitors', str(new_monitor["id"]), new_monitor)
            print("Pulling monitor: \"{}\" with id: {}, writing to file: {}".format(new_monitor["name"].encode('utf8'), new_monitor["id"], path))
    print("Retrieved '{}' monitors.".format(count))

def pull_users():
    path = False
    count = 0

    users = api.User.get_all()
    for user in users["users"]:
        if not user["disabled"]: # don't pull disabled users
            count = count + 1
            json_data = api.User.get(user["handle"])
            if not arguments["--dry-run"]:
                path = _json_to_file('users', user["handle"], json_data["user"])
            print("Pulling user: {} with role: {}, writing to file: {}".format(user["handle"].encode('utf8'), user["access_role"], path))
    print("Retrieved '{}' users.".format(count))


def pull_synthetics_api_tests(options, tag):
    path = False
    count = 0
    tags = [] if not tag else tag

    r = requests.get('{}api/v1/synthetics/tests?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]))
    synthetics = r.json()
    for synthetic in synthetics["tests"]:
        if synthetic["type"] == "api":
            all_tags_found="true"
            for tag in tags:
                if not tag in synthetic["tags"]:
                    all_tags_found="false"
                    print("Tag: {} not found in synthetic: \"{}\" with tags {}".format(tag, synthetic["name"].encode('utf8'), synthetic["tags"]))
                    break

            if all_tags_found == "false":
                print("Skipping \"{}\" because its tags do not match the filter.".format(synthetic["name"].encode('utf8')))

            if all_tags_found == "true":
                count = count + 1
                json_data = requests.get('{}api/v1/synthetics/tests/{}?api_key={}&application_key={}'.format(
                    options["api_host"],
                    synthetic["public_id"],
                    options["api_key"],
                    options["app_key"]
                )).json()
                path = _json_to_file('synthetics_api_tests', synthetic["public_id"], json_data)
                print("Pulling: {} and writing to file: {}".format(synthetic["name"].encode('utf8'), path))
    print("Retrieved '{}' synthetic tests.".format(count))

def pull_synthetics_browser_tests(options, tag):
    path = False
    count = 0
    tags = [] if not tag else tag

    r = requests.get('{}api/v1/synthetics/tests?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]))
    synthetics = r.json()
    for synthetic in synthetics["tests"]:
        if synthetic["type"] == "browser":
            all_tags_found="true"
            for tag in tags:
                if not tag in synthetic["tags"]:
                    all_tags_found="false"
                    print("Tag: {} not found in synthetic: \"{}\" with tags {}".format(tag, synthetic["name"].encode('utf8'), synthetic["tags"]))
                    break

            if all_tags_found == "false":
                print("Skipping \"{}\" because its tags do not match the filter.".format(synthetic["name"].encode('utf8')))

            if all_tags_found == "true":
                count = count + 1
                json_data = requests.get('{}api/v1/synthetics/tests/browser/{}?api_key={}&application_key={}'.format(
                    options["api_host"],
                    synthetic["public_id"],
                    options["api_key"],
                    options["app_key"]
                )).json()
                path = _json_to_file('synthetics_browser_tests', synthetic["public_id"], json_data)
                print("Pulling: {} and writing to file: {}".format(synthetic["name"].encode('utf8'), path))
    print("Retrieved '{}' synthetic tests.".format(count))


def pull_awsaccounts(options):
    path = False
    count = 0

    r = requests.get('{}api/v1/integration/aws?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]))
    awsaccounts = r.json()
    for awsaccount in awsaccounts["accounts"]:
        count = count + 1
        if not arguments["--dry-run"]:
            path = _json_to_file('awsaccounts', awsaccount["account_id"], awsaccount)
    print("Retrieved '{}' AWS accounts.".format(count))

def pull_logpipelines(options):
    path = False
    count = 0

    r = requests.get('{}api/v1/logs/config/pipelines?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]))
    rJSON = r.json()
    for item in rJSON:
        count = count + 1
        path = _json_to_file('logpipelines', item["id"], item)
    print("Retrieved '{}' log pipelines.".format(count))

def pull_notebooks(options):
    path = False
    count = 0

    headers = {'content-type': 'application/json', 'DD-API-KEY': options["api_key"], 'DD-APPLICATION-KEY': options["app_key"]}
    r = requests.get('{}/api/v1/notebooks'.format(options["api_host"]), headers=headers)
    notebooks = r.json()
    if notebooks["meta"]["page"]["total_filtered_count"] == 0:
        exit("No notebook could be found for your organization.")

    for notebook in notebooks["data"]:
        count = count + 1
        path = _json_to_file('notebooks', str(notebook["id"]), {"data": notebook})
        print("Pulling notebook: {} with id: {}, writing to file: {}".format(notebook["attributes"]["name"].encode('utf8'), notebook["id"], path))
    print("Retrieved '{}' notebooks.".format(count))

def pull_slos(options):
    path = False

    count = 0
    r = requests.get('{}api/v1/slo?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]))
    slos = r.json()

    for slo in slos["data"]:
        count = count + 1
        path = _json_to_file('slos', str(slo["id"]), slo)
    print("Retrieved '{}' SLOs.".format(count))

def push_dashboards():
    count = 0
    dashboards = _files_to_json("dashboards")
    if not dashboards:
        exit("No dashboards are locally available. Consider pulling dashboards first.")

    for dashboard in dashboards:
        with open(dashboard) as f:
            data = json.load(f)
            count = count + 1
            print("Pushing {}".format(data["title"].encode('utf8')))
            if not arguments["--dry-run"]:
                api.Dashboard.create(
                    title=data["title"],
                    description=data["description"],
                    widgets=data["widgets"],
                    template_variables=data["template_variables"],
                    layout_type=data["layout_type"],
                    notify_list=data["notify_list"],
                    is_read_only=data["is_read_only"]
                )
    print("Pushed '{}' dashboards".format(count))


def push_monitors():
    count = 0
    err_count = 0
    ids = {}
    monitors = _files_to_json("monitors")
    if not monitors:
        exit("No monitors are locally available. Consider pulling monitors first.")

    # first loop to import non composite monitors
    for monitor in monitors:
        with open(monitor) as f:
            data = json.load(f)
            if not data["type"] == "composite":
                old_id = str(data["id"])
                print("Pushing monitors:", data["id"], data["name"].encode('utf8'))
                if not arguments["--dry-run"]:
                    result = api.Monitor.create(type=data['type'],
                                        query=data['query'],
                                        name=data['name'],
                                        message=data['message'],
                                        tags=data['tags'],
                                        options=data['options'])
                    if 'errors' in result:
                        print('Error pushing monitor:',data["id"],json.dumps(result, indent=4, sort_keys=True))
                        err_count=err_count+1

                    else:
                        count = count + 1
                        new_id= result['id']
                        api.Monitor.mute(new_id)
                        print("New monitor ", str(new_id)," has been muted.")
                        ids[old_id] = str(new_id)
                else:
                    # Fake new id for dry-run purpose
                    ids[old_id] = old_id[:3] + "xxx"


    # Second loop to import composite monitors
    for monitor in monitors:
        with open(monitor) as f:
            data = json.load(f)
            if data["type"] == "composite":
                new_query = data["query"]
                for old_id, new_id in ids.items():
                    new_query=new_query.replace(old_id, new_id)
                print("Pushing composite monitors:", data["id"], data["name"].encode('utf8')," with query ", new_query.encode('utf8'))

                if not arguments["--dry-run"]:
                    result = api.Monitor.create(type=data['type'],
                                        query=new_query,
                                        name=data['name'],
                                        message=data['message'],
                                        tags=data['tags'],
                                        options=data['options'])
                    if 'errors' in result:
                        print('Error pushing monitor:',data["id"],json.dumps(result, indent=4, sort_keys=True))
                        err_count=err_count+1

                    else:
                        count = count + 1
                        new_id= result['id']
                        api.Monitor.mute(new_id)
                        print("New monitor ", str(new_id)," has been muted.")

    if count > 0:
        print("Pushed '{}' monitors in muted status, navigate to Monitors -> Manage downtime to unmute.".format(count))
    if err_count > 0:
        print("Error pushing '{}' monitors, please check !".format(err_count))

def push_users():
    count = 0
    users = _files_to_json("users")
    if not users:
        exit("No users are locally available. Consider pulling users first.")

    for user in users:
        with open(user) as f:
            data = json.load(f)
            count = count + 1
            print("Pushing: {}".format(data["handle"].encode('utf8')))
            if not arguments["--dry-run"]:
                api.User.create(
                    handle=data["handle"],
                    name=data["name"],
                    access_role=data["access_role"]
                )
    print("Pushed '{}' users".format(count))

def push_synthetics_api_tests(options):
    count = 0
    synthetics = _files_to_json("synthetics_api_tests")
    if not synthetics:
        exit("No synthetic tests are locally available. Consider synthetics first.")

    for synthetic in synthetics:
         with open(synthetic) as f:
            data = json.load(f)
            count = count + 1
            invalid_keys = ["public_id", "monitor_id"]
            list(map(data.pop, invalid_keys))
            print("Pushing {}".format(data["name"].encode('utf8')))
            if not arguments["--dry-run"]:
                r = requests.post('{}api/v1/synthetics/tests?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]), json=data)
    print("Pushed '{}' synthetic tests.".format(count))

def push_synthetics_browser_tests(options):
    count = 0
    synthetics = _files_to_json("synthetics_browser_tests")
    if not synthetics:
        exit("No synthetic tests are locally available. Consider synthetics first.")

    for synthetic in synthetics:
         with open(synthetic) as f:
            data = json.load(f)
            count = count + 1
            invalid_keys = ["public_id", "monitor_id"]
            list(map(data.pop, invalid_keys))
            print("Pushing {}".format(data["name"].encode('utf8')))
            if not arguments["--dry-run"]:
                r = requests.post('{}api/v1/synthetics/tests?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]), json=data)
    print("Pushed '{}' synthetic tests.".format(count))

def push_awsaccounts(options):
    count = 0
    awsaccounts = _files_to_json("awsaccounts")
    if not awsaccounts:
        exit("No awsaccounts are locally available. Consider pulling awsaccounts first.")

    for awsaccount in awsaccounts:
        with open(awsaccount) as f:
            data = json.load(f)
            count = count + 1
            print("Pushing {}".format(data["account_id"].encode('utf8')))
            if not arguments["--dry-run"]:
                r = requests.post('{}api/v1/integration/aws?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]), json=data)
                json_data = json.loads(r.text)
                json_data["account_id"] = data["account_id"]
                print(json.dumps(json_data))
                path = _json_to_file('awsaccounts.out', data["account_id"], json_data)
    print("Pushed '{}' AWS accounts.".format(count))
    print("You can now use the json files in the awsaccounts.out folder to automate the AWS External ID onboarding using AWS APIs.")

def push_logpipelines(options):
    count = 0
    fJSON = _files_to_json("logpipelines")
    if not fJSON:
        exit("No logpipelines are locally available. Consider pulling logpipelines first.")

    for item in fJSON:
        with open(item) as f:
            data = json.load(f)
            count = count + 1
            print("Pushing {}".format(data["id"].encode('utf8')))
            itemId = data['id']
            del data['id']
            del data['is_read_only']
            del data['type']
            headers = {'content-type': 'application/json'}
            if not arguments["--dry-run"]:
                r = requests.post('{}api/v1/logs/config/pipelines?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]), headers=headers, json=data)
                json_data = json.loads(r.text)
                json_data["id"] = itemId
                path = _json_to_file('logpipelines.out', itemId, json_data)
    print("Pushed '{}' log pipelines.".format(count))


def push_notebooks(options):
    count = 0
    notebooks = _files_to_json("notebooks")
    if not notebooks:
        exit("No notebooks are locally available. Consider pulling notebooks first.")

    for notebook in notebooks:
        with open(notebook) as f:
            data = json.load(f)
            count = count + 1
            print("Pushing: {}".format(data["data"]["attributes"]["name"].encode('utf8')))
            if not arguments["--dry-run"]:
                headers={'content-type': 'application/json', 'DD-API-KEY': options["api_key"], 'DD-APPLICATION-KEY': options["app_key"]}
                r = requests.post('{}/api/v1/notebooks'.format(options["api_host"]), headers=headers, json=data)
    print("Pushed '{}' notebooks".format(count))

def push_slos(options):
    count=0
    slos = _files_to_json("slos")
    if not slos:
        exit("No SLOs are locally available.  Consider pulling the SLOs first.")

    for slo in slos:
        with open(slo) as f:
            data = json.load(f)
            count = count + 1
            print("Pushing: {}".format(data["name"].encode('utf-8')))
            if not arguments["--dry-run"]:
                r = requests.post('{}api/v1/slo?api_key={}&application_key={}'.format(options["api_host"], options["api_key"], options["app_key"]), json=data)
    print("Pushed '{}' SLOs".format(count))

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1rc')

    if arguments["--dry-run"]:
        print("You are running in dry-mode. No changes will be commmited to your Datadog account(s).")

    if arguments["pull"]:
        _init_options("pull")
        if arguments['<type>'] == 'dashboards':
            pull_dashboards()
        elif arguments['<type>'] == 'monitors':
            pull_monitors(arguments["--tag"])
        elif arguments['<type>'] == 'users':
            pull_users()
        elif arguments['<type>'] == 'synthetics_api_tests':
            pull_synthetics_api_tests(_init_options("pull"), arguments["--tag"])
        elif arguments['<type>'] == 'synthetics_browser_tests':
            pull_synthetics_browser_tests(_init_options("pull"), arguments["--tag"])
        elif arguments['<type>'] == 'awsaccounts':
            pull_awsaccounts(_init_options("pull"))
        elif arguments['<type>'] == 'logpipelines':
            pull_logpipelines(_init_options("pull"))
        elif arguments['<type>'] == 'notebooks':
            pull_notebooks(_init_options("pull"))
        elif arguments['<type>'] == 'slos':
            pull_slos(_init_options("pull"))
    elif arguments["push"]:
        _init_options("push")
        if arguments['<type>'] == 'dashboards':
            push_dashboards()
        elif arguments['<type>'] == 'monitors':
            push_monitors()
        elif arguments['<type>'] == 'users':
            push_users()
        elif arguments['<type>'] == 'synthetics_api_tests':
            push_synthetics_api_tests(_init_options("push"))
        elif arguments['<type>'] == 'synthetics_browser_tests':
            push_synthetics_browser_tests(_init_options("push"))
        elif arguments['<type>'] == 'awsaccounts':
            push_awsaccounts(_init_options("push"))
        elif arguments['<type>'] == 'logpipelines':
            push_logpipelines(_init_options("push"))
        elif arguments['<type>'] == 'notebooks':
            push_notebooks(_init_options("push"))
        elif arguments['<type>'] == 'slos':
            push_slos(_init_options("push"))
