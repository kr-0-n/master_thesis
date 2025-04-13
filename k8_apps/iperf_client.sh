#!/bin/sh

while true; do
    # Start iperf3 in background
    iperf3 -c "$TARGET" --bandwidth "$BANDWIDTH" -p 5001 >> /logs/"$HOSTNAME".log &
    IPERF_PID=$!

    # Start ping in background
    ping -c 10 "$TARGET" >> /logs/"$HOSTNAME".log &
    PING_PID=$!

    # Wait for both to finish
    wait $IPERF_PID
    wait $PING_PID

    # Sleep for 1-10 seconds
    sleep $((RANDOM % 10 + 1))
done