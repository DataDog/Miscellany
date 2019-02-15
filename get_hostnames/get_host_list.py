#!/usr/bin/python
import requests, json, csv

api_key = '<API_KEY>'
application_key = '<APP_KEY>'

url = "https://app.datadoghq.com/reports/v2/overview?api_key="+api_key+"&application_key="+application_key+"&window=3h&metrics=avg%3Asystem.cpu.idle%2Cavg%3Aaws.ec2.cpuutilization%2Cavg%3Avsphere.cpu.usage%2Cavg%3Aazure.vm.processor_total_pct_user_time%2Cavg%3Asystem.cpu.iowait%2Cavg%3Asystem.load.norm.15&with_apps=true&with_sources=true&with_aliases=true&with_meta=true&with_mute_status=true&with_tags=true"
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.get(url,headers=headers)

print "status:", r.status_code

def get_host_info(data):
	host = host_info(data)
	with open ("host_all.json",'w') as outfile:
		json.dump(host, outfile)
	print "saved host_all.json"

def host_info(data):
	all_hosts = []
	for hosts in data["rows"]:
		if "agent_version" in hosts["meta"]:
		
			all_hosts.append({"host_name": hosts["host_name"]})
	
	print "extract host info"
	return all_hosts	

if r.status_code == 200:
	data = r.json()
	with open ("JSON_API_permalink.json",'w') as outfile:
		json.dump(r.json(), outfile)
	print "saved JSON_API_permalink.json"
	get_host_info(data)
