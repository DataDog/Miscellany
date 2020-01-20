FROM ubuntu:latest
LABEL maintainer="Misiu Pajor misiu.pajor@datadoghq.com"

WORKDIR /app
ADD sources.list /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y libfontconfig1 libpcre3 libpcre3-dev git dpkg-dev libpng-dev ca-certificates gcc make&& \
    apt-get autoclean && apt-get autoremove

RUN cd /app && apt-get source nginx && \
    cd /app/ && git clone https://github.com/chobits/ngx_http_proxy_connect_module && \
    # we are running nginx 1.14, if the nginx version should be different see: https://github.com/chobits/ngx_http_proxy_connect_module#install
    cd /app/nginx-* && patch -p1 < ../ngx_http_proxy_connect_module/patch/proxy_connect_1014.patch && \
    cd /app/nginx-* && ./configure --add-module=/app/ngx_http_proxy_connect_module && make && make install

ADD nginx.conf /usr/local/nginx/conf/nginx.conf

EXPOSE 8888

CMD /usr/local/nginx/sbin/nginx
