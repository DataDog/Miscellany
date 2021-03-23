package com.foogaro.datadog.ddog.command.ping.server;

import java.net.InetSocketAddress;

import io.netty.bootstrap.Bootstrap;
import io.netty.channel.Channel;
import io.netty.channel.ChannelFuture;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.nio.NioDatagramChannel;

import static com.foogaro.datadog.ddog.DDogConsts.DEFAULT_PING_BIND_ADDRESS;

public class NettyUdpServer {

    private String bindAddress;
    private int port;
    private Channel channel;
    private EventLoopGroup workerGroup;

    public NettyUdpServer(String bindAddress, int port) {
        this.port = port;
        this.bindAddress = bindAddress;
    }

    public ChannelFuture start() throws InterruptedException {
        workerGroup = new NioEventLoopGroup();

        Bootstrap bootstrap = new Bootstrap();
        bootstrap.group(workerGroup)
                .channel(NioDatagramChannel.class)
                .handler(new ServerChannelInitializer());

        ChannelFuture channelFuture = bootstrap.bind(new InetSocketAddress(bindAddress, port)).syncUninterruptibly();
        channel = channelFuture.channel();

        return channelFuture;
    }

    public void stop() {
        if (channel != null) {
            channel.close();
        }
        workerGroup.shutdownGracefully();
    }
}
