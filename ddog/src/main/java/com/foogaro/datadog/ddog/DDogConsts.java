package com.foogaro.datadog.ddog;

public class DDogConsts {


    public static final String DEFAULT_METRIC_NAME = "puppy";
    public static final String DEFAULT_METRIC_PREFIX = "ddog";
    public static final String DEFAULT_METRIC_HOST = "localhost";
    public static final String DEFAULT_METRIC_PORT = "8125";
    public static final String DEFAULT_METRIC_TAGS = "env:ddog,service:send-metric,version:1.0.0";
    public static final int DEFAULT_METRIC_SIZE = 1;
    public static final int DEFAULT_METRIC_MAX_VALUE = 1000;
    public static final int DEFAULT_METRIC_MAX_INTERVAL = 2000;


    public static final String DEFAULT_TRACE_ENDPOINT = "/v0.3/traces";
    public static final String DEFAULT_TRACE_SPAN = "DDog";
    public static final String DEFAULT_TRACE_RESOURCE = "/trace.dog";
    public static final String DEFAULT_TRACE_SERVICE = "DDog.SendTrace";
    public static final int DEFAULT_TRACE_MAX_TRACE_ID = Integer.MAX_VALUE;
    public static final int DEFAULT_TRACE_MAX_SPAN_ID = Integer.MAX_VALUE;
    public static final int DEFAULT_TRACE_MIN_DURATION = 1000000000;
    public static final int DEFAULT_TRACE_MAX_DURATION = Integer.MAX_VALUE;
    public static final String DEFAULT_TRACE_START_IN_NS = "000000";
    public static final String DEFAULT_TRACE_HOST = "localhost";
    public static final String DEFAULT_TRACE_PORT = "8126";
    public static final int DEFAULT_TRACE_SIZE = 1;
    public static final int DEFAULT_TRACE_MIN_INTERVAL = 300;
    public static final int DEFAULT_TRACE_MAX_INTERVAL = 600;

    public static final String DEFAULT_LOG_URL = "https://http-intake.logs.datadoghq.com/v1/input";
    public static final String DEFAULT_LOG_CONTENT = "Ddog sending log";
    public static final String DEFAULT_LOG_CONTENT_TYPE = "application/json";
    public static final String DEFAULT_LOG_TAGS = "env:ddog,service:send-log,version:1.0.0";
    public static final int DEFAULT_LOG_SIZE = 1;
    public static final int DEFAULT_LOG_MAX_INTERVAL = 600;

    public static final String DEFAULT_PING_MESSAGE = "ddog";
    public static final String DEFAULT_PING_BIND_ADDRESS = "0.0.0.0";
    public static final int DEFAULT_PING_BIND_PORT = 4405;
    public static final String DEFAULT_PING_TARGET_HOST = "localhost";
    public static final int DEFAULT_PING_TARGET_PORT = 4405;

}
