# List all services

This script will get all the combination of service, env, secondary_primary_tag.

**Note**: This script will hit an API rate limited. 

## Get started

1. Create a virtual enviroment: `python3 -m venv penv`
1. Activate the virtualenv: `source penv/bin/activate`
1. Install libraries: `pip install -r requirements.txt`
1. Run the script: `python main.py -k <your-api-key> -a <your-app-key>` *(Alternatively set `DD_API_KEY` and `DD_APP_KEY` as environment variables)*
