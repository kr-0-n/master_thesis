#!/bin/sh

while true; do
    echo "TIME: $(date +%s)" >> /logs/"$HOSTNAME".log
    # Try iperf3 on a range of ports and run the first one that works
    for port in $(seq 5002 5012); do
        iperf3 -c "$TARGET" --bandwidth "$BANDWIDTH" -p "$port" >> /logs/"$HOSTNAME".log 
        if [[ "$?" -eq 0 ]]; then
          break 
        fi

    done

    # Start hping3 in TCP mode in background
    hping3 --syn -p 5001 -c 10 "$TARGET" >> /logs/"$HOSTNAME".log 

    # Sleep for 1-10 seconds
    sleep $((RANDOM % 10 + 1))
done
