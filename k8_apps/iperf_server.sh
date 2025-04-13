#!/bin/sh
for port in $(seq 5001 5012); do
    iperf3 -s -p $port >> /logs/$HOSTNAME.log &
done
