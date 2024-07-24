This script will list all the tags of the metrics which are not in use in the datadog.
It is useful in cases where you want to list the metrics and their tags. This script is using 2 API's https://docs.datadoghq.com/api/latest/metrics/?code-lang=python#list-tags-by-metric-name and https://docs.datadoghq.com/api/latest/metrics/?code-lang=python#list-active-tags-and-aggregations.
The 1st API will fetch all the tags of the metric and other one will just list all active tags and attributes.
After filtering and converting both into the python list. It will perform subtraction of active tags from all tags list, which will show the unused tags.

I've tested this script on Ubuntu 22.04.3 LTS, and it should work with most flavors of Linux running a kernel version of 2.6 or higher. 

The script depends on the datadog Python3 and its package, both of which can be installed with the pip install command.

To use the script, enter your API and app keys in the options dictionary. Then, specify the path to the file which will have list of metrics. The script will excecute for all the metrics mentioned in that file.