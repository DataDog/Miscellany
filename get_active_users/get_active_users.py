# Import Datadog API Library. Make sure to `pip install datadog` first!
from datadog import initialize, api

# Fill in your API and APP keys here
options = {
    'api_key': '<API_KEY>',
    'app_key': '<APP_KEY>'
}

initialize(**options)

user_list = api.User.get_all()
users = user_list["users"]
active_users = []

# Iterate through list of users
for user in users:
  # Check for active users
  if user["disabled"] == False and user["verified"] == True:
    name = user["name"]
    handle = user["handle"] # login email
    email = user["email"] # communications email
    role = user["access_role"] # adm=admin, su=standard user, ro=read only
    # add them to an array
    active_users.append(f"{name},{handle},{email},{role}\n")

# Turn array into string, and create csv file in pwd
all_users = "".join(active_users)
with open("active_users.csv", "w") as f:
  f.write(all_users)
