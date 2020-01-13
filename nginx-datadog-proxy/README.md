# Nginx forward proxy for Datadog agent
If your network configuration restrict outbound traffic you can proxy all the outbound traffic through a web proxy, for example nginx. This repository includes a working example of a nginx forwarder proxy that you can configure your Datadog agent to use.

## Build and run the docker image
The dockerfile in this repository is using nginx with the `ngx_http_proxy_connect_module`, the nginx.conf only allows outbound traffic to datadog domains `*.datadoghq.eu` and `*.datadoghq.com`, it also blocks all outgoing traffic to other domains by default.

1. Build the image
`docker build -t datadog-nginx-forward-proxy .` 

2. Run the container
`docker run -d -p 8888:8888 datadog-nginx-forward-proxy` 

## Configure your Datadog agent to use the proxy
Traditional web proxies are supported natively by the Datadog agent. If you need to connect to the internet through a proxy, edit your agent configuration file `datadog.yaml` to include:
```
proxy:
    https: "http://<PROXY_SERVER>:8888"
    http: "http://<PROXY_SERVER>:8888"
```
See [Datadog's official documentation](https://docs.datadoghq.com/agent/proxy/?tab=agentv6v7#using-a-web-proxy-as-proxy) for additional information. 

## Credits
Thanks goes to these wonderful people:

* Robert Reiz ([@reiz](https://github.com/reiz)) – https://github.com/reiz/nginx_proxy
* Oskar Rittsél ([@rittsel](https://github.com/Rittsel)) – Datadog Inc.

