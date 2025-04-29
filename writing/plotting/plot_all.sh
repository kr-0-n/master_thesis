#!/bin/bash

if [ -z "$1" ]; then
    echo "Please specify a run id as argument"
    exit 1
fi

./evaluation_plot.py "$1"
./evaluation_variance_plot.py "$1"
./evaluation_cumulative_plot.py "$1"
./pod_assign_change_cumulative_plot.py "$1"
./pod_uptime.py "$1"