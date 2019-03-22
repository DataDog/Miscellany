#make sure the datadogpy library is downloaded in this machine or environment first
from datadog import initialize,api
import re

def get_all_dashboard_id_list(resp, is_screenboard):
    getter = ''
    #the returned data for screenboards and timeboards are different, requiring a different 'getter' for each
    if is_screenboard:
        getter = 'screenboards'
    else:
        getter = 'dashes'
    dashboard_id_list = [int(d['id']) for d in resp.get(getter)]
    return dashboard_id_list

def get_metric_report(ids_list, metrics_to_eval, is_screenboard):
    #The final string to be returned is built on dashboards_with_metric
    board_title = ''
    getter = ''
    #different 'getter's are required again to account for differences in data returned for timeboards and screenboards title naming
    if is_screenboard:
        getter = 'board_title'
        print('\nSCREENBOARDS:\n')
    else:
        print('\nTIMEBOARDS:\n')
        getter = 'title'
    #Get the screen or timeboard
    for id in ids_list:
        #this prints just to let the user know it's not frozen, just working still
        #discrepencies in data returned require different instructions for screenboards vs. timeboards
        if is_screenboard:
            getter_two = 'widgets'
            resp = api.Screenboard.get(str(id))
        else:
            getter_two = 'graphs'
            resp = api.Timeboard.get(str(id)).get('dash')
        #in order to use the find method to check if metrics are present in the dashboard, I had to cast resp to a str type
        str_resp = str(resp.get(getter_two))
        for metric in metrics_to_eval:
                if str_resp.find(metric) != -1:
                    #build the dashboards with metrics string for each board, adding title of the board and metric name
                    #encoding was necessary here, as non-ascii characters are used in our front-end
                    if board_title != resp[getter].encode('utf-8'):
                        board_title = resp[getter].encode('utf-8')
                        print('\n\tBoard: ' + board_title)
                    print('\n\t\t Metric: ' + metric)

#user input logic flow
choice = ''
while choice != 'y':
    api_key = raw_input ('This program is designed to return a list of Datadog Dashboards that contain specific metrics. \nTo get started, please enter your API Key:\n')
    print('\n')
    app_key = raw_input ('Thank you.  Please enter a valid app_key\n')
    print('\n')
    num_of_metrics_to_search = input('How many metrics would you like to search for?\n')
    print('\n')
    #declare empty list to populate with metrics
    metrics_to_eval = []
    #gather metric names from user
    for i in range(0,num_of_metrics_to_search):
        metric = raw_input('Enter metric #' + str(i+1)+': ')
        metrics_to_eval.append(metric)

    choice = raw_input('api_key: ' + api_key + '\napp_key: ' + app_key + '\nnumber of metrics to search: ' + str(num_of_metrics_to_search) + '\nlist of metrics to search for: ' + str(metrics_to_eval) + '\nIf this is correct enter \'y\' to continue, or enter any other key to start over: ')
    print('\n')
#run it!

#initialize app and api keys for making API calls
print('Intializing API...\n')
options = {
    'api_key' : api_key,
    'app_key' : app_key
}
initialize(**options)
print('Intialized!\n')

#return every dashboard
print('Getting All Screenboards\n')
screen_resp = api.Screenboard.get_all()
print('All Screenboards Received!\n')
print('Getting All Timeboards\n')
time_resp = api.Timeboard.get_all()
print('All Timeboards Received!\n')


#get lists of ids from every dashboard
print('Getting Screenboard Id\'s\n')
screenboard_id_list = get_all_dashboard_id_list(screen_resp, True)
print('Screenboard Id\'s Received!\n')
timeboard_id_list = get_all_dashboard_id_list(time_resp, False)
#format and output to the console
print('Getting Metrics on Dashboards\n')
get_metric_report(screenboard_id_list, metrics_to_eval, True)
get_metric_report(timeboard_id_list, metrics_to_eval, False)