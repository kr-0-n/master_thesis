import re
import sys
import matplotlib.pyplot as plt
from datetime import datetime

# -----------------------------
# Parsing helpers
# -----------------------------

def parse_iperf(block):
    """
    Extract sender throughput (Mbits/sec) from iperf block
    """
    for line in block.splitlines():
        if line.strip().endswith("sender"):
            m = re.search(r"([\d\.]+)\s*Mbits/sec", line)
            if m:
                return float(m.group(1))
    return None


def parse_hping(block):
    """
    Extract average RTT (ms) from hping block
    """
    rtts = []
    for line in block.splitlines():
        m = re.search(r"rtt=([\d\.]+)\s*ms", line)
        if m:
            rtts.append(float(m.group(1)))

    if not rtts:
        return None

    return sum(rtts) / len(rtts)


# -----------------------------
# Main parser
# -----------------------------

def analyze_file(filename):
    with open(filename, "r") as f:
        text = f.read()

    # Split by TIME markers (keep timestamp)
    blocks = re.split(r"TIME:\s*(\d+)", text)

    results = []

    # blocks looks like: [preamble, ts1, block1, ts2, block2, ...]
    for i in range(1, len(blocks), 2):
        timestamp = int(blocks[i])
        block = blocks[i + 1]

        iperf = parse_iperf(block)
        hping = parse_hping(block)

        if iperf is None or hping is None:
            continue

        results.append({
            "time": timestamp,
            "iperf_mbps": iperf,
            "rtt_ms": hping
        })

    return results


# -----------------------------
# Plotting
# -----------------------------

def plot_results(results):
    times = [r["time"] for r in results]
    iperf = [r["iperf_mbps"] for r in results]
    rtt = [r["rtt_ms"] for r in results]

    times_dt = [datetime.fromtimestamp(t) for t in times]

    fig, ax1 = plt.subplots(figsize=(11, 6))

    # Throughput (blue)
    ax1.plot(
        times_dt,
        iperf,
        marker="o",
        color="tab:blue",
        label="Throughput"
    )
    ax1.set_ylabel("Throughput (Mbits/sec)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.set_xlabel("Time")
    ax1.grid(True)

    # RTT (red)
    ax2 = ax1.twinx()
    ax2.plot(
        times_dt,
        rtt,
        marker="s",
        color="tab:red",
        label="Avg RTT"
    )
    ax2.set_ylabel("Average RTT (ms)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    plt.title("Network Performance Over Time")
    plt.tight_layout()
    plt.savefig("network_performance_over_time.png", dpi=150)
    plt.close()

    print("Saved plot to network_performance_over_time.png")


# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <logfile>")
        sys.exit(1)

    results = analyze_file(sys.argv[1])

    if not results:
        print("No valid measurements found.")
        sys.exit(1)

    plot_results(results)
