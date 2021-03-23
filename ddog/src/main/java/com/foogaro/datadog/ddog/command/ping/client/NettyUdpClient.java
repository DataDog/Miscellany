package com.foogaro.datadog.ddog.command.ping.client;

import java.net.InetSocketAddress;

import io.netty.bootstrap.Bootstrap;
import io.netty.channel.Channel;
import io.netty.channel.ChannelFuture;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.nio.NioDatagramChannel;

public class NettyUdpClient {

    private int port;
    private String host;
    private EventLoopGroup workerGroup;
    private Channel channel;

    public NettyUdpClient(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public ChannelFuture start() throws InterruptedException {
        workerGroup = new NioEventLoopGroup();

        Bootstrap bootstrap = new Bootstrap();
        bootstrap.group(workerGroup)
                .channel(NioDatagramChannel.class)
                .handler(new ClientChannelInitializer());

        ChannelFuture channelFuture = bootstrap.bind(new InetSocketAddress(0));
        channelFuture.syncUninterruptibly();

        channel = channelFuture.channel();

        return channelFuture;
    }

    public ChannelFuture write(Object msg) throws InterruptedException {
        ChannelFuture channelFuture = channel.writeAndFlush(msg).sync();

        return channelFuture;
    }

    public void stop() {
        if (channel != null) {
            channel.close();
        }
        workerGroup.shutdownGracefully();
    }
}
