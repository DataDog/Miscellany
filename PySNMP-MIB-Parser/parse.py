import re


mibname = raw_input("Type the name of the PySNMP-converted MIB you would like to parse into yaml - include .py in the name\n     (For example: /opt/datadog-agent/embedded/lib/python2.7/site-packages/pysnmp_mibs/HOST-RESOURCES-MIB.py): ")


def listit(t):
    return list(map(listit, t)) if isinstance(t, (list, tuple)) else t


def parse_mib():

    f = open(mibname, 'r')

    
    r1 = re.findall(r'(\w+)\s\=\s\w+\(\(([\d+,\s]+)\)', f.read()) #pulls back all OIDs including table, rows, object identifiers
    
    global lst
    lst = listit(r1)

    for x in range(len(lst)):
      lst[x][1]=lst[x][1].replace(", ",".")


def build_yaml():
    file = open('begin.yaml', 'r')
    contents = file.read()
    file.close()  
    
    for x in range(len(lst)):
      contents=contents+"      - OID: "+lst[x][1]+"\n        name: "+lst[x][0]+"\n"
    
    file = open('end.yaml', 'w')
    file.write(contents)
    file.close()
    print(".\n..\n...\nWriting all OIDs from "+mibname+" into 'end.yaml'.\n...\n..\n.\n")


parse_mib()
build_yaml()
print("Next steps to finish configuring SNMP integration:\n 1. Rename 'end.yaml' to 'conf.yaml'\n 2. Place 'conf.yaml' in the agent's /conf.d/snmp.d/ directory\n 3. Edit the conf.yaml to include information about your SNMP device: hostname, port, community string, etc.\n 4. Remove OIDs that don't return gauges, counters, integers, or double values (ie. strings)\n 5. Restart the Datadog Agent") 
