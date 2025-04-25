# Agent Integration Defaults
Collects example configs for core agent integrations in a YAML file.

1. Copies the integrations-core repo.
2. Collects the `conf.yaml` or `conf.yaml example` file in each integration directory. 
3. Stores the data in a YAML file without comments. 
4. Outputs one big YAML file with the name of the integration, path, and default configuration.

## Why?
Configs with comments are useful to see available options, but they can be hard to read. I'm working on something.

## Prerequisites
- Docker 
    - If you want to build the image to run and update the list.
- yq (optional)

## Usage
```bash
# build
docker build -t datadog-config-exporter .

# run the container and drop the output in this directory
docker run --rm -v $(pwd):/output -u $(id -u):$(id -g) datadog-config-exporter

# check
yq '.nginx' collected_integrations.yaml 
```
### Nginx output
```yaml
config:
  init_config: null
  instances:
    - disable_generic_tags: true
      nginx_status_url: http://localhost:81/nginx_status/
      only_query_enabled_endpoints: true
```
