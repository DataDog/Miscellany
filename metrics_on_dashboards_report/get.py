from datadog import api

# all_dashboard_id_list returns a list of all dashboard id's found in a dashboard get_all() response
def all_dashboard_id_list(resp):
    id_list = [d['id'] for d in resp.get("dashboards")]
    return id_list

# metric_report outputs a list of where metrics are being used in your Datadog account
def metric_report(ids_list, metrics_to_eval):
    board_title = ''

    for id in ids_list:
        resp = api.Dashboard.get(str(id))

        str_resp = str(resp.get("widgets"))

        for metric in metrics_to_eval:
                if str_resp.find(metric) != -1:

                    if board_title != resp["title"]:
                        print('\n\n\tBoard: ' + resp["title"])
                    print('\n\t\t Metric: ' + metric)