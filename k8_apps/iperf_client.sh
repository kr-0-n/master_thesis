#!/bin/sh

while true; do
    # Try iperf3 on a range of ports and run the first one that works
    for port in $(seq 5001 5012); do
        iperf3 -c "$TARGET" --bandwidth "$BANDWIDTH" -p "$port" >> /logs/"$HOSTNAME".log &
        IPERF_PID=$!
        sleep 1  # Give it a moment to fail if it's going to

        # Check if the process has exited (e.g., failed to connect)
        if kill -0 "$IPERF_PID" 2>/dev/null; then
            # iperf is still running, so assume success and break
            break
        fi
    done

    # Start hping3 in TCP mode in background
    hping3 -S -c 10 "$TARGET" >> /logs/"$HOSTNAME".log &
    HPING_PID=$!

    # Wait for both to finish
    wait "$IPERF_PID"
    wait "$HPING_PID"

    # Sleep for 1-10 seconds
    sleep $((RANDOM % 10 + 1))
done