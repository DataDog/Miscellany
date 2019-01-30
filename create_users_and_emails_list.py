from datadog import initialize, api

options = {
    'api_key': '<API KEY>',
    'app_key': '<APP KEY>'
}

initialize(**options)

user_list = api.User.get_all()

users = user_list["users"]

emails = []
names = []

for user in users:
  emails.append(user["handle"])
  if user["name"] is None: 
  	names.append(user["handle"])
  else:
  	names.append(user["name"])

all_emails = ",".join(emails)
all_users = ",".join(names)	

with open("email_list.csv", "a") as f:
	f.write(all_users+"\n")
	f.write(all_emails)
