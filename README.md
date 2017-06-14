# Miscellany
Intended to be a repository for miscellaneous scripts and tools to be shared.

## count_hosts_by_tag.py

This script will return the number of hosts with a given tag applied. If the tag
is only the `key` of a `key:value` pair, all related values will be counted.

### Usage examples

```bash
$ python count_hosts_by_tag.py -k <api_key> -a <app_key> windows
Querying hosts with tag "windows"...
2 	 windows
```

```bash
$ python count_hosts_by_tag.py -k <api_key> -a <app_key> availability-zone
Querying hosts with tag "availability-zone"...
340 	 availability-zone:us-east-1a
203 	 availability-zone:us-east-1c
142 	 availability-zone:us-east-1d
30 	 availability-zone:us-east-1b
14 	 availability-zone:us-east-1e
14 	 availability-zone:eastus
13 	 availability-zone:europe-west1-b
12 	 availability-zone:us-west-2b
9 	 availability-zone:us-central1-b
9 	 availability-zone:us-central1-a
7 	 availability-zone:us-west-2c
```