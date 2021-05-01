# Metrics on Dashboards Report

## Overview
This program is for anyone wondering "where the heck am I using this metric in my account?"

It is a simple console program written in Python 3 that utilizes the datadogpy API library to return a list of places in your account that contains any metric in a series of user provided metrics present on dashboards and/or monitors.

This program requires that the datadogpy library be installed on the machine or environment on which the program is running.  Download and installation instructions can be found [here](https://github.com/DataDog/datadogpy)

The command to install datadogpy for Python3 is `pip3 install datadog`

**NOTE**: This program is not recommended for use with Python3.  Python3 string objects do not use utf-8 encoding, meaning that any non ASCII character in a board or metric name will break this program if it runs in Python2.

## How to Run It
Once you have copied this program locally, it can be run in a terminal from the directory it is stored in by running `python3 main.py`.  All required values should first be entered into the constant variables located in config.py

### Sample Config File
```
#Your Datadog API Key
API_KEY = "<redacted>"

#Your Datadog Application Key
APP_KEY = "<redacted>"

# should the program check for metrics present in dashboards?
CHECK_DASHBOARDS = True

# should the program check for metrics present in monitors?
CHECK_MONITORS = True

# a list of strings, values should match metrics tpresent in your account
METRICS_TO_EVAL = ["pi.temp", "datadog.agent.up", "system.cpu.idle"]
```



#### Sample Run Through
Below is a sample run of the program:

API Intialized!


Getting Your Metrics Report


# Metric Usage Report

### Table of Contents
- [dd.synth.live_riders](#ddsynthlive-riders)
  - [Dashboards](#dashboards-1)
  - [Monitors](#monitors-1)

## dd.synth.live_riders

### Dashboards

| Title | Author | Widgets |
|-|-|-|
| [Devlin Screenboard](https://app.datadoghq.com/dashboard/edf-ahb-7ab/devlin-screenboard) | nicholas.devlin@datadoghq.com | - [untitled](https://app.datadoghq.com/dashboard/edf-ahb-7ab/devlin-screenboard?fullscreen_widget=3314397860069546) |
| [Datadog Application Screenboard [ML] (cloned)](https://app.datadoghq.com/dashboard/e9z-6tn-u7r/datadog-application-screenboard-ml-cloned) | mike.laning@datadoghq.com | - [Active Users](https://app.datadoghq.com/dashboard/e9z-6tn-u7r/datadog-application-screenboard-ml-cloned?fullscreen_widget=9) |
| [Executive Dashboard SLA [JSK]](https://app.datadoghq.com/dashboard/8bt-w6d-pdc/executive-dashboard-sla-jsk) | josh.king@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/8bt-w6d-pdc/executive-dashboard-sla-jsk?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/8bt-w6d-pdc/executive-dashboard-sla-jsk?fullscreen_widget=23) |
| [Delta Executive Summary](https://app.datadoghq.com/dashboard/t5t-hmv-bxq/delta-executive-summary) | tom.nedbal@datadoghq.com | - [Active Users](https://app.datadoghq.com/dashboard/t5t-hmv-bxq/delta-executive-summary?fullscreen_widget=8453605587563902) |
| [Cody - Shopist.io Executive Summary](https://app.datadoghq.com/dashboard/6fu-svz-t65/cody---shopistio-executive-summary) | cody.borders@datadoghq.com | - [Active Users](https://app.datadoghq.com/dashboard/6fu-svz-t65/cody---shopistio-executive-summary?fullscreen_widget=8453605587563902) |
| [Executive Dashboard SLA [JSK] (cloned)](https://app.datadoghq.com/dashboard/qgm-zif-pn9/executive-dashboard-sla-jsk-cloned) | fallon.tierney@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/qgm-zif-pn9/executive-dashboard-sla-jsk-cloned?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/qgm-zif-pn9/executive-dashboard-sla-jsk-cloned?fullscreen_widget=23) |
| [Executive Dashboard SLA [JSK] (cloned)](https://app.datadoghq.com/dashboard/96g-caf-en5/executive-dashboard-sla-jsk-cloned) | dylan.ward@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/96g-caf-en5/executive-dashboard-sla-jsk-cloned?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/96g-caf-en5/executive-dashboard-sla-jsk-cloned?fullscreen_widget=23) |
| [E-commerce Dashboard (Cooper)](https://app.datadoghq.com/dashboard/ygw-u2g-ihy/e-commerce-dashboard-cooper) | cooper.hollingsworth@datadoghq.com | - [New Customer Signups](https://app.datadoghq.com/dashboard/ygw-u2g-ihy/e-commerce-dashboard-cooper?fullscreen_widget=4) |
| [Executive Dashboard SLA [LJ]](https://app.datadoghq.com/dashboard/bbz-wwq-7nu/executive-dashboard-sla-lj) | lauren.perchitti@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/bbz-wwq-7nu/executive-dashboard-sla-lj?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/bbz-wwq-7nu/executive-dashboard-sla-lj?fullscreen_widget=23) |
| [Executive Dashboard SLA [JSK] (cloned)](https://app.datadoghq.com/dashboard/anb-eh9-6fy/executive-dashboard-sla-jsk-cloned) | boyan.syarov@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/anb-eh9-6fy/executive-dashboard-sla-jsk-cloned?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/anb-eh9-6fy/executive-dashboard-sla-jsk-cloned?fullscreen_widget=23) |
| [Q's Dashboard for new customers](https://app.datadoghq.com/dashboard/k7v-itf-mwa/qs-dashboard-for-new-customers) | q.lee@datadoghq.com | - [신규 가입 고객 추이](https://app.datadoghq.com/dashboard/k7v-itf-mwa/qs-dashboard-for-new-customers?fullscreen_widget=1129007089666515) |
| [Datadog Application Screenboard [GB]](https://app.datadoghq.com/dashboard/em9-hkz-ytp/datadog-application-screenboard-gb) | griffin.bossard@datadoghq.com | - [Active Users](https://app.datadoghq.com/dashboard/em9-hkz-ytp/datadog-application-screenboard-gb?fullscreen_widget=9) |
| [Datadog Application Screenboard (Cody)](https://app.datadoghq.com/dashboard/hk6-kzy-pwh/datadog-application-screenboard-cody) | cody.borders@datadoghq.com | - [Active Users](https://app.datadoghq.com/dashboard/hk6-kzy-pwh/datadog-application-screenboard-cody?fullscreen_widget=9) |
| [[ML] AWS, APM, Logs, K8s (cloned)](https://app.datadoghq.com/dashboard/vui-s3f-759/ml-aws-apm-logs-k8s-cloned) | mike.laning@datadoghq.com | - [Traffic Forecast](https://app.datadoghq.com/dashboard/vui-s3f-759/ml-aws-apm-logs-k8s-cloned?fullscreen_widget=1780853485751600) |
| [Application + infrastructure overview (cloned) (cloned)](https://app.datadoghq.com/dashboard/bfs-94n-dij/application--infrastructure-overview-cloned-cloned) | emily.chang@datadoghq.com | - [API queries](https://app.datadoghq.com/dashboard/bfs-94n-dij/application--infrastructure-overview-cloned-cloned?fullscreen_widget=9) |
| [Oncology Analytics - Azure, APM, Logs](https://app.datadoghq.com/dashboard/kft-n4x-y6k/oncology-analytics---azure-apm-logs) | bailey.marshall@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/kft-n4x-y6k/oncology-analytics---azure-apm-logs?fullscreen_widget=488791753742774) |
| [Executive Dashboard SLA [Exodus]](https://app.datadoghq.com/dashboard/7nf-yru-4t9/executive-dashboard-sla-exodus) | bailey.marshall@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/7nf-yru-4t9/executive-dashboard-sla-exodus?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/7nf-yru-4t9/executive-dashboard-sla-exodus?fullscreen_widget=23) |
| [E-commerce Dashboard](https://app.datadoghq.com/dashboard/kks-m2t-mdp/e-commerce-dashboard) | bailey.marshall@datadoghq.com | - [New Customer Signups](https://app.datadoghq.com/dashboard/kks-m2t-mdp/e-commerce-dashboard?fullscreen_widget=4) |
| [Infrastructure, Apps, and Security Overview {DD}](https://app.datadoghq.com/dashboard/mt6-q8y-cfy/infrastructure-apps-and-security-overview-dd) | hank.boudreau@datadoghq.com | - [API queries](https://app.datadoghq.com/dashboard/mt6-q8y-cfy/infrastructure-apps-and-security-overview-dd?fullscreen_widget=9) |
| [[Siti] Executive Dashboard SLA [JSK] (cloned)](https://app.datadoghq.com/dashboard/hk3-3mh-z4p/siti-executive-dashboard-sla-jsk-cloned) | siti.chen@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/hk3-3mh-z4p/siti-executive-dashboard-sla-jsk-cloned?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/hk3-3mh-z4p/siti-executive-dashboard-sla-jsk-cloned?fullscreen_widget=23) |
| [Datadog Application Screenboard [ML] (cloned) (cloned)](https://app.datadoghq.com/dashboard/4z2-iwk-6rk/datadog-application-screenboard-ml-cloned-cloned) | mike.laning@datadoghq.com | - [New User Sign Ups](https://app.datadoghq.com/dashboard/4z2-iwk-6rk/datadog-application-screenboard-ml-cloned-cloned?fullscreen_widget=5972581587240929) |
| [Datadog Application Screenboard [ML] (cloned) 3/4 (cloned)](https://app.datadoghq.com/dashboard/k48-z2b-k9n/datadog-application-screenboard-ml-cloned-34-cloned) | mike.laning@datadoghq.com | - [New User Sign Ups](https://app.datadoghq.com/dashboard/k48-z2b-k9n/datadog-application-screenboard-ml-cloned-34-cloned?fullscreen_widget=8952563613979188) |
| [Datadog Application Screenboard [ML] (cloned) 4/3](https://app.datadoghq.com/dashboard/kiv-5fy-jk5/datadog-application-screenboard-ml-cloned-43) | mike.laning@datadoghq.com | - [New User Sign Ups](https://app.datadoghq.com/dashboard/kiv-5fy-jk5/datadog-application-screenboard-ml-cloned-43?fullscreen_widget=5091842815964150) |
| [eComm metrics (Bailey - PetCareRx)](https://app.datadoghq.com/dashboard/mbv-asd-9yi/ecomm-metrics-bailey---petcarerx) | bailey.marshall@datadoghq.com | - [New Customer Signups](https://app.datadoghq.com/dashboard/mbv-asd-9yi/ecomm-metrics-bailey---petcarerx?fullscreen_widget=4) |
| [Executive Dashboard SLA [JSK] (Lowe's)](https://app.datadoghq.com/dashboard/72k-ngw-mff/executive-dashboard-sla-jsk-lowes) | josh.king@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/72k-ngw-mff/executive-dashboard-sla-jsk-lowes?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/72k-ngw-mff/executive-dashboard-sla-jsk-lowes?fullscreen_widget=23) |
| [Application Dashboard [ML] (cloned) 2/7](https://app.datadoghq.com/dashboard/vkg-k7q-nws/application-dashboard-ml-cloned-27) | mike.laning@datadoghq.com | - [Number of Platform Users](https://app.datadoghq.com/dashboard/vkg-k7q-nws/application-dashboard-ml-cloned-27?fullscreen_widget=5648676845717422) |
| [Datadog Application Screenboard [ML] (cloned) 2/7](https://app.datadoghq.com/dashboard/8c9-f6a-kxf/datadog-application-screenboard-ml-cloned-27) | mike.laning@datadoghq.com | - [New Customer Signups](https://app.datadoghq.com/dashboard/8c9-f6a-kxf/datadog-application-screenboard-ml-cloned-27?fullscreen_widget=8116841758769111) |
| [Datadog Application Screenboard [ML] (cloned) (cloned)](https://app.datadoghq.com/dashboard/txm-4hq-m9p/datadog-application-screenboard-ml-cloned-cloned) | mike.laning@datadoghq.com | - [New Customer Signups](https://app.datadoghq.com/dashboard/txm-4hq-m9p/datadog-application-screenboard-ml-cloned-cloned?fullscreen_widget=2732982015772769) |
| [Datadog Application Screenboard [ML] (cloned) (cloned) SH](https://app.datadoghq.com/dashboard/bym-uun-w54/datadog-application-screenboard-ml-cloned-cloned-sh) | mike.laning@datadoghq.com | - [New Customer Signups](https://app.datadoghq.com/dashboard/bym-uun-w54/datadog-application-screenboard-ml-cloned-cloned-sh?fullscreen_widget=1793135011628892) |
| [[Pej] EDF Business Dash](https://app.datadoghq.com/dashboard/3cr-nqk-pch/pej-edf-business-dash) | pejman.tabassomi@datadoghq.com | - [Forecast of Rejected Orders](https://app.datadoghq.com/dashboard/3cr-nqk-pch/pej-edf-business-dash?fullscreen_widget=5891560296862141) |
| [[ML] Overview Screenboard Demo [10/11]](https://app.datadoghq.com/dashboard/qk3-bwe-6wi/ml-overview-screenboard-demo-1011) | mike.laning@datadoghq.com | - [New Customer Signups](https://app.datadoghq.com/dashboard/qk3-bwe-6wi/ml-overview-screenboard-demo-1011?fullscreen_widget=6959321286136815) |
| [Infrastructure, Apps, and Security Overview (cloned) Lauren](https://app.datadoghq.com/dashboard/s9d-aup-vsk/infrastructure-apps-and-security-overview-cloned-lauren) | lauren.phillips@datadoghq.com | - [API queries](https://app.datadoghq.com/dashboard/s9d-aup-vsk/infrastructure-apps-and-security-overview-cloned-lauren?fullscreen_widget=9) |
| [Infrastructure, Apps, and Security Overview](https://app.datadoghq.com/dashboard/dc9-h6u-d2e/infrastructure-apps-and-security-overview) | priyanka.prakash@datadoghq.com | - [API queries](https://app.datadoghq.com/dashboard/dc9-h6u-d2e/infrastructure-apps-and-security-overview?fullscreen_widget=9) |
| [Executive Dashboard SLA dp (cloned)](https://app.datadoghq.com/dashboard/nbv-qba-8k2/executive-dashboard-sla-dp-cloned) | donald.pasquarello@datadoghq.com | * [Reqs per sec](https://app.datadoghq.com/dashboard/nbv-qba-8k2/executive-dashboard-sla-dp-cloned?fullscreen_widget=15)<br> * [Storage Requests](https://app.datadoghq.com/dashboard/nbv-qba-8k2/executive-dashboard-sla-dp-cloned?fullscreen_widget=23) |
| [Executive Dashboard CoxAuto](https://app.datadoghq.com/dashboard/ybv-qgn-59v/executive-dashboard-coxauto) | josh.king@datadoghq.com | - [Reqs per sec](https://app.datadoghq.com/dashboard/ybv-qgn-59v/executive-dashboard-coxauto?fullscreen_widget=15)<br> - [Storage Requests](https://app.datadoghq.com/dashboard/ybv-qgn-59v/executive-dashboard-coxauto?fullscreen_widget=23) |
