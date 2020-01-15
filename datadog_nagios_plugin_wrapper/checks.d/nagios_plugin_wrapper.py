import re
from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException
from datadog_checks.utils.subprocess_output import get_subprocess_output

__version__ = "1.0.0"
__author__ = "Misiu Pajor <misiu.pajor@datadoghq.com>"

class NagiosPluginWrapperCheck(AgentCheck):
    PERFDATA_RE = (
        r"([^\s]+|'[^']+')=([-.\d]+)(c|s|ms|us|B|KB|MB|GB|TB|%)?" +
        r"(?:;([-.\d]+))?(?:;([-.\d]+))?(?:;([-.\d]+))?(?:;([-.\d]+))?")

    def check(self, instance):
        check_command = instance.get('check_command')
        metric_namespace = instance.get('metric_namespace')
        tags = instance.get('tags', [])
        create_service_check = instance.get('create_service_check', False)

        if not check_command:
            raise CheckException("Configuration error. Missing check_command definition, please fix nagios_plugin_wrapper.yaml")

        if not metric_namespace:
            raise CheckException("Configuration error. Missing metric_namespace definition, please fix nagios_plugin_wrapper.yaml")

        raw_output = None
        err = None
        ret = None
        try:
            raw_output, err, ret = get_subprocess_output(check_command, self.log)
        except Exception as e:
            error = "Failed to execute check_command {check_command} - {error}".format(
                check_command=check_command, error=e)
            self.log.warning(error)
            raise CheckException("check_command '{check_command}' failed to execute, see agent.log for more information.".format(
                check_command=check_command
        ))

        output, metrics = self._parse_output(raw_output)
        if metrics:
            metrics = self._parse_perfdata(metrics)
            for label, value in metrics:
                label = self._sanitize(label)
                self.log.debug("metric_namespace: {namespace} | tags: {tags} | value: {value} | ret_code: {ret}".format(
                    namespace=metric_namespace, tags=tags, value=value, ret=ret))
                self.gauge('{metric_namespace}.{label}'.format(
                    metric_namespace=metric_namespace, label=label), value, tags=tags)

        if output and create_service_check:
            if ret == 0:
                status = AgentCheck.OK
            elif ret == 1:
                status = AgentCheck.WARNING
            elif ret == 2:
                status = AgentCheck.CRITICAL
            else:
                status = AgentCheck.UNKNOWN
            self.service_check(metric_namespace, status, tags=tags, message=output.rstrip())

    def _parse_output(self, s):
        """Parse the output text and performance data string"""
        try:
            output, metrics = s.rsplit('|', 1)
        except ValueError:
            self.log.debug("No performance data found in string: {string}, skipping...".format(
                string=s))
            return s, None
        return output, metrics

    def _parse_perfdata(self, s):
        """Parse performance data from a perfdata string"""
        metrics = []
        counters = re.findall(self.PERFDATA_RE, s)
        if counters is None:
            self.log.warning("Failed to parse performance data: {s}".format(
                s=s))
            return metrics

        for (key, value, uom, warn, crit, min, max) in counters:
            try:
                norm_value = self._normalize_to_unit(float(value), uom)
                metrics.append((key, norm_value))
            except ValueError:
                self.log.warning(
                    "Couldn't convert value '{value}' to float".format(
                        value=value))

        return metrics

    def _normalize_to_unit(self, value, unit):
        """Normalize the value to the unit returned.
        We use base-1000 for second-based units, and base-1024 for
        byte-based units. Sadly, the Nagios-Plugins specification doesn't
        disambiguate base-1000 (KB) and base-1024 (KiB).
        """
        if unit == 'ms':
            return value / 1000.0
        if unit == 'us':
            return value / 1000000.0
        if unit == 'KB':
            return value * 1024
        if unit == 'MB':
            return value * 1024 * 1024
        if unit == 'GB':
            return value * 1024 * 1024 * 1024
        if unit == 'TB':
            return value * 1024 * 1024 * 1024 * 1024

        return value

    def _sanitize(self, s):
        """Sanitize the name of a metric to remove unwanted chars
        """
        return re.sub("[^\w-]", "", s)
