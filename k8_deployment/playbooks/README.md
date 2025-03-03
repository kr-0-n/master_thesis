# Playbooks
The playbooks connect to the severs and configure them.\
To use them, make sure to specify you correct ssh-key and the inventory file which includes the info for where to connect\
`ansible-playbook --private-key=~/.ssh/uio-ifi-nd-msc-k8-nrec -i terraform.yaml playbook.yml`
## K3S
This playbook installs and configures K3S on the servers. Dont forget to update your kubectl config if you want to connect to the cluster