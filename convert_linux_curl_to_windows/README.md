# <img src="https://cdn.pixabay.com/photo/2016/03/23/14/55/matrix-1274888_1280.png" alt="code conversion icon" width="" height="">

## What does this script do

The `curl` command examples provided in our API documentation (https://docs.datadoghq.com/api/latest/) are Linux specific.

If a Windows user run these examples directly, they will run into syntax errors.

Manually converting curl syntaxt from Linux to Windows could be tedious, despite the fact that the general rules are simple:
* Change single quotes to double quotes
* Change the line continuation character from `\` to `^`
* Change the URL position from after the HTTP method to just before the payload.
* And lastly, remove the end of file condition `@- << EOF`

`convert_curl.py` will automatically apply the above rules to easily convert the syntaxt.

## Instructions

`convert_curl.py` takes a bash script containing the Linux `curl` command as an argument and will print out the Windows `curl` version.

- - - -
## Example

If `downtime.sh` contains:
```
curl -X POST "https://api.datadoghq.com/api/v1/downtime" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: " \
-H "DD-APPLICATION-KEY: " \
-d @- << EOF
{
  "message": "Example-Downtime",
  "recurrence": {
    "period": 1,
    "type": "years"
  },
  "scope": [
    "host:COMP-1"
  ],
  "start": 1693299442,
  "end": 1756684799,
  "timezone": "Etc/UTC",
  "mute_first_recovery_notification": true,
  "monitor_tags": [
    "tag0"
  ],
  "notify_end_states": [
    "alert",
    "warn"
  ],
  "notify_end_types": [
    "expired"
  ]
}
EOF
```

Then running the command `python convert_curl.py downtime.sh` will output:
```
curl -X POST  ^
-H "Accept: application/json" ^
-H "Content-Type: application/json" ^
-H "DD-API-KEY: " ^
-H "DD-APPLICATION-KEY: " ^
"https://api.datadoghq.com/api/v1/downtime" -d "^
{ ^
  "message": "Example-Downtime", ^
  "recurrence": { ^
    "period": 1, ^
    "type": "years" ^
  }, ^
  "scope": [ ^
    "host:COMP-1" ^
  ], ^
  "start": 1693299442, ^
  "end": 1756684799, ^
  "timezone": "Etc/UTC", ^
  "mute_first_recovery_notification": true, ^
  "monitor_tags": [ ^
    "tag0" ^
  ], ^
  "notify_end_states": [ ^
    "alert", ^
    "warn" ^
  ], ^
  "notify_end_types": [ ^
    "expired" ^
  ] ^
} "
```
