# Datadog Nagios Plugin Wrapper
Oh, hi! You probably found this repository because you are moving your monitoring to Datadog from a Nagios-based solution and you came to think of that you have **a lot** of custom Nagios plugins built by smart people in your organisation that you don't feel comfortable spending time rewriting to native Datadog checks.

Not a problem, this repository was created to help you with just that.

## So, what does this do for you?
In short, this Datadog check will act as a wrapper so that you can reuse your existing Nagios plugins without having to rewrite them for Datadog, and it does _not_ require a Nagios instance running. It will create custom metrics in Datadog based on the performance data your plugin returns, it can also create service checks that follow the Nagios API Plugin standard (ala, "exit codes").

For example, you might have a Nagios plugin that returns an exit code of `0` (ie., "OK") and the following output:

```PING OK - Packet loss = 0%, RTA = 0.80 ms | percent_packet_loss=0, rta=0.80``` 

This Datadog check will convert that output to two Datadog metrics with the tags you define in `conf.yaml`:
- `<metric_namespace>.percent_package_loss` with a timeseries value of: `0` 
- `<metric_namespace>.rta` with a timeseries value of: `0.80`

**Optional**

This check can create a Datadog service check if you set `create_service_check: true` in conf.yaml, the result will be:

- message = `PING OK - Packet loss = 0%, RTA = 0.80 ms` (performance data is stripped from the message)
- status = `OK` (since your plugin returned exit code `0`)
- tags = tags you've defined in `conf.yaml`


## Setup
To install the Datadog Nagios Plugin Wrapper check:
1. Place the `nagios_plugin_wrapper.py` in the checks.d/ folder of your Datadog agent.
2. Create a `nagios_plugin_wrapper.d/` folder in the conf.d/ folder at the root of your [Datadog Agent's configuration directory](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7#agent-configuration-directory).
3. Create a `conf.yaml` file in the `nagios_plugin_wrapper.d/` folder previously created.
4. Consult the sample conf.yaml.example file and copy its content in to the conf.yaml file.
5. Edit the conf.yaml to run your custom Nagios plugins.

At this point you should have the following structure setup:

```<agent root>/conf.d/nagios_plugin_wrapper.d/conf.yaml```

```<agent root>/checks.d/nagios_plugin_wrapper.py```

6. [Restart the agent](https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent)

## Validation
[Run the Agent's status subcommand](https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7#service-status) and look for nagios_plugin_wrapper under the Checks section.

## Author
* Misiu Pajor (misiu.pajor@datadoghq.com)

## Credits
Thanks goes to these wonderful people:
* Oskar Rittsél ([@rittsel](https://github.com/Rittsel)) – Datadog Inc.
* python-diamond ([@python-diamond](https://github.com/python-diamond))
