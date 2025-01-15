# Define required providers
terraform {
  required_version = ">= 1.0"
  required_providers {
    openstack = {
      source = "terraform-provider-openstack/openstack"
    }
    ansible = {
      version = "~> 1.3.0"
      source  = "ansible/ansible"
    }
  }
}

# Configure the OpenStack Provider
# Empty means using environment variables "OS_*". More info:
# https://registry.terraform.io/providers/terraform-provider-openstack/openstack/latest/docs
provider "openstack" {}

# Create a server
resource "openstack_compute_instance_v2" "k8-worker" {
  name        = "k8-worker-${count.index}"
  count       = lookup(var.role_count, "worker")
  image_name  = var.image
  flavor_name = lookup(var.role_flavor, "worker")

  key_pair        = "lorenz_generic"
  security_groups = ["default", "SSH and ICMP"]

  network {
    name = var.network
  }
}

resource "openstack_compute_instance_v2" "k8-manager" {
  name        = "k8-manager-${count.index}"
  count       = lookup(var.role_count, "manager")
  image_name  = var.image
  flavor_name = lookup(var.role_flavor, "manager")

  key_pair        = "lorenz_generic"
  security_groups = ["default", "SSH and ICMP", "Kubernetes Control Pane"]

  network {
    name = var.network
  }
}


resource "ansible_host" "k8-worker" {
  count  = lookup(var.role_count, "worker", 0)
  name   = "k8-worker-${count.index}"
  groups = ["worker"] # Groups this host is part of

  variables = {
    ansible_host = trim(openstack_compute_instance_v2.k8-worker[count.index].access_ip_v4, "[]")
  }
}

resource "ansible_host" "k8-manager" {
  count  = lookup(var.role_count, "manager", 0)
  name   = "k8-manager-${count.index}"
  groups = ["manager"] # Groups this host is part of

  variables = {
    ansible_host = trim(openstack_compute_instance_v2.k8-manager[count.index].access_ip_v4, "[]")
  }
}

# Ansible web group
resource "ansible_group" "worker_group" {
  name     = "worker_group"
  children = ["worker"]
  variables = {
    ansible_user = "ubuntu"
  }
}

resource "ansible_group" "manager_group" {
  name     = "manager_group"
  children = ["manager"]
  variables = {
    ansible_user = "ubuntu"
  }
}