#!/bin/bash

# Create logs directory'
EXPERIMENT=experiment-$(( $(ls . | grep experiment | tail -1 | cut -d '-' -f 2) + 1 ))
mkdir $EXPERIMENT

# Copy logs
EXPERIMENT=$EXPERIMENT ansible-playbook --private-key=~/.ssh/uio-ifi-nd-msc-k8-nrec -i ~/uni/master_thesis/k8_deployment/terraform.yaml ~/uni/master_thesis/k8_deployment/playbooks/copylogs.yml