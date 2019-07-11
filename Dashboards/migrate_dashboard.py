from datadog import initialize, api

options = {
    'api_key': '<YOUR_OLD_ACCT_API_KEY>',
    'app_key': '<YOUR_OLD_ACCT_APP_KEY>'
}

dashboard_id = '<DASHBOARD_ID>'

initialize(**options)

dashboard = api.Dashboard.get(dashboard_id)

print(dashboard)


options = {
    'api_key': '<YOUR_NEW_ACCT_API_KEY>',
    'app_key': '<YOUR_NEW_ACCT_APP_KEY>'
}

initialize(**options)

new = api.Dashboard.create(
	title=dashboard['title'],
	widgets=dashboard['widgets'],
	layout_type=dashboard['layout_type'],
	description=dashboard['description'],
	is_read_only=dashboard['is_read_only'],
	notify_list=dashboard['notify_list'],
	template_variables=dashboard['template_variables'],
)

print(new)
