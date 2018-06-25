# Export screenboard and save JSON to new file named 'sb.json' in the 
# same directory

from datadog import initialize, api
import json

options = {
    'api_key': 'API_KEY',
    'app_key': 'APP_KEY'
}

initialize(**options)

sb = api.Screenboard.get(123456)
file = open("sb.json", "w")
file.write(json.dumps(sb, indent=4, sort_keys=True))
