# Custom Check Shell
Spins up a VM using vagrant that installs the Datadog agent on it with a simple
custom check using shell as described in [this Datadog KB
article](https://help.datadoghq.com/hc/en-us/articles/115000722623-How-can-I-gather-metrics-from-the-UNIX-shell-).

# Prerequesites
- [Vagrant](https://www.vagrantup.com/)

# Run
`DD_API_KEY=<YOURAPIKEYHERE> vagrant up`

# Metrics
Custom metrics will show up in Datadog as `example.mem.free.pct`

# Looking in
- `vagrant ssh`
- `sudo su -`
- `/etc/init.d/datadog-agent configcheck`
- `/etc/init.d/datadog-agent info`
