#!/bin/sh
# Make sure you replace the API key below with the one for your account

# NOTE: In CentOS and variants, the crontab path is /usr/bin:/bin and lsof is /usr/sbin/lsof
# So you will need to add this to the script, otherwise it will report 0:
#
# PATH=$PATH:/usr/sbin

USER="user_name_here"
process_name="process_name"

for pid in $(ps -fu ${USER} | grep "${process_name}" | grep -v "grep" | awk '{print $2}'); do
    # echo "pid is ${pid}"
    val=`lsof -p ${pid} | wc -l`
    # echo "val is ${val}"

    # If you want to include your hostname as a tag (in the form of host:xyz), then include it here
    host_name="your_host_name"

    if [ -n $pid ]; then
      currenttime=$(date +%s)
      curl  -X POST -H "Content-type: application/json" \
      -d "{ \"series\" :
               [{\"metric\":\"linux.open_file_descriptors\",
                \"points\":[[$currenttime, $val]],
                \"type\":\"gauge\",
                \"host\":\"$host_name\",
                \"tags\":[\"process_name:$process_name\",\"pid:$pid\"]}
              ]
          }" \
      'https://app.datadoghq.com/api/v1/series?api_key=YOUR_API_KEY_HERE'
    fi
done
