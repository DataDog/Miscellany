from datadog import initialize, api
from os import environ
from sys import argv

# This is not essential; see https://github.com/DataDog/datadogpy#environment-variables
OPTIONS = {
    'api_key': environ['DD_API_KEY'],
    'app_key': environ['DD_APP_KEY'],
    'api_host': environ['DD_SITE_URL']
}
# Initialize the Datadog API client.
initialize(**OPTIONS)

# These are the types of widgets that would be updated.
# See https://docs.datadoghq.com/dashboards/widgets
SUPPORTED_WIDGETS = ['timeseries', 'query_value', 'toplist', 'change']


def get_dashboard_ids():
    all_dashboards = api.Dashboard.get_all()
    dashboard_ids = []
    for dashboard in all_dashboards['dashboards']:
        dashboard_ids.append(dashboard['id'])
    return dashboard_ids


def get_dashboard_details(dashboard_ids):
    dashboard_details = []
    for id in dashboard_ids:
        dashboard_details.append(api.Dashboard.get(id=id))
    return dashboard_details


def prepare_dashboards_to_update(dashboard_details, old_metric, new_metric):
    # Holds dashboard IDs that need updating.
    dashboard_ids_to_update = []
    # Holds updated dashboard details.
    dashboard_details_to_update = []
    for dashboard in dashboard_details:
        # Holds a given widgets index position.
        widget_index = 0
        for widget in dashboard['widgets']:
            widget_definition = widget['definition']
            if widget_definition['type'] in SUPPORTED_WIDGETS:
                widget_requests = widget_definition['requests']
                # Holds updated request queries for a given widget.
                updated_requests = []
                for request in widget_requests:
                    # Only update a widget if the old metric is in one of its queries.
                    if old_metric in request['q']:
                        request['q'] = request['q'].replace(
                            old_metric, new_metric)
                        updated_requests.append(request)
                        if dashboard['id'] not in dashboard_ids_to_update:
                            dashboard_ids_to_update.append(dashboard['id'])
                # Reassign the updated list of widgets to its previous position.
                dashboard['widgets'][widget_index]['definition']['requests'] = updated_requests
            widget_index += 1
        # Only append to the list of dashaboards those that need updating.
        if dashboard['id'] in dashboard_ids_to_update:
            dashboard_details_to_update.append(dashboard)
    return dashboard_details_to_update


def update_dashboards():
    if(len(argv) < 3):
        print('Arguments needed: --destructive|--dry_run old_metric new_metric')
        exit(0)
    else:
        all_dashboard_ids = get_dashboard_ids()
        all_dashboard_details = get_dashboard_details(all_dashboard_ids)
        dashboards_to_update = prepare_dashboards_to_update(
            all_dashboard_details, argv[2], argv[3])
        for dashboard in dashboards_to_update:
            print('DASHBOARD: ' +
                  dashboard['title'] + ' by ' + dashboard['author_name'])
            print('URL: ' + dashboard['url'])
            if argv[1] == '--destructive':
                api.Dashboard.update(
                    dashboard['id'], title=dashboard['title'], widgets=dashboard['widgets'], layout_type=dashboard['layout_type'])
                print('UPDATED: True')
            elif argv[1] == '--dry_run':
                print('UPDATED: False')


update_dashboards()
