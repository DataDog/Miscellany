from datadog import initialize, api

options = {
    'api_key': '<API KEY ORIGINAL ACCOUNT>',
    'app_key': '<APP KEY ORIGINAL ACCOUNT>'
}

initialize(**options)

dashboard_ids = []
dashboard_data = [] 

## Gather all the dashboard IDs in original account
response = api.Dashboard.get_all()
dashboards = response["dashboards"]

for dashboard in dashboards: 
    id = dashboard['id']
    dashboard_ids.append(id)

print (dashboard_ids)

## Gather dashboard data via dashboard IDs
for dashboard_id in dashboard_ids:
    dashboard = api.Dashboard.get(dashboard_id)
    dashboard_data.append(dashboard)

options = {
    'api_key': '<API KEY NEW ACCOUNT>',
    'app_key': '<APP KEY NEW ACCOUNT>'
}

initialize(**options)

## Iterate through dashboard data and create a new dashboard in new account
for dashboard in dashboard_data:
    id = dashboard['id']
    print('-------------------------------------------------------------------')
    print(f'Creating new dashboard with id:{id}')
    print('-------------------------------------------------------------------')
    new = api.Dashboard.create(
      title=dashboard['title'],
      author_name=dashboard['author_name'],
      widgets=dashboard['widgets'],
      layout_type=dashboard['layout_type'],
      description=dashboard['description'],
      is_read_only=dashboard['is_read_only'],
      notify_list=dashboard['notify_list'],
      template_variables=dashboard['template_variables'],
)

print('Done importing all dashboards!')
