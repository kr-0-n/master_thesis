# How to use Ansible alongside Terraform via Openstack
The following steps are all on your own personal machine.

## Install tools
Depending on your distro, install `python-openstackclient`, `terraform` and `ansible`.\
Next install the ansible terraform plugin via:
```
ansible-galaxy collection install cloud.terraform
```
you can verify the installation via:
```
ansible-galaxy collection list | grep terraform
```

## Configuration
Configure your openstack client according to this [documentation](https://docs.nrec.no/api.html#openstack-command-line-interface-cli)\
Next initialize your terraform project:
```
terraform init
```
This should install everything you need.

## Usage
To then run a test command on the worker nodes you can use 
```
ansible --key-file path/to/your/key -i ./terraform.yaml worker -m ping
```


