#!/bin/bash

source ~/.sandbox.conf.sh

echo "Provisioning!"

echo "apt-get updating"
sudo apt-get update
echo "install curl if not there..."
sudo apt-get install curl

echo "Installing dd-agent from api_key: ${DD_API_KEY}..."
DD_API_KEY=${DD_API_KEY} DD_INSTALL_ONLY=true bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"

echo "Adding Custom Check (test_custom_check) to dd-agent"
sudo cp ~/data/test_custom_check.yaml /etc/dd-agent/conf.d/test_custom_check.yaml
sudo cp ~/data/test_custom_check.py /etc/dd-agent/checks.d/test_custom_check.py
sudo sed -i.bak "s/# hostname: mymachine.mydomain/hostname: $HOSTNAME_BASE.custom_check/g" /etc/dd-agent/datadog.conf
sudo sed -i.bak "s/# tags: mytag, env:prod, role:database/tags: $TAG_DEFAULTS,tester:custom_check/g" /etc/dd-agent/datadog.conf
sudo rm /etc/dd-agent/datadog.conf.bak

sudo /etc/init.d/datadog-agent start