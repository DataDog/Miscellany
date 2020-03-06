from datadog import api

# all_id_list returns a list of all id's found in an api resource's get_all() response
def all_id_list(resp, resource):
    id_list = []

    if resource == "dash":
        id_list = [d['id'] for d in resp.get("dashboards")]
    elif resource == "monitor":
        id_list = [m['id'] for m in resp]
    else:
        print(resource + " is an invalid resource name, exiting.")
        quit()

    return id_list

# metric_report outputs a list of where metrics are being used in your Datadog account
def metric_report(ids_list, metrics_to_eval, resource):
    title = ''
    resp = {}
    query = ''
    getter = ''

    for id in ids_list:
        if resource == "dash":
            resp = api.Dashboard.get(str(id))
            query = str(resp.get("widgets"))
            getter = "title"
        elif resource == "monitor":
            resp = api.Monitor.get(str(id))
            query = str(resp.get("query"))
            getter = "name"
        else:
            print(resource + " is an invalid resource name, exiting.")
            quit()

        for metric in metrics_to_eval:
                if query.find(metric) != -1:
                    if title != resp[getter]:
                        title = resp[getter]
                        print('\n\n\tTitle: ' + resp[getter])
                    print('\n\t\t Metric: ' + metric)