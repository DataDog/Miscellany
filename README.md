# Miscellany
Intended to be a repository for miscellaneous scripts and tools from Datadog to be shared with the public.

## Contributing
When adding a new script/tool, be sure to do the following:
- Open a PR for review
- Add a link and description to one of the tables above

We encourage creating a subfolder with a seperate README that gives more details on the script/tool.

## Scripts & Tools
These scripts and tools live in this repo, some scripts/tools have their own README in thheir subfolder with further explaintation and usage.

| Name                                     | Language                          | Function                          |
| -----------------------------------------|-----------------------------------|-----------------------------------|  
| [count_hosts_by_tag](./count_hosts_by_tag.py) | Python | This script will return the number of hosts with a given tag applied. If the tag is only the `key` of a `key:value` pair, all related values will be counted. |
| [mute_monitors_with_tags](./monitors/mute_monitors_with_tags.py) | Python | This script mutes all monitors that are tagged with a set of monitor tags |
| [linux_odfs_API](./linux_odfs_API.sh) | Bash | Script to capture linux open file descriptor metrics |
| [query_freshness](./query_freshness.py) | Python | Report the "freshness" (how long ago a metric was submitted) of a metric. See this [KB](https://help.datadoghq.com/hc/en-us/articles/115001360786-How-to-track-the-freshness-of-a-metric-) for more info |
| [custom_check_shell](./custom_check_shell) | Python/Bash | Spins up a VM using vagrant that installs the Datadog agent on it with a simple custom check using shell |
| [empty_dash](./empty_dash) | Python | Creates an empty dashboard for test purposes |
| [get_all_boards](./get_all_boards) | Python | Gets all boards for a given organization and print out their json. Useful for malformed boards created via the API |
| [Remove old dashboards & monitors]() | Python | Will remove all old dashboards and monitors from an account belonging to the email as specified in the script's parameter. |
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
| [migrate_dashboard](./migrate_dashboard.py) | Python | Migrate a screenboard from one account (or org) to another |
| [dash_to_json](./dash_to_json.py) | Python | Convert Dashboard to JSON and Create Dashboard from JSON |
| [import_screenboard](./Dashboards/import_screenboard.py) | Python | Creates a new screenboard from json |
| [export_screenboard](./Dashboards/export_screenboard.py) | Python | Exports a single screenboard to a json file |
| [base_scripts](./base_scripts) | Python | A collection of generic scripts that can be used as a starting point for creating your own custom scripts |
| [remove_lingering_aws_host_tags](./remove_lingering_aws_host_tags.py) | Python | This is a tool for removing AWS host-level tags from your infrastructure in Datadog. It is intended for users who have removed their EC2 instances from their AWS integration and if they no longer want to see AWS tags associated with the hosts that still run datadog-agents. |
| [remove_single_tag_tmp](./remove_single_tag_tmp.py) | Python | Removes a single tag from a host |
| [update_multiple_monitors_example](./update_multiple_monitors_example.py) | Python | example of how to update multiple monitors at once |
| [create_monitor](./create_monitor) | Python | simple example of creating metric query monitor with thresholds |
| [weatherExample](./custom_agent_checks/weatherExample.py) | Python | Example script that submits the temperature and wind speed from the Wunderground API to Datadog as metrics |
| [sql_redacted](./custom_agent_checks/sql_redacted.py) | Python | Submits a metric based on a SQL query |
| [multi_org_create_users](./multi_org_create_users) | Python | Creates multiple Datadog users across multiple Datadog Orgs |
| [create_monitor_terraform](./create_monitor_terraform) | Terraform | Creates a monitor using Terraform |


## Additional tools
These are some additional tools and scripts written by Datadog.

| Name                                     | Language                          | Function                          |
| -----------------------------------------|-----------------------------------|-----------------------------------|  
| [csv_exporter](https://github.com/DataDog/csv_exporter) | Python | Exports a given metric from Datadog as a csv |

## Getting started
For any Python code, you'll want to run:
```
pip install datadog
```
