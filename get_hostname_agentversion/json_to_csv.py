#!/usr/bin/python
import json
import csv

with open("host_agent_all.json") as file:
	jsondata = json.load(file)

keys = jsondata[0].keys()

#assert len(keys) == 2, Exception
with open ("host_agent_all.csv",'w') as outfile:
	csv_file = csv.writer(outfile)
	csv_file.writerow(keys)

	for rows in jsondata:
		ele = []
		for key in keys:
 			ele.append(rows[key])		
		csv_file.writerow(ele)
print "complete converting json to csv"