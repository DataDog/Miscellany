# Agent Integration Defaults
Collects example configs for core agent integrations in a YAML file.

1. Runs python script that lists available integrations at `/etc/datadog-agent/conf.d`.
2. Collects the `conf.yaml` or `conf.yaml example` file in each directory. 
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
docker build -t config-collector .

# generate
docker run --rm -v "$PWD:/output" config-collector bash -c "python3 collect_configs.py && cp /app/collected_integrations.yaml /output/"

# see
yq '.nginx' collected_integrations.yaml 
```
### Nginx output
```yaml
config_path: /etc/datadog-agent/conf.d/nginx.d/conf.yaml
config:
  init_config: null
  instances:
    - nginx_status_url: http://localhost:81/nginx_status/
      only_query_enabled_endpoints: true
      disable_generic_tags: true
```
