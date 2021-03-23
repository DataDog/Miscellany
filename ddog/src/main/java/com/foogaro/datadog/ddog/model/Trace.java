package com.foogaro.datadog.ddog.model;

import java.io.Serializable;

import static com.foogaro.datadog.ddog.DDogConsts.DEFAULT_TRACE_START_IN_NS;

public class Trace implements Serializable {

    private int duration;
    private String span;
    private String resource;
    private String service;
    private int spanId;
    private long start;
    private int traceId;

    private Trace(TraceBuilder traceBuilder) {
        this.duration=traceBuilder.duration;
        this.span=traceBuilder.span;
        this.resource=traceBuilder.resource;
        this.service=traceBuilder.service;
        this.spanId=traceBuilder.spanId;
        this.start=traceBuilder.start;
        this.traceId=traceBuilder.traceId;
    }

    @Override
    public String toString() {
        return "{"
                + "\"duration\":" + duration + ""
                + ",\"name\":\"" + span + "\""
                + ",\"resource\":\"" + resource + "\""
                + ",\"service\":\"" + service + "\""
                + ",\"span_id\":" + spanId + ""
                + ",\"start\":" + start + DEFAULT_TRACE_START_IN_NS
                + ",\"trace_id\":" + traceId + ""
                + "}";
    }

    public static class TraceBuilder {

        private int duration;
        private String span;
        private String resource;
        private String service;
        private int spanId;
        private long start;
        private int traceId;

        public TraceBuilder() {
        }

        public TraceBuilder span(String span) {
            this.span=span;
            return this;
        }

        public TraceBuilder spanId(int spanId) {
            this.spanId=spanId;
            return this;
        }

        public TraceBuilder resource(String resource) {
            this.resource=resource;
            return this;
        }

        public TraceBuilder service(String service) {
            this.service=service;
            return this;
        }

        public TraceBuilder traceId(int traceId) {
            this.traceId=traceId;
            return this;
        }

        public TraceBuilder duration(int duration) {
            this.duration=duration;
            return this;
        }

        public TraceBuilder start(long start) {
            this.start=start;
            return this;
        }

        public Trace build() {
            return new Trace(this);
        }
    }
}
