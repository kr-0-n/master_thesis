#!/bin/sh
while true; do
    iperf3 -c $TARGET --bandwidth $BANDWIDTH >> /logs/$HOSTNAME.log
    sleep $((RANDOM % 10 + 1))
done