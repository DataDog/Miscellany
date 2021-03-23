package com.foogaro.datadog.ddog.command.send;

import com.timgroup.statsd.NonBlockingStatsDClient;
import com.timgroup.statsd.StatsDClient;
import picocli.CommandLine;

import java.util.Random;
import java.util.StringTokenizer;

import static com.foogaro.datadog.ddog.DDogConsts.*;

@CommandLine.Command(name = "send-metric", helpCommand = true, description = "Send a metric.", mixinStandardHelpOptions = true)
public class SendMetric implements Runnable {

    @CommandLine.Spec
    CommandLine.Model.CommandSpec spec;

    @CommandLine.Option(names = {"--name"}, description = "Name of the metric. Default is " + DEFAULT_METRIC_NAME + ". Prefixed by " + DEFAULT_METRIC_PREFIX + ".", defaultValue = DEFAULT_METRIC_NAME)
    private String name;

    @CommandLine.Option(names = {"--value"}, description = "Value of the metric. Default is random 0.." + DEFAULT_METRIC_MAX_VALUE + ".")
    private double value;

    @CommandLine.Option(names = {"--host"}, description = "Datadog Agent host binding interface. Default is " + DEFAULT_METRIC_HOST + ".", defaultValue = DEFAULT_METRIC_HOST)
    private String host;

    @CommandLine.Option(names = {"--port"}, description = "Datadog Agent host listening port. Default is " + DEFAULT_METRIC_PORT + ".", defaultValue = DEFAULT_METRIC_PORT)
    private int port;

    @CommandLine.Option(names = {"--tags"}, description = "Tags use to group the metric. Defaults are: " + DEFAULT_METRIC_TAGS + ".", defaultValue = DEFAULT_METRIC_TAGS)
    private String tags;
    private String[] tagz;

    @CommandLine.Option(names = {"--size"}, description = "Number of metric to send. Default is " + DEFAULT_METRIC_SIZE + ".", defaultValue = DEFAULT_METRIC_SIZE+"")
    private int size;

    @CommandLine.Option(names = {"--interval"}, description = "Number of milliseconds to wait before sending the next metric. Default is 0.." + DEFAULT_METRIC_MAX_INTERVAL + ".", defaultValue = DEFAULT_METRIC_MAX_INTERVAL+"")
    private int interval;

    @CommandLine.Option(names = "--verbose", description = "Verbose output of the command. Default is false.")
    private boolean verbose = Boolean.FALSE;

    private StatsDClient statsd;

    @Override
    public void run() {

/*
        statsd = new NonBlockingStatsDClientBuilder()
                    .prefix(DEFAULT_METRIC_PREFIX)
                    .hostname(host)
                    .port(port)
                    .build();
*/
        statsd = new NonBlockingStatsDClient(DEFAULT_METRIC_PREFIX,host,port,tagz);
        try {


            tagz = extractTags();

            if (verbose) dumpParameters();

            if (size == 1) {
                sendOneMetric();
            } else {
                sendMultipleMetrics();
            }

            statsd.close();
        } catch (Throwable t) {
            System.err.println(t.getMessage());
        }

    }

    private void dumpParameters() {
        System.out.println("Parameters");
        System.out.println("\tname: " + name);
        System.out.println("\tvalue: " + value);
        System.out.println("\thost: " + host);
        System.out.println("\tport: " + port);
        System.out.println("\ttags: " + tags);
        System.out.println("\tsize: " + size);
        System.out.println("\tinterval: " + interval);
        System.out.println("\tverbose: " + verbose);
    }

    private void sendOneMetric(){
        System.out.println("Sending metric " + DEFAULT_METRIC_PREFIX + "." + name + "=" + value);
        sendMetric();
    }

    private void sendMultipleMetrics(){
        for (int i = 0; i < size; i++) {
            value = Math.random() * DEFAULT_METRIC_MAX_VALUE;
            System.out.println("Sending metric [" + (i+1) + "/" + size + "] " + DEFAULT_METRIC_PREFIX + "." + name + "=" + value);
            sendMetric();
            try {
                Thread.sleep(new Random().nextInt(interval));
            } catch (InterruptedException e) {
                System.err.println(e.getMessage());
                break;
            }
        }
    }

    private void sendMetric() {
        statsd.recordGaugeValue(name, value, 1, tagz);
        statsd.count(name+".count", value, 1, tagz);
        statsd.recordHistogramValue(name+".histogram", value, 1, tagz);
        statsd.recordDistributionValue(name+".distribution", value, 1, tagz);
    }

    private String[] extractTags() {
        String[] tagz = new String[]{""};
        if (tags != null) {
            StringTokenizer stringTokenizer = new StringTokenizer(tags);
            tagz = new String[stringTokenizer.countTokens()];
            int count = 0;
            while (stringTokenizer.hasMoreElements()) {
                tagz[count++] = (String) stringTokenizer.nextElement();
            }
        }
        if (verbose) {
            System.out.println("Tags:");
            for (String tag : tagz) System.out.println("\t" + tag);
        }
        return tagz;
    }
}
