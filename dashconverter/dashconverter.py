from datadog import initialize, api
from argparse import ArgumentParser

import sys
import os

# python2 compatability
try:
    input = raw_input
except NameError:
    pass

parser = ArgumentParser(
    description='Convert from screenboard to timeboard and vice versa. Set api-key and app-key via flags or env vars e.g. DD_API_KEY, DD_APP_KEY')
parser.add_argument('dashboard_id', help='The dashboard ID')
parser.add_argument('--api-key', help='Datadog API key', required=False)
parser.add_argument('--app-key', help='Datadog APP key', required=False)
parser.add_argument(
    '--title', help='Title for the converted dashboard', required=False)
parser.add_argument('--api-host', help='Datadog API endpoint URL', required=False)

args = parser.parse_args()

options = {
    'api_key': args.api_key if args.api_key else os.environ.get('DD_API_KEY'),
    'app_key': args.app_key if args.app_key else os.environ.get('DD_APP_KEY'),
}
if args.api_host:
    options.update({'api_host': args.api_host})

if not all(options.values()):
    parser.print_help()
    sys.exit(1)

initialize(**options)


class converter(object):
    graphs = []
    board = []
    board_type = ""
    widgets = []
    template_variables = []
    title = args.title or ""

    @classmethod
    def getdash(cls, dash):
        # Get the dashboard or the screenboard associated with the ID in the arg
        # Set the dashboard type

        try:
            cls.board = api.Timeboard.get(dash)
            cls.template_variables = cls.board['dash']['template_variables']
            if not cls.title:
                cls.title = "Screenboard (converted from " + \
                    cls.board['dash']['title'] + ")"
        except:
            pass
        print(cls.board_type)

        if 'errors' in cls.board:
            print("Reference ## is not in your timeboards")
            try:
                cls.board = api.Screenboard.get(dash)
                cls.template_variables = cls.board['template_variables']
                if not cls.title:
                    cls.title = "Timeboard (converted from " + \
                        cls.board['board_title'] + ")"
            except:
                pass
        else:
            cls.board_type = "timeboard"
            return cls.board_type

        if 'errors' in cls.board:
            print("Reference ## is not in your screenboards")
        else:
            cls.board_type = "screenboard"

    @classmethod
    def delete_dash(cls, dash):
        print("\nIf you have any warning above about outdated widget types, you should not delete the original dashboard. Follow the described procedure to properly convert the dashboard. \n")
        delete = input("Do you want to delete the dash (Y/n): ")
        if delete == "Y" and cls.board_type == "screenboard":
            print("deleting screenboard: " + cls.board['board_title'])
            api.Screenboard.delete(dash)

        elif delete == "Y" and cls.board_type == "timeboard":
            print("deleting timeboard " + cls.board['dash']['title'])
            api.Timeboard.delete(dash)

        elif delete == "n":
            print("No further action needed")

        else:
            print("Please select Y or n.")
            cls.delete_dash(dash)

    @classmethod
    def widget_transform(cls):
        # Transform the widget list so they are properly formatted
        # Take off the Screenboard widgets not available in the Timeboards
        # Returns the list of the different widgets

        if cls.board_type == "screenboard":
            # Get the widgets
            finaltimeboard_widgets = []
            screenwidgets = cls.board['widgets']
            # Filter the illegal widgets
            forbidden_widget = ['free_text', 'alert_value', 'check_status',
                                'event_timeline', 'event_stream', 'image', 'note', 'alert_graph', 'iframe']
            tmp = [screenwidgets[x]['type']
                   not in forbidden_widget for x in range(len(screenwidgets))]

            # Add the valid widgets
            for x in range(len(tmp)):
                if tmp[x]:
                    finaltimeboard_widgets.append(screenwidgets[x])
            return finaltimeboard_widgets

        else:
            return cls.board['dash']['graphs']

        # Convert the widgets
    @classmethod
    def convert_s2t(cls, widgets):
        # Function to convert Screenboard to Timeboard.
        # Takes the widgets as input and output the widgets properly formatted.
        # Appends an additional attribute for the hostmap.
        # no output, just tranforms the cls.graphs
        # If "show a title" is unchecked, use the query as the new widget title.

        for i in range(len(widgets)):

            if 'tile_def' in widgets[i]:
                if 'conditional_formats' not in widgets[i]['tile_def']['requests'][0]:
                    widgets[i]['tile_def']['requests'][0]['conditional_formats'] = []
            else:
                widgets[i]['tile_def'] = 'outdated'
                print("One of the widgets' type is outdated and won't be ported.\n To solve this, just click on edit the dashboard, open a widget, hit done and save the dashboard.\n Then run the script again.")

            if not (('title_text' in widgets[i]) and (isinstance(widgets[i]['title_text'], str if sys.version_info[0] >= 3 else basestring))):
                widgets[i]['title_text'] = widgets[i]['tile_def']['requests'][0]['q']

            if widgets[i]['type'] == 'hostmap':
                cls.graphs.append({
                    "definition": {
                        "style": widgets[i]['tile_def']['style'],
                        "requests": widgets[i]['tile_def']['requests'],
                        "viz": widgets[i]['type'],
                    },
                    "title": widgets[i]['title_text']
                })
            elif widgets[i]['tile_def'] == 'outdated':
                pass
            else:

                cls.graphs.append({
                    "definition": {
                        "events": [],
                        "requests": widgets[i]['tile_def']['requests'],
                        "markers": widgets[i]['tile_def']['markers'] if 'markers' in widgets[i]['tile_def'] else [],
                        "viz": widgets[i]['type'],
                    },
                    "title": widgets[i]['title_text']
                })

        # Convert the widgets
    @classmethod
    def convert_t2s(cls, graphs):
        # Function to convert Timeboard to Screenboard.
        # Takes the widgets as input and output the widgets properly formatted.
        # pos_x, pos_y and tmp_y assure the right position of the widgets
        # margin, height and width are hardcoded values representing the default size of the widgets
        # hostmap, heatmap and distribution have specific treatment as their payload is different on a TB and on a SB

        pos_x = 0
        pos_y = 0
        height = 13
        width = 47
        margin = 5
        tmp_y = 0
        for i in range(len(graphs)):

            if i % 2 == 0 and i != 0:
                pos_x = 0
                tmp_y = pos_y

            elif i % 2 == 1 and i != 0:
                tmp_y = pos_y
                pos_y = pos_y + height + margin
                pos_x = width + margin

            if 'viz' not in graphs[i]['definition']:
                print("One of the widgets' type is outdated and won't be ported.\n To solve this, just click on edit the dashboard, open a widget, hit done and save the dashboard.\n Then run the script again.")
                # Defaults to timeseries to avoid having an empty screenboard.
                graphs[i]['definition']['viz'] = "timeseries"
                # If the vizualisation is a QVW, the user will have to open the original dashboard, Open and Save the faulty widget.
                print(graphs[i])

            if graphs[i]['definition']['viz'] not in ["note", "hostmap", "distribution", "heatmap"]:
                cls.widgets.append({
                    'height': height,
                    'width': width,
                    'timeframe': '4h',
                    'x': pos_x,
                    'y': tmp_y,
                    "tile_def": {
                        "requests": graphs[i]['definition']['requests'],
                        "viz": graphs[i]['definition']['viz'],
                    },
                    "title_text": graphs[i]['title'],
                    "title": True,
                    "type": graphs[i]['definition']['viz']
                })

            elif graphs[i]['definition']['viz'] == "heatmap" or graphs[i]['definition']['viz'] == "distribution":
                graphs[i]['definition']['requests'][0]['type'] = 'line'
                graphs[i]['definition']['requests'][0]['aggregator'] = 'avg'
                cls.widgets.append({
                    'height': height,
                    'width': width,
                    'timeframe': '4h',
                    'x': pos_x,
                    'y': tmp_y,
                    "tile_def": {
                        "requests": graphs[i]['definition']['requests'],
                        "viz": graphs[i]['definition']['viz'],
                    },
                    "title_text": graphs[i]['title'],
                    "title": True,
                    "type": "timeseries"
                })

            elif graphs[i]['definition']['viz'] == "hostmap":
                cls.widgets.append({
                    'height': height,
                    'width': width,
                    'timeframe': '4h',
                    'x': pos_x,
                    'y': tmp_y,
                    "tile_def": graphs[i]['definition'],
                    "title_text": graphs[i]['title'],
                    "title": True,
                    "type": "hostmap"
                })

            elif graphs[i]['definition']['viz'] == "note":
                cls.widgets.append({
                    'title': False,
                    'height': height,
                    'width': width,
                    'x': pos_x,
                    'y': pos_y,
                    'html': graphs[i]['definition']['content'],
                    'text_align': graphs[i]['definition']['text_align'],
                    'font_size': graphs[i]['definition']['font_size'],
                    'bgcolor': graphs[i]['definition']['background_color'],
                    "tick": True,
                    "tick_pos": graphs[i]['definition']['tick_pos'],
                    "tick_edge": graphs[i]['definition']['tick_edge'],
                    "type": "note"
                })

    @classmethod
    def main(cls, dash):
        # Main fuction to fetch the dashboards, extract the widgets, transform the widgets and push the result
        # Takes the dash to convert as an input
        # Outputs the url of the new dash

        cls.getdash(dash)
        if cls.board_type == "screenboard":
            widgets = cls.widget_transform()
            cls.convert_s2t(widgets)
            output = api.Timeboard.create(title=cls.title, description='description',
                                          graphs=cls.graphs, template_variables=cls.template_variables, read_only=False)
            cls.delete_dash(dash)
            print('Your new Timeboard is available at: {url}'.format(url=api._api_host + output['url']))

        else:
            graphs = cls.widget_transform()
            cls.convert_t2s(graphs)
            output = api.Screenboard.create(board_title=cls.title, description='description',
                                            widgets=cls.widgets, template_variables=cls.template_variables)
            cls.delete_dash(dash)
            print('Your new Screenboard is available at: {url}'.format(url=api._api_host + '/screen/' + str(output['id'])))


converter().main(args.dashboard_id)
