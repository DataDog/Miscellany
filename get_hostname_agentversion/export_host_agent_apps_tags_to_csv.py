################################################################################################
#                                                                                              #
# Usage: python3 export_hosts_and_agents_to_csv.py <DATADOG_API_KEY> <DATADOG_APPLICATION_KEY> #
#                                                                                              #
################################################################################################

from os import error, execlp
from os.path import exists
import sys, requests, json, csv


def get_host_info(data):
    host_info = []
    for hosts in data["rows"]:
        if "agent_version" in hosts["meta"]:
            host_info.append({"host_name": hosts["host_name"],"agent_version": hosts["meta"]["agent_version"],"apps": hosts["apps"],"tags": hosts["tags_by_source"]})
    
    return host_info


def main():
    api_key = sys.argv[1]
    application_key = sys.argv[2]

    url = "https://app.datadoghq.com/reports/v2/overview?api_key="+api_key+"&application_key="+application_key+"&window=3h&metrics=avg%3Asystem.cpu.idle%2Cavg%3Aaws.ec2.cpuutilization%2Cavg%3Avsphere.cpu.usage%2Cavg%3Aazure.vm.processor_total_pct_user_time%2Cavg%3Asystem.cpu.iowait%2Cavg%3Asystem.load.norm.15&with_apps=true&with_sources=true&with_aliases=true&with_meta=true&with_mute_status=true&with_tags=true"
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    try:
        print("Requesting Datadog JSON Permalink list of hosts.")
        r = requests.get(url,headers=headers)

        if r.status_code == 200:
            print("Request successful. Filtering JSON permalink data and extracting column headers.")
            data = r.json()
            jsondata = get_host_info(data)
            keys = jsondata[0].keys()
            print(keys)

            with open ("host_info.csv",'w') as outfile:
                csv_file = csv.writer(outfile)
                csv_file.writerow(keys)
                
                print("Converting filtered JSON to CSV. ")
                for rows in jsondata:
                    ele = []
                    for key in keys:
                        ele.append(rows[key])
                    csv_file.writerow(ele)
            print(ele)
    except error as e:
        print(e)

    if exists("./host_info.csv"):
        print("host_info.csv created in current working directory.")
    else:
        print("host_info.csv not found.")


if __name__ == "__main__":
    main()

