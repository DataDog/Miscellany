# After editing 'sb.json' dump contents into a new python script
# Usually all you will need to do is copy and paste the widgets section
# Then change lowercase 'true' to True, 'false' to False, and 'null' to ""​ 

from datadog import initialize, api
import json

options = {
    'api_key': 'API_KEY',
    'app_key': 'APP_KEY'
}

initialize(**options)

board_title = "New Screenboard"
description = ""
width = 1024

widgets = [
    {
        "board_id": 360007,
        "height": 16,
        "isShared": False,
        "legend": True,
        "legend_size": "0",
        "tile_def": {
            "autoscale": True,
            "requests": [
                    {
                        "q": "avg:aws.ec2.network_out{host:i-4988043403}",
                        "style": {
                            "palette": "warm",
                            "type": "solid",
                            "width": "normal"
                        },
                        "type": "line"
                    }
            ],
            "viz": "timeseries"
        },
        "time": {
            "live_span": "1d"
        },
        "title": True,
        "title_align": "left",
        "title_size": 16,
        "title_text": "Network (MB) In/Out",
        "type": "timeseries",
        "width": 47,
        "x": 103,
        "y": 511
    }
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

api.Screenboard.create(board_title=board_title,
                       description=description,
                       widgets=widgets,
                       template_variables=template_variables,
                       width=width)
