# Note: this script utilizes the updated Dashboard API endpoint that unifies the screenboard and timeboard APIs
# See API documentation for additional details: https://docs.datadoghq.com/api/?lang=python#dashboards

# Scripts that access the deprecated Screenboard and Timeboard endpoints are available in https://github.com/DataDog/Miscellany/tree/master/Dashboards 

from datadog import initialize, api

old_api = "*****"
old_app = "*****"
dashboard_id = "****"

options = {
    'api_key': old_api,
    'app_key': old_app
}

initialize(**options)

dashboard = api.Dashboard.get(dashboard_id)

print(dashboard)

new_api = '*****'
new_app = '*****'

options = {
   'api_key': new_api,
   'app_key': new_app
}

initialize(**options)

new = api.Dashboard.create(
	title=dashboard['title'],
	widgets=dashboard['widgets'],
	template_variables=dashboard['template_variables'],
	layout_type=dashboard['layout_type']
)

print(new)



