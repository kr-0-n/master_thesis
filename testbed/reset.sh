#!/bin/bash

# Source for openstack
source ../k8_deployment/keystone_rc.sh

# Run terraform
cd ~/uni/master_thesis/k8_deployment
terraform destroy

# Kill forwarding
pkill -f "kubectl port-forward"