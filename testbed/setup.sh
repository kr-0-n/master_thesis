#!/bin/bash

REPO_PATH=~/uni/master_thesis

# Source for openstack
echo "Source for openstack"
source $REPO_PATH/k8_deployment/keystone_rc.sh

# Run terraform
echo "Run terraform"
cd $REPO_PATH/k8_deployment
terraform apply

sleep 5

# Install k3s
echo "Install k3s"
ansible-playbook --private-key=~/.ssh/uio-ifi-nd-msc-k8-nrec -i $REPO_PATH/k8_deployment/terraform.yaml $REPO_PATH/k8_deployment/playbooks/k3s.yml

# Install network connections
echo "Install network connections"
ansible-playbook --private-key=~/.ssh/uio-ifi-nd-msc-k8-nrec -i $REPO_PATH/k8_deployment/terraform.yaml $REPO_PATH/k8_deployment/playbooks/network.yml

# Ask user to insert the IP in the kubeconfig file
read -p "Enter the IP address: " ip
sed -i "s/127.0.0.1/$ip/g" $REPO_PATH/k8_deployment/playbooks/kubeconfig.yml

# Export KUBECONFIG
echo "Export KUBECONFIG"
export KUBECONFIG=$REPO_PATH/k8_deployment/playbooks/kubeconfig.yml

# Setup Secret for the registry
echo "Setup Secret for the registry"
kubectl create secret generic regcred --from-file=.dockerconfigjson=$REPO_PATH/k8_deployment/deployments/config.json --type=kubernetes.io/dockerconfigjson

# Install the API Server
echo "Install the API Server"
kubectl apply -f $REPO_PATH/k8_deployment/deployments/api_server.yml

sleep 5

# Port forward the API Server
echo "Port forward the API Server"
kubectl port-forward $(kubectl get pods | grep apiserver | awk '{print $1}') 50051 &

sleep 5

# Populate API Server
echo "Populate API Server"
cd $REPO_PATH/api_server/proto
grpcurl -plaintext -d '{"from": "k8-manager-0", "to": "k8-worker-0", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-0", "to": "k8-manager-0", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-manager-0", "to": "k8-worker-1", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-1", "to": "k8-manager-0", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-manager-0", "to": "k8-worker-2", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-2", "to": "k8-manager-0", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData

grpcurl -plaintext -d '{"from": "k8-manager-0", "to": "k8-worker-6", "latency": 2, "throughput": 1000}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-6", "to": "k8-manager-0", "latency": 2, "throughput": 1000}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData

grpcurl -plaintext -d '{"from": "k8-worker-6", "to": "k8-worker-3", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-3", "to": "k8-worker-6", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-6", "to": "k8-worker-4", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-4", "to": "k8-worker-6", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-6", "to": "k8-worker-5", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData
grpcurl -plaintext -d '{"from": "k8-worker-5", "to": "k8-worker-6", "latency": 20, "throughput": 100}' -proto message.proto 127.0.0.1:50051 links.LinkService/SendData

# Install the client-server app
echo "Install the client-server app"
cd $REPO_PATH/k8_deployment/deployments
helm install app-test ./test-app

