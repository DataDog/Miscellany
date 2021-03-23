package com.foogaro.datadog.ddog.command.send;

import com.foogaro.datadog.ddog.DDog;
import com.foogaro.datadog.ddog.model.Trace;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import picocli.CommandLine;

import java.io.IOException;
import java.io.UnsupportedEncodingException;

import static com.foogaro.datadog.ddog.DDogConsts.*;

@CommandLine.Command(name = "send-trace", helpCommand = true, description = "Send a trace.", mixinStandardHelpOptions = true)
public class SendTrace implements Runnable {

    @CommandLine.ParentCommand
    private DDog parent;

    @CommandLine.Option(names = "--span", description = "Name of the trace", defaultValue = DEFAULT_TRACE_SPAN)
    private String span;

    @CommandLine.Option(names = "--span-id", description = "SpanID identifying the span.")
    private int spanId;

    @CommandLine.Option(names = "--resource", description = "Name of the resource requested.", defaultValue = DEFAULT_TRACE_RESOURCE)
    private String resource;

    @CommandLine.Option(names = "--service", description = "Name of the service/app.", defaultValue = DEFAULT_TRACE_SERVICE)
    private String service;

    @CommandLine.Option(names = "--trace-id", description = "TraceID identifying the trace.")
    private int traceId;

    @CommandLine.Option(names = "--duration", description = "Duration of the trace in nanoseconds (ns)(1s=1000ms=1000000μs=1000000000ns).")
    private int duration;

    @CommandLine.Option(names = "--start", description = "Timestamp of the start of the trace in milliseconds since epoch.")
    private long start;

    @CommandLine.Option(names = "--host", description = "Datadog Agent host binding interface.", defaultValue = DEFAULT_TRACE_HOST)
    private String host;

    @CommandLine.Option(names = "--port", description = "Datadog Agent host listening port.", defaultValue = DEFAULT_TRACE_PORT)
    private String port;

    @CommandLine.Option(names = "--size", description = "Number of traces to send. Default is 1 (one)")
    private int size;

    @CommandLine.Option(names = {"--interval"}, description = "Number of milliseconds to wait before sending the next trace. Default is 0..2000 (two thousands).")
    private int interval;

    @CommandLine.Option(names = "--hierarchical", description = "Datadog Agent host listening port. Default is false.")
    private boolean hierarchical = Boolean.FALSE;

    @CommandLine.Option(names = "--verbose", description = "Verbose output of the command. Default is false.")
    private boolean verbose = Boolean.FALSE;

    @Override
    public void run() {
        if (spanId == 0) spanId = generateSpanId();
        if (traceId == 0) traceId = generateTraceId();
        if (duration == 0) duration = (int) Math.round((Math.random() * DEFAULT_TRACE_MAX_DURATION));
        if (interval == 0) interval = (int) Math.round((Math.random() * DEFAULT_TRACE_MAX_INTERVAL) + DEFAULT_TRACE_MIN_INTERVAL);
        if (start == 0) start = System.currentTimeMillis();
        if (size == 0) size = DEFAULT_TRACE_SIZE;

        if (verbose) dumpParameters();

        if (size > 1) {
            if (hierarchical) {
                sendOneTraceWithMultipleSpans();
            } else {
                sendMultipleTraceWithOneSpan();
            }
        } else {
            sendOneTrace();
        }
    }

    private void sendOneTrace() {
        Trace.TraceBuilder traceBuilder = new Trace.TraceBuilder()
                .span(span)
                .resource(resource)
                .service(service)
                .traceId(traceId)
                .spanId(spanId)
                .duration(duration)
                .start(System.currentTimeMillis());

        System.out.print("Sending trace [1/1]");
        int result = sendTrace(traceBuilder.build());
    }

    private void sendMultipleTraceWithOneSpan() {
        for (int i=0; i < size; i++) {
            Trace.TraceBuilder traceBuilder = new Trace.TraceBuilder()
                    .span(span)
                    .resource(resource)
                    .service(service)
                    .traceId(generateTraceId())
                    .spanId(generateSpanId())
                    .duration(generateDuration())
                    .start(System.currentTimeMillis());

            System.out.println("Sending trace [" + (i+1) + "/" + size + "]");
            int result = sendTrace(traceBuilder.build());
            try {
                Thread.sleep(interval);
            } catch (InterruptedException e) {
                System.err.println(e.getMessage());
            }
        }

    }

    private void sendOneTraceWithMultipleSpans() {
        int nextDuration = duration;

        for (int i=0; i < size; i++) {
            Trace.TraceBuilder traceBuilder = new Trace.TraceBuilder()
                    .span(span)
                    .resource(resource)
                    .service(service+"-"+(i+1))
                    .traceId(traceId)
                    .spanId(generateSpanId())
                    .start(System.currentTimeMillis());

            if (i == 0) {
                traceBuilder.duration(duration);
            } else {
                nextDuration = (int) Math.round((Math.random() * (nextDuration/2))+(nextDuration/2));
                traceBuilder.duration(nextDuration);
            }

            System.out.println("Sending trace [" + (i+1) + "/" + size + "]");
            int result = sendTrace(traceBuilder.build());
        }
    }

    private void dumpParameters() {
        System.out.println("Parameters");
        System.out.println("\tspan: " + span);
        System.out.println("\tspan-id: " + spanId);
        System.out.println("\tresource: " + resource);
        System.out.println("\tservice: " + service);
        System.out.println("\ttrace-id: " + traceId);
        System.out.println("\tduration: " + duration);
        System.out.println("\tstart: " + start);
        System.out.println("\thost: " + host);
        System.out.println("\tport: " + port);
        System.out.println("\tsize: " + size);
        System.out.println("\tinterval: " + interval);
        System.out.println("\thierarchical: " + hierarchical);
        System.out.println("\tverbose: " + verbose);
    }

    private int sendTrace(Trace trace) {
        StringBuilder url = new StringBuilder("http://").append(host).append(":").append(port).append(DEFAULT_TRACE_ENDPOINT);
        if (verbose) System.out.println("\t" + url);
        if (verbose) System.out.println("\t" + trace);

        try {
            HttpPost httpPost = new HttpPost(url.toString());
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");

            StringEntity entity = new StringEntity("[[" + trace.toString() + "]]");
            httpPost.setEntity(entity);
            CloseableHttpClient client = HttpClients.createDefault();
            CloseableHttpResponse response = client.execute(httpPost);
            client.close();
            int result = response.getStatusLine().getStatusCode();
            if (verbose) System.out.println("\thttp[" + result + "]");
            return result;
        } catch (UnsupportedEncodingException e) {
            System.err.println(e.getMessage());
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
        return -1;
    }

    private int generateTraceId() {
        return (int) Math.round((Math.random() * DEFAULT_TRACE_MAX_TRACE_ID) + 1);
    }
    private int generateSpanId() {
        return (int) Math.round((Math.random() * DEFAULT_TRACE_MAX_SPAN_ID) + 1);
    }
    private int generateDuration() {
        return (int) Math.round((Math.random() * DEFAULT_TRACE_MAX_DURATION));
    }
}
