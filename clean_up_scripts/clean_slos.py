from datadog import initialize, api
import argparse
import sys

parser = argparse.ArgumentParser(description='Count number of SLOs in account')
parser.add_argument("-q", "--query")
parser.add_argument("api_key")
parser.add_argument("app_key")
args = parser.parse_args()

print("apikey",args.api_key)
print("appkey",args.app_key)
print("query",args.query)

options = {
    'api_key': args.api_key,
    'app_key': args.app_key
}

initialize(**options)

slos = []
offset=0
while True:
    result = api.ServiceLevelObjective.get_all(query=args.query, offset=offset)
    if "errors" in result:
        sys.exit(result)
    if not result["data"]:
        break
    slos += result["data"]
    offset += 100

print(len(slos))
