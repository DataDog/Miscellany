# Get All Boards
This script will get all boards for a given organization and print out their
json. Useful for malformed boards created via the API.

# Run Code
- Setup a python virtualenv: `virtualenv get_all_boards`
- Activate the virtualenv: `source get_all_boards/bin/activate`
- Run `pip install -r requirements.txt`
- Run `python get_all_boards.py -k <your-api-key> -a <your-app-key>`
  - Alternatively set `DD_API_KEY` and `DD_APP_KEY` as environment variables
