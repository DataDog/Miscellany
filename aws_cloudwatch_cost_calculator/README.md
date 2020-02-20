# Calculate Datadog costs for crawling AWS CloudWatch Custom Metrics
This script will _estimate_ the cost of Datadog crawling AWS for its CloudWatch metrics.

The purpose of this script is to help answer questions like:
`Datadog, if we would like to poll Cloudwatch more/less frequent than the default 10 minute polling interval you provide us with – what are the cost implications of doing so?`

## How to run it
`python cost_calculator.py (number of cloudwatch metrics) (polling interval in minutes)`

**Note**: Default Datadog crawling interval is 10 minutes.

**For example:**
If there are 10,000 custom CloudWatch metrics to be polled, at 5 minutes intervals:
```
./cost_calculator.py 10000 5
Hourly cost to crawl: $1.2
Monthly cost to crawl: $864.0
```

## How to find a count of custom CloudWatch metrics
Find your custom metric in the CloudWatch console:
1. Open the CloudWatch console.
2. Choose Metrics.
3. Choose the All Metrics tab.
4. Choose Custom.
5. Look for a counter.




