from datadog import initialize, api
import inotify
import inotify.adapters

# Enter you app and API keys below
options = {'api_key': 'api_key',
           'app_key': 'app_key'}

# Enter the path to the directory you would like to monitor. This script will monitor the directory recursively.
dir = 'the/directory/you/want/to/monitor'

initialize(**options)

i = inotify.adapters.InotifyTree(dir)
for event in i.event_gen(yield_nones=False):
    (_, type_names, path, filename) = event
    for name in type_names:
        title = "Event " + name + " occurred in " + path + filename
        text = "event text"
        tags = ["tag:1", "security:high"]
        api.Event.create(title=title, text=text, tags=tags)
