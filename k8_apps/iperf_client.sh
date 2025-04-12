#!/bin/sh
while true; do
    iperf3 -c $TARGET --bandwidth $BANDWIDTH -p 5001 >> /logs/$HOSTNAME.log &
    ping -c 10 $TARGET >> /logs/$HOSTNAME.log
    sleep $((RANDOM % 10 + 1))
done