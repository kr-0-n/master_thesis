#!/bin/sh

# Check if tc is installed
if ! command -v tc &> /dev/null
then
    echo "tc is not installed"
    exit 1
fi

#Check if limit was supplied as an argument
if [ -z "$1" ]; then
    echo "No limit was supplied as an argument"
    exit 1
fi

# Flush both interfaces
ip link set eth0 down
ip addr flush dev eth0
ip link set eth0 up
echo "Flushed eth0"
ip link set eth1 down
ip addr flush dev eth1
ip link set eth1 up
echo "Flushed eth1"

# Delete old qdiscs (if they exist)
tc qdisc del dev eth0 root
tc qdisc del dev eth1 root
echo "Deleted old qdiscs"

# Bridge eth0 and eth1
# Create a bridge device named br0
ip link add name br0 type bridge

# Add your interfaces to the bridge
ip link set eth0 master br0
ip link set eth1 master br0

# Bring up the interfaces and the bridge
ip link set eth0 up
ip link set eth1 up
ip link set br0 up
echo "Bridged eth0 and eth1"

# Install throughput limit in both directions
tc qdisc add dev eth0 root handle 1: htb default 12
tc class add dev eth0 parent 1: classid 1:12 htb rate "$1"mbit

tc qdisc add dev eth1 root handle 1: htb default 12
tc class add dev eth1 parent 1: classid 1:12 htb rate "$1"mbit