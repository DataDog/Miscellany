# host_info_as_tags

This script fetches host metadata from Datadog that is natively collected from the agent ([example](https://github.com/DataDog/datadog-agent/tree/1c76b8381a195a0b0f629011a6225e936fe1d37a/pkg/metadata/host)), and applies the metadata as tags on the hosts

Currently it will update the following tags:
- platform
- platform_version
- os
- kernel_name
- kernel_release

There is additional metadata to be added if necessary that is not included here. To see all other available metadata, look at the output of the [api call](https://docs.datadoghq.com/api/?lang=python#search-hosts)  `api.Hosts.search()`


Include your `api_key` and `app_key` before running the script
