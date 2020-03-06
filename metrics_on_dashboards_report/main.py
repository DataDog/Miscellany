
from datadog import api

import re

import api_init
import util
import get

if __name__ == "__main__":
    #gather information from the user
    confirm = ''
    
    while confirm != 'y':
        print("This program is designed to return a list of Datadog Dashboards that contain specific metrics.")
        api_key = util.get_key_from_user("API")
        print('\n')
        app_key = util.get_key_from_user("APP")
        print('\n')

        num_of_metrics_to_search = util.get_num_of_metrics_from_user()
                
        metrics_to_eval = util.get_metric_names_from_user(num_of_metrics_to_search)
        
        print("\n--------")

        confirm = util.confirm_inputs(api_key, app_key, num_of_metrics_to_search, metrics_to_eval)

    #run the report
    api_init.init(api_key, app_key)
    api_init.test_init()

    print('Getting All Dashboards\n\n')
    resp = api.Dashboard.get_all()
    print('All Dashboards Received!\n\n')

    print('Getting Dashboard Id\'s\n\n')
    id_list = get.all_dashboard_id_list(resp)
    print("ID\'s received\n\n")

    print('Getting Your Report')
    get.metric_report(id_list, metrics_to_eval)