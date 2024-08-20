we can have good latency but insufficient throughput and vice verse
throuput might work on one link and latency on another - how do we deal with this? (I suggest to prioritize throuput)
we cant control the path a packet takes

up and download on all links is assumed to be the same

capacity utilization of CPU and Mem can vary over time (hard to compute)

how do we measure CPU usage?

write nice visualization for evolutionary solver?

# ACO
- uses evaluation function as heuristic


---------------------------
# Perfect Solve
should it only solve every step perfectly or the entire time? (would need knowledge of the future)

# Evolutionary solve
Performs worse in some scenarios with this heuristic - early pods occupy a node and pods with stronger network requirements now have to go to a suboptimal node