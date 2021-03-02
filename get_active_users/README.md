Collects a list of all active (ie. non disabled or pending) users in a Datadog organization and outputs them to a csv file.

## How to Use

### Setup

1. Ensure Python 3 is installed, and know if it is located as `python` or `python3` (and `pip` or `pip3` respectively) on your system.
2. `cd` into the directory this script is downloaded, then run `pip install datadog`.
3. Replace `<API_KEY>` and `<APP_KEY>`  with [your API and APP keys](https://app.datadoghq.com/account/settings#api) inside of the script.
4. Save.

### Running

This application can be run after setup by running `python get_active_users.py`. It should then create a file titled `active_users.csv` in the same directory as the script.

### Issues/Feedback/Etc.

Create an issue in GitHub or make a PR.