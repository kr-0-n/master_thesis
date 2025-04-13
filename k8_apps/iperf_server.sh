#!/bin/sh
nc -l -p 5001 &
for port in $(seq 5002 5012); do
    iperf3 -s -p $port >> /logs/$HOSTNAME.log &
done


wait