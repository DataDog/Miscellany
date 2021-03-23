package com.foogaro.datadog.ddog.command.send;

import com.foogaro.datadog.ddog.model.Log;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import picocli.CommandLine;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.Random;
import java.util.StringTokenizer;

import static com.foogaro.datadog.ddog.DDogConsts.*;

@CommandLine.Command(name = "send-log", helpCommand = true, description = "Send a log event.", mixinStandardHelpOptions = true)
public class SendLog implements Runnable {

    @CommandLine.Spec
    CommandLine.Model.CommandSpec spec;

    @CommandLine.Option(names = {"--apiKey"}, description = "The Datadog API KEY used to consume the Datadog API to send the log to.", required = true)
    private String apiKey;

    @CommandLine.Option(names = {"--content"}, description = "Content of the log event. Default is a text message: \"" + DEFAULT_LOG_CONTENT + "\".", defaultValue = DEFAULT_LOG_CONTENT)
    private String content;

    @CommandLine.Option(names = {"--content-type"}, description = "Content type of the log. Default is \"" + DEFAULT_LOG_CONTENT_TYPE + "\".", defaultValue = DEFAULT_LOG_CONTENT_TYPE)
    private String contentType;

    @CommandLine.Option(names = {"--url"}, description = "The endpoint of the Datadog API to send the log to. Default is \"" + DEFAULT_LOG_URL + "\".", defaultValue = DEFAULT_LOG_URL)
    private String url;

    @CommandLine.Option(names = {"--tags"}, description = "Tags use to identify the log. Defaults are: " + DEFAULT_LOG_TAGS + ".", defaultValue = DEFAULT_LOG_TAGS)
    private String tags;
    private String[] tagz;

    @CommandLine.Option(names = {"--size"}, description = "Number of logs to send. Default is " + DEFAULT_LOG_SIZE + ".", defaultValue = DEFAULT_LOG_SIZE+"")
    private int size;

    @CommandLine.Option(names = {"--interval"}, description = "Number of milliseconds to wait before sending the next log event. Default is 0.." + DEFAULT_LOG_MAX_INTERVAL + ".", defaultValue = DEFAULT_LOG_MAX_INTERVAL+"")
    private int interval;

    @CommandLine.Option(names = "--verbose", description = "Verbose output of the command. Default is false.")
    private boolean verbose = Boolean.FALSE;

    @Override
    public void run() {
        if (verbose) dumpParameters();

        if (size == 1) {
            sendOneLog();
        } else {
            sendMultipleLogs();
        }
    }

    private void dumpParameters() {
        System.out.println("Parameters");
        System.out.println("\tapiKey: " + apiKey);
        System.out.println("\tcontent: " + content);
        System.out.println("\tcontentType: " + contentType);
        System.out.println("\turl: " + url);
        System.out.println("\ttags: " + tags);
        System.out.println("\tsize: " + size);
        System.out.println("\tinterval: " + interval);
        System.out.println("\tverbose: " + verbose);
    }

    private void sendOneLog(){
        Log.LogBuilder logBuilder = new Log.LogBuilder()
                .message(content)
                .tags(DEFAULT_LOG_TAGS)
                .timestamp(System.currentTimeMillis());
        sendLog(logBuilder.build());
    }

    private void sendMultipleLogs() {
        Log.LogBuilder logBuilder = new Log.LogBuilder()
                .message(content)
                .tags(DEFAULT_LOG_TAGS);

        for (int i = 0; i < size; i++) {
            sendLog(logBuilder.timestamp(System.currentTimeMillis()).build());
            try {
                Thread.sleep(new Random().nextInt(interval));
            } catch (InterruptedException e) {
                System.err.println(e.getMessage());
                break;
            }
        }
    }

    private int sendLog(Log log) {
        if (verbose) System.out.println("Sending log");
        if (verbose) System.out.println("\turl: " + url.toString());
        if (verbose) System.out.println("\tcontentType: " + contentType);
        if (verbose) System.out.println("\tlog: " + log);

        try {
            HttpPost httpPost = new HttpPost(url.toString());
            httpPost.setHeader("Accept", contentType);
            httpPost.setHeader("Content-Type", contentType);
            httpPost.setHeader("DD-API-KEY", apiKey);

            StringEntity entity = new StringEntity(log.toString());
            httpPost.setEntity(entity);
            CloseableHttpClient client = HttpClients.createDefault();
            CloseableHttpResponse response = client.execute(httpPost);
            client.close();
            int result = response.getStatusLine().getStatusCode();
            if (verbose) System.out.println("\tresponse:\n\t"+response);
            if (verbose) System.out.println("\thttp[" + result + "]");
            return result;
        } catch (UnsupportedEncodingException e) {
            if (verbose) e.printStackTrace();
            System.err.println(e.getMessage());
        } catch (IOException e) {
            if (verbose) e.printStackTrace();
            System.err.println(e.getMessage());
        }
        return -1;
    }

}
