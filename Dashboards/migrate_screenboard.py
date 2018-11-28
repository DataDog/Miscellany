from datadog import initialize, api

old_api = "*****"
old_app = "*****"
screenboard_id = ****

options = {
    'api_key': old_api,
    'app_key': old_app
}

initialize(**options)

screenboard = api.Screenboard.get(screenboard_id)

print(screenboard)

new_api = '*****'
new_app = '*****'

options = {
   'api_key': new_api,
   'app_key': new_app
}

initialize(**options)

new = api.Screenboard.create(
	board_title=screenboard['board_title'],
	widgets=screenboard['widgets'],
	template_variables=screenboard['template_variables'],
	height=screenboard['height'],
	width=screenboard['width']
)

print(new)
