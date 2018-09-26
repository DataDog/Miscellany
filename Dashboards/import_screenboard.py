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
        "board_id": 275605,
            "generated_title": "system.cpu.user",
            "height": 32,
            "isShared": False,
            "legend": False,
            "legend_size": "0",
            "tile_def": {
                "autoscale": True,
                "requests": [
                    {
                        "aggregator": "avg",
                        "conditional_formats": [],
                        "q": "avg:system.cpu.user{*}+avg:system.cpu.system{*}",
                        "style": {
                            "palette": "dog_classic",
                            "type": "solid",
                            "width": "normal"
                        },
                        "type": "line"
                    }
                ],
                "viz": "timeseries"
            },
            "time": {},
            "title": True,
            "title_align": "left",
            "title_size": 16,
            "title_text": "",
            "type": "timeseries",
            "width": 47,
            "x": 4,
            "y": 2
    }
]

template_variables = []

api.Screenboard.create(board_title=board_title,
                       description=description,
                       widgets=widgets,
                       template_variables=template_variables,
                       width=width)
