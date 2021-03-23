package com.foogaro.datadog.ddog.model;

import java.io.Serializable;

public class Log implements Serializable {

    private String message;
    private long timestamp;
    private String ddsource;
    private String ddtags;
    private String hostname;

    private Log(LogBuilder logBuilder) {
        this.message=logBuilder.message;
        this.timestamp=logBuilder.timestamp;
        this.ddsource=logBuilder.ddsource;
        this.ddtags=logBuilder.ddtags;
        this.hostname=logBuilder.hostname;
    }

    @Override
    public String toString() {
        return "{"
                + "\"message\":\"" + message + "\""
                + ",\"ddsource\":\"ddog\""
                + ",\"ddtags\":\"" + ddtags + "\""
                + ",\"hostname\":\"ddog.local\""
                + ",\"service\":\"ddog.service\""
                + ",\"timestamp\":\"" + timestamp + "\""
                + "}";
    }

    public static class LogBuilder {

        private String message;
        private long timestamp;
        private String ddsource;
        private String ddtags;
        private String hostname;

        public LogBuilder() {
        }

        public LogBuilder message(String message) {
            this.message=message;
            return this;
        }

        public LogBuilder timestamp(long timestamp) {
            this.timestamp=timestamp;
            return this;
        }

        public LogBuilder source(String ddsource) {
            this.ddsource=ddsource;
            return this;
        }

        public LogBuilder tags(String ddtags) {
            this.ddtags=ddtags;
            return this;
        }

        public LogBuilder hostname(String hostname) {
            this.hostname=hostname;
            return this;
        }

        public Log build() {
            return new Log(this);
        }
    }
}
