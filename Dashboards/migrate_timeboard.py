from datadog import initialize, api

old_api = '*****'
old_app = '*****'
timeboard_id = ****

options = {
    'api_key': old_api,
    'app_key': old_app
}

initialize(**options)

timeboard = api.Timeboard.get(timeboard_id)

print(timeboard)

new_api = '*****'
new_app = '*****'

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
