#########################################################################
#Use a cronjob to submit regularily the Metric  						 
#																		 
#crontab -e 															 
#(vim) */1 * * * * cd <path_to_the_script> ; python query_freshness.py   
#(vim) !wq																 
#crontab -l 															 
#########################################################################

from datadog import initialize, api
import time
options = {
    'api_key': '149***e4',
    'app_key': 'f2e***a5'
}
initialize(**options)
now = int(time.time())

query = 'system.cpu.system{*}' # Modify the metric you want to track the freshness of

metric = api.Metric.query(start=now - 3600, end=now, query=query) # how far back in time you want to go (the default is one hour)

nb_points = len(metric['series'][0]['pointlist']) - 1
last_submission = int(metric['series'][0]['pointlist'][nb_points][0]) / 1000

freshness = now - last_submission

print "freshness is: ", freshness


api.Metric.send(metric='freshness', points=freshness, tags=["metric:" + str(query)])