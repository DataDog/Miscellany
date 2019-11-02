#make sure the datadogpy library is downloaded in this machine or environment first
try:
    from datadog import initialize,api
except ImportError:
    print("please make sure the datadogpy library is downloaded in this machine or environment first.  You can find installation instructions at https://github.com/DataDog/datadogpy")
    quit()
import re

def get_all_dashboard_id_list(resp):

    id_list = [d['id'] for d in resp.get("dashboards")]
    return id_list

def get_metric_report(ids_list, metrics_to_eval):

    board_title = ''

    #Get the dashboard
    for id in ids_list:

        resp = api.Dashboard.get(str(id))

        #cast resp to string and find
        str_resp = str(resp.get("widgets"))
        #check for metrics on dash
        for metric in metrics_to_eval:
                if str_resp.find(metric) != -1:

                    #build the dashboards with metrics string for each board, adding title of the board and metric name
                    if board_title != resp["title"]:
                        print('\n\n\tBoard: ' + resp["title"])
                    print('\n\t\t Metric: ' + metric)

#user input logic flow

choice = ''

while choice != 'y':

    #get api and app keys from user

    api_key = input ('This program is designed to return a list of Datadog Dashboards that contain specific metrics. \n\nTo get started, please enter your API Key:\n')
    print('\n')
    app_key = input ('Thank you.  Please enter a valid app_key\n')
    print('\n')

    #get number of metrics to evaluate from user
    is_number = False
    while not is_number:
        try:
            num_of_metrics_to_search = input('How many metrics would you like to search for?\n')
            print('\n\n')
            is_number = True
        except NameError:
            print('Whoops!  This entry must be an integer.  Please try again. \n\n')
            
    #declare empty list to populate with metrics
    metrics_to_eval = []

    #gather metric names from user
    for i in range(0,int(num_of_metrics_to_search)):
        metric = input('Enter metric #' + str(i+1)+': ')
        metrics_to_eval.append(metric)
    
    print("\n--------")

    choice = input('\napi_key: ' + api_key + '\n\napp_key: ' + app_key + '\n\nnumber of metrics to search: ' + str(num_of_metrics_to_search) + '\n\nlist of metrics to search for: ' + str(metrics_to_eval) + '\n\nIf this is correct enter \'y\' to continue, or enter any other key to start over: ')
    print('\n\n')
#run it!

#initialize app and api keys for making API calls
print('Intializing API...\n\n')
options = {
    'api_key' : api_key,
    'app_key' : app_key
}

initialize(**options)

#Test to see that we're properly initialized by making a call to the API that requires no arguments
test_resp = api.DashboardList.get_all()
if test_resp.get('errors') is None:
    print('API Intialized!\n\n')
else:
    print('There was a problem Initialiizing the API.  Please restart and check your API and App Keys for validity.')
    quit()

#return every dashboard
print('Getting All Dashboards\n\n')
resp = api.Dashboard.get_all()
print('All Dashboards Received!\n\n')

#get lists of ids from every dashboard
print('Getting Dashboard Id\'s\n\n')
id_list = get_all_dashboard_id_list(resp)
print("ID\'s received\n\n")

#format and output to the console
print('Getting Your Report\n\n')
get_metric_report(id_list, metrics_to_eval)