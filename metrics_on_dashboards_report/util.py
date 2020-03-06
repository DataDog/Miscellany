def get_key_from_user(app_or_api):
    return input ("\n\nPlease enter your " + app_or_api + " Key:\n")

def get_num_of_metrics_from_user():
    is_number = False
    while not is_number:
        try:
            num_of_metrics_to_search = input('How many metrics would you like to search for?\n')
            print('\n\n')
            is_number = True
        except NameError:
            print('Whoops!  This entry must be an integer.  Please try again. \n\n')
        return num_of_metrics_to_search

def get_metric_names_from_user(num_of_metrics_to_search):
    metrics_to_eval = []
    for i in range(0,int(num_of_metrics_to_search)):
        metric = input('Enter metric #' + str(i+1)+': ')
        metrics_to_eval.append(metric)
    return metrics_to_eval

def confirm_inputs(api_key, app_key, num_of_metrics_to_search, metrics_to_eval):
    return input('\napi_key: ' + api_key + '\n\napp_key: ' + app_key + '\n\nnumber of metrics to search: ' + str(num_of_metrics_to_search) + '\n\nlist of metrics to search for: ' + str(metrics_to_eval) + '\n\nIf this is correct enter \'y\' to continue, or enter any other key to start over: ')