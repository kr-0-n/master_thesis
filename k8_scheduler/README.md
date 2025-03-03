# Scheduler
To connect to the cluster, the code expects the correct kubectl config file here `k8_deployment/k3s.yaml/k8-manager-0/etc/rancher/k3s/k3s.yaml`. Make sure its available.

To connect to the API Server, a pod forwarding is recommended\
`kubectl port-forward pod/apiserver-669b498c78-xnqzm 50051:50051 -n default`
