from datadog import initialize, api

options = {
    'api_key': '-',
    'app_key': '-'
}

initialize(**options)

# Get all monitor details
id_offset = 0
all_ids = []

while True:
  response = api.Monitor.get_all(id_offset=id_offset)
  if len(response) == 0:
    break
  id_offset = response[-1]["id"]
  for m in response:
    all_ids.append(m["id"])
  print(len(response),id_offset)

# Confirm there are no duplicates in all_ids
print(len(all_ids), len(set(all_ids)))
