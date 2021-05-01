#make sure the datadogpy library is downloaded in this machine or environment first
import config
import os
try:
    from datadog import initialize, api
except ImportError:
    print("Please make sure the datadogpy library is downloaded in this machine or environment first.  You can find installation instructions at https://github.com/DataDog/datadogpy")
    quit()

def init():
    # initializes the datadog library to forward to the Datadog API
    options = {
    "api_key" : config.API_KEY,
    "app_key" : config.APP_KEY
    }

    initialize(**options)

    # confirm that api/apps keys are valid
    test_resp = api.DashboardList.get_all()
    if test_resp.get("errors") is None:
        print("API Intialized!\n\n")
    else:
        print("There was a problem initializing the API. Please verify your API and App Keys.")
        print(test_resp.get("code"), test_resp.get("errors"))
        quit()
    
    # set file paths to be created relative to script
    config.DB_CACHE_PATH = os.path.join(os.path.dirname(__file__), config.DB_CACHE_PATH)
    config.JSON_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), config.JSON_OUTPUT_PATH)
    config.CSV_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), config.CSV_OUTPUT_PATH)
    config.MARKDOWN_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), config.MARKDOWN_OUTPUT_PATH)


