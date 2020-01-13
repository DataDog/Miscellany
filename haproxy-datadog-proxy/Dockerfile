FROM haproxy:latest
LABEL maintainer="Misiu Pajor misiu.pajor@datadoghq.com"

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
RUN apt-get update && \
	apt-get install -y ca-certificates && \
        apt-get autoclean && apt-get autoremove
