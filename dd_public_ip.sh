#!/bin/bash

function usage
{
    echo 'usage dd-public-ip-tag.sh --api_key "<key>" --app_key "<key>"'
}

#### Main
api_key=""
app_key=""

while [ "$1" != "" ]; do
    case $1 in
        -i | --api_key )        shift
                                api_key=$1
                                ;;
        -p | --app_key )        shift
                                app_key=$1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

if [ "$api_key" = "" -o "$app_key" = "" ]; then
  usage
  exit 1
fi

private_ip=`wget -q -O - http://instance-data/latest/meta-data/local-ipv4`
private_ip='ip-'`echo $private_ip | sed 's/\./-/g'`
instance_id=`wget -q -O - http://instance-data/latest/meta-data/instance-id`
public_ip=`wget -qO- http://instance-data/latest/meta-data/public-ipv4`
tag='"tags" : ["public_ip:'$public_ip'"]'
echo 'api_key:     '$api_key
echo 'app_key:     '$app_key
echo 'instance_id: '$instance_id
echo 'public_ip:   '$public_ip

curl  -X POST -H "Content-type: application/json" \
-d '{
      "tags" : ["public_ip:'$public_ip'"]
    }' \
"https://app.datadoghq.com/api/v1/tags/hosts/${instance_id}?api_key=${api_key}&application_key=${app_key}"