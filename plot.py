#!/usr/bin/env python3

import matplotlib.pyplot as plt
import sys
from math import sqrt, cbrt, log

plt.close()

# Read 'data.csv' file containing:
# n, lookup time, binary search time

data = []
for line in open("data.csv", "r"):
    line = line.strip().split(",")
    print(line)
    n = int(line[0]) * 4  # u32
    ds = [float(x) for x in line[1:]]

    # if n < 10**4:
    #     continue
    # if n > 10**9:
    #     continue
    data.append((n, *ds))

# Plot the data

# by = "#fcc007"  # yellow
# by2 = by  # yellow
by = by2 = "black"

plt.figure(figsize=(6, 4))

# plt.plot(
#     [x[0] for x in data],
#     [x[5] for x in data],
#     label="S-tree",
#     ls="-",
#     marker="s",
#     ms=4,
#     c="green",
#     alpha=0.6,
# )

# plt.plot(
#     [x[0] for x in data],
#     [x[3] for x in data],
#     label="Sqrt",
#     ls=":",
#     marker="s",
#     ms=4,
#     c="purple",
#     # c=by,
#     alpha=0.6,
# )
plt.plot(
    [x[0] for x in data],
    [x[2] for x in data],
    label="Binary Search",
    ls="-",
    marker="o",
    ms=2.5,
    # c="blue",
    c="black",
    alpha=0.6,
)
# plt.plot(
#     [x[0] for x in data],
#     [x[4] for x in data],
#     label="Eytzinger",
#     ls="-",
#     marker="s",
#     ms=4,
#     c="red",
#     alpha=0.6,
# )
# plt.plot(
#     [x[0] for x in data],
#     [x[1] for x in data],
#     label="Array indexing",
#     marker="x",
#     c="blue",
#     # ls="--",
#     alpha=0.6,
# )


# xs = [2**14, 8 * 2**40]
xs = [data[0][0], data[-1][0]]
plt.plot(
    [x for x in xs],
    [log(x, 2) / log(data[0][0], 2) * data[0][2] for x in xs],
    label="~lg(n)",
    # marker="x",
    c="blue",
    ls="-",
    lw=0.7,
    # alpha=0.6,
)
# plt.plot(
#     [x for x in xs],
#     [sqrt(x / data[14][0]) * data[14][1] for x in xs],
#     label="~sqrt(n)",
#     # marker="x",
#     c="blue",
#     ls="-",
#     lw=0.5,
#     # alpha=0.6,
# )
# plt.plot(
#     [x for x in xs],
#     [(x / 2**40) * 2*10**5 for x in xs],
#     label="~n",
#     # marker="x",
#     c="pink",
#     ls="-",
#     lw=0.5,
#     # alpha=0.6,
# )
# plt.plot(
#     [x[0] for x in data],
#     [cbrt(x[0] / data[7][0]) * data[7][1] for x in data],
#     label="~cbrt(n)",
#     # marker="x",
#     c="blue",
#     ls=":",
#     alpha=0.6,
# )

# Specific data points

plt.xlabel("Array size (B)")

plt.ylabel("Latency (ns)", c=by2)
plt.title("Latency of binary search")
# plt.grid(True)
plt.xscale("log")
# plt.yscale("log")
plt.ylim(ymin=0)
# plt.yticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
ax = plt.gca()
# ax.set_yticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512], c=by2)

ax.grid(True, axis="y")
# plt.xticks([])
ax.tick_params(axis="both", which="minor", left=False, right=False)
ax.set_xticks(
    list(2**i for i in range(14, 33, 2)),
    [
        # "8K",
        "16K",
        "32K",
        "64K",
        "128K",
        "256K",
        "512K",
        "1M",
        "2M",
        "4M",
        "8M",
        "16M",
        "32M",
        "64M",
        "128M",
        "256M",
        "512M",
        "1G",
        "2G",
        "4G",
    ][::2],
)
ax.set_xticks(list(2**i for i in range(15, 30)), [], minor=True)

caches = [
    # ("word", 8),
    # ("registers", 1440),
    ("L1", 32 * 1024),
    ("L2", 256 * 1024),
    ("L3", 12 * 1024 * 1024),
    ("RAM", 32 * 1024 * 1024 * 1024),
    # ("SSD (8TiB)", 8 * 1024 * 1024 * 1024 * 1024),
]
for name, c in caches[:-1]:
    ax.axvline(c, color="red", lw=0.3)
    ax.text(c, 10, name + " ", ha="right", c="red", size="large", alpha=0.5)
ax.text(data[-1][0], 10, caches[-1][0], ha="right", c="red", size="large", alpha=0.5)

ax.legend(loc="upper left")

# plt.plot(
#     [32 * 2**30, 8 * 2**40],
#     [56000] * 2,
#     marker="x",
#     color="black",
#     ls="-",
#     label="SSD",
#     alpha=0.6,
# )
# plt.plot([8 * 2**40], [10**6], marker="x", color="black", label="Network", alpha=0.6)

plt.savefig("plot.svg", bbox_inches="tight")
plt.savefig("plot.png", bbox_inches="tight", dpi=300)
# plt.gcf().show()
