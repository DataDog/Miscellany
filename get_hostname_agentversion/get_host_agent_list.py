#!/usr/bin/python
import requests, json, csv

api_key = '<your API key>'
application_key = '<Your application key>'

url = "https://app.datadoghq.com/reports/v2/overview?api_key="+api_key+"&application_key="+application_key+"&window=3h&metrics=avg%3Asystem.cpu.idle%2Cavg%3Aaws.ec2.cpuutilization%2Cavg%3Avsphere.cpu.usage%2Cavg%3Aazure.vm.processor_total_pct_user_time%2Cavg%3Asystem.cpu.iowait%2Cavg%3Asystem.load.norm.15&with_apps=true&with_sources=true&with_aliases=true&with_meta=true&with_mute_status=true&with_tags=true"
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.get(url,headers=headers)

print("status:", r.status_code)

def get_host_agentVersion(data):
	host_agent = agent_version(data)
	with open ("host_agent_all.json",'w') as outfile:
		json.dump(host_agent, outfile)
	print("saved host_agent_all.json")

def agent_version(data):
	host_agent = []
	for hosts in data["rows"]:
		if "agent_version" in hosts["meta"]:
			
			#if you want to get hosts that have the 5.10.1 version of the agent running on it. 
			#please uncomment L27 & L28 and comment out L29. 

			#if hosts["meta"]["agent_version"] == "5.10.1":
			#	host_agent.append({"host_name": hosts["host_name"],"agent_version": hosts["meta"]["agent_version"]})
			host_agent.append({"host_name": hosts["host_name"],"agent_version": hosts["meta"]["agent_version"]})
	
	print("extract host and agent version")
	return host_agent	

if r.status_code == 200:
	data = r.json()
	with open ("JSON_API_permalink.json",'w') as outfile:
		json.dump(r.json(), outfile)
	print("saved JSON_API_permalink.json")
	get_host_agentVersion(data)
