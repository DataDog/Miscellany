# DD Example
This serves as an example project to run to generate metrics, traces, and logs within Datadog.

# Setup / Prerequisites
- [install docker](https://docs.docker.com/install/)
- [install minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
- Start Minikube
  - Run: `minikube start`
  - Run: `eval $(minikube docker-env)`
    - Sets the docker environment to the one minikube offers instead of the one that you may already have installed in your local environment

# Run the example app
## Build Docker Images
```
docker build -t sample_flask:latest ./raw_files/flask/
docker build -t sample_postgres:latest ./raw_files/postgres/
```

## Put API Key secret in minikube
Replace `API_KEY` with your actual API Key from your Datadog Account.
```
kubectl create secret generic datadog-api --from-literal=token=API_KEY
```

## Deploy to minikube
- Run:
  ```
  kubectl apply -f postgres_deployment.yaml -f flask_deploy.yaml -f datadog-agent.yaml -f kubernetes
  ```

## Confirm it works & generate traffic
- Grab the `CLUSTER-IP` for flaskapp:
  - `kubectl get services`
  - Example output:
  ```
  ⇒  kubectl get services
  NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
  flaskapp     ClusterIP   10.104.65.215   <none>        5005/TCP   3m11s
  kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    32m
  postgres     ClusterIP   10.99.143.193   <none>        5432/TCP   3m11s
  ```
- SSH into minikube: `minikube ssh`
- Hit the flask endpoints:
  ```
  curl http://CLUSTER-IP:5005/
  curl http://CLUSTER-IP:5005/bad
  curl http://CLUSTER-IP:5005/query
  curl http://CLUSTER-IP:5005/log
  ```
  - where `CLUSTER-IP` is the one found from the previous command

You will need to hit these endpoints several times to generate traces and logs. If you **have not** setup logs before, you'll need to go through the setup screen, choose containers, choose kubernetes, then wait until the DD app let's you move to the explorer screen.

### Observe in Datadog
In a few minutes, you should be able to see metrics, traces, hosts, logs, etc:
- [metric summary page](https://app.datadoghq.com/metric/summary)
- [host map](https://app.datadoghq.com/infrastructure/map)
- [Traces](https://app.datadoghq.com/apm/search)
- [Logs](https://app.datadoghq.com/logs)
- [processes](https://app.datadoghq.com/process)
- [Postgres OOTB Dashboard](https://app.datadoghq.com/screen/integration/235/)
- etc...
