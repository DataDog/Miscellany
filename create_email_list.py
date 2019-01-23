from datadog import initialize, api

# This script will create a CSV file in the same directory containing a list of all user log in handles

options = {
    'api_key': '<API_KEY>',
    'app_key': '<APP_KEY>'
}

initialize(**options)

user_list = api.User.get_all()

users = user_list["users"]

emails = []

for user in users:
  emails.append(user["handle"])

all_emails = ",".join(emails)

with open("email_list.csv", "w") as f:
  f.write(all_emails)
