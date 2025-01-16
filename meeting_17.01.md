# Meeting
## Simulator

## Kubernetes
### Terraform
`source keystone_rc.sh`\
`terraform apply`

### Ansible
`ansible all -i terraform.yaml --list-hosts`\
`ansible --private-key=~/.ssh/uio-ifi-nd-msc-k8-nrec -i terraform.yaml worker_group -m ping`
`ansible-playbook --private-key=~/.ssh/uio-ifi-nd-msc-k8-nrec -i terraform.yaml playbook.yml`

### Kubectl
Dont forget to set the IP\
`KUBECONFIG=/home/kron/uni/master_thesis/k8_deployment/k3s.yaml/k8-manager-0/etc/rancher/k3s/k3s.yaml kubectl get nodes`

## API