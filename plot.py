#!/usr/bin/env python3

import matplotlib.pyplot as plt
import sys

# Read 'data.csv' file containing:
# n, lookup time, binary search time

data = []
for line in open("data.csv", "r"):
    line = line.strip().split(",")
    print(line)
    n, l, bs, s = line
    n = int(n) * 8
    l = float(l)
    bs = float(bs)
    s = float(s)

    if n < 10**8:
        data.append((n, l, bs, s))

# Plot the data

by = "#fcc007"  # yellow
by2 = by  # yellow

plt.figure(figsize=(10, 5))
plt.plot(
    [x[0] for x in data],
    [x[3] for x in data],
    label="Sqrt",
    ls=":",
    marker="s",
    ms=4,
    c="blue",
    # c=by,
    alpha=0.6,
)
plt.plot(
    [x[0] for x in data],
    [x[2] for x in data],
    label="Binary Search",
    ls="--",
    marker="o",
    ms=4,
    # c="blue",
    c=by,
    alpha=0.6,
)
plt.plot(
    [x[0] for x in data],
    [x[1] for x in data],
    label="Array indexing",
    marker="x",
    c=by,
    # ls="--",
    alpha=0.6,
)

plt.xlabel("Array size")

plt.ylabel("Latency (ns)", c=by2)
plt.legend(loc="upper left")
plt.title("Array indexing vs binary search latency")
# plt.grid(True)
plt.xscale("log")
plt.yscale("log")
plt.ylim(ymin=1, ymax=4096)
plt.yticks([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
ax = plt.gca()
ax.set_yticklabels([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048], c=by2)

# Add secondary axis with the ratio
ax2 = plt.gca().twinx()
ax2.plot(
    [x[0] for x in data],
    [x[2] / x[1] for x in data],
    label="Ratio (binary search / array indexing)",
    color="black",
    lw=3,
    # linestyle="--",
)
ax2.set_ylabel("Ratio (binary search / array indexing)")
ax2.legend(loc="upper right")
# ax2.set_yscale("log")
ymax = 40
ax2.set_ylim(ymin=1, ymax=ymax)
# ax2.set_xlim(xmin=2**13, xmax=1.15 * 10**8)
ax2.set_yticks(range(0, ymax, 4))
ax2.set_yticklabels(range(0, ymax, 4))
ax2.grid(True)
plt.xticks([])
ax.tick_params(axis="both", which="minor", bottom=False, left=False)
ax.set_xticks(list(2**i for i in range(14, 27)))
ax.set_xticklabels(
    [
        # "8KiB",
        "16KiB",
        "32KiB",
        "64KiB",
        "128KiB",
        "256KiB",
        "512KiB",
        "1MiB",
        "2MiB",
        "4MiB",
        "8MiB",
        "16MiB",
        "32MiB",
        "64MiB",
        # "128MiB",
    ]
)

caches = [("L1", 32 * 1024), ("L2", 256 * 1024), ("L3", 12 * 1024 * 1024)]
for name, c in caches:
    plt.axvline(c, color="red", lw=0.7)
    plt.text(c, 1.05, name + " ", ha="right", c="red", size="x-large")

# plt.savefig("plot.svg", bbox_inches="tight")
# plt.savefig("plot.png", bbox_inches="tight", dpi=300)
plt.show()
