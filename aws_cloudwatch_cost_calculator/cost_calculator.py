#!/usr/bin/python
import sys
if len(sys.argv) != 3:
        print("{} <number of cloudwatch metrics> <polling interval, default is 10>".format(sys.argv[0]))
        exit()
# number of metrics as argument
n = sys.argv[1]
polling_interval = sys.argv[2] # default is every '10' minutes
calls_per_hour = int(60) / int(polling_interval)
cost_to_crawl_once = (int(n) / int(1000)) * float(0.01)
hourly_cost_to_crawl = cost_to_crawl_once * calls_per_hour
monthly_cost_per_crawl = (hourly_cost_to_crawl * int(24)) * int(30)
print("Hourly cost to crawl: ${}\nMonthly cost to crawl: ${}".format(hourly_cost_to_crawl, monthly_cost_per_crawl))
