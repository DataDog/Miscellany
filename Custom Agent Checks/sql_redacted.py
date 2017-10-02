'''
         ____        __        ____
        / __ \____ _/ /_____ _/ __ \____  ____ _
       / / / / __ `/ __/ __ `/ / / / __ \/ __ `/
      / /_/ / /_/ / /_/ /_/ / /_/ / /_/ / /_/ /
     /_____/\__,_/\__/\__,_/_____/\____/\__, /
                                       /____/
'''

import pyodbc #pyodbc is included with the Datadog agent, so you should not have to install any additional libraries
from checks import AgentCheck #Datadog library for Custom Agent Check

class SQL_query(AgentCheck):
   def check(self, instance):
      server = 'tcp:127.0.0.1' #put Database connection path here
      database = 'DatadogDB' # put Database name here
      username = 'ddagent' # put Database username here
      password = '9IeP4mB0btF1G346UskTCoMh' # put Database Password here

      cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
      cursor = cnxn.cursor()
      #Sample select query
      cursor.execute("SELECT * FROM dbo.Products;") #What to query?
      row = cursor.fetchone() #iterate through until you hit the end of table
      while row:
          dd_tags = [   #set datadog tags
            'ProductName:' + row[1],
            'ProductDescription:' + row[3],
          ]
          self.gauge('sqlserver.product.price', row[2], tags=dd_tags) #Set metric name and tags, and pass to Datadog agent
          row = cursor.fetchone()
      cnxn.close() #close connection
