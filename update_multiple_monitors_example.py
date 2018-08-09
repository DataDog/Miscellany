from datadog import initialize, api

options = {
    'api_key': 'API KEY',
    'app_key': 'APP KEY'
}


class Monitor:
    def __init__(self, monitor_id, monitor_query, monitor_name, monitor_tags):
        self.monitor_id = monitor_id
        self.monitor_query = monitor_query
        self.monitor_name = monitor_name
        self.monitor_tags = monitor_tags


initialize(**options)

if __name__=="__main__":

    monitor_list = []

    # Examples: ID, query, name, tags, in that order :)
    nginx_monitor = Monitor(5026334,
                            "avg(last_1m):avg:nginx.net.request_per_s{*} > 75",
                            "NGINX Web Server is not happy!",
                            ['from:nginx']
                            )
    
    mysql_monitor = Monitor(5026335,
                            "avg(last_1m):avg:mysql.net.connections{*} > 60",
                            "MySQL Database Server says: TOO MANY CONNECTIONS!",
                            ['from:mysql']
                            )

    monitor_list.append(nginx_monitor)
    monitor_list.append(mysql_monitor)

    for monitor in monitor_list:

        api.Monitor.update(
            monitor.monitor_id,
            query=monitor.monitor_query,
            name=monitor.monitor_name,
            tags=monitor.monitor_tags
            )
