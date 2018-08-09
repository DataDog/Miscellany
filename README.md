# Miscellany
Intended to be a repository for miscellaneous scripts and tools from Datadog to be shared with the public.

## Scripts & Tools

These scripts and tools live in this repo

| Name                                     | Language                          | Function                          |
| -----------------------------------------|-----------------------------------|-----------------------------------|  
| [weatherExample](./custom_agent_checks/weatherExample.py) | Python | Example script that submits the temperature and wind speed from the Wunderground API to Datadog as metrics | 
| [sql_redacted](./custom_agent_checks/sql_redacted.py) | Python | Submits a metric based on a SQL query | 
| [import_screenboard](./Dashboards/import_screenboard.py) | Python | Creates a new screenboard from json | 
| [export_screenboard](./Dashboards/export_screenboard.py) | Python | Exports a single screenboard to a json file | 
| [base_scripts](./base_scripts) | Python | A collection of generic scripts that can be used as a starting point for creating your own custom scripts | 
| [custom_check_shell](./custom_check_shell) | Python/Bash | Spins up a VM using vagrant that installs the Datadog agent on it with a simple custom check using shell | 
| [empty_dash](./empty_dash) | Python | Creates an empty dashboard for test purposes | 
| [get_all_boards](./get_all_boards) | Python | Gets all boards for a given organization and print out their json. Useful for malformed boards created via the API | 
| [get_hostname_agentversion](./get_hostname_agentversion) | Python | Gets the version of the agent running for each host | 
| [s3_permissions](./s3_permissions) | Python | Checks S3 bucket ACL permissions for read/write access and reports a metric to Datadog | 
| [uptime](./uptime) | Python | Custom check to track uptime. At the time that this check was written, it wasn't possible to view a monitor's uptime on a dashboard or via the API, or to view uptime with multiple decimals of precision, but please check if those features are available before using this check. | 
| [api_limits_as_custom_metrics](./api_limits_as_custom_metrics.py) | Python | Gets the Datadog API rate limits from the Datadog API and submits them as metrics | 
| [cross-org-metric-broker](./cross-org-metric-broker.py) | Python | Takes metrics from one account (org) and posts them to another account (org) | 
| [csvmod](./csvmod.py) | Python | Example script of grabbing a timeseries and dumping to a CSV | 
| [dashconverter](./dashconverter.py) | Python | Convert from screenboard to timeboard and vice versa | 
| [dd_public_ip](./dd_public_ip.sh) | Bash | Script to run from an AWS instance that will add a tag for the public ip | 
| [fullmetrics_dash](./fullmetrics_dash.py) | Python | Creates a dashboard for a given integration with all metrics being reported through that integration | 
| [hosts_with_aws_without_agent](./hosts_with_aws_without_agent.py) | Python | List of ec2 instances without the datadog-agent installed | 
| [merge_screenboards](./merge_screenboards.py) | Python | Takes two screenboards and combines them into one | 
| [migrate_dashboard](./migrate_dashboard.py) | Python | Migrate a screenboard from one account to another | 
| [remove_lingering_aws_host_tags](./remove_lingering_aws_host_tags.py) | Python | This is a tool for removing AWS host-level tags from your infrastructure in Datadog. It is intended for users who have removed their EC2 instances from their AWS integration and if they no longer want to see AWS tags associated with the hosts that still run datadog-agents. | 
| [remove_single_tag_tmp](./remove_single_tag_tmp.py) | Python | Removes a single tag from a host | 
| [update_multiple_monitors_example](./update_multiple_monitors_example.py) | Python | example of how to update multiple monitors at once | 


## Additional tools

These are some additional tools and scripts written by Datadog.

| Name                                     | Language                          | Function                          |
| -----------------------------------------|-----------------------------------|-----------------------------------|  
| [csv_exporter](https://github.com/DataDog/csv_exporter) | Python | Exports a given metric from Datadog as a csv | 

## Contributing

When adding a new script/tool, be sure to do the following:
- Open a PR for review
- Add a link and description to one of the tables above
