from datadog import initialize, api
import json
import re
options = {
    'api_key': '73320a11a32a33deab5858a6a46440e0',
    'app_key': 'cdbad717fe7be46c681385cc4bb5d57412922d61'
}

initialize(**options)


#the get api.Hosts.search endpoint it paginated with a max of 1000 results, so need to loop over all hosts if >1000
total_hosts = api.Hosts.totals().get('total_active')
n = 0
while n < total_hosts: 

	#api call to get all host level information https://docs.datadoghq.com/api/?lang=python#search-hosts
	hosts_information = api.Hosts.search(start=n, count=1000)
	
	#creates list of hosts to iterate over from api call
	host_list = hosts_information.get('host_list')

	#iterate over hosts and update tags
	for i in range(len(host_list)):
		hosti = host_list[i]
		host_name = hosti.get('host_name')

		#found in meta
		platform = hosti.get('meta').get('platform')

		#found in meta.gohai.platform.GOOS
		os = json.loads(hosti.get('meta').get('gohai')).get('platform').get('GOOS')
		
		#found in meta.gohai.platform.os, scrub out special chars
		os_detail = re.sub("[^A-Za-z0-9]+", "", json.loads(hosti.get('meta').get('gohai')).get('platform').get('os'))

		#found in meta.gohai.platform.os.kernel_release
		kernel_release = json.loads(hosti.get('meta').get('gohai')).get('platform').get('kernel_release')

		#found in meta.gohai.platform.os
		kernel_name = json.loads(hosti.get('meta').get('gohai')).get('platform').get('kernel_name')
		
		#extract and set platform versions. these are found under meta. nixV , winV, fbsd and macV
		if str(hosti.get('meta').get('nixV')[0]).replace("None" , "") != "":
			#nix version
			platform_version = str(hosti.get('meta').get('nixV')[0])+'-'+str(hosti.get('meta').get('nixV')[1])
		elif str(hosti.get('meta').get('winV')[0]).replace("None" , "") != "":
			#win version
			platform_version = str(hosti.get('meta').get('winV')[0]).replace(" ","_")+'-'+str(hosti.get('meta').get('winV')[1]).replace(" ","_")
		elif str(hosti.get('meta').get('macV')[0]).replace(" ","_") != "":
			#mac version
			platform_version = str(hosti.get('meta').get('macV')[0]).replace(" ","_")
		else:
			#fbsd
			platform_version = str(hosti.get('meta').get('fbsdV')[0]).replace(" ","_")

		#update host tags api call https://docs.datadoghq.com/api/?lang=python#update-host-tags
		# NOTE: this will replace any exisiting "User" tags. To instead add these as additional tags, use api.Tag.create() https://docs.datadoghq.com/api/?lang=python#add-tags-to-a-host
		api.Tag.update(host_name, tags=[str('platform:'+platform), str('os:'+os), str('os_detail:'+os_detail), str('kernel_release:'+kernel_release), str('kernel_name:'+kernel_name), str('platform_version:'+platform_version)])

	n += 1000




