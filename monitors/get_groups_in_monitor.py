# slight edit to get monitor details API call that will grab all groups in a monitor 
# use case would be to get a list of groups in a monitor on one page (ran into a customer that didnt like having to click 
# through multiple pages for groups on the monitor status page in the UI

from datadog import initialize, api

options = {
    'api_key': '<YOUR_API_KEY>',
    'app_key': '<YOUR_APP_KEY>'
}

initialize(**options)

monitor_details = api.Monitor.get(<MONITOR_ID>, group_states='all')

for group in monitor_details["state"]["groups"]:
	print group
