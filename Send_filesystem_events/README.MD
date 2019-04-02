# README

This script will send an event to the event stream when it detects a change in a file or folder in the directory tree that it is watching. It is useful in cases where you might want to monitor if files in a directory containing SSH keys or AWS secrets may have been modified or deleted. The script only sends events to the event stream, if you need an alert when a file is deleted or modified, you can [set up an event monitor](https://docs.datadoghq.com/monitors/monitor_types/event/) on the events it sends.

I've tested this script on Ubuntu 16.04, and it should work with most flavors of Linux running a kernel version of 2.6 or higher. Please note that it does *not* work with MacOS or Windows operating systems.

The script depends on the [datadog Python package](https://pypi.org/project/datadog/) and the [inotify Python package](https://pypi.org/project/inotify/), both of which can be installed with the `pip install` command. The inotify Python package hooks into the inotify subsystem of the Linux kernel, which monitors changes to the filesystem.

To use the script, enter your API and app keys in the `options` dictionary. Then, specify the path to the directory you would like to monitor. The script will recursively monitor any subdirectories.

A word of warning: this script is very chatty, and will send events about everything that's going on in the monitored part of your file system! If you want to know more about what the events this library is sending, explanations for them are listed in the inotify events section of the [inotify man page](http://man7.org/linux/man-pages/man7/inotify.7.html).

If you want to reduce the chattiness, you can add some logic to not send events for some of these messages. I've decided to err on the side of chattiness so users can customize the script to suit their use cases.
