from datadog import initialize, api

old_api = #'<Organization_You_Are_Migrating_From_API_KEY>'
old_app = #'<Organization_You_Are_Migrating_From_APP_KEY>'

timeboard_id = #<Timeboard's ID>

new_api = #'<Organization_You_Are_Migrating_To_API_KEY>'
new_app = #'<Organization_You_Are_Migrating_To_APP_KEY>'

options = {
    'api_key': old_api,
    'app_key': old_app
}

initialize(**options)

timeboard = api.Timeboard.get(timeboard_id)

print(timeboard)

options = {
   'api_key': new_api,
   'app_key': new_app
}

initialize(**options)


new = api.Timeboard.create(
	title=timeboard['dash']['title'],
	description=timeboard['dash']['description'],
# If you have template variables for your Timeboard just uncomment the line below.
#	template_variables=timeboard['dash']['template_variables'],
	graphs=timeboard['dash']['graphs']
)


print(new)
