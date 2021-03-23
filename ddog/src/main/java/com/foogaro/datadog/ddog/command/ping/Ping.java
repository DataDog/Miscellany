package com.foogaro.datadog.ddog.command.ping;

import com.foogaro.datadog.ddog.command.ping.client.NettyUdpClient;
import com.foogaro.datadog.ddog.command.ping.server.NettyUdpServer;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.channel.ChannelFuture;
import io.netty.channel.socket.DatagramPacket;
import io.netty.util.CharsetUtil;
import picocli.CommandLine;

import java.net.InetSocketAddress;
import java.util.Locale;

import static com.foogaro.datadog.ddog.DDogConsts.*;

@CommandLine.Command(name = "ping", helpCommand = true, description = "Used to check connectivity between servers.", mixinStandardHelpOptions = true)
public class Ping implements Runnable {

    @CommandLine.Spec
    CommandLine.Model.CommandSpec spec;

    @CommandLine.Option(names = {"--message"}, description = "The message to send over the wire.", required = true)
    private String message;

    @CommandLine.Option(names = {"--mode"}, description = "The mode to be used: client or server.", required = true)
    private String mode;

    @CommandLine.Option(names = {"--bind-address"}, description = "Bind address. Default is " + DEFAULT_PING_BIND_ADDRESS + ".")
    private String bindAddress = DEFAULT_PING_BIND_ADDRESS;

    @CommandLine.Option(names = {"--bind-port"}, description = "Server port. Default is " + DEFAULT_PING_BIND_PORT + ".")
    private int bindPort = DEFAULT_PING_BIND_PORT;

    @CommandLine.Option(names = {"--target-host"}, description = "Target host:port pairs. Default is " + DEFAULT_PING_TARGET_HOST + ".")
    private String targetHost = DEFAULT_PING_TARGET_HOST;

    @CommandLine.Option(names = {"--target-port"}, description = "Target port. Default is " + DEFAULT_PING_TARGET_PORT + ".")
    private int targetPort = DEFAULT_PING_TARGET_PORT;

    @CommandLine.Option(names = "--verbose", description = "Verbose output of the command. Default is false.")
    private boolean verbose = Boolean.FALSE;


    @Override
    public void run() {
        dumpParameters();

        PingMode pingMode = PingMode.valueOf(mode.toUpperCase());
        switch (pingMode) {
            case CLIENT:
                client();
            case SERVER:
                server();
            default:
                throw new AssertionError("The mode must be client or server.");
        }
    }

    private void dumpParameters() {
        System.out.println("Parameters");
        System.out.println("\tmessage: " + message);
        System.out.println("\tmode: " + mode);
        System.out.println("\tbind-address: " + bindAddress);
        System.out.println("\tbind-port: " + bindPort);
        System.out.println("\ttarget-host: " + targetHost);
        System.out.println("\ttarget-port: " + targetPort);
        System.out.println("\tverbose: " + verbose);
    }

    private void client() {
        InetSocketAddress remoteAddress = new InetSocketAddress(targetHost, targetPort);

        NettyUdpClient client = new NettyUdpClient(targetHost, targetPort);

        try {
            ChannelFuture channelFuture = client.start();

            System.out.println("Client sending message " + message + " to server");
            ByteBuf byteBuf = Unpooled.copiedBuffer(message, CharsetUtil.UTF_8);
            client.write(new DatagramPacket(byteBuf, remoteAddress));

            // Wait until the connection is closed.
            channelFuture.channel().closeFuture().sync();

        } catch (Exception ex) {
            System.err.println(ex.getMessage());
        }
    }

    private void server() {
        NettyUdpServer server = null;

        try {
            server = new NettyUdpServer(bindAddress, bindPort);
            ChannelFuture future = server.start();

            // Wait until the connection is closed.
            future.channel().closeFuture().sync();
        } catch (InterruptedException ex) {
            System.err.println(ex.getMessage());
        }
    }

    public enum PingMode {
        CLIENT,
        SERVER
    }

}
