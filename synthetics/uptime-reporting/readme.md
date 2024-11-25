# Python script to export Synthetics uptimes and alert periods

```sh
# Create a virtual env
python3 -m venv .venv
source .venv/bin/activate
# Install the Datadog Python client
python -m pip install -r requirements.txt
# Run the script
DD_API_KEY="<API KEY>" DD_APP_KEY="<APPLICATION KEY>" python extract-synthetics-uptimes.py
```
