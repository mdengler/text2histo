#!/usr/bin/env python
"""
Example

seq 1 15 | text2histo.py

"""

import datetime, sys, os, math


if "--help" in sys.argv:
    print __doc__
    sys.exit(1)


counts = {}

for line in sys.stdin.readlines():
    line = line.strip()
    try:
        count = int(line)
    except Exception, msg:
        count = len(line)

    if count not in counts:
        counts[count] = 0
    counts[count] = counts[count] + 1

max_c = max(counts.keys())
min_c = min(counts.keys())

bins = min(20, len(counts.keys()))
bin_range = (max_c - min_c)
bin_increment = bin_range / math.ceil(float(bins))

bin_start = max_c
bin_increment = (max_c - min_c) / bins
for i in range(bins):
    bin_end = bin_start - bin_increment
    size = len([c for c in counts if (c <= bin_start) and (c > bin_end)])
    print "%10s .. %10s | [%5s] %s" % (bin_start,
                                       bin_end,
                                       size,
                                       "#" * size)
    bin_start = bin_end

bin_end = min_c
size = len([c for c in counts if (c <= bin_start) and (c > bin_end)])
print "%10s .. %10s | [%5s] %s" % (bin_start,
                                   bin_end,
                                   size,
                                   "#" * size)

