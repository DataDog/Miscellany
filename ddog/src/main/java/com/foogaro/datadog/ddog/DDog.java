package com.foogaro.datadog.ddog;

import com.foogaro.datadog.ddog.command.ping.Ping;
import com.foogaro.datadog.ddog.command.send.SendLog;
import com.foogaro.datadog.ddog.command.send.SendMetric;
import com.foogaro.datadog.ddog.command.send.SendTrace;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import picocli.CommandLine;

@CommandLine.Command(name = "ddog", description = "Used to check connectivity between servers.",
        subcommands = {SendMetric.class, SendTrace.class, SendLog.class, Ping.class})
public class DDog {

    @CommandLine.Spec
    CommandLine.Model.CommandSpec spec;

    public static void main(String[] args) {
        CloseableHttpClient client = HttpClients.createDefault();
        client.hashCode();

        System.exit(new CommandLine(new DDog()).execute(args));
    }

}
