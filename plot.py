#!/usr/bin/env python3

import matplotlib.pyplot as plt
import sys
from math import sqrt, cbrt

plt.close()

# Read 'data.csv' file containing:
# n, lookup time, binary search time

data = []
for line in open("data.csv", "r"):
    line = line.strip().split(",")
    print(line)
    n = int(line[0]) * 4  # u32
    ds = [float(x) for x in line[1:]]

    if n < 10**4:
        continue
    if n > 10**9:
        continue
    data.append((n, *ds))

# Plot the data

# by = "#fcc007"  # yellow
# by2 = by  # yellow
by = by2 = "black"

plt.figure(figsize=(6, 4))

plt.plot(
    [x[0] for x in data],
    [x[5] for x in data],
    label="S-tree",
    ls="-",
    marker="s",
    ms=4,
    c="green",
    alpha=0.6,
)

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
    ms=4,
    # c="blue",
    c="black",
    alpha=0.6,
)
plt.plot(
    [x[0] for x in data],
    [x[4] for x in data],
    label="Eytzinger",
    ls="-",
    marker="s",
    ms=4,
    c="red",
    alpha=0.6,
)
plt.plot(
    [x[0] for x in data],
    [x[1] for x in data],
    label="Array indexing",
    marker="x",
    c="blue",
    # ls="--",
    alpha=0.6,
)


# xs = [2**14, 8 * 2**40]
xs = [data[0][0], data[-1][0]]
plt.plot(
    [x for x in xs],
    [sqrt(x / data[14][0]) * data[14][1] for x in xs],
    label="~sqrt(n)",
    # marker="x",
    c="blue",
    ls="-",
    lw=0.5,
    # alpha=0.6,
)
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

plt.xlabel("Array size")

plt.ylabel("Latency (ns)", c=by2)
plt.title("Latency of array indexing and binary search")
# plt.grid(True)
plt.xscale("log")
plt.yscale("log")
plt.ylim(ymin=1, ymax=1024)
plt.yticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
ax = plt.gca()
ax.set_yticklabels([1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024], c=by2)

# Add secondary axis with the ratio
ax2 = plt.gca().twinx()
ax.plot(
    [x[0] for x in data],
    [x[2] / x[1] for x in data],
    label="Ratio (binary search / array indexing)",
    color="black",
    lw=1,
    linestyle="--",
)
# ax2.plot(
#     [x[0] for x in data],
#     [x[4] / x[1] for x in data],
#     # label="Ratio (eytzinger / array indexing)",
#     color="red",
#     lw=1,
#     linestyle="--",
# )
# ax2.plot(
#     [x[0] for x in data],
#     [x[5] / x[1] for x in data],
#     # label="Ratio (S-tree / array indexing)",
#     color="green",
#     lw=1,
#     linestyle="--",
# )
ax2.set_ylabel("Ratio to array indexing")
# ax2.legend(loc="lower right")
if False:
    ymax = 40
    ax2.set_ylim(ymin=0, ymax=ymax)
    ax2.set_yticks(range(1, ymax, 4))
    ax2.set_yticklabels(range(1, ymax, 4))
else:
    ymax = 10
    ax2.set_ylim(ymin=1, ymax=2**ymax)
    ax2.set_yscale("log")
    ax2.set_yticks([2**i for i in range(0, ymax + 1)])
    ax2.set_yticklabels([2**i for i in range(0, ymax + 1)])
    ax2.set_xticks([])
    ax2.set_xticks([], minor=True)
    ax2.set_xticklabels([])
    # ax2.set_xticklabels([], minor=True)

ax.grid(True, axis="y")
# plt.xticks([])
ax.tick_params(axis="both", which="minor", left=False, right=False)
ax.set_xticks(
    list(2**i for i in range(14, 31, 2)),
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
        "128MiB",
        "256MiB",
        "512MiB",
        "1GiB",
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
    ax.axvline(c, color="red", lw=0.7)
    ax.text(c, 1.05, name + " ", ha="right", c="red", size="x-large")
ax.text(data[-1][0], 1.05, caches[-1][0] + " ", ha="right", c="red", size="x-large")

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
