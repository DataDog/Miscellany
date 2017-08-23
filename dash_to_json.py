import json
import sys
import os

from argparse import ArgumentParser
from datadog import initialize, api

'''Example usage:

Convert dash to json:
python dash_to_json.py get -d 214520 -a your_api_key_here -p your_app_key_here

Convert dash to json, specifying output file:
python dash_to_json.py get -d 214520 -f my_screenboard.json -a your_api_key_here -p your_app_key_here

Create dash from json file:
python dash_to_json.py create -f my_timeboard.json -a your_api_key_here -p your_app_key_here'''

def dash_to_json(dash, board_type, filename):
    dash_dict = {}
    if board_type == "timeboard":
        dash_dict = {
            "read_only": dash.get('read_only', 'False'),
            "description": dash.get('description', ''),
            "title": dash.get('title', 'New Timeboard'),
            "graphs": dash.get('graphs', []),
            "template_variables": dash.get('template_variables', []),
        }
    elif board_type == "screenboard":
        dash_dict = {
            "board_title": dash.get('board_title', 'New Screenboard'),
            "description": dash.get('description', ''),
            "widgets": dash.get('widgets', []),
            "width": dash.get('width', 1024),
            "template_variables": dash.get('template_variables', [])
        }
    print "Writing {} to {}".format(board_type, filename)
    with open(filename, 'wt') as out:
        json.dump(dash_dict, out, sort_keys=True, indent=4, separators=(',', ': '))

def create_dash(dash_dict, board_type):
    if board_type == "timeboard":
        title = dash_dict.get('title', 'New Timeboard')
        read_only = dash_dict.get('read_only', 'False')
        description = dash_dict.get('description', '')
        graphs = dash_dict.get('graphs', [])
        template_variables = dash_dict.get('template_variables', [])
        res = api.Timeboard.create(title=title, description=description, graphs=graphs,
                                   template_variables=template_variables, read_only=read_only)
        if res.get('errors', None):
            print res
        else:
            print "Successfully created timeboard"
    elif board_type == "screenboard":
        title = dash_dict.get('board_title', 'New Screenboard')
        description = dash_dict.get('description', '')
        widgets = dash_dict.get('widgets', [])
        width = dash_dict.get('width', 1024)
        template_variables = dash_dict.get('template_variables', [])
        res = api.Screenboard.create(board_title=title, description=description,
                                     widgets=widgets, template_variables=template_variables, width=width)
        if res.get('errors', None):
            print res
        else:
            print "Successfully created screenboard"
    else:
        print_error("Board type undefined")

def print_error(msg):
    print "\nERROR: {}\n".format(msg)
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    parser = ArgumentParser(description='Download dashboard as JSON and create new Dash from JSON')
    parser.add_argument('action', help='Either get or create')
    parser.add_argument('-d', help='The dashboard ID', required=False)
    parser.add_argument('-f', help='file_name', required=False)
    parser.add_argument('-a', help='Datadog API key', required=False)
    parser.add_argument('-p', help='Datadog APP key', required=False)

    args = parser.parse_args()

    action = args.action
    api_key = args.a if args.a else os.environ.get('DD_API_KEY'),
    app_key = args.p if args.p else os.environ.get('DD_APP_KEY'),
    file_name = args.f
    dash_id = args.d

    api_key = api_key[0] if isinstance(api_key, tuple) else api_key
    app_key = app_key[0] if isinstance(app_key, tuple) else app_key

    if not api_key or not app_key:
        print_error("Need to provide api_key and app_key either as an argument or set as an environment variable")
    if action not in ['get', 'create']:
        print_error("The first argument must be an action.  Options: get / create")

    options = {
        'api_key': api_key,
        'app_key': app_key
    }

    initialize(**options)

    if action == 'get':
        board = ''
        board_type = ''

        if not dash_id:
            print_error("Specify a dashboard id using --d if you are using action: get")

        try:
            res = api.Timeboard.get(dash_id)
            board = res['dash']
            board_type = "timeboard"
        except:
            pass

        if 'errors' in board or not board:
            try:
                board = api.Screenboard.get(dash_id)
                board_type = "screenboard"
            except:
                pass

        print "Dashboard {} is a {}...".format(dash_id, board_type)

        if board and board_type:
            file_name = file_name if file_name else board_type + '-' + dash_id + '.json'
            dash_to_json(board, board_type, file_name)
        else:
            print_error("Could not download dashboard")
    else:
        if not file_name:
            print_error("Must specify a file name --f when creating a dashboard")
        try:
            with open(file_name) as data_file:
                data = json.load(data_file)
            board_type = ''
            if data.get('widgets', None):
                board_type = "screenboard"
            elif data.get('graphs', None):
                board_type = "timeboard"
            if data and board_type:
                create_dash(data, board_type)
            else:
                print_error("Could not load data from JSON file")
        except:
            print_error("There was an error creating the dashboard")
    sys.exit(0)
