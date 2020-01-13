# HAProxy forward proxy for Datadog agent
If your network configuration restrict outbound traffic you can proxy all the outbound traffic through a web proxy, for example HAProxy. This repository includes a working example of a HAProxy forwarder proxy that you can configure your Datadog agent to use.

## Build and run the docker image
The Dockerfile in this repository come with HAProxy and a configuration file (haproxy.cfg) that forwards all your data to **Datadog US** (ie., datadoghq.com)

**Note:** if you are on Datadog EU you must update your haproxy.cfg to include the contents as described in [Datadog's official documentation](https://docs.datadoghq.com/agent/proxy/?tab=datadogeusite#haproxy-configuration)

1. Build the image
`docker build -t datadog-haproxy-forward-proxy .` 

2. Run the container
`docker run -d -p 3833:3833 -p 3834:3834 -p 3835:3835 -p 3836:3836 -p 10514:10514 datadog-haproxy-forward-proxy` 

## Configure your Datadog agent to use the proxy
Traditional web proxies are supported natively by the Datadog agent. If you need to connect to the internet through a proxy, edit your agent configuration file `datadog.yaml` to include at the _bare minimum_ the parameters below, don't forget to update <PROXY_SERVER> to the correct value for your HAProxy container.

```
api_key: <your datadog api key>
dd_url: https://<PROXY_SERVER>:3834
skip_ssl_validation: true

process_config:
  enabled: true
  process_dd_url: https://<PROXY_SERVER>:3836

apm_config:
  enabled: true
  apm_dd_url: https://<PROXY_SERVER>:3835
  receiver_port: 8126

logs_enabled: true
logs_config:
  logs_dd_url: <PROXY_SERVER>:10514
  logs_no_ssl: true
```
See [Datadog's official documentation](https://docs.datadoghq.com/agent/proxy/?tab=agentv6v7#using-a-web-proxy-as-proxy) for additional information. 

## Credits
Thanks goes to these wonderful people:
* Oskar Rittsél ([@rittsel](https://github.com/Rittsel)) – Datadog Inc.
