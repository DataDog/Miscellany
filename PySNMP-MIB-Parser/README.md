# PySNMP-MIB-Parser
Converts a MIB file (in PySNMP format) to a yaml file that can be used by Datadog's SNMP agent integration: https://docs.datadoghq.com/integrations/snmp/

## Pre-Requisites

**MIB Format**

Datadog SNMP agent integration requires all MIB files to be in PySNMP format. The agent comes packaged with a list of MIBs that can be used out-of-the-box (in Linux environments this can be found here: /opt/datadog-agent/embedded/lib/python2.7/site-packages/pysnmp_mibs)

If looking to use your own MIB that is not already packaged with the Datadog agent follow the steps in the following documentation to convert to PySNMP format: https://docs.datadoghq.com/integrations/snmp/#use-your-own-mib

Once your MIB is in PySNMP format you can use this tool to parse the MIB and convert it into a usable yaml file.

## Steps for Parsing MIB

1. Clone this repository.
2. Run `python parse.py`  
This script will:  
    a. Prompt you for the location/name of the MIB file  
    b. Parse OIDs from MIB file  
    c. Creates a file `end.yaml` that contains the contents of `begin.yaml` with the parsed OIDs appended to the end of it
3. Rename `end.yaml` to `conf.yaml`
4. Place `conf.yaml` in the agent's /conf.d/snmp.d/ directory
5. Edit the `conf.yaml` to include information about your SNMP device: hostname, port, community string, etc.
6. Remove unwanted OIDs from `conf.yaml` and OIDs that don't return gauges, counters, integers, or double values (ie. strings)
7. Restart the Datadog Agent
