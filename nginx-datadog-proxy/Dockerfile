FROM ubuntu:16.04
LABEL maintainer="Misiu Pajor misiu.pajor@datadoghq.com"

WORKDIR /app
ADD sources.list /etc/apt/sources.list

RUN apt-get update && \
	apt-get install -y libfontconfig1 libpcre3 libpcre3-dev git dpkg-dev libpng-dev ca-certificates && \
	apt-get autoclean && apt-get autoremove

RUN cd /app && apt-get source nginx && \
    cd /app/ && git clone https://github.com/chobits/ngx_http_proxy_connect_module && \
    cd /app/nginx-* && patch -p1 < ../ngx_http_proxy_connect_module/patch/proxy_connect.patch && \
    cd /app/nginx-* && ./configure --add-module=/app/ngx_http_proxy_connect_module && make && make install

ADD nginx.conf /usr/local/nginx/conf/nginx.conf

EXPOSE 8888

CMD /usr/local/nginx/sbin/nginx
