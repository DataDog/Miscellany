'''
         ____        __        ____
        / __ \____ _/ /_____ _/ __ \____  ____ _
       / / / / __ `/ __/ __ `/ / / / __ \/ __ `/
      / /_/ / /_/ / /_/ /_/ / /_/ / /_/ / /_/ /
     /_____/\__,_/\__/\__,_/_____/\____/\__, /
                                       /____/
'''
 
import requests
import time
from checks import AgentCheck
import json

class cgmChecker(AgentCheck):
    def check(self, instance):
        r = requests.get('http://api.wunderground.com/api/<<APIKEYGOESHERE>>/conditions/q/CO/Broomfield.json') #Replace w/ your API key
        if r.status_code == requests.codes.ok: #ensure API response is sucessful (200)
          response = r.json() #set JSON response to response variable
          temp_f = response["current_observation"]["temp_f"] #iterate through API response and set custom metrics
          wind_mph = response["current_observation"]["wind_mph"] #iterate through API response and set custom metrics
          self.gauge('temp_f_broomfield', temp_f, tags=['weather_check']) #Pass the metric to the Datadog agent
          self.gauge('wind_mph_broomfield', wind_mph, tags=['weather_check']) #Pass the metric to the Datadog agent
