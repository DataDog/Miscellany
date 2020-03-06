#make sure the datadogpy library is downloaded in this machine or environment first
try:
    from datadog import initialize, api
except ImportError:
    print("please make sure the datadogpy library is downloaded in this machine or environment first.  You can find installation instructions at https://github.com/DataDog/datadogpy")
    quit()
import re

# init initializes the datadog library to forward to the Datadog API
def init(api_key, app_key):
    options = {
    'api_key' : api_key,
    'app_key' : app_key
    }

    initialize(**options)

# test_init confirms that initialization of the datadog api wrapper client has been successful
def test_init():
    test_resp = api.DashboardList.get_all()
    if test_resp.get('errors') is None:
        print('API Intialized!\n\n')
    else:
        print('There was a problem Initialiizing the API.  Please restart and check your API and App Keys for validity.')
        quit()
