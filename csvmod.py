from datadog import initialize, api
import time
import json
import csv

options = {
    'api_key': 'blah', #Your API_KEY and APP_KEY, see https://app.datadoghq.com/account/settings#api
    'app_key': 'blah'
}

initialize(**options)

start = int(time.time()) - 3600 #Here you can specify the time period over which you want to fetch the data, it's in seconds so here we fetch one hour
end = start + 3600

query = 'system.cpu.idle{*}' #Select the metric you want to get, see your list here: https://app.datadoghq.com/metric/summary . Select the host from which you want the data, see here: https://app.datadoghq.com/infrastructure

results = api.Metric.query(start=start - 3600, end=end, query=query)

print (results) #That should display the results in the terminal (JSON form)

parsed_results = json.dumps(results).encode('utf8')
print(parsed_results)

parsed_json = json.loads(parsed_results)

print type(parsed_json)
with open('mycsv.csv', 'wb') as csvWriter:
    w = csv.writer(csvWriter)
    for key, val in parsed_json.items():
        w.writerow([key, val])

#Note: using 'with open' mitigates the need to close the file afterwards :)
