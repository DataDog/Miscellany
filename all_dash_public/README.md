# All Public Dashboards
This script will get all public dashboards for a given DD org.

# Run Code
- Use `pyenv` to set your Python version to `2.7.15`
- Setup a python virtualenv: `virtualenv all_dash`
- Activate the virtualenv: `source all_dash/bin/activate`
- Run `pip install -r requirements.txt`
- Run `python all-dash-public.py -k <your-api-key> -a <your-app-key>`
  - Alternatively set `DATADOG_API_KEY` or `DD_API_KEY` and `DATADOG_APP_KEY` or
    `DD_APP_KEY` as environment variables
