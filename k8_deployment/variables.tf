variable "region" {
    default = "osl"
}

variable "name" {
  default = "k3s-test"
}

variable "ssh_public_key" {
  default = "~/.ssh/uio-ifi-nd-msc-k8-nrec.pub"
}

variable "network" {
  default = "dualStack"
}

# Mapping between role and image
variable "image" {
  default = "GOLD Ubuntu 22.04 LTS"
}

# Mapping between role and flavor
variable "role_flavor" {
  type = map(string)
  default = {
    "worker" = "m1.small"
    "manager"  = "m1.large"
  }
}

# Mapping between role and number of instances (count)
variable "role_count" {
  type = map(string)
  default = {
    "worker" = 2
    "manager"  = 1
  }
}