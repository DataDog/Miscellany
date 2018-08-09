from datadog import initialize, api
import time
import json
import csv

#instantiate metricsGetter by using API key/APP key in constructor. metricsGetter can only work with both keys, otherwise the engine (API) won't start
class Metrics_Getter(object):

    def __init__(self, api_key, app_key):
        #To strongly suggest that outside objects don't access a property or method
        #prefix it with a double underscore, this will perform name mangling on the
        #attribute in question. 
        self.__api_key = api_key
        self.__app_key = app_key

        myKeys = {
            'api_key':self.__api_key,
            'app_key':self.__app_key
            }

        initialize(**myKeys) #call the API's initialize function that unpacks the myKeys dict, and uses those key-value pairs as parameters

    #function that takes a JSON object and converts it to a python dictionary
    def convert_JSON_To_Dict(self, jsonFile):
        parsed_results = json.dumps(jsonFile).encode('utf8')
        parsed_json = json.loads(parsed_results)

        return parsed_json

    #function that takes a python dict and writes it to a csv file
    def convert_Dict_To_CSV(self, dictFile, fileName):
        with open(fileName, 'wb') as csvWriter:
            w = csv.writer(csvWriter)
            for key, val in dictFile.items():
                w.writerow([key, val])
            print('CSV has been written!')
            #Note: using 'with open' mitigates the need to close the file afterwards :)

    #function that creates the metric query string, based on a given time interval and metric, and returns a JSON object
    def create_metrics_query(self):
        time_interval = {'past 1 hour':3600,
                         'past 4 hours':14400,
                         'past day':86400,
                         'pastv  2 days':172800,
                         'past week':604800}

        start = int(time.time()) - time_interval['past 1 hour']
        end = start + time_interval['past 1 hour']

        #eventually retrieve list of possible metrics to build out query string
        query = 'system.net.bytes_rcvd{*}'

        results = api.Metric.query(start=start - 3600, end=end, query=query)

        return results


#Mini Bits DEMANDS three things! 1.) Api key 2.) app key 3.) file name for csv
#create function
options = {
    'api_key': '', #Your API_KEY and APP_KEY, see https://app.datadoghq.com/account/settings#api
    'app_key': ''
}

#Eventually build in error handling EVERYWHERE
#Mini Bits is a tiny metrics getter utilizing the API
Mini_Bits = Metrics_Getter(options['api_key'], options['app_key'])


#Create exception for if JSON file is not properly generated
jsonResults = Mini_Bits.create_metrics_query()

#if there is no JSON file to use, do not proceed
resultsDict = Mini_Bits.convert_JSON_To_Dict(jsonResults)

#Instantiate file name or ask for user input as to where file location is
myFile = 'APIcsv.csv'

#if there is no file name, do not proceed to this function, and also if there is no dictionary to use!
Mini_Bits.convert_Dict_To_CSV(resultsDict, myFile)
