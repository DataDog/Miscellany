# Datadog on Minikube

**Table of content**

1. Installation with the DaemonSet
  1. Setup your environment
1. Installation with Helm
  1. Setup your environment
1. Tips

## Setup your environment

1. Install Minikube: [minikube.sigs.k8s.io/docs/start](https://minikube.sigs.k8s.io/docs/start/)
1. Install Kubectl: [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/#kubectl)
1. Install Helm (only if you target the Helm installation): [helm.sh/docs/intro/install](https://helm.sh/docs/intro/install/)
1. Start Minikube: `minikube start --memory='8g' --cpus='2'`
1. Check your installation: `$ kubectl get nodes`

```
NAME       STATUS   ROLES                  AGE   VERSION
minikube   Ready    control-plane,master   9d    v1.22.2
```

## Installation with the DaemonSet

### Install Datadog agent

Follow the first steps from this documentation (1 and 2): [docs.datadoghq.com/agent/kubernetes](https://docs.datadoghq.com/agent/kubernetes/?tab=daemonset)

From the step 3, pick the full installation: [Manifest template](https://docs.datadoghq.com/resources/yaml/datadog-agent-all-features.yaml). The reason is, if you want to monitor your entire cluster, inculding Kubernetes resources, you have to monitor the process.

If you don't need the full install (for example if you don't use the APM module, or the Security), you can as well remove these components from the Yaml file, or choose another installation flavor, keeping in mind you'll have to implement the process monitoring by hand. See (docs.datadoghq.com/agent/kubernetes/?tab=daemonset#kubernetes-resources-for-live-containers)[https://docs.datadoghq.com/agent/kubernetes/?tab=daemonset#kubernetes-resources-for-live-containers].

### Specific configuration for Minikube

In order to be able to monitor the control plane, we need some more tuning, and that's not a specificity of Minikube. But Minikube (which relies on Kubeadm) have its specifities as well, and the second section address these specificities.

#### Initial configuration

In this section, we assume that you use [datadog-agent-all-features.yaml](https://docs.datadoghq.com/resources/yaml/datadog-agent-all-features.yaml) yaml file as a base configuration.

To be able apply the configuration file, some customization a required:

- Remove or comment the secret part, as the secret is already created in step 2

```yaml
---
# Source: datadog/templates/secret-api-key.yaml
apiVersion: v1
kind: Secret
metadata:
  name: datadog-agent
  namespace: default
  labels: {}
type: Opaque
data:
  api-key: PUT_YOUR_BASE64_ENCODED_API_KEY_HERE
```

- Replace `PUT_A_BASE64_ENCODED_RANDOM_STRING_HERE` (needs to be at least 32 characters a-zA-z)

```bash
$ echo -n abcdefghijklmnopqrstuvwxyz1234567890|base64
YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkw
```

```yaml
---
# Source: datadog/templates/secret-cluster-agent-token.yaml
apiVersion: v1
kind: Secret
metadata:
  name: datadog-agent-cluster-agent
  namespace: default
  labels: {}
type: Opaque
data:
  token: YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkw
```

- For all the container, add the variable `DD_CLUSTER_NAME`, as this variable can't be extrated from cloud provider metadata

```yaml
- name: DD_CLUSTER_NAME
  value: "minikube"
```

- Do the same with `DD_KUBELET_TLS_VERIFY` to allow the agent to communicate with kubelet

```yaml
- name: DD_KUBELET_TLS_VERIFY
  value: "false"
```

Apply the configuration file:

```
$ kubectl apply -f datadog-agent-all-features.yaml
$ kubectl get pods
NAME                                           READY   STATUS    RESTARTS   AGE
datadog-agent-cluster-agent-6f66d65d7b-58lzg   1/1     Running   0          3m31s
datadog-agent-gfhxk                            5/5     Running   0          3m23s
```

By executing `agent status` against the agent pod, you can see that many component are already running correctly, and some not. That is expected, because monitoring the control plane require some more configuration. For the moment, let's see what is already working:

```bash
$ kubectl exec -ti datadog-agent-gfhxk -- agent status
=====================
Datadog Cluster Agent
=====================

  - Datadog Cluster Agent endpoint detected: https://10.101.197.84:5005
  Successfully connected to the Datadog Cluster Agent.
  - Running: 1.15.1+commit.b9b97b0

==========
Logs Agent
==========

    Sending compressed logs in HTTPS to agent-http-intake.logs.datadoghq.com on port 443
    BytesSent: 2.205683e+06
    EncodedBytesSent: 147647
    LogsProcessed: 2169
    LogsSent: 2165

   kubelet (7.0.0)
    ---------------
      Instance ID: kubelet:5bbc63f3938c02f4 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kubelet.d/conf.yaml.default
      Total Runs: 11
      Metric Samples: Last Run: 928, Total: 10,058
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 4, Total: 44
      Average Execution Time : 295ms
      Last Execution Date : 2021-11-19 14:44:09 UTC (1637333049000)
      Last Successful Execution Date : 2021-11-19 14:44:09 UTC (1637333049000)

    kube_apiserver_metrics (1.10.0)
    -------------------------------
      Instance ID: kube_apiserver_metrics:64b51327a52a8e5 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kube_apiserver_metrics.d/auto_conf.yaml
      Total Runs: 13
      Metric Samples: Last Run: 9,274, Total: 115,119
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 1, Total: 13
      Average Execution Time : 1.002s
      Last Execution Date : 2021-11-19 14:44:03 UTC (1637333043000)
      Last Successful Execution Date : 2021-11-19 14:44:03 UTC (1637333043000)
```

![minikube_without_control_plane_monitoring](https://user-images.githubusercontent.com/13923756/142644417-79898351-cf5d-4417-8f28-6498397b8d85.png)

In the next part, we'll configure the agent to be able to monitor the control plane:

- etcd
- kube_controller_manager
- kube_scheduler

#### Monitoring the controle plane

##### etcd

etcd is the brain of Kubernetes, where the state of everything is stored. Obviously, you want to be able to monitor it.

[docs.datadoghq.com/integrations/etcd](https://docs.datadoghq.com/integrations/etcd/?tab=containerized)

To be able to monitor etcd, we need:

1. the certificates to communicate with
1. a customized configuration for the Datadog agent, which by default relies on auto-discovery to configure etcd monitoring

The certificates used by etcd can be found directly on the minikube filesystem:

```bash
$ minikube ssh
$ cd /var/lib/minikube/certs/etcd
$ ls
ca.crt	ca.key	healthcheck-client.crt	healthcheck-client.key	peer.crt  peer.key  server.crt	server.key
```

So, all we need to do it mounting them inside the agent pod. Find the volumes section in `datadog-agent-all-features.yaml`, and add a new volume of type hostPath:

```yaml
- hostPath:
    path: /var/lib/minikube/certs/etcd
  name: etcd-certs
```

Only the agent container need to access to etcd, so we just need now to update the agent volumeMounts:

```yaml
- name: etcd-certs
  mountPath: /etc/datadog-agent/minkikube
  readOnly: true
```

Now, let's create a configMap to replace the actual `auto_conf.yaml` file in `/etc/datadog-agent/conf.d/etcd.d` (you can place it just above the daemonset configuration):

```yaml
---
kind: ConfigMap
apiVersion: v1
metadata:
     name: ad-etcd
     namespace: default
data:
     conf.yaml: |-
          ad_identifiers:
            - etcd
          instances:
            - prometheus_url: https://%%host%%:2379/metrics
              tls_ca_cert: /etc/datadog-agent/minkikube/ca.crt
              tls_cert: /etc/datadog-agent/minkikube/server.crt
              tls_private_key: /etc/datadog-agent/minkikube/server.key
```

To be able to use it in the agent pod, we have to create a volume from it. Once again, in the volumes section, add the following:

```yaml
- name: dd-etcd
  configMap:
    name: ad-etcd
```

Then, in the agent container volumeMounts:

```yaml
- name: dd-etcd
  mountPath: /etc/datadog-agent/conf.d/etcd.d/
```

Because we created the configuration file ourself, we don't want to rely on the autoconf for etcd anymore. In order to disable autoconf for etcd, add this new variable in the agent container:

```yaml
- name: DD_IGNORE_AUTOCONF
  value: etcd
```

It's now time to test our configuration, by deploying one more time the agent:

```bash
$ kubectl apply -f datadog-agent-all-features.yaml
$ kubectl get po
NAME                                           READY   STATUS    RESTARTS   AGE
datadog-agent-cluster-agent-6f66d65d7b-58lzg   1/1     Running   0          53m
datadog-agent-t9rtl                            5/5     Running   0          38s
$ kubectl exec -ti datadog-agent-t9rtl -- agent status

    etcd (2.7.1)
    ------------
      Instance ID: etcd:d09e4493abb0512 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/etcd.d/conf.yaml
      Total Runs: 5
      Metric Samples: Last Run: 1,059, Total: 5,295
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 1, Total: 5
      Average Execution Time : 126ms
      Last Execution Date : 2021-11-19 15:33:31 UTC (1637336011000)
      Last Successful Execution Date : 2021-11-19 15:33:31 UTC (1637336011000)
      metadata:
        version.major: 3
        version.minor: 5
        version.patch: 0
        version.raw: 3.5.0
        version.scheme: semver
```

#### controller manager and scheduler

These two components have a very similar configuration, and now that we already know how to update a configuration in the agent, let's do this in a bulk.

In kubeadm, controller manager and scheduler are only listening on the hostnetwork, on 127.0.0.1. To be able to reach them, we also need to run the agent on the hostnetwork. We just need one more variable to do so:

```yaml
hostNetwork: true
```

We have to place it at the daemonset level:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: datadog-agent
  namespace: default
  labels: {}
spec:
  selector:
    matchLabels:
      app: datadog-agent
  template:
    metadata:
      labels:
        app: datadog-agent
      name: datadog-agent
    spec:
      hostPID: true
      hostNetwork: true
```

Next, let's create two more configmaps, one for the scheduler and one for the controller manager in order to replace autoconf:

```yaml
kind: ConfigMap
apiVersion: v1
metadata:
     name: ad-scheduler
     namespace: default
data:
     conf.yaml: |-
          ad_identifiers:
            - kube-scheduler

          init_config:

          instances:
            - prometheus_url: https://localhost:10259/metrics
              bearer_token_auth: true
              ssl_verify: false
              leader_election: false
---
kind: ConfigMap
apiVersion: v1
metadata:
     name: ad-controller-manager
     namespace: default
data:
     conf.yaml: |-
          ad_identifiers:
            - kube-controller-manager

          init_config:

          instances:
            - prometheus_url: https://localhost:10257/metrics
              bearer_token_auth: true
              ssl_verify: false
              leader_election: false
```

We can place it just below the etcd configmap. This two components are by default autoconfigured by the agent, which is not what we want here, so let's update the `DD_IGNORE_AUTOCONF` variable:

```yaml
- name: DD_IGNORE_AUTOCONF
  value: etcd kube-scheduler kube-controller-manager
```

Next, as previously, we need to create a volume to be able to these data in our containers.

```yaml
- name: ad-scheduler
  configMap:
    name: ad-scheduler
- name: ad-controller-manager
  configMap:
    name: ad-controller-manager
```

Finaly, we need to mount the volumes in the container. Let's update one more time the volumeMounts of the agent:

```yaml
volumeMounts:
  - name: ad-scheduler
    mountPath: /etc/datadog-agent/conf.d/kube_scheduler.d/
  - name: ad-controller-manager
    mountPath: /etc/datadog-agent/conf.d/kube_controller_manager.d/
```

Now let's apply this config:

```
$ kubectl apply -f datadog-agent-all-features.yaml
$ kubectl get po
NAME                                           READY   STATUS    RESTARTS        AGE
datadog-agent-cluster-agent-6f66d65d7b-58lzg   1/1     Running   1 (2d16h ago)   2d18h
datadog-agent-k897l                            5/5     Running   0               114s
$ kubectl exec -ti datadog-agent-k897l -- agent status

    kube_controller_manager (2.0.1)
    -------------------------------
      Instance ID: kube_controller_manager:aa60000b603ad467 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kube_controller_manager.d/conf.yaml
      Total Runs: 2
      Metric Samples: Last Run: 1,423, Total: 2,846
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 2, Total: 4
      Average Execution Time : 200ms
      Last Execution Date : 2021-11-22 09:04:08 UTC (1637571848000)
      Last Successful Execution Date : 2021-11-22 09:04:08 UTC (1637571848000)


    kube_scheduler (2.0.1)
    ----------------------
      Instance ID: kube_scheduler:855aa9d114404c21 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kube_scheduler.d/conf.yaml
      Total Runs: 2
      Metric Samples: Last Run: 49, Total: 98
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 2, Total: 4
      Average Execution Time : 74ms
      Last Execution Date : 2021-11-22 09:04:05 UTC (1637571845000)
      Last Successful Execution Date : 2021-11-22 09:04:05 UTC (1637571845000)
```

Voilà! Everything is working fine now, are we are able to monitor every single piece of our Kubernetes cluster.

## Installation with Helm

### Install Datadog agent

The process is straightforward, as explained in the following documentation: [docs.datadoghq.com/agent/kubernetes](https://docs.datadoghq.com/agent/kubernetes/?tab=helm)

```bash
$ helm repo add datadog https://helm.datadoghq.com
$ helm repo update
$ helm install datadog --set datadog.apiKey=<DATADOG_API_KEY> datadog/datadog
```

However, to expect monitoring minikube properly, some changes in `values.yaml` must be performed.

### Retrive values.yaml file

The easiest way to capture the values of the helm chart, is to execute the folling command:

```bash
$ helm show values datadog/datadog > values.yaml
```

Now that we have a complete `values.yaml`, we can start editing.

### Basic configuration

Around line 59, provide a name to your cluster:

```yaml
clusterName: minikube
```

Around line 147, turn `tlsVerify` to false:

```yaml
tlsVerify: false
```

Around line 221, turn logs on:

```yaml
logs:
  # datadog.logs.enabled -- Enables this to activate Datadog Agent log collection
  ## ref: https://docs.datadoghq.com/agent/basic_agent_usage/kubernetes/#log-collection-setup
  enabled: true
```

With these modifications in place, let's deploy the agent:

```bash
$ helm install datadog -f values.yaml --set datadog.apiKey=<DATADOG_API_KEY> datadog/datadog
NAME: datadog
LAST DEPLOYED: Fri Nov 26 10:55:58 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Datadog agents are spinning up on each node in your cluster. After a few
minutes, you should see your agents starting in your event stream:
    https://app.datadoghq.com/event/stream
```

They are some points that we have to fix:

```bash
  Loading Errors
  ==============
    kube_controller_manager
    -----------------------
      Core Check Loader:
        Check kube_controller_manager not found in Catalog

      JMX Check Loader:
        check is not a jmx check, or unable to determine if it's so

      Python Check Loader:
        could not configure check instance for python check kube_controller_manager: could not invoke 'kube_controller_manager' python check constructor. New constructor API returned:
Traceback (most recent call last):
  File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/kube_controller_manager/kube_controller_manager.py", line 136, in __init__
    if url is None and re.search(r'/metrics$', prometheus_url):
  File "/opt/datadog-agent/embedded/lib/python3.8/re.py", line 201, in search
    return _compile(pattern, flags).search(string)
TypeError: expected string or bytes-like object
Deprecated constructor API returned:
__init__() got an unexpected keyword argument 'agentConfig'

    kube_scheduler
    --------------
      Core Check Loader:
        Check kube_scheduler not found in Catalog

      JMX Check Loader:
        check is not a jmx check, or unable to determine if it's so

      Python Check Loader:
        could not configure check instance for python check kube_scheduler: could not invoke 'kube_scheduler' python check constructor. New constructor API returned:
Traceback (most recent call last):
  File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/kube_scheduler/kube_scheduler.py", line 140, in __init__
    if url is None and re.search(r'/metrics$', prometheus_url):
  File "/opt/datadog-agent/embedded/lib/python3.8/re.py", line 201, in search
    return _compile(pattern, flags).search(string)
TypeError: expected string or bytes-like object
Deprecated constructor API returned:
__init__() got an unexpected keyword argument 'agentConfig'

    etcd (2.8.0)
    ------------
      Instance ID: etcd:b584110e00adcdae [ERROR]
      Configuration Source: file:/etc/datadog-agent/conf.d/etcd.d/auto_conf.yaml
      Total Runs: 2
      Metric Samples: Last Run: 0, Total: 0
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 23ms
      Last Execution Date : 2021-11-30 09:50:22 UTC (1638265822000)
      Last Successful Execution Date : Never
      Error: Detected 1 error while loading configuration model `InstanceConfig`:
prometheus_url
  field required
      Traceback (most recent call last):
        File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/base/checks/base.py", line 992, in run
          initialization()
        File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/base/checks/base.py", line 407, in load_configuration_models
          instance_config = self.load_configuration_model(package_path, 'InstanceConfig', raw_instance_config)
        File "/opt/datadog-agent/embedded/lib/python3.8/site-packages/datadog_checks/base/checks/base.py", line 447, in load_configuration_model
          raise_from(ConfigurationError('\n'.join(message_lines)), None)
        File "<string>", line 3, in raise_from
      datadog_checks.base.errors.ConfigurationError: Detected 1 error while loading configuration model `InstanceConfig`:
      prometheus_url
        field required
```

### etcd 

In this guided part, we are folling the instructions on monitoring the control plane with Datadog agent: https://docs.datadoghq.com/agent/kubernetes/control_plane/?tab=helm#Kubeadm

Let's start with etcd. To be able to monitor etcd, we need the certificates necessary to communicate with it. In minikube, we can find them under `/var/lib/minikube/certs/` :

```bash
$ ls /var/lib/minikube/certs/
apiserver-etcd-client.crt  apiserver-kubelet-client.crt  apiserver.crt	ca.crt	etcd		    front-proxy-ca.key	    front-proxy-client.key  proxy-client-ca.key  proxy-client.key  sa.pub
apiserver-etcd-client.key  apiserver-kubelet-client.key  apiserver.key	ca.key	front-proxy-ca.crt  front-proxy-client.crt  proxy-client-ca.crt     proxy-client.crt	 sa.key
```

Since we need to mount these certificates in the agent pod, we fisrt need to create a volume. Edit the `values.yaml` (around line 1066):

```yaml
  # agents.volumes -- Specify additional volumes to mount in the dd-agent container
  volumes: []
    - hostPath:
        path: /var/lib/minikube/certs/etcd
      name: etcd-certs
```

Then, let's create the associated volumeMounts (just below in the file):

```yaml
  # clusterAgent.volumeMounts -- Specify additional volumes to mount in the cluster-agent container
  volumeMounts:
    - name: etcd-certs
      mountPath: /etc/datadog-agent/minkikube
      readOnly: true
```

Now, we have to create a new entry in conf.d for etcd (around line 281):

```yaml
  # datadog.confd -- Provide additional check configurations (static and Autodiscovery)
  ## Each key becomes a file in /conf.d
  ## ref: https://github.com/DataDog/datadog-agent/tree/main/Dockerfiles/agent#optional-volumes
  ## ref: https://docs.datadoghq.com/agent/autodiscovery/
  confd:
    etcd.yaml: |-
      ad_identifiers:
        - etcd
      instances:
        - prometheus_url: https://%%host%%:2379/metrics
          tls_ca_cert: /etc/datadog-agent/minkikube/ca.crt
          tls_cert: /etc/datadog-agent/minkikube/server.crt
          tls_private_key: /etc/datadog-agent/minkikube/server.key
```

Because we created a manual configuration for etcd, we also want to disable autodiscovery for the component. To do so, let's update `ignoreAutoConfig` around line 469:

```yaml
  # datadog.ignoreAutoConfig -- List of integration to ignore auto_conf.yaml.
  ## ref: https://docs.datadoghq.com/agent/faq/auto_conf/
  ignoreAutoConfig:
    - etcd
```

With these element in place, let's update our config:

```bash
$ helm upgrade datadog -f values.yaml --set datadog.apiKey=<DATADOG_API_KEY> datadog/datadog
$ kubectl exec -ti datadog-dqx48 -- agent status

    etcd (2.8.0)
    ------------
      Instance ID: etcd:ed7fa7d544bf41bd [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/etcd.yaml
      Total Runs: 3
      Metric Samples: Last Run: 1,060, Total: 3,180
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 1, Total: 3
      Average Execution Time : 134ms
      Last Execution Date : 2021-11-30 13:15:29 UTC (1638278129000)
      Last Successful Execution Date : 2021-11-30 13:15:29 UTC (1638278129000)
      metadata:
        version.major: 3
        version.minor: 5
        version.patch: 0
        version.raw: 3.5.0
        version.scheme: semver
```

#### controller manager and scheduler

We will update the entry in conf.d (around line 289):

```yaml
  # datadog.confd -- Provide additional check configurations (static and Autodiscovery)
  ## Each key becomes a file in /conf.d
  ## ref: https://github.com/DataDog/datadog-agent/tree/main/Dockerfiles/agent#optional-volumes
  ## ref: https://docs.datadoghq.com/agent/autodiscovery/
  confd:
    etcd.yaml: |-
      ad_identifiers:
        - etcd
      instances:
        - prometheus_url: https://%%host%%:2379/metrics
          tls_ca_cert: /etc/datadog-agent/minkikube/ca.crt
          tls_cert: /etc/datadog-agent/minkikube/server.crt
          tls_private_key: /etc/datadog-agent/minkikube/server.key
    kube_scheduler.yaml: |-
      ad_identifiers:
        - kube-scheduler
      instances:
        - prometheus_url: http://localhost:10259/metrics
          ssl_verify: false
          bearer_token_auth: true
          leader_election: false
    kube_controller_manager.yaml: |-
      ad_identifiers:
        - kube-controller-manager
      instances:
        - prometheus_url: http://localhost:10257/metrics
          ssl_verify: false
          bearer_token_auth: true
          leader_election: false
```

And also `ignoreAutoConfig` (line 476)

```yaml
  # datadog.ignoreAutoConfig -- List of integration to ignore auto_conf.yaml.
  ## ref: https://docs.datadoghq.com/agent/faq/auto_conf/
  ignoreAutoConfig:
    - etcd
    - kube_scheduler
    - kube_controller_manager
```

And finally on line 1094, configure the agent to use host network:

```yaml
  # agents.useHostNetwork -- Bind ports on the hostNetwork
  ## Useful for CNI networking where hostPort might
  ## not be supported. The ports need to be available on all hosts. It Can be
  ## used for custom metrics instead of a service endpoint.
  ##
  ## WARNING: Make sure that hosts using this are properly firewalled otherwise
  ## metrics and traces are accepted from any host able to connect to this host.
  useHostNetwork: true
```

Then update the agent:

```bash
$ helm upgrade datadog -f values.yaml --set datadog.apiKey=<DATADOG_API_KEY> datadog/datadog
$ kubectl exec -ti datadog-dqx48 -- agent status

    kube_controller_manager (2.0.1)
    -------------------------------
      Instance ID: kube_controller_manager:d2f8d67dc8653df9 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kube_controller_manager.yaml
      Total Runs: 2
      Metric Samples: Last Run: 1,424, Total: 2,848
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 2, Total: 4
      Average Execution Time : 204ms
      Last Execution Date : 2021-11-30 13:48:21 UTC (1638280101000)
      Last Successful Execution Date : 2021-11-30 13:48:21 UTC (1638280101000)


    kube_scheduler (2.1.1)
    ----------------------
      Instance ID: kube_scheduler:b74dcfe4c1e75a03 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kube_scheduler.yaml
      Total Runs: 2
      Metric Samples: Last Run: 68, Total: 136
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 2, Total: 4
      Average Execution Time : 117ms
      Last Execution Date : 2021-11-30 13:48:13 UTC (1638280093000)
      Last Successful Execution Date : 2021-11-30 13:48:13 UTC (1638280093000)
```

TADA! 🎉

## Tips

You probably noticed this line in the scheduler and controller-manager configmap:

```yaml
leader_election: false
```

Leader election, in simple words, is the mechanism that guarantees that only one instance of the kube-scheduler — or one instance of the kube-controller-manager — is actively making decisions, while all the other instances are inactive, but ready to take leadership if something happens to the active one. [Leader election in Kubernetes control plane](https://blog.heptio.com/leader-election-in-kubernetes-control-plane-heptioprotip-1ed9fb0f3e6d#:~:text=Leader%20election%2C%20in%20simple%20words,happens%20to%20the%20active%20one.)

Because only one instance is actively making decisions, it's crucial to always monitor this very one. So why do we used `leader_election: false`? For two reasons:

1. There is only one instance of kube-scheduler and kube-controller-manager by master node. And because Minikube is mono-master, we are sure to always monitor the leader one.
1. Leader election status is commonly detected through endpoints, but in Kubernetes the default parameter for `leader-elect-resource-lock` is leases ([kube-controller-manager](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/)), which means there is no endpoint to parse to capture this specific information:

```bash
$ kubectl get ep -n kube-system
NAME                       ENDPOINTS                                     AGE
k8s.io-minikube-hostpath   <none>                                        16d
kube-dns                   172.17.0.2:53,172.17.0.2:53,172.17.0.2:9153   16d
```

However, it's easy to change this specific behavior (ok, for minikube is useless, but a good gotcha for your other Kubernetes implementation, if your goal is to run it in production). Let's start a new minikube instance instance with the following parameters:

```bash
$ minikube start -p new --memory='8g' --cpus='2' --extra-config=controller-manager.leader-elect-resource-lock=endpoints \
  --extra-config=controller-manager.leader-elect=true \
  --extra-config=scheduler.leader-elect-resource-lock=endpoints \
  --extra-config=scheduler.leader-elect=true
$ kubectl get ep -n kube-system
NAME                       ENDPOINTS                                     AGE
k8s.io-minikube-hostpath   <none>                                        3m34s
kube-controller-manager    <none>                                        4m21s
kube-dns                   172.17.0.2:53,172.17.0.2:53,172.17.0.2:9153   4m7s
kube-scheduler             <none>                                        4m19s
$ kubectl describe ep -n kube-system kube-controller-manager
Name:         kube-controller-manager
Namespace:    kube-system
Labels:       <none>
Annotations:  control-plane.alpha.kubernetes.io/leader:
                {"holderIdentity":"leader-elec_d57d3e05-aec6-4a47-b6fc-354ca5b6c8a1","leaseDurationSeconds":15,"acquireTime":"2021-11-22T09:34:49Z","renew...
Subsets:
Events:
  Type    Reason          Age    From                     Message
  ----    ------          ----   ----                     -------
  Normal  LeaderElection  5m21s  kube-controller-manager  leader-elec_d57d3e05-aec6-4a47-b6fc-354ca5b6c8a1 became leader
```

That's it! So now let's update this line from the kube-scheduler and kube-controller-manager:

```yaml
leader_election: true
```

An then, apply our config in this cluster:

> Don't forget, because it's a brand new cluster, you have to go through steps 1 and 2 of [docs.datadoghq.com/agent/kubernetes](https://docs.datadoghq.com/agent/kubernetes/?tab=daemonset) to create RBAC rules and to encode your Datadog API key in a secret.

```bash
$ kubectl get po
NAME                                           READY   STATUS    RESTARTS   AGE
datadog-agent-cluster-agent-6f66d65d7b-gjrpw   1/1     Running   0          59s
datadog-agent-nbhvm                            5/5     Running   0          59s

$ kubectl exec -ti datadog-agent-nbhvm -- agent status
    kube_controller_manager (2.0.1)
    -------------------------------
      Instance ID: kube_controller_manager:11266a51fd1eaec8 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kube_controller_manager.d/conf.yaml
      Total Runs: 4
      Metric Samples: Last Run: 1,426, Total: 5,704
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 3, Total: 12
      Average Execution Time : 766ms
      Last Execution Date : 2021-11-22 09:51:43 UTC (1637574703000)
      Last Successful Execution Date : 2021-11-22 09:51:43 UTC (1637574703000)


    kube_scheduler (2.0.1)
    ----------------------
      Instance ID: kube_scheduler:50f753a83ecda252 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/kube_scheduler.d/conf.yaml
      Total Runs: 3
      Metric Samples: Last Run: 72, Total: 216
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 3, Total: 9
      Average Execution Time : 102ms
      Last Execution Date : 2021-11-22 09:51:35 UTC (1637574695000)
      Last Successful Execution Date : 2021-11-22 09:51:35 UTC (1637574695000)
```

This time, we are able to collecte the status of the leader election, so even with multi-master cluster kube-scheduler and kube-controller-manager is consistent.

I know it's a lot of configuration, and because dealing with configuration is always error prone, I'm providing you with a full example of Daemonset configuration: [datadog-agent-all-features](./datadog-agent-all-features.yaml).